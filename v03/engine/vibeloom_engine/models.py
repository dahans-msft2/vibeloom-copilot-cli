"""Core dataclasses for the engine.

JSON-serializable. Mirrors the §6 frontmatter shapes plus the in-memory
graph used by structural eval, dispatch, and status.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Artifact-level enums
# ---------------------------------------------------------------------------


class ArtifactType(str, Enum):
    """Recognised v0.3 artifact_type values (§6)."""

    INTENT = "intent"
    DEFAULTS = "defaults"
    PRD = "prd"
    USM = "usm"
    DM = "dm"
    UX = "ux"
    SYSTEM = "system"
    CONTAINERS = "containers"
    CONTAINER = "container"
    COMPONENT = "component"
    BDD = "bdd"
    CONFIG = "config"
    VALIDATION_REGISTRY = "validation-registry"


CONTRACT_TYPES: frozenset[ArtifactType] = frozenset(
    {
        ArtifactType.INTENT,
        ArtifactType.DEFAULTS,
        ArtifactType.PRD,
        ArtifactType.USM,
        ArtifactType.DM,
        ArtifactType.UX,
        ArtifactType.SYSTEM,
        ArtifactType.CONTAINERS,
        ArtifactType.CONTAINER,
        ArtifactType.COMPONENT,
    }
)

CONTEXT_TYPES: frozenset[ArtifactType] = frozenset(
    {ArtifactType.CONFIG, ArtifactType.BDD}
)


class Tier(str, Enum):
    INTENT_SPECS = "intent-specs"
    PRODUCT_SPECS = "product-specs"
    UX_SPECS = "ux-specs"
    SYSTEM_SPECS = "system-specs"
    CONTEXT = "context"
    META = "meta"


class ScopeKind(str, Enum):
    ROOT = "root"
    CONTAINER = "container"
    COMPONENT = "component"


class Status(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"


class ApprovalMode(str, Enum):
    """Lives on the approval trace (§8.1), NOT on the artifact (per §6.1)."""

    USER = "user"
    DELEGATED = "delegated"


class ContainerLayer(str, Enum):
    PRESENTATION = "presentation"
    APPLICATION = "application"
    DOMAIN = "domain"
    INFRASTRUCTURE = "infrastructure"


# ---------------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------------


@dataclass
class Scope:
    """An artifact's governance scope."""

    kind: ScopeKind
    scope_id: str

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind.value, "scope_id": self.scope_id}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Scope":
        return cls(kind=ScopeKind(d["kind"]), scope_id=d["scope_id"])


# ---------------------------------------------------------------------------
# Item & Artifact
# ---------------------------------------------------------------------------


@dataclass
class Item:
    """An addressable item (PREFIX-NNNN) within an artifact body."""

    item_id: str
    artifact_id: str
    section: str
    tier: str
    scope: Scope
    derives_from: list[str] = field(default_factory=list)
    description: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

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
    """A parsed Markdown artifact with frontmatter and extracted items.

    `approval_unit` is v0.3-new (§6.1). `approval_mode` is v0.3-removed
    from the artifact (it lives on the trace per §8.1).
    """

    artifact_id: str
    artifact_type: ArtifactType
    tier: str
    scope: Scope
    path: str
    status: Status | None  # contract-only
    timestamp: str | None
    approval_unit: str | None  # contract-only
    derives_from: list[str] = field(default_factory=list)
    items: list[Item] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)
    mtime: float | None = None

    # Container-only field; None if not a container.
    layer: ContainerLayer | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type.value,
            "tier": self.tier,
            "scope": self.scope.to_dict(),
            "path": self.path,
            "status": self.status.value if self.status else None,
            "timestamp": self.timestamp,
            "approval_unit": self.approval_unit,
            "derives_from": list(self.derives_from),
            "items": [item.to_dict() for item in self.items],
            "extras": dict(self.extras),
            "mtime": self.mtime,
            "layer": self.layer.value if self.layer else None,
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
            approval_unit=d.get("approval_unit"),
            derives_from=list(d.get("derives_from", [])),
            items=[Item.from_dict(i) for i in d.get("items", [])],
            extras=dict(d.get("extras", {})),
            mtime=d.get("mtime"),
            layer=ContainerLayer(d["layer"]) if d.get("layer") else None,
        )


@dataclass
class Edge:
    """Forward-derivation edge: source derives_from target."""

    source: str
    target: str

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source, "target": self.target}


@dataclass
class Graph:
    """In-memory contract graph: artifacts, items, edges, plus index helpers."""

    artifacts: dict[str, Artifact] = field(default_factory=dict)
    items: dict[str, Item] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    def upstream(self, item_id: str) -> list[str]:
        item = self.items.get(item_id)
        return list(item.derives_from) if item else []

    def downstream(self, item_id: str) -> list[str]:
        return [e.source for e in self.edges if e.target == item_id]

    def items_by_prefix(self, prefix: str) -> list[Item]:
        marker = f"{prefix}-"
        return [i for i in self.items.values() if i.item_id.startswith(marker)]

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifacts": {aid: a.to_dict() for aid, a in self.artifacts.items()},
            "items": {iid: i.to_dict() for iid, i in self.items.items()},
            "edges": [e.to_dict() for e in self.edges],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Graph":
        return cls(
            artifacts={aid: Artifact.from_dict(a) for aid, a in d.get("artifacts", {}).items()},
            items={iid: Item.from_dict(i) for iid, i in d.get("items", {}).items()},
            edges=[Edge(source=e["source"], target=e["target"]) for e in d.get("edges", [])],
        )


# ---------------------------------------------------------------------------
# Findings (used by eval)
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    severity: str  # "blocking" | "advisory"
    artifact_id: str
    check: str
    message: str
    item_id: str | None = None
    finding_id: str | None = None  # FIND-####, assigned by eval

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "artifact_id": self.artifact_id,
            "check": self.check,
            "message": self.message,
            "item_id": self.item_id,
            "finding_id": self.finding_id,
        }


__all__ = [
    "ArtifactType",
    "CONTRACT_TYPES",
    "CONTEXT_TYPES",
    "Tier",
    "ScopeKind",
    "Status",
    "ApprovalMode",
    "ContainerLayer",
    "Scope",
    "Item",
    "Artifact",
    "Edge",
    "Graph",
    "Finding",
]
