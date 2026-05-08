"""Markdown + YAML-frontmatter parser for v0.3 artifacts.

Responsibilities:
- Extract YAML frontmatter between leading `---` fences (narrow flat subset).
- Parse body H2/H3 sections and GFM tables.
- Extract IDed items per the §5.1 prefix table and §17.3 column conventions.
- Container-frontmatter `layer` enum (§6.3).
- Component-frontmatter `hosted_bounded_contexts` etc. (§6.4).

Lenient by design: schema validation lives in `schema.py` / `eval_.py`.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from vibeloom_engine.ids import parse_semantic_id
from vibeloom_engine.io_ import DiscoveredFile, read_text
from vibeloom_engine.models import (
    Artifact,
    ArtifactType,
    CONTEXT_TYPES,
    ContainerLayer,
    Item,
    Scope,
    ScopeKind,
    Status,
)


_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(?P<yaml>.*?)\n---\s*\n(?P<body>.*)$",
    re.DOTALL,
)


# ---------------------------------------------------------------------------
# YAML frontmatter (narrow flat subset, stdlib only)
# ---------------------------------------------------------------------------


_INT_RE = re.compile(r"^-?\d+$")
_FLOAT_RE = re.compile(r"^-?\d+\.\d+$")


def _parse_scalar(raw: str) -> Any:
    if raw == "" or raw == "null" or raw == "~":
        return None
    if raw == "true":
        return True
    if raw == "false":
        return False
    if len(raw) >= 2 and raw[0] in ('"', "'") and raw[-1] == raw[0]:
        return raw[1:-1]
    if _INT_RE.match(raw):
        return int(raw)
    if _FLOAT_RE.match(raw):
        return float(raw)
    return raw


def _parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse v0.3 frontmatter: a narrow flat subset of YAML.

    Supports:
      - `key: value` with scalar values
      - inline-flow lists: `key: []` or `key: [a, b, c]`
      - block-style scalar lists with `- value` lines under a top-level key
        (used for `owned_paths`, `hosted_bounded_contexts`)
      - blank lines and `# comment` lines
    """
    result: dict[str, Any] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        # Top-level key (no leading indent)
        leading = len(raw_line) - len(raw_line.lstrip())
        if leading != 0:
            raise ValueError(
                f"top-level frontmatter must not be indented: {raw_line!r}"
            )
        if ":" not in stripped:
            raise ValueError(f"frontmatter line missing ':': {raw_line!r}")
        key, _, rest = stripped.partition(":")
        key = key.strip()
        if not key:
            raise ValueError(f"frontmatter line missing key: {raw_line!r}")
        rest = rest.strip()
        if rest == "":
            # block-style list follows: collect adjacent `- item` lines
            items: list[Any] = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                next_stripped = next_line.strip()
                if not next_stripped:
                    j += 1
                    continue
                if next_line.startswith(("  - ", "- ")):
                    # Strip the leader
                    item_str = next_stripped[2:].strip() if next_stripped.startswith("- ") else next_stripped[2:].strip()
                    items.append(_parse_scalar(item_str))
                    j += 1
                else:
                    break
            result[key] = items
            i = j
            continue
        if rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            if not inner:
                value: Any = []
            else:
                value = [_parse_scalar(it.strip()) for it in inner.split(",")]
            result[key] = value
        else:
            result[key] = _parse_scalar(rest)
        i += 1
    return result


