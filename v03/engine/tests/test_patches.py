"""Tests for patches.py — staging + atomic apply."""

from pathlib import Path

import pytest

from vibeloom_engine.patches import (
    apply_atomic,
    list_staged_paths,
    stage_task_files,
    task_dir,
)


def test_stage_writes_under_files_dir(fresh_repo: Path):
    td = stage_task_files(
        fresh_repo,
        "RUN-1",
        "TASK-1",
        files={"prd.md": "hello\n"},
        summary="ok",
    )
    assert td.is_dir()
    assert (td / "files" / "prd.md").read_text() == "hello\n"
    assert (td / "summary.yaml").read_text() == "ok"


def test_apply_atomic_copies_into_working_tree(fresh_repo: Path):
    stage_task_files(fresh_repo, "RUN-1", "TASK-1", {"foo.md": "x\n"})
    applied = apply_atomic(fresh_repo, "RUN-1", "TASK-1")
    assert applied == ["foo.md"]
    assert (fresh_repo / "foo.md").read_text() == "x\n"


def test_apply_atomic_respects_allowed_paths(fresh_repo: Path):
    stage_task_files(fresh_repo, "RUN-1", "TASK-1", {"foo.md": "x\n"})
    with pytest.raises(ValueError):
        apply_atomic(fresh_repo, "RUN-1", "TASK-1", allowed_write_paths=["bar.md"])


def test_apply_atomic_glob_allowed(fresh_repo: Path):
    stage_task_files(fresh_repo, "RUN-1", "TASK-1", {"web/src/index.ts": "x\n"})
    applied = apply_atomic(fresh_repo, "RUN-1", "TASK-1", allowed_write_paths=["web/src/**"])
    assert applied == ["web/src/index.ts"]


def test_list_staged_paths(fresh_repo: Path):
    stage_task_files(fresh_repo, "RUN-1", "TASK-1", {"a.md": "x", "b/c.md": "y"})
    paths = list_staged_paths(fresh_repo, "RUN-1", "TASK-1")
    assert paths == ["a.md", "b/c.md"]


def test_apply_atomic_no_files_returns_empty(fresh_repo: Path):
    out = apply_atomic(fresh_repo, "RUN-x", "TASK-x")
    assert out == []
