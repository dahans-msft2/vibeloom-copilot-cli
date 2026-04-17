"""Core data model for the engine.

Dataclasses for artifacts, items, derivation edges, and the context graph.
Designed to be JSON-serializable for graph-cache persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# Re-export Tier from ids.py so callers can import from models
from vibeloom_engine.ids import Tier  # noqa: F401


class ArtifactType(str, Enum):
    """Every recognized artifact_type in v2."""

    # Contract
    INTENT = "intent"
    DEFAULTS = "defaults"
    PRD = "prd"
    USM = "usm"
    DM = "dm"
    SYSTEM = "system"
    CONTAINERS = "containers"
    CONTAINER = "container"
    COMPONENT = "component"
    # Context
    CONFIG = "config"
    PDR = "pdr"
    ADR = "adr"
    BDD = "bdd"


CONTRACT_TYPES: frozenset[ArtifactType] = frozenset(
    {
        ArtifactType.INTENT,
        ArtifactType.DEFAULTS,
        ArtifactType.PRD,
        ArtifactType.USM,
        ArtifactType.DM,
        ArtifactType.SYSTEM,
        ArtifactType.CONTAINERS,
        ArtifactType.CONTAINER,
        ArtifactType.COMPONENT,
    }
)

CONTEXT_TYPES: frozenset[ArtifactType] = frozenset(
    {
        ArtifactType.CONFIG,
        ArtifactType.PDR,
        ArtifactType.ADR,
        ArtifactType.BDD,
    }
)


class ScopeKind(str, Enum):
    ROOT = "root"
    CONTAINER = "container"
    COMPONENT = "component"


class Status(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"


class ApprovalMode(str, Enum):
    USER = "user"
    DELEGATED = "delegated"


@dataclass
class Scope:
    """An artifact's governance scope."""

    kind: ScopeKind
    scope_id: str  # "root", or a container-slug, or "<container-slug>.<component-slug>"

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind.value, "scope_id": self.scope_id}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Scope":
        return cls(kind=ScopeKind(d["kind"]), scope_id=d["scope_id"])


@dataclass
class Item:
    """An addressable item within an artifact body (e.g., FR-0001).

    Items may be graph entities (participating in derivation) or structured
    content (addressable but not DAG nodes, e.g., IF-####, DEP-####).
    """

    item_id: str  # PREFIX-####
    artifact_id: str  # Owning artifact's artifact_id
    section: str  # e.g., "Functional requirements" (from the H2 header)
    tier: str  # intent-specs | product-specs | system-specs | context
    scope: Scope
    derives_from: list[str] = field(default_factory=list)  # upstream short item IDs
    description: str = ""  # from the "description" column if present
    extra: dict[str, Any] = field(default_factory=dict)  # other columns (notes, priority, etc.)

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "artifact_id": self.artifact_id,
            "section": self.section,
            "tier": self.tier,
            "scope": self.scope.to_dict(),
            "derives_from": list(self.derives_from),
            "description": self.description,
            "extra": dict(self.extra),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Item":
        return cls(
            item_id=d["item_id"],
            artifact_id=d["artifact_id"],
            section=d["section"],
            tier=d["tier"],
            scope=Scope.from_dict(d["scope"]),
            derives_from=list(d.get("derives_from", [])),
            description=d.get("description", ""),
            extra=dict(d.get("extra", {})),
        )


