"""Tests for cache.py — regenerable from artifacts + traces."""

from pathlib import Path

from vibeloom_engine.cache import (
    cache_dir,
    clear_cache,
    load_graph,
    load_status,
    save_graph,
    save_status,
)
from vibeloom_engine.graph import build_graph
from vibeloom_engine.parser import parse_repo_path


def test_save_and_load_graph_roundtrip(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    save_graph(graph, tiny_repo)
    loaded = load_graph(tiny_repo)
    assert loaded is not None
    assert loaded.items.keys() == graph.items.keys()


def test_load_graph_missing_returns_none(fresh_repo: Path):
    assert load_graph(fresh_repo) is None


def test_save_and_load_status_roundtrip(tiny_repo: Path):
    payload = {"x": 1, "items": {}}
    save_status(payload, tiny_repo)
    out = load_status(tiny_repo)
    assert out == payload


def test_clear_cache_drops_files(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    save_graph(graph, tiny_repo)
    save_status({"x": 1}, tiny_repo)
    assert load_graph(tiny_repo) is not None
    clear_cache(tiny_repo)
    assert not cache_dir(tiny_repo).exists()
    assert load_graph(tiny_repo) is None


def test_cache_regenerates_from_artifacts(tiny_repo: Path):
    """Per the constraints: deleting cache must allow rebuild from artifacts."""
    artifacts = parse_repo_path(tiny_repo)
    graph1 = build_graph(artifacts)
    save_graph(graph1, tiny_repo)
    clear_cache(tiny_repo)
    # rebuild
    graph2 = build_graph(parse_repo_path(tiny_repo))
    assert graph2.items.keys() == graph1.items.keys()
    assert {(e.source, e.target) for e in graph2.edges} == {(e.source, e.target) for e in graph1.edges}
