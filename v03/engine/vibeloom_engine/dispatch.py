"""Dispatch plan + execute_plan (impl §13).

The engine assembles waves from an affected set per §13.2's deterministic
rules; `execute_plan(plan, callback)` is the single primitive that turns a
plan into committed work, calling back to the orchestrator for actual
subagent spawning. Wave-rule tests live in `tests/test_dispatch.py`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from vibeloom_engine.affected import AffectedSet
from vibeloom_engine.models import Graph


# ---------------------------------------------------------------------------
# Scope shape (engine-emitted; orchestrator translates to subagent task header)
# ---------------------------------------------------------------------------


@dataclass
class Scope:
    scope_id: str
    kind: str  # "product-specs" | "ux-specs" | "system-specs" | "component-code" | ...
    owned_paths: tuple[str, ...] = ()
    allowed_read_paths: tuple[str, ...] = ()
    task_template_id: str = ""
    is_reconciliation: bool = False
    is_eval: bool = False
    derives_from_scopes: tuple[str, ...] = ()  # scope_id strings of upstream scopes

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "kind": self.kind,
            "owned_paths": list(self.owned_paths),
            "allowed_read_paths": list(self.allowed_read_paths),
            "task_template_id": self.task_template_id,
            "is_reconciliation": self.is_reconciliation,
            "is_eval": self.is_eval,
            "derives_from_scopes": list(self.derives_from_scopes),
        }


# ---------------------------------------------------------------------------
# Wave assembly per §13.2
# ---------------------------------------------------------------------------


def _paths_overlap(a: tuple[str, ...], b: tuple[str, ...]) -> bool:
    """Strict prefix-aware overlap. Globs (`**`) are treated as prefix
    expressions: `web/src/**` matches anything under `web/src/`."""
    def normalize(path: str) -> str:
        return path.split("**", 1)[0]

    a_pref = [normalize(p) for p in a]
    b_pref = [normalize(p) for p in b]
    for pa in a_pref:
        for pb in b_pref:
            if not pa or not pb:
                continue
            if pa == pb:
                return True
            if pa.startswith(pb) or pb.startswith(pa):
                return True
    return False


def assemble_waves(
    scopes: list[Scope],
    max_wave_size: int = 5,
) -> list[list[Scope]]:
    """Assemble scopes into waves per §13.2.

    Rules (in order):
      1. Disjoint ownership — same wave iff `owned_paths` disjoint.
      2. Derivation precedence — B is in a strictly later wave than A iff
         B.derives_from_scopes ⊇ A.scope_id.
      3. Concurrency cap — wave size bounded by `max_wave_size`.
      4. Reconciliation singletons — reconciliation scopes go alone.
      5. Eval ordering — read-only eval may run alongside generation in the
         same wave only on a different scope (already covered by rule 1
         since eval scopes don't write); otherwise separate wave after.
    """
    # Index by scope_id for derivation precedence
    by_id = {s.scope_id: s for s in scopes}

    # Compute transitive depth: 0 for sinks, else 1 + max upstream depth.
    # Cycles aren't possible in a contract DAG; if a malformed input gives us
    # one, we treat unresolved upstreams as depth 0 (orchestrator should have
    # already failed structural eval).
    depth_cache: dict[str, int] = {}

    def depth(sid: str, visiting: set[str]) -> int:
        if sid in depth_cache:
            return depth_cache[sid]
        if sid in visiting:
            return 0
        s = by_id.get(sid)
        if s is None or not s.derives_from_scopes:
            depth_cache[sid] = 0
            return 0
        visiting.add(sid)
        try:
            d = 1 + max(depth(up, visiting) for up in s.derives_from_scopes)
        finally:
            visiting.discard(sid)
        depth_cache[sid] = d
        return d

    # Topological-style placement: assign each scope to the earliest wave
    # not blocked by rules 1, 2, 4. Process in increasing transitive depth
    # so upstream scopes always land before downstream.
    waves: list[list[Scope]] = []
    placed: dict[str, int] = {}  # scope_id → wave index

    def sort_key(s: Scope) -> tuple:
        # Sort primarily by transitive depth so upstreams place first;
        # within a depth, place generation before reconciliation (so
        # reconciliation singletons land in the latest wave they need to);
        # then scope_id for determinism.
        return (
            depth(s.scope_id, set()),
            1 if s.is_reconciliation else 0,
            s.scope_id,
        )

    for scope in sorted(scopes, key=sort_key):
        # Min wave from rule 2: max(placed[upstream]) + 1, else 0.
        min_wave = 0
        for up in scope.derives_from_scopes:
            if up in placed:
                min_wave = max(min_wave, placed[up] + 1)
        # Find the first wave at or after min_wave that satisfies rules 1, 3, 4.
        target = min_wave
        while True:
            if target >= len(waves):
                waves.append([])
            wave = waves[target]
            # rule 4: reconciliation singletons.
            if scope.is_reconciliation and wave:
                target += 1
                continue
            if not scope.is_reconciliation and wave and any(s.is_reconciliation for s in wave):
                target += 1
                continue
            # rule 3: concurrency cap.
            if len(wave) >= max_wave_size:
                target += 1
                continue
            # rule 1: disjoint ownership.
            collide = False
            for s in wave:
                if _paths_overlap(scope.owned_paths, s.owned_paths):
                    collide = True
                    break
            if collide:
                target += 1
                continue
            wave.append(scope)
            placed[scope.scope_id] = target
            break

    # Stable sort within wave by scope_id for deterministic output.
    for w in waves:
        w.sort(key=lambda s: s.scope_id)
    return waves


# ---------------------------------------------------------------------------
# Plan assembly
# ---------------------------------------------------------------------------


def dispatch_plan(
    graph: Graph,
    affected: AffectedSet,
    max_wave_size: int = 5,
    today: str | None = None,
) -> dict[str, Any]:
    """Assemble a dispatch plan from the affected set.

    The engine derives `Scope` records by mapping each affected artifact to
    a scope kind. This is a deterministic translation:
      - `prd`/`usm`/`dm` → product-specs scope (owned_paths: those files)
      - `ux` → ux-specs scope
      - `system`/`containers`/`container` → system-specs scope
      - `component` artifacts → one component-code scope per component

    Caller-supplied scopes (richer scoping for components) can be added by
    the orchestrator pre-call; this function is the deterministic baseline.
    """
    if today is None:
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
    plan_id = f"PLAN-{today}-001"

    scopes_by_id: dict[str, Scope] = {}

    # Build artifact_id → kind map first.
    for aid in affected.affected_artifacts:
        a = graph.artifacts.get(aid)
        if a is None:
            continue
        atype = a.artifact_type.value
        if atype in ("prd", "usm", "dm"):
            sid = "product-specs"
            kind = "product-specs"
            owned: list[str] = ["prd.md", "usm.md", "dm.md"]
            allowed = ["intent.md", "defaults.md"]
            template = "generate-product-specs"
            derives_scopes: list[str] = []
        elif atype == "ux":
            sid = "ux-specs"
            kind = "ux-specs"
            owned = ["ux.md"]
            allowed = ["intent.md", "prd.md", "usm.md", "ux-specs/mockups/**"]
            template = "generate-ux-specs"
            derives_scopes = ["product-specs"] if any(
                graph.artifacts.get(x) and graph.artifacts[x].artifact_type.value in ("prd", "usm", "dm")
                for x in affected.affected_artifacts
            ) else []
        elif atype in ("system", "containers", "container"):
            sid = "system-specs"
            kind = "system-specs"
            owned = ["system.md", "containers.md"]
            allowed = ["intent.md", "prd.md", "usm.md", "ux.md"]
            template = "generate-system-specs"
            derives_scopes = ["product-specs"] if any(
                graph.artifacts.get(x) and graph.artifacts[x].artifact_type.value in ("prd", "usm", "dm")
                for x in affected.affected_artifacts
            ) else []
        elif atype == "component":
            sid = f"component:{a.scope.scope_id}"
            kind = "component-code"
            # Use owned_paths from extras if present; else file-only fallback.
            paths_extra = a.extras.get("owned_paths") or []
            owned = list(paths_extra) if paths_extra else [a.path]
            allowed = ["**/component.md", "**/AGENTS.md", "**/CLAUDE.md"]
            template = "generate-component-code"
            derives_scopes = ["system-specs"]
        else:
            # context, validation-registry — no generation scope at engine level
            continue

        if sid in scopes_by_id:
            # Merge owned paths if the same scope_id surfaces twice.
            existing = scopes_by_id[sid]
            merged = tuple(sorted(set(existing.owned_paths) | set(owned)))
            scopes_by_id[sid] = Scope(
                scope_id=sid,
                kind=kind,
                owned_paths=merged,
                allowed_read_paths=tuple(sorted(set(existing.allowed_read_paths) | set(allowed))),
                task_template_id=template,
                is_reconciliation=existing.is_reconciliation,
                is_eval=existing.is_eval,
                derives_from_scopes=tuple(sorted(set(existing.derives_from_scopes) | set(derives_scopes))),
            )
        else:
            scopes_by_id[sid] = Scope(
                scope_id=sid,
                kind=kind,
                owned_paths=tuple(owned),
                allowed_read_paths=tuple(allowed),
                task_template_id=template,
                derives_from_scopes=tuple(derives_scopes),
            )

    waves = assemble_waves(list(scopes_by_id.values()), max_wave_size=max_wave_size)

    # Wave dependencies (W_n → W_n+1 for non-empty waves).
    deps: list[dict[str, str]] = []
    for i in range(1, len(waves)):
        deps.append({"from": f"W{i}", "to": f"W{i + 1}"})

    return {
        "plan_id": plan_id,
        "affected_set": list(affected.affected_items),
        "waves": [
            {
                "wave_id": f"W{i + 1}",
                "scopes": [s.to_dict() for s in wave],
                "dependencies": [d for d in deps if d["to"] == f"W{i + 1}"],
            }
            for i, wave in enumerate(waves)
        ],
        "max_wave_size": max_wave_size,
    }


# ---------------------------------------------------------------------------
# execute_plan
# ---------------------------------------------------------------------------


@dataclass
class ExecuteOutcome:
    plan_id: str
    completed_scopes: list[str] = field(default_factory=list)
    failed_scopes: list[str] = field(default_factory=list)
    callback_invocations: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "completed_scopes": list(self.completed_scopes),
            "failed_scopes": list(self.failed_scopes),
            "callback_invocations": self.callback_invocations,
        }


SubagentCallback = Callable[[dict[str, Any]], dict[str, Any]]


def execute_plan(
    plan: dict[str, Any],
    callback: SubagentCallback,
    run_id: str | None = None,
    today: str | None = None,
) -> ExecuteOutcome:
    """Drive `plan` to completion via `callback`.

    `callback(task_header)` is the only subagent contract per §13.4.
    The engine builds a deterministic header for each scope, invokes the
    callback (which the skill wires up to a real subagent spawn), and
    accumulates outcomes. The engine itself never spawns subagents.

    Returns an `ExecuteOutcome` summarizing completed and failed scopes.

    For each scope, a header dict matching §13.4 is constructed and passed
    to the callback. The callback returns a dict with at least:
      {"status": "ok" | "failed", "patch": ..., "summary": ...}
    The engine treats "failed" as a non-blocking peer-failure per §13.3.
    """
    if today is None:
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
    if run_id is None:
        run_id = f"RUN-{today}-001"
    outcome = ExecuteOutcome(plan_id=plan.get("plan_id", "PLAN-unknown"))
    task_seq = 0

    for wave in plan.get("waves", []):
        # Sort scopes deterministically by scope_id (per §13.3).
        scopes = sorted(wave.get("scopes", []), key=lambda s: s.get("scope_id", ""))
        results: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for scope in scopes:
            task_seq += 1
            header = {
                "task_id": f"TASK-{today}-{task_seq:03d}",
                "run_id": run_id,
                "wave_id": wave.get("wave_id"),
                "template_id": scope.get("task_template_id"),
                "scope": {
                    "scope_id": scope.get("scope_id"),
                    "kind": scope.get("kind"),
                    "owned_paths": scope.get("owned_paths", []),
                },
                "allowed_read_paths": scope.get("allowed_read_paths", []),
                "allowed_write_paths": scope.get("owned_paths", []),
                "validation_contract": ["structural-eval-on-output"],
                "result_shape_id": f"{scope.get('kind')}-summary",
                "budget": {"max_tokens": 50000, "max_wall_ms": 60000},
            }
            outcome.callback_invocations += 1
            result = callback(header)
            results.append((header, result or {}))
        # Process in deterministic scope_id order (already sorted).
        for header, result in results:
            sid = header["scope"]["scope_id"]
            status = (result or {}).get("status", "failed")
            if status == "ok":
                outcome.completed_scopes.append(sid)
            else:
                outcome.failed_scopes.append(sid)

    return outcome


__all__ = [
    "Scope",
    "assemble_waves",
    "dispatch_plan",
    "ExecuteOutcome",
    "execute_plan",
]
