"""Per-record markdown rendering for decision traces (§8.5.1).

Renders `.vibeloom/traces/decisions.jsonl` to
`/decisions/<record_type>/<TRACE_ID>-<slug>.md`. Idempotent. The body
prose is written from `payload` on first materialization, then preserved
on subsequent renders (the engine never overwrites a body the user has
edited; it does refresh the frontmatter when other JSONL fields change).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from vibeloom_engine.io_ import decisions_dir, ensure_dir
from vibeloom_engine.parser import split_frontmatter
from vibeloom_engine.traces import iter_trace_records


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = _SLUG_RE.sub("-", s)
    return s.strip("-") or "untitled"


# ---------------------------------------------------------------------------
# Frontmatter rendering
# ---------------------------------------------------------------------------


def _emit_yaml_value(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        if not v:
            return "[]"
        # inline form for short lists of scalars
        return "[" + ", ".join(_emit_yaml_value(x) for x in v) + "]"
    s = str(v)
    if any(ch in s for ch in ":#[]{}\"'") or s.lower() in ("true", "false", "null", "yes", "no"):
        return f'"{s}"'
    return s


def render_frontmatter(rec: dict[str, Any]) -> str:
    lines = ["---"]
    # Standard ordering for diffability.
    ordered_keys = [
        "trace_id", "kind", "record_type", "timestamp", "author",
        "topic", "load_bearing", "affects",
    ]
    for k in ordered_keys:
        if k in rec:
            lines.append(f"{k}: {_emit_yaml_value(rec[k])}")
    # Any other fields after the standard set (deterministic)
    for k in sorted(rec.keys()):
        if k in ordered_keys or k in ("schema_version", "payload"):
            continue
        lines.append(f"{k}: {_emit_yaml_value(rec[k])}")
    lines.append("---")
    return "\n".join(lines)


def render_body(rec: dict[str, Any]) -> str:
    """Render the default Nygard ADR body from `payload` (first materialization).

    The body has Context / Decision / Consequences sections. `payload` may
    be a dict (with those keys) or a freeform string; the engine renders
    sensibly in either case.
    """
    rt = rec.get("record_type") or "general"
    trace_id = rec.get("trace_id") or "unknown"
    topic = rec.get("topic") or "untitled"
    title = f"# {trace_id} — {topic}"
    payload = rec.get("payload")
    if isinstance(payload, dict):
        ctx = payload.get("context", "")
        dec = payload.get("decision", "")
        cons = payload.get("consequences", "")
    else:
        ctx = ""
        dec = str(payload or "")
        cons = ""
    parts = [title, "", "## Context", "", str(ctx).strip() or "_to be filled_", "",
             "## Decision", "", str(dec).strip() or "_to be filled_", "",
             "## Consequences", "", str(cons).strip() or "_to be filled_", ""]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# render_decisions — public entry
# ---------------------------------------------------------------------------


def render_decisions(repo_root: Path) -> list[str]:
    """Render every decision record. Idempotent.

    Returns the list of relative paths written/refreshed.
    """
    out_paths: list[str] = []
    try:
        records = list(iter_trace_records(repo_root, "decision"))
    except FileNotFoundError:
        return []

    base = decisions_dir(repo_root)
    for rec in records:
        rt = (rec.get("record_type") or "general").lower()
        trace_id = rec.get("trace_id") or "DEC-unknown"
        topic = rec.get("topic") or "untitled"
        slug = slugify(topic)
        rel = f"{rt}/{trace_id}-{slug}.md"
        target = base / rel
        ensure_dir(target.parent)

        new_frontmatter = render_frontmatter(rec)
        if target.is_file():
            # Preserve existing body; refresh frontmatter only.
            existing = target.read_text(encoding="utf-8")
            fm, body = split_frontmatter(existing)
            if fm is None:
                # No frontmatter → treat as fresh body, rewrite frontmatter only.
                content = new_frontmatter + "\n\n" + existing.strip() + "\n"
            else:
                # Preserve body verbatim; rewrite frontmatter.
                content = new_frontmatter + "\n" + body
                if not content.endswith("\n"):
                    content += "\n"
        else:
            content = new_frontmatter + "\n\n" + render_body(rec) + "\n"

        target.write_text(content, encoding="utf-8")
        out_paths.append(str(target.relative_to(repo_root)))
    return out_paths


__all__ = ["render_decisions", "slugify", "render_frontmatter", "render_body"]
