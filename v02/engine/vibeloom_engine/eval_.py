"""Structural eval.

Implements the nine structural checks from vibeloom-methodology.md ## Generation ### Eval:

1. Lifecycle consistency — draft/approved states consistent across the approval unit
2. Reference integrity — all derives_from point to existing items
3. Required fields — every artifact has required frontmatter fields per template
4. Declared relationships — items owned by correct artifacts, scopes, tiers
5. Stack integrity — tiers in correct dependency order
6. Coverage — every non-terminal upstream item appears in at least one downstream derives_from
7. Contradiction — no downstream item conflicts with its derives_from basis (partial: structural only)
8. Componentization fit — every component maps to exactly one BC; BCs fully contained in one container
9. Context sufficiency — code-owning components have config; populated containers have container-level config

Checks 1, 3, 4 are handled by schema.py (per-artifact). This module adds the
cross-artifact and graph-level checks (2, 5, 6, 7 structural, 8, 9).
"""

from __future__ import annotations

from vibeloom_engine.ids import (
    DAG_EDGES,
    ROOT_PREFIXES,
    TERMINAL_BY_TYPE_PREFIXES,
    parse_id,
    spec_for_id,
    valid_edge,
)
from vibeloom_engine.models import (
    Artifact,
    ArtifactType,
    CONTEXT_TYPES,
    CONTRACT_TYPES,
    Graph,
)
from vibeloom_engine.schema import Finding, validate_repo

# Tier order constraint for stack-integrity: if a lower-tier artifact exists,
# its upstream tiers must also exist.
_TIER_ORDER: tuple[str, ...] = (
    "intent-specs",
    "product-specs",
    "system-specs",
    "context",
    "code",
)


def _reference_integrity(graph: Graph) -> list[Finding]:
    findings: list[Finding] = []
    for item in graph.items.values():
        for up in item.derives_from:
            if up not in graph.items:
                findings.append(
                    Finding(
                        severity="error",
                        artifact_id=item.artifact_id,
                        check="reference-integrity",
                        message=f"dangling derives_from reference in {item.item_id}: {up} not found",
                    )
                )
    return findings


def _edge_validity(graph: Graph) -> list[Finding]:
    findings: list[Finding] = []
    for item in graph.items.values():
        parsed = parse_id(item.item_id)
        if not parsed:
            continue
        prefix, _ = parsed
        # Structured-content prefixes and ledger records are exempt from DAG validation.
        if prefix not in DAG_EDGES:
            continue

        # Special case: CST-#### inside defaults.md is a `default` entity (not a
        # root constraint). Per methodology DAG: default derives from constraint.
        owning = graph.artifacts.get(item.artifact_id)
        is_default = (
            prefix == "CST"
            and owning is not None
            and owning.artifact_type.value == "defaults"
        )
        if is_default:
            # Must have derives_from; each entry must be a CST (constraint) item
            # owned by intent.
            if not item.derives_from:
                findings.append(
                    Finding(
                        severity="error",
                        artifact_id=item.artifact_id,
                        check="reference-integrity",
                        message=f"{item.item_id} in defaults must derive from at least one CST item in intent",
                    )
                )
            for up in item.derives_from:
                up_parsed = parse_id(up)
                if not up_parsed or up_parsed[0] != "CST":
                    # Dangling handled elsewhere; here we only flag wrong prefix.
                    if up_parsed:
                        findings.append(
                            Finding(
                                severity="error",
                                artifact_id=item.artifact_id,
                                check="reference-integrity",
                                message=(
                                    f"{item.item_id} in defaults has invalid derivation edge "
                                    f"default ← {up_parsed[0]} (via {up}); allowed: constraint (CST)"
                                ),
                            )
                        )
            continue

        # Root prefixes: must not have derives_from entries.
        if prefix in ROOT_PREFIXES:
            if item.derives_from:
                findings.append(
                    Finding(
                        severity="error",
                        artifact_id=item.artifact_id,
                        check="reference-integrity",
                        message=f"{item.item_id} is a root entity type but has derives_from entries",
                    )
                )
            continue
        # Non-root prefixes: every derives_from entry must be a valid typed edge.
        if not item.derives_from:
            # Handled by coverage/completeness below; not a reference-integrity issue here.
            continue
        for up in item.derives_from:
            up_parsed = parse_id(up)
            if not up_parsed:
                # Dangling reference; reported by _reference_integrity.
                continue
            up_prefix = up_parsed[0]
            if not valid_edge(prefix, up_prefix):
                findings.append(
                    Finding(
                        severity="error",
                        artifact_id=item.artifact_id,
                        check="reference-integrity",
                        message=(
                            f"{item.item_id} has invalid derivation edge "
                            f"{prefix} ← {up_prefix} (via {up}); "
                            f"allowed: {', '.join(DAG_EDGES[prefix]) or '(root only)'}"
                        ),
                    )
                )
    return findings


