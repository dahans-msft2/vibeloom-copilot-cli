"""Shared fixtures for engine smoke tests."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """Return an empty repo root rooted at a tmp_path."""
    return tmp_path


def write(repo: Path, rel: str, content: str) -> Path:
    """Write a file under repo at rel path, creating parent dirs."""
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(dedent(content).lstrip(), encoding="utf-8")
    return p


@pytest.fixture
def vibe_repo(tmp_path: Path) -> Path:
    """A minimal governed `vibe` repo with intent + defaults + flat system."""
    write(
        tmp_path,
        "intent.md",
        """
        ---
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
        | CAP-0001 | Users can create an account | |

        ## Constraints

        | id | description | notes |
        |---|---|---|
        | CST-0001 | All API calls require authentication | |
        """,
    )
    write(
        tmp_path,
        "defaults.md",
        """
        ---
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
        | CST-0002 | Python 3.11+ as runtime | [CST-0001] | |
        """,
    )
    write(
        tmp_path,
        "system.md",
        """
        ---
        artifact_id: system
        artifact_type: system
        tier: system-specs
        scope_kind: root
        scope_id: root
        status: draft
        timestamp: "2026-04-16T00:00:00Z"
        derives_from: []
        ---

        # System (vibe)

        ## Container inventory

        | id | slug | description | runtime | derives_from | notes |
        |---|---|---|---|---|---|
        | CONT-0001 | api | API service | Python | | |

        ## Component inventory

        | id | slug | container_id | description | derives_from | notes |
        |---|---|---|---|---|---|
        | CMP-0001 | users | CONT-0001 | User management | [CONT-0001] | |
        """,
    )
    return tmp_path
