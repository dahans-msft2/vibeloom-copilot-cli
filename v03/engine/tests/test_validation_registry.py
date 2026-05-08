"""Tests for validation_registry.py — runner inventory parsing."""

import textwrap
from pathlib import Path

from vibeloom_engine.validation_registry import parse_validation_registry


def test_parse_validation_registry(fresh_repo: Path):
    (fresh_repo / "validation-registry.md").write_text(textwrap.dedent("""
        ---
        artifact_type: validation-registry
        tier: meta
        ---

        # Validation registry

        ```yaml
        - runner_id: typecheck
          command: tsc --noEmit
          scope: workspace
          inputs:  [src/**]
          outputs: [status, logs]

        - runner_id: unit
          command: npm test --workspace ${component}
          scope: component
        ```

        Some additional prose.

        ```text
        ignored block
        ```
        """).lstrip(), encoding="utf-8")
    runners = parse_validation_registry(fresh_repo)
    assert len(runners) == 2
    assert runners[0].runner_id == "typecheck"
    assert runners[0].command == "tsc --noEmit"
    assert runners[0].scope == "workspace"
    assert runners[0].inputs == ["src/**"]
    assert runners[1].runner_id == "unit"


def test_parse_no_registry_file(fresh_repo: Path):
    runners = parse_validation_registry(fresh_repo)
    assert runners == []
