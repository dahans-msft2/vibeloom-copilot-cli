"""Staleness computation and direct-edit detection.

Staleness is a computed property: an artifact is stale when its approved
upstream basis has changed since the artifact was last synchronized to that
basis. For contract artifacts, synchronization is approval. For context/code,
synchronization is generation or reconciliation.

Direct-edit detection uses a two-tier compare against each artifact's
approval snapshot: filesystem mtime as a fast filter, per-item canonical hash
as the authoritative check. A hash mismatch means the file has been edited
outside the skill's flow; the artifact should be automatically reopened to
`draft`. Pure-cosmetic edits (whitespace, non-semantic frontmatter) pass the
mtime filter but match on every hash and are not reported.

See vibeloom-methodology.md ## Generation ### Staleness And Regeneration and
vibeloom-implementation.md ## Metadata Format ### Staleness / ### Direct Edit
Detection.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from vibeloom_engine.graph import canonical_item_hash, reachable_forward
from vibeloom_engine.models import CONTEXT_TYPES, Graph, Status


@dataclass
class StaleArtifact:
    artifact_id: str
    reason: str  # "upstream-changed" | "context-not-regenerated"
    triggering_item_id: str | None  # item that triggered the stale mark, if applicable


def compute_stale(graph: Graph) -> list[StaleArtifact]:
    """Return the list of artifacts considered stale.

    An artifact is stale when any item in its upstream transitive closure has
    been modified or removed since the upstream artifact was approved.

    Algorithm:
      1. For each approved-artifact snapshot, compare current item hashes to
         the snapshot hashes. Collect items classified as modified (hash
         differs) or removed (absent from current state) into the
         changed-upstream set. Added items do not contribute.
      2. For each changed-upstream item, find all downstream items:
         - modified items: forward-walk the derivation graph from the item
         - removed items: the forward edges are not materialized (the item is
           gone), so seed from every current item whose `derives_from` still
           references the removed ID, then forward-walk from there
      3. Map downstream items to their owning artifacts; emit one
         StaleArtifact per unique owning artifact.
    """
    modified_items: set[str] = set()
    removed_items: set[str] = set()
    for artifact_id, snapshot in graph.approved_snapshots.items():
        owning_artifact = graph.artifacts.get(artifact_id)
        for item_id, approved_hash in snapshot.item_hashes.items():
            current = graph.items.get(item_id)
            if current is None:
                removed_items.add(item_id)
                continue
            # Only compare if the item is still in the same artifact; if it
            # moved (unusual, since IDs are unique per repo), treat as removed
            # from the original artifact.
            if owning_artifact is not None and current.artifact_id != artifact_id:
                removed_items.add(item_id)
                continue
            if canonical_item_hash(current) != approved_hash:
                modified_items.add(item_id)

    stale: list[StaleArtifact] = []
    seen_artifacts: set[str] = set()

    def mark_stale(downstream_id: str, trigger_id: str) -> None:
        d_item = graph.items.get(downstream_id)
        if d_item is None:
            return
        if d_item.artifact_id in seen_artifacts:
            return
        stale.append(
            StaleArtifact(
                artifact_id=d_item.artifact_id,
                reason="upstream-changed",
                triggering_item_id=trigger_id,
            )
        )
        seen_artifacts.add(d_item.artifact_id)

    # Modified items: forward-walk reaches downstream via materialized edges.
    for modified_id in modified_items:
        downstream = reachable_forward(graph, [modified_id]) - {modified_id}
        for d_id in downstream:
            mark_stale(d_id, modified_id)

    # Removed items: edges aren't in the graph (upstream endpoint gone), so
    # seed the forward walk from each current item that still references the
    # removed ID in its `derives_from`. Those downstream items are then
    # forward-walked to pick up transitive staleness.
    for removed_id in removed_items:
        for item in graph.items.values():
            if removed_id in item.derives_from:
                mark_stale(item.item_id, removed_id)
                downstream = reachable_forward(graph, [item.item_id]) - {item.item_id}
                for d_id in downstream:
                    mark_stale(d_id, removed_id)

    return stale


@dataclass
class EditedArtifact:
    artifact_id: str
    path: str
    last_approved_mtime: float
    current_mtime: float
    added_items: list[str] = field(default_factory=list)
    removed_items: list[str] = field(default_factory=list)
    modified_items: list[str] = field(default_factory=list)


def detect_direct_edits(graph: Graph) -> list[EditedArtifact]:
    """Detect approved contract artifacts edited outside the skill's flow.

    Two-tier compare against each artifact's approval snapshot:
      1. Fast filter: if current mtime matches snapshot mtime (within 10ms
         jitter), skip — the file is byte-identical to approval.
      2. Authoritative check: compute each current item's canonical hash and
         classify items as added (present now, absent in snapshot), removed
         (present in snapshot, absent now), or modified (hash differs).

    An artifact is reported as edited only when at least one item is added,
    removed, or modified. Pure-cosmetic edits (whitespace, non-semantic
    frontmatter) pass the mtime filter but produce no classification changes
    and are silently ignored; the caller is free to leave the artifact
    approved.
    """
    edited: list[EditedArtifact] = []
    for artifact_id, snapshot in graph.approved_snapshots.items():
        a = graph.artifacts.get(artifact_id)
        if a is None or a.mtime is None:
            continue
        # Only contract artifacts participate in this check.
        if a.artifact_type in CONTEXT_TYPES:
            continue
        if a.status != Status.APPROVED:
            continue
        # Fast filter: allow small float jitter.
        if abs(a.mtime - snapshot.mtime) <= 0.01:
            continue

        # Hash comparison per item.
        current_ids = {item.item_id for item in a.items}
        snapshot_ids = set(snapshot.item_hashes.keys())
        added = sorted(current_ids - snapshot_ids)
        removed = sorted(snapshot_ids - current_ids)
        modified: list[str] = []
        for item in a.items:
            prior_hash = snapshot.item_hashes.get(item.item_id)
            if prior_hash is None:
                continue  # already counted as added
            if canonical_item_hash(item) != prior_hash:
                modified.append(item.item_id)
        modified.sort()

        if not (added or removed or modified):
            # Cosmetic edit only (mtime changed, all hashes match). No reopen.
            continue

        edited.append(
            EditedArtifact(
                artifact_id=a.artifact_id,
                path=a.path,
                last_approved_mtime=snapshot.mtime,
                current_mtime=a.mtime,
                added_items=added,
                removed_items=removed,
                modified_items=modified,
            )
        )
    return edited
