"""Tests for schema.py — per-artifact frontmatter validation."""

import textwrap
from pathlib import Path

from vibeloom_engine.parser import parse_repo_path
from vibeloom_engine.schema import validate_artifact, validate_repo


def test_validate_clean(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    findings = validate_repo(artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    assert blocking == []


def test_missing_approval_unit_blocking(fresh_repo: Path):
    (fresh_repo / "intent.md").write_text(textwrap.dedent("""
        ---
        artifact_id: intent
        artifact_type: intent
        tier: intent-specs
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
    findings = validate_repo(artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    assert any("approval_unit" in f.message for f in blocking)


def test_missing_status_blocking(fresh_repo: Path):
    (fresh_repo / "intent.md").write_text(textwrap.dedent("""
        ---
        artifact_id: intent
        artifact_type: intent
        tier: intent-specs
        approval_unit: intent-specs
        scope_kind: root
        scope_id: root
        timestamp: 2026-05-08T00:00:00Z
        derives_from: []
        ---
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    findings = validate_repo(artifacts)
    assert any("status" in f.message for f in findings if f.severity == "blocking")


def test_container_missing_layer_blocking(fresh_repo: Path):
    (fresh_repo / "web/container.md").parent.mkdir(parents=True, exist_ok=True)
    (fresh_repo / "web/container.md").write_text(textwrap.dedent("""
        ---
        artifact_id: container.web
        artifact_type: container
        tier: system-specs
        approval_unit: system-specs
        scope_kind: container
        scope_id: web
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CAP-0001]
        ---
        """).lstrip(), encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    findings = validate_repo(artifacts)
    assert any("layer" in f.message for f in findings if f.severity == "blocking")


def test_duplicate_artifact_id_blocking(fresh_repo: Path):
    """Two artifacts at different paths sharing the same artifact_id is blocking."""
    import copy
    artifact_text = textwrap.dedent("""
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
        """).lstrip()
    (fresh_repo / "intent.md").write_text(artifact_text, encoding="utf-8")
    artifacts = parse_repo_path(fresh_repo)
    # Synthesize a copy at a different path (deep copy to avoid alias).
    if artifacts:
        dup = copy.deepcopy(artifacts[0])
        dup.path = "synthetic-dup.md"
        artifacts.append(dup)
    findings = validate_repo(artifacts)
    assert any("duplicate artifact_id" in f.message for f in findings)
