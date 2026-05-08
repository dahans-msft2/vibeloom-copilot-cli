"""Structural eval — the decidable rung (methodology §14.3, impl §14.1).

Engine-side, no LLM, no semantic judgment. Includes:
- lifecycle consistency
- required-field presence (delegated to schema.py for per-artifact)
- ID validity & registry consistency
- reference integrity (dangling derives_from)
- tier order & DAG validity (cycle detection)
- coverage / uncovered downstream obligations
- ownership rules (component → 1 container; BC → 1 component;
  BCs only in domain-layer components)
- context sufficiency (component with owned_paths has component-level config)
- `derives_from` per §5.1 + §8.2: non-root must have ≥1 upstream;
  upstream prefix must be allowed; chain must transitively reach CAP/CST.
"""

from __future__ import annotations

from vibeloom_engine.graph import find_cycles
from vibeloom_engine.ids import (
    GRAPH_ENTITY_PREFIXES,
    ROOT_PREFIXES,
    allowed_upstream,
    is_known_prefix,
    parse_semantic_id,
    prefix_spec,
    spec_for_id,
    valid_edge,
)
from vibeloom_engine.models import (
    Artifact,
    ArtifactType,
    CONTEXT_TYPES,
    CONTRACT_TYPES,
    ContainerLayer,
    Finding,
    Graph,
    Status,
)
from vibeloom_engine.schema import validate_repo


def _f(severity: str, artifact_id: str, check: str, message: str, item_id: str | None = None) -> Finding:
    return Finding(
        severity=severity,
        artifact_id=artifact_id,
        check=check,
        message=message,
        item_id=item_id,
    )


# ---------------------------------------------------------------------------
# 1. ID validity (per item)
# ---------------------------------------------------------------------------


def _id_validity(graph: Graph) -> list[Finding]:
    findings: list[Finding] = []
    for item in graph.items.values():
        parsed = parse_semantic_id(item.item_id)
        if not parsed:
            findings.append(
                _f("blocking", item.artifact_id, "id-validity",
                   f"malformed item ID {item.item_id!r}", item_id=item.item_id)
            )
            continue
        if not is_known_prefix(parsed[0]):
            findings.append(
                _f("blocking", item.artifact_id, "id-validity",
                   f"unknown prefix family in {item.item_id!r}: {parsed[0]!r}",
                   item_id=item.item_id)
            )
    return findings


# ---------------------------------------------------------------------------
# 2. Reference integrity (dangling)
# ---------------------------------------------------------------------------


def _reference_integrity(graph: Graph) -> list[Finding]:
    findings: list[Finding] = []
    for item in graph.items.values():
        for up in item.derives_from:
            if up not in graph.items:
                findings.append(
                    _f(
                        "blocking",
                        item.artifact_id,
                        "reference-integrity",
                        f"dangling derives_from in {item.item_id}: {up} not found",
                        item_id=item.item_id,
                    )
                )
    return findings


# ---------------------------------------------------------------------------
# 3. derives_from rules (§5.1 + §8.2 + §16 acceptance bullet)
# ---------------------------------------------------------------------------


def _derives_from_rules(graph: Graph) -> list[Finding]:
    findings: list[Finding] = []
    # cache transitive-root reachability — memoize per item
    reaches_root: dict[str, bool] = {}

    def _reaches_root(item_id: str, visiting: set[str]) -> bool:
        if item_id in reaches_root:
            return reaches_root[item_id]
        if item_id in visiting:
            # cycle — treat as not reaching (cycle eval reports separately)
            return False
        item = graph.items.get(item_id)
        if item is None:
            return False
        parsed = parse_semantic_id(item_id)
        if not parsed:
            return False
        prefix = parsed[0]
        if prefix in ROOT_PREFIXES:
            reaches_root[item_id] = True
            return True
        if not item.derives_from:
            reaches_root[item_id] = False
            return False
        visiting.add(item_id)
        try:
            for up in item.derives_from:
                if _reaches_root(up, visiting):
                    reaches_root[item_id] = True
                    return True
            reaches_root[item_id] = False
            return False
        finally:
            visiting.discard(item_id)

    for item in graph.items.values():
        parsed = parse_semantic_id(item.item_id)
        if not parsed:
            continue
        prefix = parsed[0]
        # Only graph-entity prefixes are subject to the rule.
        if prefix not in GRAPH_ENTITY_PREFIXES:
            continue
        if prefix in ROOT_PREFIXES:
            if item.derives_from:
                findings.append(
                    _f(
                        "blocking",
                        item.artifact_id,
                        "derives-from",
                        f"{item.item_id} is a root prefix ({prefix}); must not have derives_from",
                        item_id=item.item_id,
                    )
                )
            continue
        # Non-root: must have ≥1 upstream
        if not item.derives_from:
            findings.append(
                _f(
                    "blocking",
                    item.artifact_id,
                    "derives-from",
                    f"{item.item_id} ({prefix}) is non-root but has no derives_from (§5.1, §8.2)",
                    item_id=item.item_id,
                )
            )
            continue
        # Each upstream prefix must be allowed.
        for up in item.derives_from:
            up_parsed = parse_semantic_id(up)
            if not up_parsed:
                # dangling — handled by _reference_integrity
                continue
            up_prefix = up_parsed[0]
            if not valid_edge(prefix, up_prefix):
                allowed = allowed_upstream(prefix)
                findings.append(
                    _f(
                        "blocking",
                        item.artifact_id,
                        "derives-from",
                        (
                            f"{item.item_id} has invalid edge {prefix} ← {up_prefix} (via {up}); "
                            f"allowed upstream prefixes: {sorted(allowed) if allowed else '(root only)'}"
                        ),
                        item_id=item.item_id,
                    )
                )
        # Universal-trace (transitive root reachability per §8.2)
        if not _reaches_root(item.item_id, set()):
            findings.append(
                _f(
                    "blocking",
                    item.artifact_id,
                    "derives-from",
                    (
                        f"{item.item_id} does not transitively reach a root (CAP/CST) "
                        "via derives_from (§8.2 universal-trace)"
                    ),
                    item_id=item.item_id,
                )
            )
    return findings