def split_frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    """Return (frontmatter_dict_or_None, body)."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    try:
        parsed = _parse_frontmatter(m.group("yaml"))
    except ValueError:
        return None, m.group("body")
    return parsed, m.group("body")


# ---------------------------------------------------------------------------
# Body sectioning + table parsing
# ---------------------------------------------------------------------------


_H2_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
_H3_RE = re.compile(r"^###\s+(?P<title>.+?)\s*$")


def iter_sections(body: str, header_level: int = 2) -> list[tuple[str, str]]:
    """Split a body by `header_level` headers; returns (title, content) pairs."""
    if header_level == 2:
        pattern = _H2_RE
    elif header_level == 3:
        pattern = _H3_RE
    else:
        raise ValueError(f"unsupported header level: {header_level}")
    lines = body.splitlines()
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_body: list[str] = []
    for line in lines:
        m = pattern.match(line)
        if m:
            if current_title is not None:
                sections.append((current_title, current_body))
            current_title = m.group("title").strip()
            current_body = []
            continue
        if header_level == 3 and _H2_RE.match(line):
            if current_title is not None:
                sections.append((current_title, current_body))
                current_title = None
                current_body = []
            continue
        if current_title is not None:
            current_body.append(line)
    if current_title is not None:
        sections.append((current_title, current_body))
    return [(t, "\n".join(b)) for t, b in sections]


_TABLE_ROW_RE = re.compile(r"^\s*\|(.*)\|\s*$")
_TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")


def parse_table(section_text: str) -> list[dict[str, str]]:
    """Parse GFM tables; returns list of row dicts (header → cell)."""
    lines = section_text.splitlines()
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    seen_separator = False
    for line in lines:
        if not _TABLE_ROW_RE.match(line):
            if header is not None and seen_separator:
                header = None
                seen_separator = False
            continue
        s = line.strip()
        if s.startswith("<!--") or s.startswith("-->"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if not seen_separator:
            if _TABLE_SEPARATOR_RE.match(line):
                seen_separator = True
                continue
            header = [c.lower() for c in cells]
            continue
        row: dict[str, str] = {}
        for i, h in enumerate(header):
            row[h] = cells[i] if i < len(cells) else ""
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# derives_from cell parsing
# ---------------------------------------------------------------------------


# Order alternatives longest-first so dated-form IDs aren't truncated to
# their leading 4 digits.
_ID_REF_RE = re.compile(r"[A-Z]+-(?:\d{8}-\d{3}|\d{4})")


def parse_id_list(cell: str) -> list[str]:
    """Extract IDs from a cell or freeform string."""
    if not cell:
        return []
    s = cell.strip()
    if s in {"-", "—", "N/A", "None", "[]", ""}:
        return []
    return _ID_REF_RE.findall(s)


# ---------------------------------------------------------------------------
# Artifact assembly
# ---------------------------------------------------------------------------


CORE_FRONTMATTER_KEYS: frozenset[str] = frozenset(
    {
        "artifact_id",
        "artifact_type",
        "tier",
        "approval_unit",
        "scope_kind",
        "scope_id",
        "status",
        "timestamp",
        "derives_from",
        "layer",
        # component-shaped frontmatter (§6.4)
        "component_id",
        "container_id",
        "owned_paths",
        "owned_interfaces",
        "hosted_bounded_contexts",
    }
)


def _scope(fm: dict[str, Any]) -> Scope:
    raw_kind = fm.get("scope_kind", "root")
    sid = str(fm.get("scope_id", "root"))
    try:
        kind = ScopeKind(raw_kind)
    except ValueError:
        kind = ScopeKind.ROOT
    return Scope(kind=kind, scope_id=sid)


def _extras(fm: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in fm.items() if k not in CORE_FRONTMATTER_KEYS}


def _collect_extras_for_artifact(fm: dict[str, Any]) -> dict[str, Any]:
    out = _extras(fm)
    # Promote container/component-shape fields into extras for convenience.
    for k in (
        "component_id",
        "container_id",
        "owned_paths",
        "owned_interfaces",
        "hosted_bounded_contexts",
    ):
        if k in fm:
            out[k] = fm[k]
    return out


def _parse_table_items(body: str, artifact_id: str, tier: str, scope: Scope) -> list[Item]:
    items: list[Item] = []
    seen_ids: set[str] = set()
    for section_title, section_body in iter_sections(body, header_level=2):
        rows = parse_table(section_body)
        if not rows:
            continue
        for row in rows:
            raw_id = row.get("id", "").strip().strip("`").strip()
            parsed = parse_semantic_id(raw_id)
            if not parsed:
                continue
            if raw_id in seen_ids:
                continue
            seen_ids.add(raw_id)
            derives = parse_id_list(row.get("derives_from", ""))
            description = row.get("description", "").strip()
            extras = {
                k: v.strip()
                for k, v in row.items()
                if k not in {"id", "derives_from", "description"} and v
            }
            items.append(
                Item(
                    item_id=raw_id,
                    artifact_id=artifact_id,
                    section=section_title,
                    tier=tier,
                    scope=scope,
                    derives_from=derives,
                    description=description,
                    extra=extras,
                )
            )
    return items


def _parse_bdd_scenarios(body: str, artifact_id: str, scope: Scope) -> list[Item]:
    """Parse bdd body: H3 sections named SCN-#### under any H2 mentioning 'scenario'."""
    items: list[Item] = []
    for h2_title, h2_content in iter_sections(body, header_level=2):
        if "scenario" not in h2_title.lower():
            continue
        for h3_title, h3_content in iter_sections(h2_content, header_level=3):
            stripped = h3_title.strip("`").strip()
            parsed = parse_semantic_id(stripped)
            if not parsed or parsed[0] != "SCN":
                continue
            derives: list[str] = []
            for line in h3_content.splitlines():
                lo = line.strip().lower()
                if lo.startswith("- **derives_from:") or lo.startswith("**derives_from:"):
                    derives = parse_id_list(line)
                    break
            items.append(
                Item(
                    item_id=stripped,
                    artifact_id=artifact_id,
                    section=h3_title,
                    tier="context",
                    scope=scope,
                    derives_from=derives,
                    description="",
                )
            )
    return items


