"""Pytest fixtures for the engine tests.

`fresh_repo` produces an empty repo path; `tiny_repo` builds a minimal
intent + prd repo (one CAP, one CST, one FR derived from CAP). Other
fixtures layer on top.
"""

from __future__ import annotations

import shutil
import textwrap
from pathlib import Path
from typing import Iterator

import pytest


def _w(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip("\n"), encoding="utf-8")


@pytest.fixture
def fresh_repo(tmp_path: Path) -> Iterator[Path]:
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    yield repo
    shutil.rmtree(repo, ignore_errors=True)


@pytest.fixture
def tiny_repo(fresh_repo: Path) -> Path:
    """Minimal repo: intent + prd + one derive_from edge. Eval clean."""
    _w(
        fresh_repo / "intent.md",
        """
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

        # Intent

        ## Capabilities

        | id | description | derives_from |
        |---|---|---|
        | CAP-0001 | Track personal expenses by category. | - |

        ## Constraints

        | id | description | derives_from |
        |---|---|---|
        | CST-0001 | Must work offline. | - |
        """,
    )
    _w(
        fresh_repo / "prd.md",
        """
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

        # PRD

        ## Functional requirements

        | id | description | derives_from |
        |---|---|---|
        | FR-0001 | User can add an expense. | CAP-0001 |
        """,
    )
    return fresh_repo


@pytest.fixture
def cycle_repo(tiny_repo: Path) -> Path:
    """tiny_repo + a cycle FR-0001 ↔ FR-0002."""
    _w(
        tiny_repo / "prd.md",
        """
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

        # PRD

        ## Functional requirements

        | id | description | derives_from |
        |---|---|---|
        | FR-0001 | User can add an expense. | CAP-0001, FR-0002 |
        | FR-0002 | User can edit an expense. | FR-0001 |
        """,
    )
    return tiny_repo


@pytest.fixture
def container_layered_repo(tiny_repo: Path) -> Path:
    """tiny_repo + containers.md + presentation/web container with component
    that hosts a BC. Used to test layered-invariant: BC in non-domain layer
    must surface a finding.
    """
    _w(
        tiny_repo / "containers.md",
        """
        ---
        artifact_id: containers
        artifact_type: containers
        tier: system-specs
        approval_unit: system-specs
        scope_kind: root
        scope_id: root
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CAP-0001]
        ---

        # Containers

        ## Inventory

        | id | description | derives_from |
        |---|---|---|
        | CONT-0001 | Web app | CAP-0001 |
        """,
    )
    _w(
        tiny_repo / "web/container.md",
        """
        ---
        artifact_id: container.web
        artifact_type: container
        tier: system-specs
        approval_unit: system-specs
        scope_kind: container
        scope_id: web
        layer: presentation
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CONT-0001]
        ---

        # Web container
        """,
    )
    _w(
        tiny_repo / "web/AGENTS.md",
        """
        ---
        artifact_id: agents.web
        artifact_type: config
        tier: context
        scope_kind: container
        scope_id: web
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CONT-0001]
        ---

        # Web AGENTS
        """,
    )
    _w(
        tiny_repo / "web/search/component.md",
        """
        ---
        artifact_id: component.web.search
        artifact_type: component
        tier: system-specs
        approval_unit: system-specs
        scope_kind: component
        scope_id: web.search
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CONT-0001]
        component_id: CMP-0001
        container_id: web
        owned_paths:
          - web/src/search/**
        owned_interfaces: []
        hosted_bounded_contexts:
          - BC-0001
        ---

        # Component
        """,
    )
    return tiny_repo
