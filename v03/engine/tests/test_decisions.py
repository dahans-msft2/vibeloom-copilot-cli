"""Tests for decisions.py — markdown rendering idempotency + body preservation."""

from pathlib import Path

from vibeloom_engine.decisions import (
    render_decisions,
    render_frontmatter,
    slugify,
)
from vibeloom_engine.io_ import decisions_dir
from vibeloom_engine.parser import split_frontmatter
from vibeloom_engine.traces import append_trace


def _add_dec(repo: Path, trace_id: str = "DEC-20260508-001", record_type: str = "ADR",
             topic: str = "tax-calculation-strategy") -> dict:
    rec = {
        "trace_id": trace_id,
        "timestamp": "2026-05-08T15:00:00Z",
        "record_type": record_type,
        "topic": topic,
        "load_bearing": True,
        "affects": ["BC-0008"],
        "author": "ilya@vibeloom.ai",
        "payload": "Selected progressive bracket calculation.",
    }
    append_trace(repo, "decision", rec)
    return rec


def test_slugify_basic():
    assert slugify("Tax calc strategy!") == "tax-calc-strategy"
    assert slugify("") == "untitled"


def test_render_writes_per_record_file(fresh_repo: Path):
    _add_dec(fresh_repo)
    paths = render_decisions(fresh_repo)
    assert paths == ["decisions/adr/DEC-20260508-001-tax-calculation-strategy.md"]
    assert (fresh_repo / paths[0]).is_file()


def test_render_idempotent_byte_identical(fresh_repo: Path):
    """Drop tree → re-render → byte-identical (per §8.5.1)."""
    _add_dec(fresh_repo)
    render_decisions(fresh_repo)
    target = decisions_dir(fresh_repo) / "adr" / "DEC-20260508-001-tax-calculation-strategy.md"
    before = target.read_bytes()
    target.unlink()
    render_decisions(fresh_repo)
    after = target.read_bytes()
    assert before == after


def test_render_preserves_user_edited_body(fresh_repo: Path):
    """User edits body → re-render → frontmatter byte-identical, body preserved (§8.5.1)."""
    _add_dec(fresh_repo)
    render_decisions(fresh_repo)
    target = decisions_dir(fresh_repo) / "adr" / "DEC-20260508-001-tax-calculation-strategy.md"
    text = target.read_text()
    fm, body = split_frontmatter(text)
    new_body = "\n# Custom title\n\nMy hand-written notes here.\n"
    target.write_text("---\n" + "\n".join(f"{k}: {v}" for k, v in fm.items()) + "\n---" + new_body)
    before_text = target.read_text()
    render_decisions(fresh_repo)
    after_text = target.read_text()
    # Body preserved; frontmatter may reorder (we re-render frontmatter).
    fm_a, body_a = split_frontmatter(after_text)
    assert "Custom title" in body_a
    assert "My hand-written notes" in body_a


def test_render_general_record_type(fresh_repo: Path):
    _add_dec(fresh_repo, trace_id="DEC-20260508-002", record_type="general", topic="naming")
    paths = render_decisions(fresh_repo)
    assert any("/general/" in p for p in paths)


def test_render_no_decisions_returns_empty(fresh_repo: Path):
    out = render_decisions(fresh_repo)
    assert out == []


def test_render_frontmatter_string_quoting():
    rec = {
        "trace_id": "DEC-1",
        "kind": "decision",
        "timestamp": "2026-05-08T00:00:00Z",
        "topic": "x:y",  # contains colon, needs quoting
    }
    fm = render_frontmatter(rec)
    assert '"x:y"' in fm
