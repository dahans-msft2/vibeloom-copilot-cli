"""CLI smoke tests."""

import json
from pathlib import Path

import pytest

from vibeloom_engine.cli import main


def test_cli_parse(vibe_repo: Path, capsys: pytest.CaptureFixture):
    rc = main(["--repo", str(vibe_repo), "parse"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert isinstance(data, list)
    assert any(a["artifact_id"] == "intent" for a in data)
    assert rc == 0


def test_cli_graph(vibe_repo: Path, capsys: pytest.CaptureFixture):
    rc = main(["--repo", str(vibe_repo), "graph"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["artifacts"] >= 3
    assert data["items"] >= 4
    assert (vibe_repo / ".vibeloom" / "state" / "context-graph.json").is_file()
    assert rc == 0


def test_cli_eval_clean(vibe_repo: Path, capsys: pytest.CaptureFixture):
    rc = main(["--repo", str(vibe_repo), "eval"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["error_count"] == 0
    assert rc == 0


def test_cli_affected(vibe_repo: Path, capsys: pytest.CaptureFixture):
    rc = main(["--repo", str(vibe_repo), "affected", "--ids", "CONT-0001"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "CMP-0001" in data["items"]
    assert "system-specs" in data["tiers"]
    assert rc == 0


def test_cli_status(vibe_repo: Path, capsys: pytest.CaptureFixture):
    rc = main(["--repo", str(vibe_repo), "status"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["contract_lifecycle"]["intent-specs"] == "approved"
    assert data["contract_lifecycle"]["system-specs"] in ("draft", "absent")
    assert (vibe_repo / ".vibeloom" / "state" / "status.json").is_file()
    assert rc == 0