def _declared_relationships(graph: Graph) -> list[Finding]:
    """Items must be owned by the correct artifact, scope, tier (per prefix family)."""
    findings: list[Finding] = []
    for item in graph.items.values():
        spec = spec_for_id(item.item_id)
        if not spec:
            continue
        if spec.tier.value != item.tier:
            findings.append(
                Finding(
                    severity="warning",
                    artifact_id=item.artifact_id,
                    check="declared-relationships",
                    message=(
                        f"{item.item_id} is in tier {item.tier!r} but its prefix family {spec.prefix} "
                        f"belongs to {spec.tier.value}"
                    ),
                )
            )
    return findings


def _is_vibe_repo(graph: Graph) -> bool:
    """Heuristic: a repo is in vibe mode when it has no product-specs artifacts
    AND no containers.md/container.md/component.md artifacts."""
    types_present = {a.artifact_type for a in graph.artifacts.values()}
    vibe_absent = {
        ArtifactType.PRD,
        ArtifactType.USM,
        ArtifactType.DM,
        ArtifactType.CONTAINERS,
        ArtifactType.CONTAINER,
        ArtifactType.COMPONENT,
    }
    return types_present.isdisjoint(vibe_absent)


def _stack_integrity(graph: Graph) -> list[Finding]:
    """If a tier has artifacts, all upstream contract tiers must also have artifacts.

    In vibe mode, product-specs is intentionally absent — that is not a stack
    violation.
    """
    findings: list[Finding] = []
    tiers_present = {a.tier for a in graph.artifacts.values()}
    vibe = _is_vibe_repo(graph)
    # Contract tiers in order. In vibe, product-specs is not part of the stack.
    if vibe:
        contract_order = ("intent-specs", "system-specs")
    else:
        contract_order = ("intent-specs", "product-specs", "system-specs")
    for i, tier in enumerate(contract_order):
        if tier in tiers_present:
            for earlier in contract_order[:i]:
                if earlier not in tiers_present:
                    findings.append(
                        Finding(
                            severity="error",
                            artifact_id="(repo)",
                            check="stack-integrity",
                            message=f"tier {tier} has artifacts but upstream tier {earlier} is missing",
                        )
                    )
    return findings


def _coverage(graph: Graph) -> list[Finding]:
    """Every non-terminal upstream item should appear in at least one downstream derives_from.

    Exempts:
      - prefixes terminal by type (MET, MS, EXT, TB, SNFR, SCN)
      - intentionally terminal items (no downstream yet but flagged as such — not detectable in v0.1)
    """
    findings: list[Finding] = []
    # Build set of items referenced by any downstream derives_from.
    referenced: set[str] = set()
    for item in graph.items.values():
        for up in item.derives_from:
            referenced.add(up)
    for iid, item in graph.items.items():
        parsed = parse_id(iid)
        if not parsed:
            continue
        prefix = parsed[0]
        # Skip structured/ledger entries (they aren't DAG nodes).
        if prefix not in DAG_EDGES:
            continue
        # Skip prefixes that are terminal by type.
        if prefix in TERMINAL_BY_TYPE_PREFIXES:
            continue
        if iid in referenced:
            continue
        findings.append(
            Finding(
                severity="warning",
                artifact_id=item.artifact_id,
                check="coverage",
                message=f"orphaned non-terminal upstream: {iid} has no downstream item derives_from it",
            )
        )
    return findings


def _componentization_fit(graph: Graph) -> list[Finding]:
    """Every component must map to exactly one bounded context; BCs must live in one container."""
    findings: list[Finding] = []
    # Component → BC check: each component.md's bounded_context frontmatter must be a single BC-####.
    bc_to_container: dict[str, str] = {}  # BC id → container artifact_id
    for a in graph.artifacts.values():
        if a.artifact_type != ArtifactType.COMPONENT:
            continue
        bc = a.extras.get("bounded_context")
        if not bc:
            findings.append(
                Finding(
                    severity="error",
                    artifact_id=a.artifact_id,
                    check="componentization-fit",
                    message="component missing bounded_context",
                )
            )
            continue
        container_id = a.extras.get("container_id")
        if not container_id:
            continue
        # Track BCs → container mapping.
        prev = bc_to_container.get(bc)
        # Identify the container artifact by CONT-#### in its frontmatter.
        # We look up the CONT-#### via the component's container_id field.
        container_id_str = str(container_id)
        if prev is None:
            bc_to_container[bc] = container_id_str
        elif prev != container_id_str:
            findings.append(
                Finding(
                    severity="error",
                    artifact_id=a.artifact_id,
                    check="componentization-fit",
                    message=(
                        f"bounded context {bc} spans multiple containers ({prev} and {container_id_str})"
                    ),
                )
            )
    return findings


