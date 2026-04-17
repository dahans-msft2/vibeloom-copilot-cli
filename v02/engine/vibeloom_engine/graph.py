"""Context graph builder + queries.

Builds a Graph from a list of parsed Artifacts. Emits one Edge per item-level
derives_from reference where both endpoints exist. Artifact-level
derives_from is intentionally not expanded into edges: per the methodology,
artifact-level entries are a summary constraint set, while item-level
references are the canonical derivation.

Graph queries are provided for:
- upstream / downstream walks
- forward reachability (for affected sets)
- cycle detection (should never trigger; DAG invariant)

Approved-state snapshots (per-artifact mtime + per-item canonical hashes) are
captured at first sight of an approved artifact and preserved across rebuilds
until the artifact transitions to `draft`. See vibeloom-implementation.md
## Runtime State ### Graph Cache ### Snapshot Lifecycle.
"""

from __future__ import annotations

import hashlib
import json
from collections import deque

from vibeloom_engine.models import ApprovalSnapshot, Artifact, Edge, Graph, Item


def canonical_item_hash(item: Item) -> str:
    """Return the canonical SHA-256 hex digest of an item's semantic content.

    The hash is over a sorted-keys JSON of the item's fields, with:
      - item_id removed (it's the lookup key; a rename is remove + add)
      - derives_from sorted lexicographically (derivation is a set, not a
        sequence)

    See vibeloom-implementation.md ## Runtime State ### Graph Cache ### Canonical
    Item Hash for the full specification.
    """
    payload = item.to_dict()
    payload.pop("item_id", None)
    payload["derives_from"] = sorted(payload.get("derives_from", []))
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_graph(artifacts: list[Artifact], prior: Graph | None = None) -> Graph:
    """Build a Graph from a list of parsed Artifacts.

    The returned Graph contains:
      - artifacts indexed by artifact_id
      - items indexed by item_id
      - edges for each item-level derives_from where both endpoints exist
      - approved_snapshots: per-approved-artifact mtime + per-item hashes

    Approved-state snapshots follow the lifecycle in vibeloom-implementation.md:
    captured at first sight of an approved artifact, preserved across rebuilds,
    and dropped when the artifact transitions to `draft`. Pass `prior` (a
    previously-built graph loaded from cache) to preserve existing snapshots;
    omit it for a cold start.
    """
    g = Graph()
    prior_snapshots = prior.approved_snapshots if prior is not None else {}
    # Index artifacts and items.
    for a in artifacts:
        g.artifacts[a.artifact_id] = a
        for item in a.items:
            if item.item_id in g.items:
                # Already reported by schema.validate_repo as a duplicate; keep
                # first occurrence in the graph.
                continue
            g.items[item.item_id] = item
        # Manage approval snapshot: preserve prior if present and still approved;
        # capture fresh snapshot on first sight of an approved artifact; drop
        # snapshot for drafts.
        if a.status and a.status.value == "approved" and a.mtime is not None:
            if a.artifact_id in prior_snapshots:
                g.approved_snapshots[a.artifact_id] = prior_snapshots[a.artifact_id]
            else:
                g.approved_snapshots[a.artifact_id] = ApprovalSnapshot(
                    mtime=a.mtime,
                    item_hashes={item.item_id: canonical_item_hash(item) for item in a.items},
                )
    # Emit edges from item-level derives_from.
    for item in g.items.values():
        for upstream_id in item.derives_from:
            if upstream_id in g.items:
                g.edges.append(Edge(source=item.item_id, target=upstream_id))
    return g


# --- queries ---------------------------------------------------------------


def reachable_forward(graph: Graph, start_ids: list[str]) -> set[str]:
    """Return the set of all item IDs reachable by walking edges forward
    (downstream) from any of the start IDs. Includes the start IDs themselves.

    "Forward" means: if X derives_from Y, an edge points from X → Y, so the
    downstream direction is the reverse of that edge (we walk from Y to X).
    """
    # Build a reverse adjacency once: target -> [sources]
    adj: dict[str, list[str]] = {}
    for e in graph.edges:
        adj.setdefault(e.target, []).append(e.source)
    visited: set[str] = set()
    queue = deque(start_ids)
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for nxt in adj.get(node, ()):  # downstream of node
            if nxt not in visited:
                queue.append(nxt)
    return visited


def upstream_closure(graph: Graph, start_ids: list[str]) -> set[str]:
    """Return the set of all item IDs reachable by walking upstream (derives_from)
    from any of the start IDs. Includes the start IDs themselves.
    """
    visited: set[str] = set()
    queue = deque(start_ids)
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


def detect_cycles(graph: Graph) -> list[list[str]]:
    """Return a list of cycles (as lists of item IDs) in the graph.

    The derivation graph must be a DAG; any cycle returned by this function is
    a structural eval failure.
    """
    # Build the derives-from graph: item -> [upstream items]
    adj: dict[str, list[str]] = {iid: list(i.derives_from) for iid, i in graph.items.items()}

    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {iid: WHITE for iid in adj}
    stack: list[str] = []
    cycles: list[list[str]] = []

    def dfs(node: str) -> None:
        color[node] = GRAY
        stack.append(node)
        for nxt in adj.get(node, ()):
            if nxt not in color:
                continue  # dangling upstream ref; handled elsewhere
            if color[nxt] == GRAY:
                # Found a back-edge; extract cycle.
                try:
                    idx = stack.index(nxt)
                    cycles.append(stack[idx:] + [nxt])
                except ValueError:
                    pass
            elif color[nxt] == WHITE:
                dfs(nxt)
        stack.pop()
        color[node] = BLACK

    for iid in list(adj.keys()):
        if color[iid] == WHITE:
            dfs(iid)
    return cycles


def dangling_references(graph: Graph) -> list[tuple[str, str]]:
    """Return (item_id, missing_upstream_id) pairs where an item's
    derives_from references an item not present in the graph."""
    out: list[tuple[str, str]] = []
    for item in graph.items.values():
        for up in item.derives_from:
            if up not in graph.items:
                out.append((item.item_id, up))
    return out