# ---------------------------------------------------------------------------
# 4. Tier order / DAG validity (cycle detection)
# ---------------------------------------------------------------------------


def _cycle_findings(graph: Graph) -> list[Finding]:
    findings: list[Finding] = []
    cycles = find_cycles(graph)
    for cyc in cycles:
        path = " → ".join(cyc)
        # Pick the artifact_id of the first node in the cycle for routing.
        first = graph.items.get(cyc[0])
        artifact_id = first.artifact_id if first else "(unknown)"
        findings.append(
            _f(
                "blocking",
                artifact_id,
                "cycle",
                f"derives_from cycle: {path}",
                item_id=cyc[0],
            )
        )
    return findings


# ---------------------------------------------------------------------------
# 5. Coverage / uncovered downstream obligations
# ---------------------------------------------------------------------------

# Prefixes that legitimately have no further downstream realization.
_TERMINAL_BY_TYPE: frozenset[str] = frozenset(
    {"MET", "MS", "EXT", "TB", "SNFR", "SCN", "MOCK", "UXC", "DEF",
     "INV", "VO", "ENT", "BDD", "AGG", "CMP", "INT"}
)


def _coverage(graph: Graph) -> list[Finding]:
    findings: list[Finding] = []
    referenced: set[str] = set()
    for item in graph.items.values():
        for up in item.derives_from:
            referenced.add(up)
    for iid, item in graph.items.items():
        parsed = parse_semantic_id(iid)
        if not parsed:
            continue
        prefix = parsed[0]
        if prefix not in GRAPH_ENTITY_PREFIXES:
            continue
        if prefix in _TERMINAL_BY_TYPE:
            continue
        if iid in referenced:
            continue
        findings.append(
            _f(
                "advisory",
                item.artifact_id,
                "coverage",
                f"orphan: {iid} has no downstream item that derives_from it",
                item_id=iid,
            )
        )
    return findings


# ---------------------------------------------------------------------------
# 6. Layered architecture (methodology §6.5)
# ---------------------------------------------------------------------------


def _layered_invariants(graph: Graph, artifacts: list[Artifact]) -> list[Finding]:
    findings: list[Finding] = []

    # index containers and components
    containers = [a for a in artifacts if a.artifact_type == ArtifactType.CONTAINER]
    components = [a for a in artifacts if a.artifact_type == ArtifactType.COMPONENT]

    # cont scope_id -> layer
    container_layer: dict[str, ContainerLayer] = {}
    for c in containers:
        if c.layer is not None:
            container_layer[c.scope.scope_id] = c.layer

    # Component → exactly one container (frontmatter `container_id` matches).
    seen_container_for_component: dict[str, str] = {}
    for comp in components:
        cid = comp.extras.get("container_id")
        if not cid:
            findings.append(
                _f(
                    "blocking",
                    comp.artifact_id,
                    "ownership",
                    "component frontmatter missing container_id (methodology §6.5)",
                )
            )
            continue
        cid_str = str(cid)
        prior = seen_container_for_component.get(comp.artifact_id)
        if prior is not None and prior != cid_str:
            findings.append(
                _f(
                    "blocking",
                    comp.artifact_id,
                    "ownership",
                    f"component {comp.artifact_id} declares two container_ids ({prior}, {cid_str})",
                )
            )
        seen_container_for_component[comp.artifact_id] = cid_str

    # Bounded contexts only in domain-layer containers.
    # Track BC → component, BC → container.
    bc_to_component: dict[str, str] = {}
    for comp in components:
        hosted = comp.extras.get("hosted_bounded_contexts") or []
        if not isinstance(hosted, list):
            findings.append(
                _f(
                    "blocking",
                    comp.artifact_id,
                    "ownership",
                    "component `hosted_bounded_contexts` must be a list",
                )
            )
            continue
        # Determine layer of the parent container — by scope_id prefix or container_id link.
        cid_str = str(comp.extras.get("container_id", ""))
        # Lookup via container.scope.scope_id
        parent_container_layer: ContainerLayer | None = None
        for c in containers:
            # Match via CONT-#### items — container's items typically include a CONT row;
            # for v0.3 we trust the container artifact's scope_id == the container slug,
            # and the component's container_id refers either to that slug or a CONT-####.
            if c.scope.scope_id == cid_str:
                parent_container_layer = c.layer
                break
        # Or the container_id might refer to a CONT-#### item.
        if parent_container_layer is None and cid_str.startswith("CONT-"):
            for c in containers:
                if any(it.item_id == cid_str for it in c.items):
                    parent_container_layer = c.layer
                    break
        # If non-domain layer, hosted_bounded_contexts must be empty.
        if parent_container_layer is not None and parent_container_layer != ContainerLayer.DOMAIN:
            if hosted:
                findings.append(
                    _f(
                        "blocking",
                        comp.artifact_id,
                        "layered-architecture",
                        (
                            f"component in {parent_container_layer.value} layer hosts "
                            f"bounded_contexts {hosted!r}; only domain-layer components may "
                            "host BCs (methodology §6.4 / §6.5)"
                        ),
                    )
                )
        # BC → exactly one component.
        for bc in hosted:
            bc_str = str(bc)
            if bc_str in bc_to_component and bc_to_component[bc_str] != comp.artifact_id:
                findings.append(
                    _f(
                        "blocking",
                        comp.artifact_id,
                        "ownership",
                        f"bounded context {bc_str} hosted by both {bc_to_component[bc_str]} and {comp.artifact_id}",
                    )
                )
            bc_to_component[bc_str] = comp.artifact_id

    return findings


