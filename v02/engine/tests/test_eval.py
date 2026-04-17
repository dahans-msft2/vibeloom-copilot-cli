"""Eval smoke tests."""

from pathlib import Path

from vibeloom_engine.eval_ import eval_graph
from vibeloom_engine.graph import build_graph
from vibeloom_engine.parser import parse_repo_path


def test_eval_vibe_repo_clean(vibe_repo: Path):
    """The sample vibe_repo is intentionally clean — no error-severity findings."""
    artifacts = parse_repo_path(vibe_repo)
    graph = build_graph(artifacts)
    findings = eval_graph(graph, artifacts)
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], f"unexpected errors: {[e.message for e in errors]}"


def test_eval_detects_dangling_reference(tmp_path: Path):
    """An item with a derives_from pointing at a nonexistent ID is flagged."""
    (tmp_path / "intent.md").write_text(
        """---
artifact_id: intent
artifact_type: intent
tier: intent-specs
scope_kind: root
scope_id: root
status: approved
timestamp: "2026-04-16T00:00:00Z"
approval_mode: user
derives_from: []
---

# Intent

## Capabilities

| id | description | notes |
|---|---|---|
| CAP-0001 | Create account | |

## Constraints

| id | description | notes |
|---|---|---|
| CST-0001 | Auth required | |
""",
        encoding="utf-8",
    )
    (tmp_path / "defaults.md").write_text(
        """---
artifact_id: defaults
artifact_type: defaults
tier: intent-specs
scope_kind: root
scope_id: root
status: approved
timestamp: "2026-04-16T00:00:00Z"
approval_mode: user
derives_from: []
---

# Defaults

## Rules

| id | rule | derives_from | notes |
|---|---|---|---|
| CST-0002 | Python 3.11+ | [CST-9999] | |
""",
        encoding="utf-8",
    )
    artifacts = parse_repo_path(tmp_path)
    graph = build_graph(artifacts)
    findings = eval_graph(graph, artifacts)
    dangling = [f for f in findings if f.check == "reference-integrity" and "CST-9999" in f.message]
    assert dangling, "expected dangling reference to CST-9999 to be flagged"
