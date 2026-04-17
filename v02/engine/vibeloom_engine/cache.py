"""JSON persistence for the graph cache and status snapshot.

Cache locations (per vibeloom-implementation.md):
  .vibeloom/state/context-graph.json
  .vibeloom/state/status.json

If either file is missing or fails to parse, the engine regenerates from ground
truth (contract + context artifacts).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vibeloom_engine.io_ import ensure_state_dir, state_dir
from vibeloom_engine.models import Graph


_GRAPH_FILENAME = "context-graph.json"
_STATUS_FILENAME = "status.json"


def save_graph(graph: Graph, repo_root: Path) -> Path:
    """Persist the graph cache. Returns the written path."""
    sd = ensure_state_dir(repo_root)
    path = sd / _GRAPH_FILENAME
    payload = graph.to_dict()
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_graph(repo_root: Path) -> Graph | None:
    """Load the graph cache. Returns None if missing or invalid."""
    path = state_dir(repo_root) / _GRAPH_FILENAME
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    try:
        return Graph.from_dict(data)
    except Exception:
        return None


def save_status(status: dict[str, Any], repo_root: Path) -> Path:
    """Persist a status snapshot as JSON. Returns the written path."""
    sd = ensure_state_dir(repo_root)
    path = sd / _STATUS_FILENAME
    path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_status(repo_root: Path) -> dict[str, Any] | None:
    """Load the status snapshot. Returns None if missing or invalid."""
    path = state_dir(repo_root) / _STATUS_FILENAME
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