# ---------------------------------------------------------------------------
# 7. Context sufficiency (component owns paths → has config)
# ---------------------------------------------------------------------------


def _context_sufficiency(graph: Graph, artifacts: list[Artifact]) -> list[Finding]:
    findings: list[Finding] = []
    components = [a for a in artifacts if a.artifact_type == ArtifactType.COMPONENT]
    configs = [a for a in artifacts if a.artifact_type == ArtifactType.CONFIG]

    config_scopes: set[str] = set()
    for c in configs:
        config_scopes.add(f"{c.scope.kind.value}:{c.scope.scope_id}")

    for comp in components:
        owned = comp.extras.get("owned_paths") or []
        if owned:
            key = f"component:{comp.scope.scope_id}"
            if key not in config_scopes:
                findings.append(
                    _f(
                        "advisory",
                        comp.artifact_id,
                        "context-sufficiency",
                        (
                            f"component {comp.artifact_id} owns paths but has no component-level "
                            "config (AGENTS.md/CLAUDE.md)"
                        ),
                    )
                )
    return findings


# ---------------------------------------------------------------------------
# 8. Lifecycle consistency
# ---------------------------------------------------------------------------


def _lifecycle_consistency(graph: Graph, artifacts: list[Artifact]) -> list[Finding]:
    findings: list[Finding] = []
    # within an approval_unit, all artifacts must agree on status
    by_unit: dict[str, list[Artifact]] = {}
    for a in artifacts:
        if a.artifact_type not in CONTRACT_TYPES:
            continue
        if not a.approval_unit:
            continue
        by_unit.setdefault(a.approval_unit, []).append(a)
    for unit, members in by_unit.items():
        statuses = {m.status for m in members if m.status is not None}
        if len(statuses) > 1:
            members_str = ", ".join(f"{m.artifact_id}={m.status.value}" for m in members if m.status)
            for m in members:
                findings.append(
                    _f(
                        "blocking",
                        m.artifact_id,
                        "lifecycle",
                        f"approval_unit {unit!r} has mixed statuses: {members_str}",
                    )
                )
    return findings


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------


def structural_eval(
    graph: Graph,
    artifacts: list[Artifact],
    target: str | None = None,
) -> list[Finding]:
    """Run all structural checks across the graph.

    `target` is an optional tier filter; when set, returns only findings
    pertaining to that tier (artifacts in the tier or items in those artifacts).
    The full set of cross-artifact checks always runs — filtering is a final
    pass so the engine doesn't miss DAG-wide violations.
    """
    findings: list[Finding] = []
    findings.extend(validate_repo(artifacts))
    findings.extend(_id_validity(graph))
    findings.extend(_reference_integrity(graph))
    findings.extend(_derives_from_rules(graph))
    findings.extend(_cycle_findings(graph))
    findings.extend(_coverage(graph))
    findings.extend(_layered_invariants(graph, artifacts))
    findings.extend(_context_sufficiency(graph, artifacts))
    findings.extend(_lifecycle_consistency(graph, artifacts))

    if target:
        artifact_tier = {a.artifact_id: a.tier for a in artifacts}
        filtered: list[Finding] = []
        for f in findings:
            tier = artifact_tier.get(f.artifact_id)
            if tier == target:
                filtered.append(f)
        findings = filtered

    # Assign FIND-#### sequentially (per-invocation counter).
    for i, f in enumerate(findings, start=1):
        f.finding_id = f"FIND-{i:04d}"

    return findings


__all__ = ["structural_eval"]
