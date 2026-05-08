"""Tests for status.py — six categories per §10."""

import textwrap
from pathlib import Path

from vibeloom_engine.graph import build_graph, canonical_artifact_hash, canonical_item_hash
from vibeloom_engine.parser import parse_repo_path
from vibeloom_engine.registry import retire_semantic, save_registry
from vibeloom_engine.staleness import compute_staleness, detect_direct_edits
from vibeloom_engine.status import classify_items, compute_status
from vibeloom_engine.traces import append_trace


def _approve_state(repo: Path, trace_id: str = "APPROVAL-20260508-001"):
    """Write an approval trace covering the current state of all items+artifacts."""
    artifacts = parse_repo_path(repo)
    graph = build_graph(artifacts)
    items_map = {iid: canonical_item_hash(it) for iid, it in graph.items.items()}
    artifacts_map = {aid: canonical_artifact_hash(a) for aid, a in graph.artifacts.items()}
    append_trace(repo, "approval", {
        "trace_id": trace_id,
        "timestamp": "2026-05-08T00:00:00Z",
        "run_id": "RUN-20260508-001",
        "approval_unit": "product-specs",
        "approval_mode": "user",
        "items": items_map,
        "artifacts": artifacts_map,
    })


def test_status_uncovered_per_section_10(tiny_repo: Path):
    """§10 `uncovered`: non-root with unapproved basis."""
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    cls = classify_items(tiny_repo, graph, artifacts)
    # Without any approval trace, FR-0001 has unapproved basis (CAP-0001).
    assert cls["FR-0001"]["status"] == "uncovered"


def test_status_current_after_approval(tiny_repo: Path):
    _approve_state(tiny_repo)
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    cls = classify_items(tiny_repo, graph, artifacts)
    assert cls["FR-0001"]["status"] == "current"


def test_status_stale_when_basis_changes(tiny_repo: Path):
    _approve_state(tiny_repo)
    # Modify CAP-0001's description
    intent = (tiny_repo / "intent.md").read_text()
    intent = intent.replace("Track personal expenses by category.", "Track personal expenses.")
    (tiny_repo / "intent.md").write_text(intent)
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    cls = classify_items(tiny_repo, graph, artifacts)
    assert cls["FR-0001"]["status"] == "stale"


def test_status_dangling_when_basis_retired(tiny_repo: Path):
    _approve_state(tiny_repo)
    retire_semantic(tiny_repo, "CAP-0001")
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    cls = classify_items(tiny_repo, graph, artifacts)
    assert cls["FR-0001"]["status"] == "dangling"


def test_status_drifted_via_direct_edit(tiny_repo: Path):
    """First approve as draft (mark approved + approve), then edit body in-place."""
    # Mark prd as approved.
    prd = (tiny_repo / "prd.md").read_text().replace("status: draft", "status: approved")
    (tiny_repo / "prd.md").write_text(prd)
    _approve_state(tiny_repo)
    # Direct edit
    prd2 = (tiny_repo / "prd.md").read_text().replace("User can add an expense.", "User can add an expense quickly.")
    (tiny_repo / "prd.md").write_text(prd2)
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    cls = classify_items(tiny_repo, graph, artifacts)
    assert cls["FR-0001"]["status"] == "drifted"
    assert cls["FR-0001"]["reason"] == "direct_edit"


def test_status_obsolete_via_user_mark(tiny_repo: Path):
    _approve_state(tiny_repo)
    from vibeloom_engine.registry import load_registry, save_registry
    data = load_registry(tiny_repo)
    data.setdefault("FR", {"next": 1, "retired": [], "obsolete": []})
    data["FR"].setdefault("obsolete", []).append("FR-0001")
    save_registry(tiny_repo, data)
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    cls = classify_items(tiny_repo, graph, artifacts)
    assert cls["FR-0001"]["status"] == "obsolete"


def test_compute_status_full_report(tiny_repo: Path):
    _approve_state(tiny_repo)
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    rep = compute_status(tiny_repo, graph, artifacts)
    assert "category_counts" in rep
    assert "items" in rep
    assert "lifecycle" in rep
    assert "recommended_next" in rep
    assert rep["category_counts"]["current"] >= 1


def test_status_recommend_next_for_drifted(tiny_repo: Path):
    prd = (tiny_repo / "prd.md").read_text().replace("status: draft", "status: approved")
    (tiny_repo / "prd.md").write_text(prd)
    _approve_state(tiny_repo)
    prd2 = (tiny_repo / "prd.md").read_text().replace("User can add an expense.", "User can add an expense quickly.")
    (tiny_repo / "prd.md").write_text(prd2)
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    rep = compute_status(tiny_repo, graph, artifacts)
    assert "reconcile" in rep["recommended_next"].lower()


def test_status_inferred_mode_pm_or_dev(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    rep = compute_status(tiny_repo, graph, artifacts)
    assert rep["current_mode"] in ("pm-or-dev", "ux-or-pm")


def test_status_inferred_mode_vibe(fresh_repo: Path):
    """Vibe = no prd/usm/dm artifacts."""
    (fresh_repo / "intent.md").write_text(textwrap.dedent("""
        ---
        artifact_id: intent
        artifact_type: intent
        tier: intent-specs
        approval_unit: intent-specs
        scope_kind: root
        scope_id: root
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: []
        ---
        ## Capabilities

        | id | description | derives_from |
        |---|---|---|
        | CAP-0001 | x | - |
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    graph = build_graph(artifacts)
    rep = compute_status(fresh_repo, graph, artifacts)
    assert rep["current_mode"] == "vibe"


def test_compute_staleness_after_basis_changed(tiny_repo: Path):
    _approve_state(tiny_repo)
    intent = (tiny_repo / "intent.md").read_text().replace(
        "Track personal expenses by category.", "Track personal expenses."
    )
    (tiny_repo / "intent.md").write_text(intent)
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    stale = compute_staleness(tiny_repo, graph, artifacts)
    assert any(s["item_id"] == "FR-0001" for s in stale)


def test_detect_edits_returns_empty_after_clean_approval(tiny_repo: Path):
    prd = (tiny_repo / "prd.md").read_text().replace("status: draft", "status: approved")
    (tiny_repo / "prd.md").write_text(prd)
    _approve_state(tiny_repo)
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    edits = detect_direct_edits(tiny_repo, graph, artifacts)
    assert edits == []
