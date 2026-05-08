"""Affected-set computation per impl §15.

Given a seed list of item IDs, returns the union of those items' downstream
closures plus their owning artifacts. The orchestrator wraps this with
include filters (`stale`, `uncovered`, `drifted`, `dangling`, `obsolete`)
when assembling a plan; the engine is the deterministic substrate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from vibeloom_engine.graph import reachable_downstream
from vibeloom_engine.models import Graph


@dataclass
class AffectedSet:
    seed_ids: list[str] = field(default_factory=list)
    affected_items: list[str] = field(default_factory=list)
    affected_artifacts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "seed_ids": list(self.seed_ids),
            "affected_items": list(self.affected_items),
            "affected_artifacts": list(self.affected_artifacts),
        }


def compute_affected_set(graph: Graph, seed_ids: list[str]) -> AffectedSet:
    """Compute the affected set for a list of seed item IDs.

    Returns:
      - seed_ids: the input (unchanged, deterministic).
      - affected_items: every item reachable downstream from any seed,
        sorted lexicographically.
      - affected_artifacts: artifacts owning any affected item, sorted.

    Items that don't exist in the graph are dropped silently — the seed list
    may include retired/missing IDs in the dangling case; the orchestrator
    surfaces those separately.
    """
    valid_seeds = [s for s in seed_ids if s in graph.items]
    items = reachable_downstream(graph, valid_seeds)
    artifact_ids: set[str] = set()
    for iid in items:
        item = graph.items.get(iid)
        if item is not None:
            artifact_ids.add(item.artifact_id)
    return AffectedSet(
        seed_ids=list(seed_ids),
        affected_items=sorted(items),
        affected_artifacts=sorted(artifact_ids),
    )


__all__ = ["AffectedSet", "compute_affected_set"]