def _context_sufficiency(graph: Graph) -> list[Finding]:
    """Every component with non-empty owned_paths has component-level config;
    every container with at least one component has container-level config.
    """
    findings: list[Finding] = []
    components = [a for a in graph.artifacts.values() if a.artifact_type == ArtifactType.COMPONENT]
    containers = [a for a in graph.artifacts.values() if a.artifact_type == ArtifactType.CONTAINER]
    configs = [a for a in graph.artifacts.values() if a.artifact_type == ArtifactType.CONFIG]

    # Index configs by scope_kind + scope_id.
    config_scopes: set[str] = set()
    for c in configs:
        config_scopes.add(f"{c.scope.kind.value}:{c.scope.scope_id}")

    for comp in components:
        owned = comp.extras.get("owned_paths") or []
        if owned:
            key = f"component:{comp.scope.scope_id}"
            if key not in config_scopes:
                findings.append(
                    Finding(
                        severity="error",
                        artifact_id=comp.artifact_id,
                        check="context-sufficiency",
                        message=f"component {comp.artifact_id} owns paths but has no component-level config",
                    )
                )

    # Containers: does the container have any components?
    components_by_container: dict[str, list[Artifact]] = {}
    for comp in components:
        # scope_id for component is "<container-slug>.<component-slug>"
        container_slug = comp.scope.scope_id.rsplit(".", 1)[0]
        components_by_container.setdefault(container_slug, []).append(comp)
    for cont in containers:
        slug = cont.scope.scope_id
        if components_by_container.get(slug):
            key = f"container:{slug}"
            if key not in config_scopes:
                findings.append(
                    Finding(
                        severity="error",
                        artifact_id=cont.artifact_id,
                        check="context-sufficiency",
                        message=f"container {cont.artifact_id} has components but no container-level config",
                    )
                )
    return findings


def eval_graph(graph: Graph, artifacts: list[Artifact] | None = None) -> list[Finding]:
    """Run all structural checks against a graph and return findings.

    If `artifacts` is provided, also runs per-artifact schema.validate_repo.
    """
    findings: list[Finding] = []
    if artifacts is not None:
        findings.extend(validate_repo(artifacts))
    findings.extend(_reference_integrity(graph))
    findings.extend(_edge_validity(graph))
    findings.extend(_declared_relationships(graph))
    findings.extend(_stack_integrity(graph))
    findings.extend(_coverage(graph))
    findings.extend(_componentization_fit(graph))
    findings.extend(_context_sufficiency(graph))
    return findings


def eval_target(
    graph: Graph,
    artifacts: list[Artifact],
    target: str,
) -> list[Finding]:
    """Run structural eval scoped to a target tier or layer.

    For contract tiers, checks run across all artifacts at that tier plus
    cross-artifact graph rules. For context/code, the checks that apply are
    limited to reference integrity and ownership. Methodology says `eval` is
    always target-bounded and never inspects downstream.
    """
    if target in CONTRACT_TYPES:
        # Target is an artifact type name, not a tier. Accept either form.
        pass
    tier_map = {
        "intent-specs": "intent-specs",
        "product-specs": "product-specs",
        "system-specs": "system-specs",
        "context": "context",
        "code": "code",
    }
    tier = tier_map.get(target)
    if tier is None:
        raise ValueError(f"Unknown eval target: {target}")
    # Filter artifacts to this tier for schema.validate_repo and per-artifact checks.
    scoped_artifacts = [a for a in artifacts if a.tier == tier]
    findings: list[Finding] = []
    # Always run reference integrity + edge validity across the whole graph —
    # they are cheap and catch regressions even when scoped.
    findings.extend(validate_repo(scoped_artifacts))
    findings.extend(_reference_integrity(graph))
    findings.extend(_edge_validity(graph))
    if tier in ("intent-specs", "product-specs", "system-specs"):
        findings.extend(_stack_integrity(graph))
        findings.extend(_coverage(graph))
    if tier == "system-specs":
        findings.extend(_componentization_fit(graph))
    if tier == "context":
        findings.extend(_context_sufficiency(graph))
    return findings
