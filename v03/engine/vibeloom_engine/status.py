"""Status computation per §10 (six categories).

`current` / `stale` / `uncovered` / `dangling` / `drifted` / `obsolete`.

The classifier consumes:
- the parsed graph (current items + artifacts)
- the latest approval traces (per-item approved hash, per-artifact hash)
- the id-registry's retired list (for `dangling`)
- eval findings (a finding on an item triggers `drifted` per §10's
  "semantic mismatch flagged by eval" wording for items, vs `current`
  requiring "no eval finding")
- direct-edit detections (which trigger `drifted` per §10)
- user-marked obsolete IDs (passed in or sourced from registry — the
  v0.3 engine surfaces obsolete candidates but never auto-marks; explicit
  marking is via `vibeloom mark-obsolete <id>` at the orchestrator level,
  recorded in the registry).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from vibeloom_engine.eval_ import structural_eval
from vibeloom_engine.graph import canonical_artifact_hash, canonical_item_hash
from vibeloom_engine.ids import GRAPH_ENTITY_PREFIXES, ROOT_PREFIXES, parse_semantic_id
from vibeloom_engine.models import Artifact, ArtifactType, Graph, Status
from vibeloom_engine.registry import load_registry
from vibeloom_engine.staleness import (
    detect_direct_edits,
    latest_approval_per_artifact,
    latest_approval_per_item,
)


# ---------------------------------------------------------------------------
# Per-item classification
# ---------------------------------------------------------------------------


def _is_dangling(item_id: str, item, graph: Graph, retired_ids: set[str]) -> tuple[bool, str | None]:
    """Return (True, basis) if any basis is retired-or-missing."""
    for basis in item.derives_from:
        if basis in retired_ids:
            return True, basis
        if basis not in graph.items:
            return True, basis
    return False, None


def _required_downstream(graph: Graph) -> dict[str, set[str]]:
    """Return {parent_artifact_id: {required_kind}}.

    Heuristic per impl §6 / methodology §6.2 / §6.4:
      - intent.md (CAP/CST) → requires prd.md (FR)
      - Approved CMP that has owned_paths but no SCN/BDD → uncovered
        (kept simple in v0.3; the spec is silent on full enumeration).

    The §10 `uncovered` definition is broader: "approved upstream item
    lacks required downstream realization." For v0.3 we surface the most
    common cases and leave the rest for skill-side semantic eval.
    """
    out: dict[str, set[str]] = {}
    return out


def classify_items(
    repo_root: Path,
    graph: Graph,
    artifacts: list[Artifact],
) -> dict[str, dict[str, Any]]:
    """Return {item_id: {status, reason, ...}} per §10."""
    item_approved = latest_approval_per_item(repo_root)
    artifact_approved = latest_approval_per_artifact(repo_root)
    direct_edits = detect_direct_edits(repo_root, graph, artifacts)
    edited_item_ids: set[str] = set()
    for e in direct_edits:
        for iid in e.get("modified_items", []):
            edited_item_ids.add(iid)
        # Items added via direct edit are also flagged as drifted per §10
        # (unvalidated divergence).
        for iid in e.get("added_items", []):
            edited_item_ids.add(iid)

    # eval findings keyed by item_id
    findings = structural_eval(graph, artifacts)
    finding_by_item: dict[str, list[dict[str, Any]]] = {}
    for f in findings:
        if f.severity != "blocking":
            continue
        if f.item_id:
            finding_by_item.setdefault(f.item_id, []).append(f.to_dict())

    # retired ids from registry
    registry = load_registry(repo_root)
    retired_ids: set[str] = set()
    for prefix, entry in registry.items():
        if isinstance(entry, dict):
            for r in entry.get("retired") or []:
                if isinstance(r, str):
                    retired_ids.add(r)

    # obsolete-marked ids — registry may carry per-prefix `obsolete` list
    obsolete_ids: set[str] = set()
    for prefix, entry in registry.items():
        if isinstance(entry, dict):
            for o in entry.get("obsolete") or []:
                if isinstance(o, str):
                    obsolete_ids.add(o)

    out: dict[str, dict[str, Any]] = {}
    for iid, item in graph.items.items():
        parsed = parse_semantic_id(iid)
        if not parsed:
            out[iid] = {"status": "drifted", "reason": "malformed_id"}
            continue
        prefix = parsed[0]
        # only classify graph entities; structured carriers are skipped
        if prefix not in GRAPH_ENTITY_PREFIXES:
            continue
        # 1. obsolete (user-marked)
        if iid in obsolete_ids:
            out[iid] = {"status": "obsolete", "reason": "user_marked"}
            continue
        # 2. dangling
        is_d, basis = _is_dangling(iid, item, graph, retired_ids)
        if is_d:
            out[iid] = {"status": "dangling", "reason": "basis_retired_or_missing", "basis": basis}
            continue
        # 3. drifted via direct edit or eval finding
        if iid in edited_item_ids:
            out[iid] = {"status": "drifted", "reason": "direct_edit"}
            continue
        if iid in finding_by_item:
            out[iid] = {
                "status": "drifted",
                "reason": "eval_finding",
                "findings": finding_by_item[iid],
            }
            continue
        # 4. multi-basis lookup per §10
        if prefix in ROOT_PREFIXES:
            # Roots: current iff approved; uncovered otherwise (no basis to be stale)
            approved_hash = item_approved.get(iid)
            if approved_hash is None:
                out[iid] = {"status": "uncovered", "reason": "no_approval_yet"}
                continue
            current_hash = canonical_item_hash(item)
            if approved_hash != current_hash:
                # Approved root content was edited: drifted
                out[iid] = {"status": "drifted", "reason": "approved_root_changed_post_approval"}
            else:
                out[iid] = {"status": "current"}
            continue
        # Non-root: walk all bases
        any_dangling = False
        any_unapproved = False
        any_changed = False
        for basis in item.derives_from:
            basis_item = graph.items.get(basis)
            if basis_item is None:
                any_dangling = True
                continue
            approved_hash = item_approved.get(basis)
            if approved_hash is None:
                any_unapproved = True
                continue
            if canonical_item_hash(basis_item) != approved_hash:
                any_changed = True
        if any_dangling:
            out[iid] = {"status": "dangling", "reason": "basis_dangling"}
        elif any_unapproved:
            out[iid] = {"status": "uncovered", "reason": "basis_unapproved"}
        elif any_changed:
            out[iid] = {"status": "stale", "reason": "basis_changed"}
        else:
            out[iid] = {"status": "current"}

    return out


# ---------------------------------------------------------------------------
# Lifecycle per artifact
# ---------------------------------------------------------------------------


def _lifecycle_per_artifact(artifacts: list[Artifact]) -> dict[str, str]:
    out: dict[str, str] = {}
    for a in artifacts:
        if a.status is not None:
            out[a.artifact_id] = a.status.value
        else:
            out[a.artifact_id] = "n/a"
    return out


# ---------------------------------------------------------------------------
# Recommend-next
# ---------------------------------------------------------------------------


def _recommend_next(report: dict[str, Any]) -> str:
    """Recommend the next operation based on category counts (heuristic)."""
    counts = report["category_counts"]
    if counts.get("dangling", 0):
        return "reconcile (resolve dangling references)"
    if counts.get("drifted", 0):
        return "reconcile (resolve drift)"
    if counts.get("stale", 0):
        return "generate (regenerate stale downstream)"
    if counts.get("uncovered", 0):
        return "generate (cover uncovered downstream)"
    if any(v == "draft" for v in report["lifecycle"].values()):
        return "review intent-specs (then approve)"
    return "status (no action needed)"


# ---------------------------------------------------------------------------
# Public entry: compute_status
# ---------------------------------------------------------------------------


def compute_status(
    repo_root: Path,
    graph: Graph,
    artifacts: list[Artifact],
) -> dict[str, Any]:
    classification = classify_items(repo_root, graph, artifacts)
    counts: dict[str, int] = {}
    for c in ("current", "stale", "uncovered", "dangling", "drifted", "obsolete"):
        counts[c] = 0
    for v in classification.values():
        s = v.get("status", "current")
        counts[s] = counts.get(s, 0) + 1

    # Affected scope: artifacts containing any non-current item
    affected_artifacts: set[str] = set()
    for iid, info in classification.items():
        if info.get("status") != "current":
            it = graph.items.get(iid)
            if it:
                affected_artifacts.add(it.artifact_id)

    report = {
        "category_counts": counts,
        "items": classification,
        "lifecycle": _lifecycle_per_artifact(artifacts),
        "affected_artifacts": sorted(affected_artifacts),
        "uncovered_artifacts": [],
        "current_mode": _infer_mode(graph, artifacts),
    }
    report["recommended_next"] = _recommend_next(report)
    return report


def _infer_mode(graph: Graph, artifacts: list[Artifact]) -> str:
    """Heuristic mode inference. Vibe = no product/system files."""
    types = {a.artifact_type for a in artifacts}
    # vibe: only intent + defaults + system + config
    full_required = {ArtifactType.PRD, ArtifactType.USM, ArtifactType.DM}
    has_full = bool(full_required & types)
    has_ux = ArtifactType.UX in types
    if not has_full:
        return "vibe"
    if has_ux:
        return "ux-or-pm"
    return "pm-or-dev"


__all__ = ["classify_items", "compute_status"]
