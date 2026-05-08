"""Cache management at `.vibeloom/cache/` per §3.

Cache is regenerable, never authoritative. If deleted, the engine rebuilds
it from artifacts + the trace history.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from vibeloom_engine.io_ import cache_dir, ensure_dir
from vibeloom_engine.models import Graph


_GRAPH_FILE = "contract-graph.json"
_STATUS_FILE = "status.json"


def save_graph(graph: Graph, repo_root: Path) -> Path:
    cd = ensure_dir(cache_dir(repo_root))
    p = cd / _GRAPH_FILE
    p.write_text(
        json.dumps(graph.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return p


def load_graph(repo_root: Path) -> Graph | None:
    p = cache_dir(repo_root) / _GRAPH_FILE
    if not p.is_file():
        return None
    try:
        return Graph.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError, KeyError):
        return None


def save_status(status: dict[str, Any], repo_root: Path) -> Path:
    cd = ensure_dir(cache_dir(repo_root))
    p = cd / _STATUS_FILE
    p.write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return p


def load_status(repo_root: Path) -> dict[str, Any] | None:
    p = cache_dir(repo_root) / _STATUS_FILE
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def clear_cache(repo_root: Path) -> None:
    cd = cache_dir(repo_root)
    if cd.exists():
        shutil.rmtree(cd)


__all__ = [
    "save_graph",
    "load_graph",
    "save_status",
    "load_status",
    "clear_cache",
]
