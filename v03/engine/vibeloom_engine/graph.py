"""Contract graph builder + queries.

Builds the v0.3 graph from parsed artifacts. Edges come from each item's
`derives_from`. The contract graph is a DAG (methodology §8); cycles are
caught by `find_cycles` and surfaced as blocking findings during eval.

Per §8.1 hashing: items have canonical SHA-256 over a normalized JSON shape
(item_id excluded, derives_from sorted).
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import deque

from vibeloom_engine.models import Artifact, Edge, Graph, Item


def canonical_item_hash(item: Item) -> str:
    """Canonical SHA-256 over the item's semantic shape.

    Excludes item_id (rename = remove + add). Sorts derives_from
    (derivation is a set).
    """
    payload = item.to_dict()
    payload.pop("item_id", None)
    payload["derives_from"] = sorted(payload.get("derives_from", []))
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def canonical_artifact_hash(artifact: Artifact) -> str:
    """Canonical SHA-256 over the artifact's semantic shape (frontmatter + items)."""
    payload = artifact.to_dict()
    payload.pop("mtime", None)
    payload.pop("path", None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_graph(artifacts: list[Artifact]) -> Graph:
    """Construct the in-memory graph from parsed artifacts."""
    g = Graph()
    for a in artifacts:
        # Last writer wins for duplicate artifact_id (eval flags it).
        g.artifacts[a.artifact_id] = a
        for item in a.items:
            if item.item_id in g.items:
                continue  # duplicate — eval reports
            g.items[item.item_id] = item
    for item in g.items.values():
        for upstream in item.derives_from:
            # Edge always emitted, even if upstream missing — eval surfaces
            # missing upstream as `dangling` separately.
            g.edges.append(Edge(source=item.item_id, target=upstream))
    return g


# ---------------------------------------------------------------------------
# Walks
# ---------------------------------------------------------------------------


def reachable_downstream(graph: Graph, start_ids: list[str]) -> set[str]:
    """All item IDs reachable downstream from any start ID (incl. starts).

    Walks the reverse-of-derives_from direction: if X derives_from Y, X is
    downstream of Y.
    """
    adj: dict[str, list[str]] = {}
    for e in graph.edges:
        adj.setdefault(e.target, []).append(e.source)
    visited: set[str] = set()
    queue: deque[str] = deque(start_ids)
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for nxt in adj.get(node, ()):
            if nxt not in visited:
                queue.append(nxt)
    return visited


def reachable_upstream(graph: Graph, start_ids: list[str]) -> set[str]:
    """All item IDs reachable upstream (along derives_from) from any start ID."""
    visited: set[str] = set()
    queue: deque[str] = deque(start_ids)
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        item = graph.items.get(node)
        if not item:
            continue
        for up in item.derives_from:
            if up not in visited:
                queue.append(up)
    return visited


# ---------------------------------------------------------------------------
# Cycle detection (full path, per §8.2 invariant)
# ---------------------------------------------------------------------------


def find_cycles(graph: Graph) -> list[list[str]]:
    """Return a list of cycles in the derives_from graph.

    Each cycle is returned as `[A, B, C, A]` where the first and last node
    are the same. The DFS is iterative to avoid Python recursion limits on
    deep chains.
    """
    # adjacency: node -> list of upstream targets (derives_from)
    adj: dict[str, list[str]] = {iid: list(item.derives_from) for iid, item in graph.items.items()}

    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {iid: WHITE for iid in adj}
    cycles: list[list[str]] = []
    found: set[tuple[str, ...]] = set()

    # Iterative DFS using a stack of (node, iter-of-neighbors, path-index)
    # so we can recover the cycle path when we hit a GRAY back-edge.
    sys.setrecursionlimit(10000)

    def dfs(start: str) -> None:
        stack: list[tuple[str, list[str], int]] = []
        path: list[str] = []
        color[start] = GRAY
        path.append(start)
        stack.append((start, adj.get(start, []), 0))
        while stack:
            node, neighbors, i = stack[-1]
            if i >= len(neighbors):
                color[node] = BLACK
                path.pop()
                stack.pop()
                continue
            stack[-1] = (node, neighbors, i + 1)
            nxt = neighbors[i]
            if nxt not in color:
                continue  # dangling upstream — handled by eval
            if color[nxt] == GRAY:
                # back-edge -> cycle
                try:
                    idx = path.index(nxt)
                    cycle = path[idx:] + [nxt]
                    key = tuple(cycle)
                    if key not in found:
                        found.add(key)
                        cycles.append(cycle)
                except ValueError:
                    pass
            elif color[nxt] == WHITE:
                color[nxt] = GRAY
                path.append(nxt)
                stack.append((nxt, adj.get(nxt, []), 0))

    for iid in list(adj.keys()):
        if color[iid] == WHITE:
            dfs(iid)
    return cycles


def dangling_references(graph: Graph) -> list[tuple[str, str]]:
    """Return (item_id, missing_upstream_id) pairs."""
    out: list[tuple[str, str]] = []
    for item in graph.items.values():
        for up in item.derives_from:
            if up not in graph.items:
                out.append((item.item_id, up))
    return out


__all__ = [
    "canonical_item_hash",
    "canonical_artifact_hash",
    "build_graph",
    "reachable_downstream",
    "reachable_upstream",
    "find_cycles",
    "dangling_references",
]
