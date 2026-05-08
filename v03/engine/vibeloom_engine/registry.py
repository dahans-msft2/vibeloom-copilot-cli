"""ID registry — `.vibeloom/traces/id-registry.json` (§5.2, §5.3).

Two registry shapes share one JSON file:

1. Semantic-item families (CAP, CST, FR, …): `{prefix: {next, retired}}`.
2. Dated families (APPROVAL, RUN, TASK, DEC, …): `{prefix: {date: next_seq}}`.

Both shapes are stored under their prefix key. The retired list is
append-only; retired IDs are never reissued.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vibeloom_engine.ids import (
    IdKind,
    PREFIX_FAMILIES,
    format_dated_id,
    format_semantic_id,
    is_known_prefix,
    prefix_spec,
)
from vibeloom_engine.io_ import ensure_dir, traces_dir


_REGISTRY_FILENAME = "id-registry.json"


# Prefixes that use the dated form per §5.3.
_DATED_PREFIXES: frozenset[str] = frozenset(
    p.prefix for p in PREFIX_FAMILIES if p.kind in (IdKind.TRACE, IdKind.RUNTIME)
)


# ---------------------------------------------------------------------------
# Registry I/O
# ---------------------------------------------------------------------------


def registry_path(repo_root: Path) -> Path:
    return traces_dir(repo_root) / _REGISTRY_FILENAME


def load_registry(repo_root: Path) -> dict[str, Any]:
    p = registry_path(repo_root)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save_registry(repo_root: Path, data: dict[str, Any]) -> Path:
    ensure_dir(traces_dir(repo_root))
    p = registry_path(repo_root)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Semantic-item allocation (PREFIX-NNNN, retired never reused)
# ---------------------------------------------------------------------------


def allocate_semantic(repo_root: Path, prefix: str, count: int = 1) -> list[str]:
    """Allocate `count` new semantic IDs for `prefix`.

    Skips numbers in the `retired` list. Persists immediately.
    """
    if not is_known_prefix(prefix):
        raise ValueError(f"unknown prefix family: {prefix!r}")
    spec = prefix_spec(prefix)
    if spec is None or spec.kind != IdKind.GRAPH_ENTITY and spec.kind != IdKind.STRUCTURED:
        raise ValueError(f"prefix {prefix!r} is not a semantic-item family")

    data = load_registry(repo_root)
    entry = data.setdefault(prefix, {"next": 1, "retired": []})
    if "next" not in entry:
        entry["next"] = 1
    if "retired" not in entry:
        entry["retired"] = []
    retired_set = {
        int(rid.split("-", 1)[1])
        for rid in entry["retired"]
        if isinstance(rid, str) and "-" in rid
    }
    out: list[str] = []
    n = entry["next"]
    while len(out) < count:
        if n not in retired_set:
            out.append(format_semantic_id(prefix, n))
        n += 1
        if n > 9999:
            raise RuntimeError(
                f"prefix {prefix!r} exhausted (next would exceed 9999)"
            )
    entry["next"] = n
    save_registry(repo_root, data)
    return out


def retire_semantic(repo_root: Path, item_id: str) -> None:
    """Append `item_id` to its prefix's retired list. Idempotent."""
    if "-" not in item_id:
        raise ValueError(f"malformed item_id {item_id!r}")
    prefix = item_id.split("-", 1)[0]
    if not is_known_prefix(prefix):
        raise ValueError(f"unknown prefix family in {item_id!r}")
    data = load_registry(repo_root)
    entry = data.setdefault(prefix, {"next": 1, "retired": []})
    if "retired" not in entry:
        entry["retired"] = []
    if item_id not in entry["retired"]:
        entry["retired"].append(item_id)
    save_registry(repo_root, data)


def is_retired(repo_root: Path, item_id: str) -> bool:
    if "-" not in item_id:
        return False
    prefix = item_id.split("-", 1)[0]
    data = load_registry(repo_root)
    entry = data.get(prefix, {})
    return item_id in (entry.get("retired") or [])


# ---------------------------------------------------------------------------
# Dated allocation (TRACE / RUNTIME)
# ---------------------------------------------------------------------------


def allocate_dated(repo_root: Path, prefix: str, today: str | None = None) -> str:
    """Allocate a `<KIND>-YYYYMMDD-NNN` ID. Per-day counter resets each day."""
    if prefix not in _DATED_PREFIXES:
        raise ValueError(f"prefix {prefix!r} is not a dated family")
    if today is None:
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
    data = load_registry(repo_root)
    entry = data.setdefault(prefix, {})
    seq = entry.get(today, 0) + 1
    entry[today] = seq
    save_registry(repo_root, data)
    return format_dated_id(prefix, today, seq)


__all__ = [
    "registry_path",
    "load_registry",
    "save_registry",
    "allocate_semantic",
    "retire_semantic",
    "is_retired",
    "allocate_dated",
]
