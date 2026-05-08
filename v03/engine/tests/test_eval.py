"""Tests for structural eval — covers §14.1 + §5.1+§8.2 derives_from."""

import textwrap
from pathlib import Path

from vibeloom_engine.eval_ import structural_eval
from vibeloom_engine.graph import build_graph
from vibeloom_engine.parser import parse_repo_path


def _f_kinds(findings, severity=None):
    out = set()
    for f in findings:
        if severity and f.severity != severity:
            continue
        out.add(f.check)
    return out


def test_eval_clean_tiny_repo(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    assert all(f.severity != "blocking" for f in findings)


def test_eval_cycle_blocking(cycle_repo: Path):
    artifacts = parse_repo_path(cycle_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    assert any(f.check == "cycle" for f in blocking)


def test_eval_dangling_reference(fresh_repo: Path):
    """A dangling derives_from reference is blocking per §14.1 reference-integrity."""
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
        | CAP-0001 | foo | - |
        """).lstrip(), encoding="utf-8")
    (fresh_repo / "prd.md").write_text(textwrap.dedent("""
        ---
        artifact_id: prd
        artifact_type: prd
        tier: product-specs
        approval_unit: product-specs
        scope_kind: root
        scope_id: root
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CAP-0001]
        ---
        ## Functional requirements

        | id | description | derives_from |
        |---|---|---|
        | FR-0001 | hi | CAP-9999 |
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    assert any(f.check == "reference-integrity" for f in blocking)


def test_eval_derives_from_missing_blocking(fresh_repo: Path):
    """Non-root item with no derives_from is blocking per §5.1+§8.2."""
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
    (fresh_repo / "prd.md").write_text(textwrap.dedent("""
        ---
        artifact_id: prd
        artifact_type: prd
        tier: product-specs
        approval_unit: product-specs
        scope_kind: root
        scope_id: root
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CAP-0001]
        ---
        ## Functional requirements

        | id | description | derives_from |
        |---|---|---|
        | FR-0001 | x |  |
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    msgs = " ".join(f.message for f in blocking)
    assert "non-root" in msgs.lower() or "no derives_from" in msgs.lower()


def test_eval_derives_from_invalid_upstream_prefix(fresh_repo: Path):
    """OBJ deriving from FR is invalid per §5.1 (OBJ allowed: CAP)."""
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
    (fresh_repo / "prd.md").write_text(textwrap.dedent("""
        ---
        artifact_id: prd
        artifact_type: prd
        tier: product-specs
        approval_unit: product-specs
        scope_kind: root
        scope_id: root
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CAP-0001]
        ---
        ## Functional requirements

        | id | description | derives_from |
        |---|---|---|
        | FR-0001 | x | CAP-0001 |

        ## Objectives

        | id | description | derives_from |
        |---|---|---|
        | OBJ-0001 | x | FR-0001 |
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    assert any("invalid edge OBJ" in f.message for f in blocking)


def test_eval_universal_trace_unreached_root(fresh_repo: Path):
    """Item that doesn't transitively reach CAP/CST → blocking per §8.2."""
    # Build a chain that loops in a sub-graph but never reaches a root.
    # OBJ-0001 derives from CAP-0001 (root). FR-0001 derives from FR-0002.
    # FR-0002 derives from FR-0003. FR-0003 derives from FR-0001 (cycle, no root).
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
    (fresh_repo / "prd.md").write_text(textwrap.dedent("""
        ---
        artifact_id: prd
        artifact_type: prd
        tier: product-specs
        approval_unit: product-specs
        scope_kind: root
        scope_id: root
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CAP-0001]
        ---
        ## Functional requirements

        | id | description | derives_from |
        |---|---|---|
        | FR-0001 | x | FR-0002 |
        | FR-0002 | x | FR-0001 |
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    msgs = " ".join(f.message for f in findings if f.severity == "blocking")
    assert "transitively reach a root" in msgs


def test_eval_root_with_derives_from_blocking(fresh_repo: Path):
    """CAP with derives_from is blocking — roots can't have upstream."""
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
        | CAP-0002 | x | CAP-0001 |
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    assert any("root prefix" in f.message and "CAP-0002" in f.message for f in blocking)


def test_eval_layered_invariant_bc_in_presentation(container_layered_repo: Path):
    """A BC hosted in a presentation-layer component is a blocking finding."""
    artifacts = parse_repo_path(container_layered_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    msgs = " ".join(f.message for f in blocking)
    assert "presentation" in msgs.lower() or "domain-layer" in msgs.lower()


def test_eval_target_filter(tiny_repo: Path):
    """target='product-specs' filters findings to product-specs artifacts only."""
    artifacts = parse_repo_path(tiny_repo)
    graph = build_graph(artifacts)
    all_findings = structural_eval(graph, artifacts)
    pdr_findings = structural_eval(graph, artifacts, target="product-specs")
    intent_findings_in_filtered = [f for f in pdr_findings if f.artifact_id == "intent"]
    assert intent_findings_in_filtered == []


def test_eval_lifecycle_consistency(fresh_repo: Path):
    """Mixed status within an approval_unit → blocking lifecycle finding."""
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
    (fresh_repo / "defaults.md").write_text(textwrap.dedent("""
        ---
        artifact_id: defaults
        artifact_type: defaults
        tier: intent-specs
        approval_unit: intent-specs
        scope_kind: root
        scope_id: root
        status: approved
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CAP-0001]
        ---
        ## Defaults

        | id | description | derives_from |
        |---|---|---|
        | DEF-0001 | x | CAP-0001 |
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    assert any(f.check == "lifecycle" for f in blocking)
