"""Additional parser tests pushing edge cases."""

import textwrap
from pathlib import Path

import pytest

from vibeloom_engine.parser import (
    iter_sections,
    parse_artifact,
    parse_repo,
    split_frontmatter,
)
from vibeloom_engine.io_ import DiscoveredFile


def test_split_frontmatter_indent_rejected():
    text = "---\n  foo: bar\n---\n"
    fm, body = split_frontmatter(text)
    # Indented top-level → frontmatter parse fails, returns None.
    assert fm is None


def test_split_frontmatter_missing_colon_rejected():
    text = "---\nfoo bar\n---\n"
    fm, body = split_frontmatter(text)
    assert fm is None


def test_split_frontmatter_quoted_with_colon():
    text = '---\nfoo: "bar:baz"\n---\n'
    fm, body = split_frontmatter(text)
    assert fm == {"foo": "bar:baz"}


def test_split_frontmatter_scalar_types():
    text = textwrap.dedent("""
        ---
        a: 1
        b: 1.5
        c: true
        d: false
        e: null
        f: ~
        ---
        """).lstrip()
    fm, _ = split_frontmatter(text)
    assert fm == {"a": 1, "b": 1.5, "c": True, "d": False, "e": None, "f": None}


def test_iter_sections_h3_with_h2_terminator():
    body = "## A\n### sub\nfoo\n## B\n bar\n"
    out = iter_sections(body, header_level=3)
    titles = [t for t, _ in out]
    assert titles == ["sub"]


def test_iter_sections_unsupported_header_level():
    with pytest.raises(ValueError):
        iter_sections("body", header_level=4)


def test_parse_artifact_unknown_type_returns_none(tmp_path: Path):
    p = tmp_path / "weird.md"
    p.write_text(textwrap.dedent("""
        ---
        artifact_id: weird
        artifact_type: unknown-type
        tier: intent-specs
        scope_kind: root
        scope_id: root
        timestamp: 2026-05-08T00:00:00Z
        derives_from: []
        ---
        """).lstrip(), encoding="utf-8")
    df = DiscoveredFile(rel_path="weird.md", abs_path=p, mtime=p.stat().st_mtime)
    assert parse_artifact(df) is None


def test_parse_artifact_no_frontmatter_returns_none(tmp_path: Path):
    p = tmp_path / "x.md"
    p.write_text("just a heading\n", encoding="utf-8")
    df = DiscoveredFile(rel_path="x.md", abs_path=p, mtime=p.stat().st_mtime)
    assert parse_artifact(df) is None


def test_parse_artifact_missing_artifact_id(tmp_path: Path):
    p = tmp_path / "x.md"
    p.write_text(textwrap.dedent("""
        ---
        artifact_type: intent
        tier: intent-specs
        scope_kind: root
        scope_id: root
        timestamp: 2026-05-08T00:00:00Z
        derives_from: []
        ---
        """).lstrip(), encoding="utf-8")
    df = DiscoveredFile(rel_path="x.md", abs_path=p, mtime=p.stat().st_mtime)
    assert parse_artifact(df) is None


def test_parse_bdd_scenarios(tmp_path: Path):
    bdd_dir = tmp_path / "web" / "search" / "context" / "bdd"
    bdd_dir.mkdir(parents=True, exist_ok=True)
    p = bdd_dir / "BDD-0001-search.md"
    p.write_text(textwrap.dedent("""
        ---
        artifact_id: bdd.search.0001
        artifact_type: bdd
        tier: context
        scope_kind: component
        scope_id: web.search
        timestamp: 2026-05-08T00:00:00Z
        derives_from: [CMP-0001]
        ---

        # Search BDD

        ## Scenarios

        ### SCN-0001
        - **derives_from:** ACC-0001

        Given foo
        When bar
        Then baz
        """).lstrip(), encoding="utf-8")
    df = DiscoveredFile(rel_path=str(p.relative_to(tmp_path)), abs_path=p, mtime=p.stat().st_mtime)
    artifact = parse_artifact(df)
    assert artifact is not None
    items = {i.item_id for i in artifact.items}
    assert "SCN-0001" in items
    scn = next(i for i in artifact.items if i.item_id == "SCN-0001")
    assert scn.derives_from == ["ACC-0001"]


def test_parse_repo_skips_unparseable(tmp_path: Path):
    df1 = DiscoveredFile(rel_path="x.md", abs_path=tmp_path / "x.md", mtime=0)
    (tmp_path / "x.md").write_text("not parseable", encoding="utf-8")
    out = parse_repo([df1])
    assert out == []


def test_parse_artifact_string_derives_from(tmp_path: Path):
    p = tmp_path / "prd.md"
    p.write_text(textwrap.dedent("""
        ---
        artifact_id: prd
        artifact_type: prd
        tier: product-specs
        approval_unit: product-specs
        scope_kind: root
        scope_id: root
        status: draft
        timestamp: 2026-05-08T00:00:00Z
        derives_from: "CAP-0001, CST-0001"
        ---
        """).lstrip(), encoding="utf-8")
    df = DiscoveredFile(rel_path="prd.md", abs_path=p, mtime=p.stat().st_mtime)
    a = parse_artifact(df)
    assert a is not None
    assert a.derives_from == ["CAP-0001", "CST-0001"]
