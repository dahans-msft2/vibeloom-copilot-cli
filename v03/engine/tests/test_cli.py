"""End-to-end CLI smoke tests via in-process main()."""

import io
import json
import sys
from pathlib import Path

import pytest

from vibeloom_engine.cli import main


def _run(argv: list[str]) -> tuple[int, dict]:
    """Run main with stdout captured; return (exit_code, parsed_json)."""
    buf = io.StringIO()
    err_buf = io.StringIO()
    real_out, real_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = buf, err_buf
    try:
        rc = main(argv)
    finally:
        sys.stdout, sys.stderr = real_out, real_err
    out_text = buf.getvalue().strip()
    if not out_text:
        return rc, {}
    return rc, json.loads(out_text)


def test_cli_parse(tiny_repo: Path):
    rc, out = _run(["--repo", str(tiny_repo), "parse"])
    assert rc == 0
    assert out["artifact_count"] == 2


def test_cli_graph(tiny_repo: Path):
    rc, out = _run(["--repo", str(tiny_repo), "graph"])
    assert rc == 0
    assert out["item_count"] >= 3
    assert out["edge_count"] >= 1
    assert out["cycles"] == []


def test_cli_eval_clean(tiny_repo: Path):
    rc, out = _run(["--repo", str(tiny_repo), "eval"])
    assert rc == 0
    assert out["blocking_count"] == 0


def test_cli_eval_cycle_blocking(cycle_repo: Path):
    rc, out = _run(["--repo", str(cycle_repo), "eval"])
    assert rc == 1
    assert out["blocking_count"] >= 1
    assert any(f["check"] == "cycle" for f in out["findings"])


def test_cli_affected(tiny_repo: Path):
    rc, out = _run(["--repo", str(tiny_repo), "affected", "--ids", "CAP-0001"])
    assert rc == 0
    assert "FR-0001" in out["affected_items"]


def test_cli_dispatch(tiny_repo: Path):
    rc, out = _run(["--repo", str(tiny_repo), "dispatch", "--ids", "CAP-0001"])
    assert rc == 0
    assert "waves" in out
    assert "plan_id" in out


def test_cli_status(tiny_repo: Path):
    rc, out = _run(["--repo", str(tiny_repo), "status"])
    assert rc == 0
    assert "category_counts" in out


def test_cli_decisions_render_empty(tiny_repo: Path):
    rc, out = _run(["--repo", str(tiny_repo), "decisions", "render"])
    assert rc == 0
    assert out["rendered_files"] == []


def test_cli_unknown_command_engine_error(tmp_path: Path):
    rc, _ = _run(["--repo", str(tmp_path), "totally-nope"])
    assert rc == 2
