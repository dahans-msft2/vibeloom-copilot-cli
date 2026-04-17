"""Graph builder smoke tests."""

from pathlib import Path

from vibeloom_engine.affected import compute_affected_set
from vibeloom_engine.graph import build_graph, dangling_references, detect_cycles
from vibeloom_engine.parser import parse_repo_path


def test_build_graph_from_vibe_repo(vibe_repo: Path):
    artifacts = parse_repo_path(vibe_repo)
    graph = build_graph(artifacts)
    assert "intent" in graph.artifacts
    assert "CAP-0001" in graph.items
    assert "CST-0001" in graph.items
    assert "CONT-0001" in graph.items
    assert "CMP-0001" in graph.items
    # At least one edge: CMP-0001 -> CONT-0001
    edge_pairs = {(e.source, e.target) for e in graph.edges}
    assert ("CMP-0001", "CONT-0001") in edge_pairs


def test_no_cycles_in_clean_graph(vibe_repo: Path):
    artifacts = parse_repo_path(vibe_repo)
    graph = build_graph(artifacts)
    assert detect_cycles(graph) == []


def test_no_dangling_references(vibe_repo: Path):
    artifacts = parse_repo_path(vibe_repo)
    graph = build_graph(artifacts)
    assert dangling_references(graph) == []


def test_affected_set_forward_walk(vibe_repo: Path):
    artifacts = parse_repo_path(vibe_repo)
    graph = build_graph(artifacts)
    affected = compute_affected_set(graph, ["CONT-0001"])
    assert "CONT-0001" in affected.item_ids
    assert "CMP-0001" in affected.item_ids  # CMP-0001 derives_from CONT-0001
    assert "system-specs" in affected.tiers
