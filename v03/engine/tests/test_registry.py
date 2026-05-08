"""Tests for registry.py — semantic + dated allocation, retired-list invariant."""

from pathlib import Path

import pytest

from vibeloom_engine.registry import (
    allocate_dated,
    allocate_semantic,
    is_retired,
    load_registry,
    retire_semantic,
    save_registry,
)


def test_allocate_semantic_starts_at_1(fresh_repo: Path):
    ids = allocate_semantic(fresh_repo, "FR", count=2)
    assert ids == ["FR-0001", "FR-0002"]


def test_allocate_semantic_persists(fresh_repo: Path):
    allocate_semantic(fresh_repo, "FR", count=1)
    ids2 = allocate_semantic(fresh_repo, "FR", count=1)
    assert ids2 == ["FR-0002"]


def test_retire_semantic_never_reused(fresh_repo: Path):
    """Per §5.2: retired IDs are never reused."""
    allocate_semantic(fresh_repo, "FR", count=5)
    retire_semantic(fresh_repo, "FR-0003")
    # Reset next to 3 to attempt reuse — would re-allocate FR-0003.
    data = load_registry(fresh_repo)
    data["FR"]["next"] = 3
    save_registry(fresh_repo, data)
    new_ids = allocate_semantic(fresh_repo, "FR", count=2)
    # FR-0003 must be skipped.
    assert "FR-0003" not in new_ids
    assert is_retired(fresh_repo, "FR-0003")


def test_retire_idempotent(fresh_repo: Path):
    allocate_semantic(fresh_repo, "FR", count=1)
    retire_semantic(fresh_repo, "FR-0001")
    retire_semantic(fresh_repo, "FR-0001")  # second call no-op
    data = load_registry(fresh_repo)
    assert data["FR"]["retired"].count("FR-0001") == 1


def test_allocate_dated(fresh_repo: Path):
    a = allocate_dated(fresh_repo, "RUN", today="20260508")
    b = allocate_dated(fresh_repo, "RUN", today="20260508")
    c = allocate_dated(fresh_repo, "RUN", today="20260509")
    assert a == "RUN-20260508-001"
    assert b == "RUN-20260508-002"
    assert c == "RUN-20260509-001"


def test_allocate_dated_rejects_semantic_prefix(fresh_repo: Path):
    with pytest.raises(ValueError):
        allocate_dated(fresh_repo, "FR")


def test_allocate_semantic_rejects_dated_prefix(fresh_repo: Path):
    with pytest.raises(ValueError):
        allocate_semantic(fresh_repo, "RUN")


def test_allocate_unknown_prefix_raises(fresh_repo: Path):
    with pytest.raises(ValueError):
        allocate_semantic(fresh_repo, "ZZZ")
