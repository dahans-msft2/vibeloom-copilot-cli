"""Staleness, multi-basis lookup, and direct-edit detection (§10, §15).

Approval traces are the canonical record of what was approved. Per §10, an
item is `stale` when its `derives_from` basis hashes don't match the latest
approval trace covering each basis. This module exposes the helper
primitives the status classifier needs.

Direct-edit detection: an artifact's body has changed since the last
approval trace covering it. Two-tier compare: file mtime + per-item canonical
hashes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from vibeloom_engine.graph import canonical_artifact_hash, canonical_item_hash
from vibeloom_engine.models import Artifact, ArtifactType, Graph, Status
from vibeloom_engine.traces import iter_trace_records


# ---------------------------------------------------------------------------
# Approval trace index
# ---------------------------------------------------------------------------


def latest_approval_per_item(repo_root: Path) -> dict[str, str]:
    """Return {item_id: approved_hash} from the latest approval trace covering each item.

    Iterates approval traces in stored order; later entries (assumed
    chronologically newer per append-only invariant) overwrite earlier
    entries. Returns the per-item map.
    """
    out: dict[str, str] = {}
    try:
        for rec in iter_trace_records(repo_root, "approval"):
            for iid, h in (rec.get("items") or {}).items():
                out[iid] = h
    except FileNotFoundError:
        return {}
    return out


def latest_approval_per_artifact(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Return {artifact_id: {hash, mtime_at_trace, trace_id, timestamp, items}}.

    `mtime_at_trace` is None unless a custom field was attached at write time;
    direct-edit detection compares hashes, not mtimes (mtime is a fast filter
    when stored).
    """
    out: dict[str, dict[str, Any]] = {}
    try:
        for rec in iter_trace_records(repo_root, "approval"):
            for aid, h in (rec.get("artifacts") or {}).items():
                out[aid] = {
                    "artifact_hash": h,
                    "trace_id": rec.get("trace_id"),
                    "timestamp": rec.get("timestamp"),
                    "items": rec.get("items") or {},
                }
    except FileNotFoundError:
        return {}
    return out


# ---------------------------------------------------------------------------
# Staleness
# ---------------------------------------------------------------------------


def compute_staleness(repo_root: Path, graph: Graph, artifacts: list[Artifact]) -> list[dict[str, Any]]:
    """Return a list of stale-item records per §10.

    Each record: {item_id, artifact_id, reason, mismatched_bases: [...]}.
    `reason` is one of: `basis_changed`, `basis_dangling`, `basis_unapproved`.

    Multi-basis lookup follows §10's protocol: per-basis-ID resolution,
    pulling the most recent approval trace containing each basis_id.
    """
    item_approved = latest_approval_per_item(repo_root)
    out: list[dict[str, Any]] = []
    for iid, item in graph.items.items():
        if not item.derives_from:
            continue
        mismatched: list[dict[str, str]] = []
        for basis in item.derives_from:
            basis_item = graph.items.get(basis)
            if basis_item is None:
                mismatched.append({"basis_id": basis, "reason": "basis_dangling"})
                continue
            current_hash = canonical_item_hash(basis_item)
            approved_hash = item_approved.get(basis)
            if approved_hash is None:
                mismatched.append({"basis_id": basis, "reason": "basis_unapproved"})
                continue
            if current_hash != approved_hash:
                mismatched.append({
                    "basis_id": basis,
                    "reason": "basis_changed",
                    "approved_hash": approved_hash,
                    "current_hash": current_hash,
                })
        if mismatched:
            # Pick the most-significant reason: changed > dangling > unapproved.
            severity_order = {"basis_changed": 0, "basis_dangling": 1, "basis_unapproved": 2}
            primary = sorted(mismatched, key=lambda m: severity_order.get(m["reason"], 9))[0]["reason"]
            out.append({
                "item_id": iid,
                "artifact_id": item.artifact_id,
                "reason": primary,
                "mismatched_bases": mismatched,
            })
    return out


# ---------------------------------------------------------------------------
# Direct edit detection
# ---------------------------------------------------------------------------


def detect_direct_edits(
    repo_root: Path,
    graph: Graph,
    artifacts: list[Artifact],
) -> list[dict[str, Any]]:
    """Detect approved contract artifacts whose current body diverges from the
    latest approval trace covering them.

    Returns: [{artifact_id, path, modified_items: [...], removed_items: [...],
                added_items: [...], approval_trace_id}]
    """
    by_artifact = latest_approval_per_artifact(repo_root)
    out: list[dict[str, Any]] = []
    # index current artifacts and items
    artifacts_by_id = {a.artifact_id: a for a in artifacts}
    for aid, info in by_artifact.items():
        a = artifacts_by_id.get(aid)
        if a is None:
            # artifact disappeared since approval — surfaces as dangling/uncovered
            continue
        if a.status != Status.APPROVED:
            # was approved at trace time, now draft — surfaces via lifecycle, not as edit
            continue
        # Compute current artifact hash
        current_hash = canonical_artifact_hash(a)
        if current_hash == info.get("artifact_hash"):
            continue
        # per-item diff. The approval trace's `items` map covers the entire
        # approval_unit (which may span multiple artifacts). To attribute
        # removed/added items to *this* artifact specifically, we restrict
        # `approved_items` to items that are still in the graph and were
        # owned by this artifact (or that are present in this artifact now,
        # in which case they're modified or unchanged). Items in the trace
        # that are missing from the graph entirely belong to retired/missing
        # contexts and surface via dangling, not direct-edit, diffing.
        approved_items_full = info.get("items") or {}
        current_item_ids = {it.item_id for it in a.items}
        # Items in the trace's items map that the current graph indexes as
        # belonging to this artifact today. (Items renamed-out-of this
        # artifact look like "removed" — the desired behaviour.)
        approved_for_this_artifact = {
            iid: h
            for iid, h in approved_items_full.items()
            if (iid in current_item_ids)
            or (iid in graph.items and graph.items[iid].artifact_id == aid)
            or (iid not in graph.items and any(it.item_id == iid for it in a.items))
        }
        approved_item_ids = set(approved_for_this_artifact.keys())
        added = sorted(current_item_ids - approved_item_ids)
        removed = sorted(approved_item_ids - current_item_ids)
        modified: list[str] = []
        for it in a.items:
            prior = approved_for_this_artifact.get(it.item_id)
            if prior is None:
                continue
            if canonical_item_hash(it) != prior:
                modified.append(it.item_id)
        modified.sort()
        if not (added or removed or modified):
            # cosmetic edit — frontmatter-only or whitespace
            continue
        out.append({
            "artifact_id": aid,
            "path": a.path,
            "added_items": added,
            "removed_items": removed,
            "modified_items": modified,
            "approval_trace_id": info.get("trace_id"),
        })
    return out


__all__ = [
    "latest_approval_per_item",
    "latest_approval_per_artifact",
    "compute_staleness",
    "detect_direct_edits",
]
