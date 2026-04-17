"""Staleness computation and direct-edit detection.

Staleness is a computed property: an artifact is stale when its approved
upstream basis has changed since the artifact was last synchronized to that
basis. For contract artifacts, synchronization is approval. For context/code,
synchronization is generation.

Direct-edit detection compares a currently-approved artifact's filesystem
modification time to the engine-recorded last-approved mtime. A mismatch means
the file has been edited outside the skill's flow; the artifact should be
automatically reopened to `draft`.

See vibeloom-methodology.md ## Generation ### Staleness And Regeneration and
vibeloom-implementation.md ## Metadata Format ### Direct Edit Detection.
"""

from __future__ import annotations

from dataclasses import dataclass

from vibeloom_engine.graph import reachable_forward
from vibeloom_engine.models import Artifact, CONTEXT_TYPES, Graph, Status


@dataclass
class StaleArtifact:
    artifact_id: str
    reason: str  # "upstream-changed" | "context-not-regenerated"
    triggering_item_id: str | None  # item that triggered the stale mark, if applicable


def compute_stale(graph: Graph) -> list[StaleArtifact]:
    """Return the list of artifacts considered stale.

    Strategy: any contract artifact whose upstream basis has changed since the
    artifact was last approved (approved_mtimes vs current mtimes) is stale.
    Context and code artifacts derived from stale contract are also stale.

    v0.1 uses a simple heuristic: if any item that a downstream artifact
    transitively derives_from belongs to an artifact whose current mtime is
    newer than the downstream artifact's own mtime, the downstream artifact is
    stale. This approximates approved-basis mismatch for now; a future pass
    can refine by comparing to persisted approved-basis snapshots.
    """
    stale: list[StaleArtifact] = []
    for a in graph.artifacts.values():
        if a.mtime is None:
            continue
        # For each downstream item (in a), walk upstream and check each source's artifact mtime.
        for item in a.items:
            for up_id in item.derives_from:
                up_item = graph.items.get(up_id)
                if not up_item:
                    continue
                up_artifact = graph.artifacts.get(up_item.artifact_id)
                if up_artifact is None or up_artifact.mtime is None:
                    continue
                if up_artifact.mtime > a.mtime:
                    stale.append(
                        StaleArtifact(
                            artifact_id=a.artifact_id,
                            reason="upstream-changed",
                            triggering_item_id=up_id,
                        )
                    )
                    break
            else:
                continue
            break  # mark artifact once and move on
    return stale


@dataclass
class EditedArtifact:
    artifact_id: str
    path: str
    last_approved_mtime: float
    current_mtime: float


def detect_direct_edits(graph: Graph) -> list[EditedArtifact]:
    """Detect approved contract artifacts whose filesystem mtime no longer
    matches the engine-recorded last-approved mtime.

    If a mismatch is found, callers should reopen the artifact to `draft`
    before proceeding with any operation.
    """
    edited: list[EditedArtifact] = []
    for artifact_id, approved_mtime in graph.approved_mtimes.items():
        a = graph.artifacts.get(artifact_id)
        if not a or a.mtime is None:
            continue
        # Only contract artifacts participate in this check.
        if a.artifact_type in CONTEXT_TYPES:
            continue
        if a.status != Status.APPROVED:
            continue
        # Allow small float jitter; treat strict inequality as an edit.
        if a.mtime > approved_mtime + 0.01:
            edited.append(
                EditedArtifact(
                    artifact_id=a.artifact_id,
                    path=a.path,
                    last_approved_mtime=approved_mtime,
                    current_mtime=a.mtime,
                )
            )
    return edited
