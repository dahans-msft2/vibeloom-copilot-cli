"""Markdown + YAML-frontmatter parser for VibeLoom artifacts.

Responsibilities:
- Extract YAML frontmatter between leading `---` fences.
- Parse body structure into sections (H2 headers) and tables.
- Extract addressable items (short-ID PREFIX-#### references) from table rows.
- Extract derives_from lists (YAML-ish string arrays inside table cells).
- Handle ledger record sections (## PDR-####, ## ADR-####) with per-record
  metadata and derives_from lists.
- Handle bdd artifacts: scenario sections (### SCN-####) with per-scenario
  derives_from.

This parser is lenient by design: it reports what it could extract and
schema.py validates whether the extracted shape is valid.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from vibeloom_engine.ids import parse_id
from vibeloom_engine.io_ import DiscoveredFile, read_text
from vibeloom_engine.models import (
    Artifact,
    ArtifactType,
    ApprovalMode,
    CONTEXT_TYPES,
    Item,
    Scope,
    ScopeKind,
    Status,
)


_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(?P<yaml>.*?)\n---\s*\n(?P<body>.*)$",
    re.DOTALL,
)


# --- frontmatter parser (narrow YAML subset, zero runtime deps) -------------

_INT_RE = re.compile(r"^-?\d+$")
_FLOAT_RE = re.compile(r"^-?\d+\.\d+$")


def _parse_scalar(raw: str) -> Any:
    """Parse a bare scalar: null, bool, int, float, quoted or bare string."""
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
    """Parse VibeLoom frontmatter: a narrow flat subset of YAML.

    Supported:
      - `key: value` with scalar values (null, bool, int, float, string)
      - Double- and single-quoted string values (may contain colons)
      - Inline-flow lists: `key: []` or `key: [a, b, c]`
      - Blank lines and `# comment` lines

    Rejected (raise ValueError; caller treats as no frontmatter):
      - Indented / nested structures (no block-style lists or mappings)
      - YAML anchors, tags, multi-document streams

    VibeLoom frontmatter is flat by design — see methodology ## Artifact
    Format ### Frontmatter. Anything beyond this subset is a schema mistake
    and should surface loudly rather than silently parse wrong.
    """
    result: dict[str, Any] = {}
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if raw_line[: len(raw_line) - len(raw_line.lstrip())]:
            raise ValueError(f"indented frontmatter lines are not supported: {raw_line!r}")
        if ":" not in stripped:
            raise ValueError(f"frontmatter line missing ':': {raw_line!r}")
        key, _, rest = stripped.partition(":")
        key = key.strip()
        if not key:
            raise ValueError(f"frontmatter line missing key: {raw_line!r}")
        rest = rest.strip()
        value: Any
        if rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            if not inner:
                value = []
            else:
                value = [_parse_scalar(item.strip()) for item in inner.split(",")]
        else:
            value = _parse_scalar(rest)
        result[key] = value
    return result


def split_frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    """Return (frontmatter_dict_or_None, body_text). Non-frontmatter text leads body."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    try:
        parsed = _parse_frontmatter(m.group("yaml"))
    except ValueError:
        return None, m.group("body")
    return parsed, m.group("body")


# --- section + table parsing -----------------------------------------------


_H2_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
_H3_RE = re.compile(r"^###\s+(?P<title>.+?)\s*$")


