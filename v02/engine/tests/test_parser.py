"""Parser smoke tests."""

from pathlib import Path

from vibeloom_engine.parser import parse_repo_path, split_frontmatter


def test_split_frontmatter_basic():
    text = "---\nkey: value\n---\nbody here\n"
    fm, body = split_frontmatter(text)
    assert fm == {"key": "value"}
    assert "body here" in body


def test_split_frontmatter_no_frontmatter():
    text = "# Heading\n\nno frontmatter"
    fm, body = split_frontmatter(text)
    assert fm is None
    assert body == text


def test_parse_vibe_repo(vibe_repo: Path):
    artifacts = parse_repo_path(vibe_repo)
    ids = {a.artifact_id for a in artifacts}
    assert "intent" in ids
    assert "defaults" in ids
    assert "system" in ids


def test_parse_items_are_extracted(vibe_repo: Path):
    artifacts = parse_repo_path(vibe_repo)
    intent = next(a for a in artifacts if a.artifact_id == "intent")
    item_ids = {i.item_id for i in intent.items}
    assert "CAP-0001" in item_ids
    assert "CST-0001" in item_ids


def test_parse_derives_from(vibe_repo: Path):
    artifacts = parse_repo_path(vibe_repo)
    system = next(a for a in artifacts if a.artifact_id == "system")
    cmp_item = next(i for i in system.items if i.item_id == "CMP-0001")
    assert "CONT-0001" in cmp_item.derives_from