def parse_artifact(file: DiscoveredFile) -> Artifact | None:
    """Parse a single discovered file into an Artifact."""
    text = read_text(file.abs_path)
    fm, body = split_frontmatter(text)
    if not fm:
        return None

    at_str = fm.get("artifact_type")
    if not at_str:
        return None
    try:
        artifact_type = ArtifactType(at_str)
    except ValueError:
        return None

    tier = str(fm.get("tier", "")).strip()
    scope = _scope(fm)
    artifact_id = str(fm.get("artifact_id", "")).strip()
    if not artifact_id:
        return None

    status: Status | None = None
    if artifact_type in CONTEXT_TYPES or artifact_type == ArtifactType.VALIDATION_REGISTRY:
        status = None
    else:
        s = fm.get("status")
        if s:
            try:
                status = Status(s)
            except ValueError:
                status = None

    # derives_from
    raw_derives = fm.get("derives_from", [])
    if isinstance(raw_derives, str):
        derives_list = parse_id_list(raw_derives)
    elif isinstance(raw_derives, list):
        derives_list = [str(x).strip().strip("`") for x in raw_derives if str(x).strip()]
    else:
        derives_list = []

    # approval_unit (contract only)
    approval_unit = None
    if artifact_type in CONTEXT_TYPES or artifact_type == ArtifactType.VALIDATION_REGISTRY:
        approval_unit = None
    else:
        approval_unit = fm.get("approval_unit")
        if approval_unit is not None:
            approval_unit = str(approval_unit)

    # container layer (only for ArtifactType.CONTAINER)
    layer: ContainerLayer | None = None
    if artifact_type == ArtifactType.CONTAINER:
        layer_raw = fm.get("layer")
        if layer_raw is not None:
            try:
                layer = ContainerLayer(str(layer_raw))
            except ValueError:
                layer = None

    timestamp = fm.get("timestamp")
    if timestamp is not None:
        timestamp = str(timestamp)

    artifact = Artifact(
        artifact_id=artifact_id,
        artifact_type=artifact_type,
        tier=tier,
        scope=scope,
        path=file.rel_path,
        status=status,
        timestamp=timestamp,
        approval_unit=approval_unit,
        derives_from=derives_list,
        items=[],
        extras=_collect_extras_for_artifact(fm),
        mtime=file.mtime,
        layer=layer,
    )

    # Body parsing per artifact type.
    if artifact_type == ArtifactType.BDD:
        artifact.items = _parse_bdd_scenarios(body, artifact_id, scope)
    elif artifact_type in CONTEXT_TYPES or artifact_type == ArtifactType.VALIDATION_REGISTRY:
        artifact.items = []
    else:
        artifact.items = _parse_table_items(body, artifact_id, tier, scope)

    return artifact


def parse_repo(files: list[DiscoveredFile]) -> list[Artifact]:
    out: list[Artifact] = []
    for f in files:
        a = parse_artifact(f)
        if a is not None:
            out.append(a)
    return out


def parse_repo_path(repo_root: Path) -> list[Artifact]:
    from vibeloom_engine.io_ import discover_artifacts

    files = discover_artifacts(repo_root)
    return parse_repo(files)


__all__ = [
    "split_frontmatter",
    "iter_sections",
    "parse_table",
    "parse_id_list",
    "parse_artifact",
    "parse_repo",
    "parse_repo_path",
    "CORE_FRONTMATTER_KEYS",
]