def iter_sections(body: str, header_level: int = 2) -> list[tuple[str, str]]:
    """Split a body by the given header level and yield (title, content) pairs.

    Content of a section includes everything until the next same-level (or higher)
    header or end of body.
    """
    if header_level == 2:
        pattern = _H2_RE
    elif header_level == 3:
        pattern = _H3_RE
    else:
        raise ValueError(f"Unsupported header level: {header_level}")

    lines = body.splitlines()
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_body: list[str] = []
    for line in lines:
        m = pattern.match(line)
        # Treat any higher-level header as also ending the current section.
        if m:
            if current_title is not None:
                sections.append((current_title, current_body))
            current_title = m.group("title").strip()
            current_body = []
            continue
        # Also end at a higher-level header when we're looking at H3.
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
    """Parse GitHub-flavored Markdown tables in a section.

    Returns a list of row dicts. Supports multiple tables by merging; but in
    VibeLoom templates each section has at most one table.

    Empty cells are returned as empty strings. Header row defines keys
    (lowercase, whitespace stripped).
    """
    lines = section_text.splitlines()
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    seen_separator = False

    for line in lines:
        if not _TABLE_ROW_RE.match(line):
            # A blank line or non-table line ends the current table block.
            if header is not None and seen_separator:
                # Reset; if another table follows we'll start fresh.
                header = None
                seen_separator = False
            continue
        # Skip HTML comments that masquerade as table rows
        stripped_line = line.strip()
        if stripped_line.startswith("<!--") or stripped_line.startswith("-->"):
            continue

        cells = [c.strip() for c in stripped_line.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if not seen_separator:
            if _TABLE_SEPARATOR_RE.match(line):
                seen_separator = True
                continue
            # First non-separator "row" without separator is malformed; treat
            # as header re-read.
            header = [c.lower() for c in cells]
            continue
        # Data row
        row = {}
        for i, h in enumerate(header):
            row[h] = cells[i] if i < len(cells) else ""
        rows.append(row)

    return rows


# --- derives_from cell parsing ---------------------------------------------


_ID_REF_RE = re.compile(r"[A-Z]+-\d{4}")


def parse_id_list(cell: str) -> list[str]:
    """Extract short IDs from a table cell.

    Accepts multiple formats:
      - "FR-0001, NFR-0002"
      - "[FR-0001, NFR-0002]"
      - "`FR-0001`, `NFR-0002`"
      - "FR-0001"
      - empty or "-" or "N/A" → []
    """
    if not cell or cell.strip() in {"-", "—", "N/A", "None", "[]", ""}:
        return []
    return _ID_REF_RE.findall(cell)


# --- artifact parsing ------------------------------------------------------


def _mk_scope(fm: dict[str, Any]) -> Scope:
    kind_str = fm.get("scope_kind", "root")
    scope_id = str(fm.get("scope_id", "root"))
    try:
        kind = ScopeKind(kind_str)
    except ValueError:
        kind = ScopeKind.ROOT
    return Scope(kind=kind, scope_id=scope_id)


def _extract_extras(fm: dict[str, Any]) -> dict[str, Any]:
    """Return frontmatter fields that aren't part of the core schema."""
    core = {
        "artifact_id",
        "artifact_type",
        "tier",
        "scope_kind",
        "scope_id",
        "status",
        "timestamp",
        "approval_mode",
        "derives_from",
    }
    return {k: v for k, v in fm.items() if k not in core}


def _parse_ledger(body: str, prefix: str) -> list[Item]:
    """Parse a pdr/adr ledger body: one Item per ## <PREFIX>-#### section."""
    items: list[Item] = []
    for title, content in iter_sections(body, header_level=2):
        # Title may be something like "PDR-0001" (possibly wrapped in backticks).
        stripped = title.strip("`").strip()
        parsed = parse_id(stripped)
        if not parsed or parsed[0] != prefix:
            continue
        # Extract per-record derives_from (looking for a list or dotted line).
        derives: list[str] = []
        recorded_at = ""
        for line in content.splitlines():
            s = line.strip()
            low = s.lower()
            if low.startswith("- **derives_from:") or low.startswith("**derives_from:"):
                derives = parse_id_list(s)
            elif low.startswith("- **recorded_at:") or low.startswith("**recorded_at:"):
                # Extract the value after the colon.
                colon = s.find(":")
                if colon >= 0:
                    recorded_at = s[colon + 1 :].strip().strip("`")
        items.append(
            Item(
                item_id=stripped,
                artifact_id=prefix.lower(),  # "pdr" or "adr"
                section=title,
                tier="context",
                scope=Scope(kind=ScopeKind.ROOT, scope_id="root"),
                derives_from=derives,
                description="",
                extra={"recorded_at": recorded_at} if recorded_at else {},
            )
        )
    return items


def _parse_bdd_scenarios(body: str, artifact_id: str, scope: Scope) -> list[Item]:
    """Parse bdd body: H3 sections named SCN-####."""
    items: list[Item] = []
    # Walk H2 sections; scenario sections live under the "Scenarios" H2 as H3.
    for h2_title, h2_content in iter_sections(body, header_level=2):
        if "scenario" not in h2_title.lower():
            continue
        for h3_title, h3_content in iter_sections(h2_content, header_level=3):
            stripped = h3_title.strip("`").strip()
            parsed = parse_id(stripped)
            if not parsed or parsed[0] != "SCN":
                continue
            derives: list[str] = []
            for line in h3_content.splitlines():
                s = line.strip()
                low = s.lower()
                if low.startswith("- **derives_from:") or low.startswith("**derives_from:"):
                    derives = parse_id_list(s)
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


def _parse_table_items(
    body: str,
    artifact_id: str,
    tier: str,
    scope: Scope,
) -> list[Item]:
    """Extract items from H2 sections that contain tables with an `id` column.

    Each row with an `id` matching PREFIX-#### becomes an Item.
    """
    items: list[Item] = []
    for section_title, section_body in iter_sections(body, header_level=2):
        rows = parse_table(section_body)
        if not rows:
            continue
        for row in rows:
            raw_id = row.get("id", "").strip().strip("`").strip()
            parsed = parse_id(raw_id)
            if not parsed:
                continue
            derives = parse_id_list(row.get("derives_from", ""))
            description = row.get("description", "").strip()
            # Collect all other columns as extras.
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


def parse_artifact(file: DiscoveredFile) -> Artifact | None:
    """Parse a single discovered file into an Artifact, or return None if not parseable."""
    text = read_text(file.abs_path)
    fm, body = split_frontmatter(text)
    if not fm:
        return None
    # Determine artifact_type from frontmatter; accept strings we recognize.
    at_str = fm.get("artifact_type")
    if not at_str:
        return None
    try:
        artifact_type = ArtifactType(at_str)
    except ValueError:
        return None

    tier = str(fm.get("tier", "")).strip()
    scope = _mk_scope(fm)
    artifact_id = str(fm.get("artifact_id", "")).strip()
    if not artifact_id:
        return None

    status: Status | None = None
    approval_mode: ApprovalMode | None = None
    if artifact_type not in CONTEXT_TYPES:
        status_str = fm.get("status")
        if status_str:
            try:
                status = Status(status_str)
            except ValueError:
                status = None
        am_str = fm.get("approval_mode")
        if am_str:
            try:
                approval_mode = ApprovalMode(am_str)
            except ValueError:
                approval_mode = None

    derives_from_fm = fm.get("derives_from", [])
    if isinstance(derives_from_fm, str):
        derives_from_fm = parse_id_list(derives_from_fm)
    elif isinstance(derives_from_fm, list):
        derives_from_fm = [str(x).strip().strip("`") for x in derives_from_fm if str(x).strip()]
    else:
        derives_from_fm = []

    extras = _extract_extras(fm)
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
        approval_mode=approval_mode,
        derives_from=derives_from_fm,
        items=[],
        extras=extras,
        mtime=file.mtime,
    )

    # Type-specific body parsing.
    if artifact_type == ArtifactType.PDR:
        artifact.items = _parse_ledger(body, "PDR")
    elif artifact_type == ArtifactType.ADR:
        artifact.items = _parse_ledger(body, "ADR")
    elif artifact_type == ArtifactType.BDD:
        artifact.items = _parse_bdd_scenarios(body, artifact_id, scope)
    elif artifact_type == ArtifactType.CONFIG:
        # Config artifacts carry no addressable items per methodology.
        artifact.items = []
    else:
        # Contract tiers: parse tables with id columns.
        artifact.items = _parse_table_items(body, artifact_id, tier, scope)

    return artifact


def parse_repo(files: list[DiscoveredFile]) -> list[Artifact]:
    """Parse all discovered files. Returns a list of Artifacts (skipping unparseable)."""
    artifacts: list[Artifact] = []
    for f in files:
        a = parse_artifact(f)
        if a is not None:
            artifacts.append(a)
    return artifacts


def parse_repo_path(repo_root: Path) -> list[Artifact]:
    """Convenience: discover + parse in one call."""
    from vibeloom_engine.io_ import discover_artifacts

    files = discover_artifacts(repo_root)
    return parse_repo(files)
