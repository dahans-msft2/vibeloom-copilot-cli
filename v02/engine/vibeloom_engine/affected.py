"""Affected-set computation.

Walking derivation edges forward from changed items yields the affected set.
Affected artifacts, tiers, and scopes are then computed by ownership lookup.

See vibeloom-methodology.md ## Context Graph ### Affected Set.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from vibeloom_engine.graph import reachable_forward
from vibeloom_engine.models import Graph


@dataclass
class AffectedSet:
    item_ids: set[str] = field(default_factory=set)
    artifact_ids: set[str] = field(default_factory=set)
    tiers: set[str] = field(default_factory=set)
    scopes: set[str] = field(default_factory=set)

    def to_dict(self) -> dict:
        return {
            "items": sorted(self.item_ids),
            "artifacts": sorted(self.artifact_ids),
            "tiers": sorted(self.tiers),
            "scopes": sorted(self.scopes),
        }


def compute_affected_set(graph: Graph, changed_ids: list[str]) -> AffectedSet:
    """Compute the affected set for a list of changed item IDs.

    Walks forward (downstream) from every changed item and projects the reached
    items to their owning artifacts, tiers, and scopes.
    """
    reached_items = reachable_forward(graph, changed_ids)
    affected = AffectedSet(item_ids=reached_items)
    for iid in reached_items:
        item = graph.items.get(iid)
        if not item:
            continue
        affected.artifact_ids.add(item.artifact_id)
        affected.tiers.add(item.tier)
        affected.scopes.add(item.scope.scope_id)
    return affected