@dataclass
class Artifact:
    """A parsed Markdown artifact with frontmatter and extracted items."""

    artifact_id: str
    artifact_type: ArtifactType
    tier: str  # intent-specs | product-specs | system-specs | context
    scope: Scope
    path: str  # relative to repo root, forward-slash form
    status: Status | None  # contract-only; None for context artifacts
    timestamp: str | None  # ISO 8601 of the last change, as written in frontmatter
    approval_mode: ApprovalMode | None  # set at approval time only
    derives_from: list[str] = field(default_factory=list)  # upstream short item IDs
    items: list[Item] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)  # container_id, component_id, owned_paths, etc.
    mtime: float | None = None  # filesystem mtime (epoch seconds); set by the IO layer

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type.value,
            "tier": self.tier,
            "scope": self.scope.to_dict(),
            "path": self.path,
            "status": self.status.value if self.status else None,
            "timestamp": self.timestamp,
            "approval_mode": self.approval_mode.value if self.approval_mode else None,
            "derives_from": list(self.derives_from),
            "items": [item.to_dict() for item in self.items],
            "extras": dict(self.extras),
            "mtime": self.mtime,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Artifact":
        return cls(
            artifact_id=d["artifact_id"],
            artifact_type=ArtifactType(d["artifact_type"]),
            tier=d["tier"],
            scope=Scope.from_dict(d["scope"]),
            path=d["path"],
            status=Status(d["status"]) if d.get("status") else None,
            timestamp=d.get("timestamp"),
            approval_mode=ApprovalMode(d["approval_mode"]) if d.get("approval_mode") else None,
            derives_from=list(d.get("derives_from", [])),
            items=[Item.from_dict(i) for i in d.get("items", [])],
            extras=dict(d.get("extras", {})),
            mtime=d.get("mtime"),
        )


@dataclass
class Edge:
    """A directed derivation edge in the context graph: source derives from target."""

    source: str  # downstream item_id
    target: str  # upstream item_id

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source, "target": self.target}


@dataclass
class ApprovalSnapshot:
    """Per-artifact approval-time state, used for direct-edit and staleness detection.

    Captured when the engine first sees an artifact with `status: approved` and
    preserved across cache rebuilds until the artifact transitions to `draft`.
    See vibeloom-implementation.md ## Runtime State ### Graph Cache ### Snapshot
    Lifecycle.
    """

    mtime: float  # filesystem mtime of the artifact at approval
    item_hashes: dict[str, str] = field(default_factory=dict)  # item_id -> canonical sha256 hex

    def to_dict(self) -> dict[str, Any]:
        return {"mtime": self.mtime, "item_hashes": dict(self.item_hashes)}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ApprovalSnapshot":
        return cls(mtime=d["mtime"], item_hashes=dict(d.get("item_hashes", {})))


@dataclass
class Graph:
    """The context graph: artifacts, items, and derivation edges."""

    artifacts: dict[str, Artifact] = field(default_factory=dict)  # by artifact_id
    items: dict[str, Item] = field(default_factory=dict)  # by item_id
    edges: list[Edge] = field(default_factory=list)
    # Per-approved-artifact snapshot: mtime + per-item hashes at last approval.
    approved_snapshots: dict[str, ApprovalSnapshot] = field(default_factory=dict)

    # --- queries -----------------------------------------------------------

    def upstream(self, item_id: str) -> list[str]:
        """Return the list of upstream item IDs for a given item."""
        item = self.items.get(item_id)
        return list(item.derives_from) if item else []

    def downstream(self, item_id: str) -> list[str]:
        """Return the list of downstream item IDs for a given item (forward edges)."""
        return [e.source for e in self.edges if e.target == item_id]

    def artifacts_by_tier(self, tier: str) -> list[Artifact]:
        """Return all artifacts belonging to the given tier."""
        return [a for a in self.artifacts.values() if a.tier == tier]

    def items_by_prefix(self, prefix: str) -> list[Item]:
        """Return all items of a given prefix family."""
        return [i for i in self.items.values() if i.item_id.startswith(f"{prefix}-")]

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifacts": {aid: a.to_dict() for aid, a in self.artifacts.items()},
            "items": {iid: i.to_dict() for iid, i in self.items.items()},
            "edges": [e.to_dict() for e in self.edges],
            "approved_snapshots": {aid: s.to_dict() for aid, s in self.approved_snapshots.items()},
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Graph":
        return cls(
            artifacts={aid: Artifact.from_dict(a) for aid, a in d.get("artifacts", {}).items()},
            items={iid: Item.from_dict(i) for iid, i in d.get("items", {}).items()},
            edges=[Edge(source=e["source"], target=e["target"]) for e in d.get("edges", [])],
            approved_snapshots={
                aid: ApprovalSnapshot.from_dict(s)
                for aid, s in d.get("approved_snapshots", {}).items()
            },
        )
