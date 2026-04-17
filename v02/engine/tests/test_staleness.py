"""Staleness and direct-edit detection tests for the v2 hash-based pipeline."""

from __future__ import annotations

import os
import time
from pathlib import Path

from vibeloom_engine.cache import load_graph, save_graph
from vibeloom_engine.graph import build_graph, canonical_item_hash
from vibeloom_engine.models import ApprovalSnapshot, Status
from vibeloom_engine.parser import parse_repo_path
from vibeloom_engine.staleness import compute_stale, detect_direct_edits


def _bump_mtime(path: Path) -> float:
    """Nudge the file's mtime forward by 1s so the mtime-filter definitely fires."""
    now = time.time() + 1
    os.utime(path, (now, now))
    return now


def test_cold_start_captures_snapshots(vibe_repo: Path) -> None:
    artifacts = parse_repo_path(vibe_repo)
    graph = build_graph(artifacts)

    # Both approved artifacts get snapshots; the draft system.md does not.
    assert "intent" in graph.approved_snapshots
    assert "defaults" in graph.approved_snapshots
    assert "system" not in graph.approved_snapshots

    intent_snap = graph.approved_snapshots["intent"]
    assert "CAP-0001" in intent_snap.item_hashes
    assert "CST-0001" in intent_snap.item_hashes
    # Each item's snapshot hash matches its canonical hash of current content.
    cap = graph.items["CAP-0001"]
    assert intent_snap.item_hashes["CAP-0001"] == canonical_item_hash(cap)


def test_snapshots_preserved_across_rebuilds(vibe_repo: Path) -> None:
    first = build_graph(parse_repo_path(vibe_repo))
    captured_mtime = first.approved_snapshots["intent"].mtime
    captured_hash = first.approved_snapshots["intent"].item_hashes["CAP-0001"]

    # Bump the intent.md mtime — no content change yet.
    _bump_mtime(vibe_repo / "intent.md")

    second = build_graph(parse_repo_path(vibe_repo), prior=first)
    # Snapshot mtime must be preserved despite the file's mtime moving forward.
    assert second.approved_snapshots["intent"].mtime == captured_mtime
    assert second.approved_snapshots["intent"].item_hashes["CAP-0001"] == captured_hash


def test_detect_direct_edits_real_edit(vibe_repo: Path) -> None:
    first = build_graph(parse_repo_path(vibe_repo))
    save_graph(first, vibe_repo)

    # Mutate CAP-0001's description — a real semantic edit.
    intent_path = vibe_repo / "intent.md"
    text = intent_path.read_text(encoding="utf-8")
    edited = text.replace("create an account", "create a premium account")
    assert edited != text
    intent_path.write_text(edited, encoding="utf-8")
    _bump_mtime(intent_path)

    prior = load_graph(vibe_repo)
    graph = build_graph(parse_repo_path(vibe_repo), prior=prior)

    edits = detect_direct_edits(graph)
    assert len(edits) == 1
    e = edits[0]
    assert e.artifact_id == "intent"
    assert e.modified_items == ["CAP-0001"]
    assert e.added_items == []
    assert e.removed_items == []


def test_detect_direct_edits_cosmetic_edit_ignored(vibe_repo: Path) -> None:
    first = build_graph(parse_repo_path(vibe_repo))
    save_graph(first, vibe_repo)

    # Append trailing whitespace / newline — mtime bumps but no item hash changes.
    intent_path = vibe_repo / "intent.md"
    intent_path.write_text(intent_path.read_text(encoding="utf-8") + "\n\n", encoding="utf-8")
    _bump_mtime(intent_path)

    prior = load_graph(vibe_repo)
    graph = build_graph(parse_repo_path(vibe_repo), prior=prior)

    # mtime filter fires but every item hash matches → no edits reported.
    assert detect_direct_edits(graph) == []


def test_detect_direct_edits_item_removed(vibe_repo: Path) -> None:
    first = build_graph(parse_repo_path(vibe_repo))
    save_graph(first, vibe_repo)

    # Remove CST-0001 from intent.md.
    intent_path = vibe_repo / "intent.md"
    text = intent_path.read_text(encoding="utf-8")
    edited = text.replace("| CST-0001 | All API calls require authentication | |\n", "")
    assert edited != text
    intent_path.write_text(edited, encoding="utf-8")
    _bump_mtime(intent_path)

    prior = load_graph(vibe_repo)
    graph = build_graph(parse_repo_path(vibe_repo), prior=prior)

    edits = detect_direct_edits(graph)
    assert len(edits) == 1
    assert edits[0].removed_items == ["CST-0001"]


def test_detect_direct_edits_skips_draft_and_context(vibe_repo: Path) -> None:
    # Seed an approved-snapshot for system.md so that status+type filters can
    # be exercised (even though build_graph wouldn't snapshot a draft).
    graph = build_graph(parse_repo_path(vibe_repo))
    graph.approved_snapshots["system"] = ApprovalSnapshot(mtime=0.0, item_hashes={})

    # system.md is a draft contract artifact — skipped by status filter even
    # with a bogus snapshot.
    assert graph.artifacts["system"].status == Status.DRAFT
    assert detect_direct_edits(graph) == []


def test_compute_stale_on_clean_repo(vibe_repo: Path) -> None:
    graph = build_graph(parse_repo_path(vibe_repo))
    # Fresh snapshot: no changes vs current → no staleness.
    assert compute_stale(graph) == []


def test_compute_stale_on_modified_upstream(vibe_repo: Path) -> None:
    first = build_graph(parse_repo_path(vibe_repo))
    save_graph(first, vibe_repo)

    # Mutate CST-0001 semantically. CST-0002 in defaults.md derives_from CST-0001.
    intent_path = vibe_repo / "intent.md"
    text = intent_path.read_text(encoding="utf-8")
    edited = text.replace("All API calls require authentication", "All API calls require MFA")
    assert edited != text
    intent_path.write_text(edited, encoding="utf-8")
    _bump_mtime(intent_path)

    prior = load_graph(vibe_repo)
    graph = build_graph(parse_repo_path(vibe_repo), prior=prior)

    stale = compute_stale(graph)
    stale_artifact_ids = {s.artifact_id for s in stale}
    assert "defaults" in stale_artifact_ids
    # Triggering item should be the modified upstream.
    defaults_mark = next(s for s in stale if s.artifact_id == "defaults")
    assert defaults_mark.triggering_item_id == "CST-0001"
    assert defaults_mark.reason == "upstream-changed"


def test_cache_roundtrip_preserves_snapshots(vibe_repo: Path) -> None:
    graph = build_graph(parse_repo_path(vibe_repo))
    save_graph(graph, vibe_repo)
    loaded = load_graph(vibe_repo)
    assert loaded is not None
    assert loaded.approved_snapshots.keys() == graph.approved_snapshots.keys()
    for aid, snap in graph.approved_snapshots.items():
        assert loaded.approved_snapshots[aid].mtime == snap.mtime
        assert loaded.approved_snapshots[aid].item_hashes == snap.item_hashes
