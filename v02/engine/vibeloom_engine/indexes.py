"""Dispatch-support indexes.

Per vibeloom-implementation.md ## Context Graph Realization ### Explicitly
Stored, the engine maintains indexes so it can answer affected-set, load-set,
and validation queries without rescanning artifacts. Typical indexes:

- interface provider / consumer index for owned_interfaces, IF-####, and DEP-#### carriers
- dependency-target index for referenced components and containers
- write-scope index derived from owned_paths
- context-relevance index linking bdd, pdr, adr records to affected scopes
- scope summary records used to build targeted foreign slices and dispatch plans

These indexes are derived views over Graph; the engine may rebuild them at
will. They are included in the graph-cache JSON for startup efficiency.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from vibeloom_engine.ids import parse_id
from vibeloom_engine.models import Artifact, ArtifactType, Graph, Item


@dataclass
class Indexes:
    """All dispatch-support indexes."""

    # IF-####/interface-name → component artifact_id that provides it.
    interface_provider: dict[str, str] = field(default_factory=dict)
    # IF-####/interface-name → list of component artifact_ids that consume it (via DEP).
    interface_consumers: dict[str, list[str]] = field(default_factory=dict)
    # DEP-#### → target (component artifact_id or external-system label).
    dependency_target: dict[str, str] = field(default_factory=dict)
    # component artifact_id → list of owned_paths (from frontmatter or body).
    write_scope: dict[str, list[str]] = field(default_factory=dict)
    # scope_id (container or component) → list of relevant context artifact_ids.
    context_relevance: dict[str, list[str]] = field(default_factory=dict)
    # scope_id → summary record (container/component slug, bc, inventory counts).
    scope_summary: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "interface_provider": dict(self.interface_provider),
            "interface_consumers": {k: list(v) for k, v in self.interface_consumers.items()},
            "dependency_target": dict(self.dependency_target),
            "write_scope": {k: list(v) for k, v in self.write_scope.items()},
            "context_relevance": {k: list(v) for k, v in self.context_relevance.items()},
            "scope_summary": {k: dict(v) for k, v in self.scope_summary.items()},
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Indexes":
        return cls(
            interface_provider=dict(d.get("interface_provider", {})),
            interface_consumers={k: list(v) for k, v in d.get("interface_consumers", {}).items()},
            dependency_target=dict(d.get("dependency_target", {})),
            write_scope={k: list(v) for k, v in d.get("write_scope", {}).items()},
            context_relevance={k: list(v) for k, v in d.get("context_relevance", {}).items()},
            scope_summary={k: dict(v) for k, v in d.get("scope_summary", {}).items()},
        )


def _owned_paths(artifact: Artifact) -> list[str]:
    raw = artifact.extras.get("owned_paths", [])
    if isinstance(raw, list):
        return [str(x) for x in raw]
    if isinstance(raw, str) and raw.strip():
        return [raw.strip()]
    return []


def _owned_interfaces(artifact: Artifact) -> list[str]:
    raw = artifact.extras.get("owned_interfaces", [])
    if isinstance(raw, list):
        return [str(x) for x in raw]
    if isinstance(raw, str) and raw.strip():
        return [raw.strip()]
    return []


def _iter_component_artifacts(graph: Graph) -> list[Artifact]:
    return [a for a in graph.artifacts.values() if a.artifact_type == ArtifactType.COMPONENT]


def build_indexes(graph: Graph) -> Indexes:
    """Compute all dispatch-support indexes from a Graph."""
    idx = Indexes()

    # interface_provider: each IF-#### item owned by a component.md provides itself.
    for item in graph.items.values():
        parsed = parse_id(item.item_id)
        if parsed and parsed[0] == "IF":
            idx.interface_provider[item.item_id] = item.artifact_id

    # Also allow named interfaces declared in owned_interfaces frontmatter.
    for a in _iter_component_artifacts(graph):
        for name in _owned_interfaces(a):
            idx.interface_provider.setdefault(name, a.artifact_id)

    # interface_consumers + dependency_target from DEP-#### items.
    for item in graph.items.values():
        parsed = parse_id(item.item_id)
        if not parsed or parsed[0] != "DEP":
            continue
        # Target is whatever `target` column put in extras.
        target = item.extra.get("target") or item.extra.get("dependency") or ""
        target = str(target).strip().strip("`").strip()
        if not target:
            continue
        idx.dependency_target[item.item_id] = target
        # If target looks like an interface or component, register a consumer.
        consumer_artifact = item.artifact_id
        if target:
            idx.interface_consumers.setdefault(target, []).append(consumer_artifact)

    # write_scope from component owned_paths.
    for a in _iter_component_artifacts(graph):
        paths = _owned_paths(a)
        if paths:
            idx.write_scope[a.artifact_id] = paths

    # context_relevance: bdd artifacts by scope_id; pdr/adr are repo-wide.
    for a in graph.artifacts.values():
        if a.artifact_type == ArtifactType.BDD:
            idx.context_relevance.setdefault(a.scope.scope_id, []).append(a.artifact_id)
        elif a.artifact_type in (ArtifactType.PDR, ArtifactType.ADR):
            idx.context_relevance.setdefault("root", []).append(a.artifact_id)

    # scope_summary: per-container and per-component quick summary.
    for a in graph.artifacts.values():
        if a.artifact_type == ArtifactType.CONTAINER:
            summary = {
                "kind": "container",
                "artifact_id": a.artifact_id,
                "container_id": a.extras.get("container_id"),
                "component_count": sum(
                    1
                    for x in graph.artifacts.values()
                    if x.artifact_type == ArtifactType.COMPONENT
                    and x.scope.scope_id.startswith(a.scope.scope_id + ".")
                ),
            }
            idx.scope_summary[a.scope.scope_id] = summary
        elif a.artifact_type == ArtifactType.COMPONENT:
            summary = {
                "kind": "component",
                "artifact_id": a.artifact_id,
                "container_id": a.extras.get("container_id"),
                "component_id": a.extras.get("component_id"),
                "bounded_context": a.extras.get("bounded_context"),
                "owned_paths": _owned_paths(a),
                "owned_interfaces": _owned_interfaces(a),
            }
            idx.scope_summary[a.scope.scope_id] = summary

    return idx
