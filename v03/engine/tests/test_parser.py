"""Parser tests."""

import textwrap
from pathlib import Path

from vibeloom_engine.io_ import discover_artifacts
from vibeloom_engine.models import ArtifactType, ContainerLayer
from vibeloom_engine.parser import (
    iter_sections,
    parse_artifact,
    parse_id_list,
    parse_repo_path,
    parse_table,
    split_frontmatter,
)


def test_split_frontmatter_basic():
    text = "---\nartifact_id: x\n---\nbody"
    fm, body = split_frontmatter(text)
    assert fm == {"artifact_id": "x"}
    assert body == "body"


def test_split_frontmatter_no_match():
    text = "no frontmatter here"
    fm, body = split_frontmatter(text)
    assert fm is None
    assert body == text


def test_split_frontmatter_inline_list():
    text = "---\nfoo: [a, b, c]\n---\n"
    fm, body = split_frontmatter(text)
    assert fm == {"foo": ["a", "b", "c"]}


def test_split_frontmatter_block_list():
    text = textwrap.dedent("""
        ---
        owned_paths:
          - web/src/**
          - api/src/**
        ---
        """).lstrip()
    fm, body = split_frontmatter(text)
    assert fm == {"owned_paths": ["web/src/**", "api/src/**"]}


def test_iter_sections_h2():
    body = "## A\n one\n## B\n two\n"
    out = iter_sections(body, header_level=2)
    titles = [t for t, _ in out]
    assert titles == ["A", "B"]


def test_parse_table_basic():
    body = "## X\n\n| id | description |\n| --- | --- |\n| FR-0001 | hello |\n"
    rows = parse_table(body)
    assert rows == [{"id": "FR-0001", "description": "hello"}]


def test_parse_id_list_variants():
    assert parse_id_list("FR-0001, NFR-0002") == ["FR-0001", "NFR-0002"]
    assert parse_id_list("[CAP-0001]") == ["CAP-0001"]
    assert parse_id_list("-") == []
    assert parse_id_list("") == []
    assert parse_id_list("FR-0001 and APPROVAL-20260508-001") == [
        "FR-0001",
        "APPROVAL-20260508-001",
    ]


def test_parse_artifact_intent(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    by_id = {a.artifact_id: a for a in artifacts}
    assert "intent" in by_id
    intent = by_id["intent"]
    assert intent.artifact_type == ArtifactType.INTENT
    assert intent.tier == "intent-specs"
    assert intent.approval_unit == "intent-specs"
    items = {i.item_id for i in intent.items}
    assert "CAP-0001" in items
    assert "CST-0001" in items


def test_parse_artifact_prd_derives(tiny_repo: Path):
    artifacts = parse_repo_path(tiny_repo)
    prd = next(a for a in artifacts if a.artifact_id == "prd")
    assert prd.derives_from == ["CAP-0001"]
    fr = next(i for i in prd.items if i.item_id == "FR-0001")
    assert fr.derives_from == ["CAP-0001"]


def test_parse_container_layer(container_layered_repo: Path):
    artifacts = parse_repo_path(container_layered_repo)
    container = next(a for a in artifacts if a.artifact_type == ArtifactType.CONTAINER)
    assert container.layer == ContainerLayer.PRESENTATION


def test_parse_component_extras(container_layered_repo: Path):
    artifacts = parse_repo_path(container_layered_repo)
    comp = next(a for a in artifacts if a.artifact_type == ArtifactType.COMPONENT)
    assert comp.extras["container_id"] == "web"
    assert comp.extras["hosted_bounded_contexts"] == ["BC-0001"]
    assert comp.extras["owned_paths"] == ["web/src/search/**"]


def test_discover_artifacts_skips_dot_dirs(tiny_repo: Path):
    (tiny_repo / ".vibeloom" / "junk").mkdir(parents=True, exist_ok=True)
    (tiny_repo / ".vibeloom" / "junk" / "container.md").write_text("garbage", encoding="utf-8")
    files = discover_artifacts(tiny_repo)
    paths = {f.rel_path for f in files}
    assert all(not p.startswith(".vibeloom/") for p in paths)
