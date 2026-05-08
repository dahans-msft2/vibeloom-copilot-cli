"""Tests for graph.py — DAG, walks, cycle detection, hashing."""

from pathlib import Path

from vibeloom_engine.graph import (
    build_graph,
    canonical_artifact_hash,
    canonical_item_hash,
    dangling_references,
    find_cycles,
    reachable_downstream,
    reachable_upstream,
)
from vibeloom_engine.parser import parse_repo_path


def test_build_graph_emits_edge(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    assert "FR-0001" in graph.items
    assert "CAP-0001" in graph.items
    edges = [(e.source, e.target) for e in graph.edges]
    assert ("FR-0001", "CAP-0001") in edges


def test_reachable_downstream(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    out = reachable_downstream(graph, ["CAP-0001"])
    assert "CAP-0001" in out
    assert "FR-0001" in out


def test_reachable_upstream(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    out = reachable_upstream(graph, ["FR-0001"])
    assert "FR-0001" in out
    assert "CAP-0001" in out


def test_find_cycles_clean(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    assert find_cycles(graph) == []


def test_find_cycles_detects(cycle_repo: Path):
    artifacts = parse_repo_path(cycle_repo)
    graph = build_graph(artifacts)
    cycles = find_cycles(graph)
    assert cycles, "expected ≥1 cycle"
    # Cycle should mention FR-0001 ↔ FR-0002.
    flat = {n for cyc in cycles for n in cyc}
    assert "FR-0001" in flat and "FR-0002" in flat


def test_dangling_references_empty(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    assert dangling_references(graph) == []


def test_canonical_item_hash_stable(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    h1 = canonical_item_hash(graph.items["FR-0001"])
    h2 = canonical_item_hash(graph.items["FR-0001"])
    assert h1 == h2
    assert h1.startswith("sha256:")


def test_canonical_item_hash_excludes_id(tiny_repo: Path):
    """Renaming an item should change identity but the hash of an item with
    the same content should not depend on id (rename = remove + add)."""
    from vibeloom_engine.models import Item, Scope, ScopeKind

    a = Item(
        item_id="FR-0001",
        artifact_id="prd",
        section="x",
        tier="product-specs",
        scope=Scope(kind=ScopeKind.ROOT, scope_id="root"),
        derives_from=["CAP-0001"],
        description="hello",
    )
    b = Item(**{**a.__dict__, "item_id": "FR-9999"})
    assert canonical_item_hash(a) == canonical_item_hash(b)


def test_canonical_artifact_hash_stable(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    a = list(graph.artifacts.values())[0]
    h1 = canonical_artifact_hash(a)
    h2 = canonical_artifact_hash(a)
    assert h1 == h2
    assert h1.startswith("sha256:")
