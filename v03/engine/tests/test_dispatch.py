"""Tests for dispatch.py — wave-assembly rules from §13.2."""

from pathlib import Path

from vibeloom_engine.affected import compute_affected_set
from vibeloom_engine.dispatch import (
    Scope,
    assemble_waves,
    dispatch_plan,
    execute_plan,
)
from vibeloom_engine.graph import build_graph
from vibeloom_engine.parser import parse_repo_path


def test_disjoint_ownership(tiny_repo: Path):
    """Rule 1: same-wave scopes must have disjoint owned_paths."""
    a = Scope("a", "k", owned_paths=("web/src/**",), task_template_id="t")
    b = Scope("b", "k", owned_paths=("api/src/**",), task_template_id="t")
    waves = assemble_waves([a, b])
    assert len(waves) == 1
    assert {s.scope_id for s in waves[0]} == {"a", "b"}


def test_disjoint_ownership_overlap_separates(tiny_repo: Path):
    """Overlapping paths force separate waves."""
    a = Scope("a", "k", owned_paths=("web/src/**",), task_template_id="t")
    b = Scope("b", "k", owned_paths=("web/src/foo.ts",), task_template_id="t")
    waves = assemble_waves([a, b])
    assert len(waves) == 2


def test_derivation_precedence():
    """Rule 2: B in strictly later wave iff B derives_from A."""
    up = Scope("up", "k", owned_paths=("a.md",), task_template_id="t")
    down = Scope("down", "k", owned_paths=("b.md",), task_template_id="t",
                 derives_from_scopes=("up",))
    waves = assemble_waves([up, down])
    assert len(waves) == 2
    assert waves[0][0].scope_id == "up"
    assert waves[1][0].scope_id == "down"


def test_concurrency_cap():
    """Rule 3: max_wave_size bounds wave size; spillover."""
    scopes = [
        Scope(f"s{i}", "k", owned_paths=(f"path/{i}.md",), task_template_id="t")
        for i in range(7)
    ]
    waves = assemble_waves(scopes, max_wave_size=3)
    assert len(waves) == 3
    assert all(len(w) <= 3 for w in waves)


def test_reconciliation_singletons():
    """Rule 4: reconciliation tasks always go in singleton waves."""
    s1 = Scope("recon:web", "k", owned_paths=("web/**",), task_template_id="t",
               is_reconciliation=True)
    s2 = Scope("recon:api", "k", owned_paths=("api/**",), task_template_id="t",
               is_reconciliation=True)
    waves = assemble_waves([s1, s2])
    assert len(waves) == 2
    assert all(len(w) == 1 for w in waves)


def test_reconciliation_does_not_share_with_generation():
    """Rule 4: reconciliation singleton blocks generation in the same wave."""
    s_rec = Scope("recon", "k", owned_paths=("a.md",), is_reconciliation=True,
                  task_template_id="t")
    s_gen = Scope("gen", "k", owned_paths=("b.md",), task_template_id="t")
    waves = assemble_waves([s_rec, s_gen])
    assert len(waves) == 2


def test_dispatch_plan_includes_metadata(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    affected = compute_affected_set(graph, ["CAP-0001"])
    plan = dispatch_plan(graph, affected)
    assert plan["plan_id"].startswith("PLAN-")
    assert "waves" in plan
    assert "max_wave_size" in plan


def test_execute_plan_calls_callback_per_scope(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    affected = compute_affected_set(graph, ["CAP-0001"])
    plan = dispatch_plan(graph, affected)
    invocations = []

    def cb(header):
        invocations.append(header)
        return {"status": "ok"}

    out = execute_plan(plan, cb)
    expected_scope_count = sum(len(w["scopes"]) for w in plan["waves"])
    assert out.callback_invocations == expected_scope_count
    if expected_scope_count:
        assert invocations[0]["scope"]["scope_id"]


def test_execute_plan_failed_task_does_not_block_peers():
    """§13.3: A failed task does not block the wave."""
    plan = {
        "plan_id": "PLAN-test",
        "waves": [
            {"wave_id": "W1", "scopes": [
                {"scope_id": "a", "kind": "k", "owned_paths": ["a.md"], "task_template_id": "t"},
                {"scope_id": "b", "kind": "k", "owned_paths": ["b.md"], "task_template_id": "t"},
            ]}
        ],
    }

    def cb(header):
        if header["scope"]["scope_id"] == "a":
            return {"status": "failed"}
        return {"status": "ok"}

    out = execute_plan(plan, cb)
    assert "a" in out.failed_scopes
    assert "b" in out.completed_scopes
