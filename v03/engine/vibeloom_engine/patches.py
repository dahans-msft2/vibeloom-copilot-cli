"""Patch staging + atomic apply (§14).

Subagent writes are not direct. They are staged at
`.vibeloom/runs/RUN-.../tasks/TASK-.../{patch.diff, summary.yaml, files/}`,
validated, then applied atomically via `apply_atomic`. The `files/`
directory contains the new file content; `patch.diff` is informative.

This module provides:
- `stage_task_files(repo, run, task, files: {rel_path: text})` — stage.
- `apply_atomic(repo, run, task, files)` — copy staged `files/*` into the
  working tree as a single transaction (move-with-rollback).
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Iterable

from vibeloom_engine.io_ import ensure_dir, runs_dir


def task_dir(repo_root: Path, run_id: str, task_id: str) -> Path:
    return runs_dir(repo_root) / run_id / "tasks" / task_id


def stage_task_files(
    repo_root: Path,
    run_id: str,
    task_id: str,
    files: dict[str, str],
    summary: str = "",
) -> Path:
    """Stage new file contents under `files/` of the task dir."""
    td = ensure_dir(task_dir(repo_root, run_id, task_id))
    files_dir = ensure_dir(td / "files")
    for rel, content in files.items():
        target = files_dir / rel
        ensure_dir(target.parent)
        target.write_text(content, encoding="utf-8")
    if summary:
        (td / "summary.yaml").write_text(summary, encoding="utf-8")
    return td


def list_staged_paths(repo_root: Path, run_id: str, task_id: str) -> list[str]:
    files_dir = task_dir(repo_root, run_id, task_id) / "files"
    if not files_dir.is_dir():
        return []
    out: list[str] = []
    for p in files_dir.rglob("*"):
        if p.is_file():
            out.append(str(p.relative_to(files_dir).as_posix()))
    return sorted(out)


def apply_atomic(
    repo_root: Path,
    run_id: str,
    task_id: str,
    allowed_write_paths: Iterable[str] | None = None,
) -> list[str]:
    """Apply staged files into the working tree atomically.

    All staged files in `files/` are copied into `repo_root` as one
    transaction. If any copy raises, the engine restores backups and
    re-raises. Returns the list of applied relative paths.
    """
    files_dir = task_dir(repo_root, run_id, task_id) / "files"
    if not files_dir.is_dir():
        return []
    rel_paths = list_staged_paths(repo_root, run_id, task_id)
    if allowed_write_paths is not None:
        allowed = list(allowed_write_paths)
        for rp in rel_paths:
            if not _path_allowed(rp, allowed):
                raise ValueError(
                    f"staged path {rp!r} is not within allowed_write_paths {allowed}"
                )

    backup_dir = Path(tempfile.mkdtemp(prefix=f"vibeloom-rollback-{task_id}-"))
    try:
        # Backup existing files, then write new
        for rp in rel_paths:
            target = repo_root / rp
            if target.exists():
                bk = backup_dir / rp
                ensure_dir(bk.parent)
                shutil.copy2(target, bk)
        for rp in rel_paths:
            src = files_dir / rp
            dest = repo_root / rp
            ensure_dir(dest.parent)
            shutil.copy2(src, dest)
    except Exception:
        # rollback from backups
        for rp in rel_paths:
            bk = backup_dir / rp
            target = repo_root / rp
            if bk.exists():
                shutil.copy2(bk, target)
        raise
    finally:
        shutil.rmtree(backup_dir, ignore_errors=True)
    return rel_paths


def _path_allowed(rel_path: str, allowed: list[str]) -> bool:
    """Check if rel_path is matched by any pattern in allowed.

    Supports `**` glob (prefix only), exact match, and trailing `/**`.
    """
    for pat in allowed:
        if pat == rel_path:
            return True
        if pat.endswith("/**"):
            prefix = pat[:-3]
            if rel_path.startswith(prefix):
                return True
        if "**" in pat:
            prefix = pat.split("**", 1)[0]
            if rel_path.startswith(prefix):
                return True
    return False


__all__ = [
    "task_dir",
    "stage_task_files",
    "list_staged_paths",
    "apply_atomic",
]
