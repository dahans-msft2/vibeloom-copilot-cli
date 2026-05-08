"""Stable IDs and prefix registry per implementation §5.

Two ID forms:
- Semantic items: `PREFIX-NNNN` (zero-padded 4-digit, append-only,
  registry-tracked, retired IDs never reused).
- Trace and runtime IDs: `<KIND>-<YYYYMMDD>-<NNN>` (per §5.3, append-only
  per (kind, date)).

The 6-column canonical prefix table from §5.1 is encoded as `PREFIX_FAMILIES`.
Every prefix the engine recognises lives there; lookups elsewhere route
through this module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


# ---------------------------------------------------------------------------
# Enum-like categorisations used widely
# ---------------------------------------------------------------------------


class Tier(str, Enum):
    """Methodology contract tiers + context + runtime + trace + meta."""

    INTENT_SPECS = "intent-specs"
    PRODUCT_SPECS = "product-specs"
    UX_SPECS = "ux-specs"
    SYSTEM_SPECS = "system-specs"
    CONTEXT = "context"
    RUNTIME = "runtime"
    TRACE = "trace"
    META = "meta"


class IdKind(str, Enum):
    """Whether the prefix participates in the contract graph or is auxiliary."""

    GRAPH_ENTITY = "graph-entity"  # contract graph node
    STRUCTURED = "structured"  # body carrier within a contract artifact
    TRACE = "trace"  # trace family (dated form)
    RUNTIME = "runtime"  # runtime family (dated form)


@dataclass(frozen=True)
class PrefixSpec:
    """Canonical row from the §5.1 ID prefix registry table.

    Six columns: prefix, name, tier, source artifact, scope, notes —
    plus internal flags the engine derives (kind, root, allowed_upstream,
    layered_constraints).
    """

    prefix: str
    name: str
    tier: Tier
    source_artifact: str
    scope: str
    kind: IdKind = IdKind.GRAPH_ENTITY
    is_root: bool = False
    allowed_upstream: tuple[str, ...] = ()
    domain_layer_only: bool = False  # for BC


# Canonical prefix registry — implementation §5.1.
# Order mirrors the spec table.
PREFIX_FAMILIES: tuple[PrefixSpec, ...] = (
    # intent-specs --------------------------------------------------------
    PrefixSpec(
        "CAP", "capability", Tier.INTENT_SPECS, "intent.md", "root",
        kind=IdKind.GRAPH_ENTITY, is_root=True, allowed_upstream=(),
    ),
    PrefixSpec(
        "CST", "hard constraint", Tier.INTENT_SPECS, "intent.md or defaults.md", "root",
        kind=IdKind.GRAPH_ENTITY, is_root=True, allowed_upstream=(),
    ),
    PrefixSpec(
        "DEF", "repo-wide default", Tier.INTENT_SPECS, "defaults.md", "root",
        # Derives from CAP/CST per §5.1 notes.
        kind=IdKind.GRAPH_ENTITY, allowed_upstream=("CAP", "CST"),
    ),
    # product-specs --------------------------------------------------------
    PrefixSpec(
        "OBJ", "objective", Tier.PRODUCT_SPECS, "prd.md", "root",
        allowed_upstream=("CAP",),
    ),
    PrefixSpec(
        "KR", "key result", Tier.PRODUCT_SPECS, "prd.md", "root",
        allowed_upstream=("OBJ",),
    ),
    PrefixSpec(
        "MET", "metric", Tier.PRODUCT_SPECS, "prd.md", "root",
        allowed_upstream=("KR", "FR", "NFR"),
    ),
    PrefixSpec(
        "FR", "functional requirement", Tier.PRODUCT_SPECS, "prd.md", "root",
        allowed_upstream=("CAP", "OBJ", "STORY"),
    ),
    PrefixSpec(
        "NFR", "non-functional requirement", Tier.PRODUCT_SPECS, "prd.md", "root",
        allowed_upstream=("CST", "OBJ"),
    ),
    PrefixSpec(
        "EPIC", "epic", Tier.PRODUCT_SPECS, "usm.md", "root",
        allowed_upstream=("CAP", "OBJ"),
    ),
    PrefixSpec(
        "FLOW", "workflow / journey", Tier.PRODUCT_SPECS, "usm.md", "root",
        allowed_upstream=("EPIC",),
    ),
    PrefixSpec(
        "STORY", "story", Tier.PRODUCT_SPECS, "usm.md", "root",
        allowed_upstream=("EPIC", "FLOW"),
    ),
    PrefixSpec(
        "ACC", "acceptance criterion", Tier.PRODUCT_SPECS, "usm.md", "per-STORY",
        allowed_upstream=("STORY",),
    ),
    PrefixSpec(
        "MS", "milestone", Tier.PRODUCT_SPECS, "usm.md", "root",
        allowed_upstream=("STORY", "OBJ"),
    ),
    PrefixSpec(
        "TERM", "ubiquitous-language term", Tier.PRODUCT_SPECS, "dm.md", "root",
        allowed_upstream=("CAP", "STORY"),
    ),
    PrefixSpec(
        "BC", "bounded context", Tier.PRODUCT_SPECS, "dm.md", "root",
        allowed_upstream=("CAP", "STORY"),
        domain_layer_only=True,
    ),
    PrefixSpec(
        "AGG", "aggregate", Tier.PRODUCT_SPECS, "dm.md", "per-BC",
        allowed_upstream=("BC",),
    ),
    PrefixSpec(
        "ENT", "entity", Tier.PRODUCT_SPECS, "dm.md", "per-AGG",
        allowed_upstream=("AGG",),
    ),
    PrefixSpec(
        "VO", "value object", Tier.PRODUCT_SPECS, "dm.md", "per-AGG",
        allowed_upstream=("AGG",),
    ),
    PrefixSpec(
        "INV", "invariant", Tier.PRODUCT_SPECS, "dm.md", "per-AGG",
        allowed_upstream=("AGG",),
    ),
    # ux-specs ------------------------------------------------------------
    PrefixSpec(
        "VIEW", "UX view", Tier.UX_SPECS, "ux.md", "root",
        allowed_upstream=("CAP", "STORY", "FLOW"),
    ),
    PrefixSpec(
        "INT", "UX interaction", Tier.UX_SPECS, "ux.md", "per-VIEW",
        allowed_upstream=("VIEW", "STORY", "ACC"),
    ),
    PrefixSpec(
        "UXC", "UX constraint", Tier.UX_SPECS, "ux.md", "root",
        allowed_upstream=("CST", "DEF"),
    ),
    PrefixSpec(
        "MOCK", "mockup reference", Tier.UX_SPECS, "ux.md", "root",
        allowed_upstream=("CAP", "CST"),
    ),
    # system-specs --------------------------------------------------------
    PrefixSpec(
        "EXT", "external actor / system", Tier.SYSTEM_SPECS, "system.md", "root",
        allowed_upstream=("CAP", "FR"),
    ),
    PrefixSpec(
        "TB", "trust boundary", Tier.SYSTEM_SPECS, "system.md", "root",
        allowed_upstream=("CST", "SNFR", "NFR"),
    ),
    PrefixSpec(
        "SNFR", "system-wide NFR boundary", Tier.SYSTEM_SPECS, "system.md", "root",
        allowed_upstream=("NFR", "CST"),
    ),
    PrefixSpec(
        "CONT", "container", Tier.SYSTEM_SPECS, "containers.md / container.md", "root",
        allowed_upstream=("FR", "STORY", "CAP"),
    ),
    PrefixSpec(
        "CMP", "component", Tier.SYSTEM_SPECS, "container.md / component.md", "per-CONT",
        allowed_upstream=("CONT",),
    ),
    # body-carriers within component.md (NOT graph nodes) -----------------
    PrefixSpec(
        "IF", "owned interface", Tier.SYSTEM_SPECS, "component.md", "per-CMP",
        kind=IdKind.STRUCTURED,
    ),
    PrefixSpec(
        "DEP", "component dependency", Tier.SYSTEM_SPECS, "component.md", "per-CMP",
        kind=IdKind.STRUCTURED,
    ),
    PrefixSpec(
        "BEH", "local technical behavior", Tier.SYSTEM_SPECS, "component.md", "per-CMP",
        kind=IdKind.STRUCTURED,
    ),
    PrefixSpec(
        "NOTE", "local test/runtime note", Tier.SYSTEM_SPECS, "component.md", "per-CMP",
        kind=IdKind.STRUCTURED,
    ),
    # context -------------------------------------------------------------
    PrefixSpec(
        "BDD", "behavioral-scenario artifact", Tier.CONTEXT, "bdd.md", "per-CMP",
        allowed_upstream=("CMP", "ACC", "STORY", "INV"),
    ),
    PrefixSpec(
        "SCN", "Gherkin scenario", Tier.CONTEXT, "bdd.md body", "per-BDD",
        allowed_upstream=("BDD", "ACC", "STORY"),
    ),
    # runtime (dated) -----------------------------------------------------
    PrefixSpec("RUN", "run", Tier.RUNTIME, ".vibeloom/runs/", "per-invocation", kind=IdKind.RUNTIME),
    PrefixSpec("TASK", "subagent task", Tier.RUNTIME, ".vibeloom/runs/", "per-task", kind=IdKind.RUNTIME),
    PrefixSpec("PLAN", "dispatch plan", Tier.RUNTIME, ".vibeloom/runs/", "per-RUN", kind=IdKind.RUNTIME),
    # traces (dated) ------------------------------------------------------
    PrefixSpec("APPROVAL", "approval trace", Tier.TRACE, ".vibeloom/traces/approvals.jsonl", "append-only", kind=IdKind.TRACE),
    PrefixSpec("SYNC", "code-sync trace", Tier.TRACE, ".vibeloom/traces/code-sync.jsonl", "append-only", kind=IdKind.TRACE),
    PrefixSpec("GEN", "generation trace", Tier.TRACE, ".vibeloom/traces/generations.jsonl", "append-only", kind=IdKind.TRACE),
    PrefixSpec("EVAL", "eval trace", Tier.TRACE, ".vibeloom/traces/evals.jsonl", "append-only", kind=IdKind.TRACE),
    PrefixSpec("DEC", "decision trace", Tier.TRACE, ".vibeloom/traces/decisions.jsonl", "append-only", kind=IdKind.TRACE),
    PrefixSpec("IMP", "import trace", Tier.TRACE, ".vibeloom/traces/imports.jsonl", "append-only", kind=IdKind.TRACE),
    # operation packets (dated) -------------------------------------------
    PrefixSpec("REVIEW", "review packet", Tier.RUNTIME, "engine-emitted", "per-op", kind=IdKind.RUNTIME),
    PrefixSpec("RECON", "reconciliation packet", Tier.RUNTIME, "engine-emitted", "per-op", kind=IdKind.RUNTIME),
)


_PREFIX_BY_NAME: dict[str, PrefixSpec] = {p.prefix: p for p in PREFIX_FAMILIES}


# Roots — only CAP and CST per §8.2.
ROOT_PREFIXES: frozenset[str] = frozenset({"CAP", "CST"})


# Decision record_type enum (per §8.5).
DECISION_RECORD_TYPES: frozenset[str] = frozenset({"IDR", "PDR", "UDR", "ADR", "general"})


# Container layer enum (per §6.3 / methodology §6.5).
CONTAINER_LAYERS: tuple[str, ...] = ("presentation", "application", "domain", "infrastructure")


# ---------------------------------------------------------------------------
# Semantic-item ID parsing/formatting (PREFIX-NNNN)
# ---------------------------------------------------------------------------


_SEMANTIC_ID_RE = re.compile(r"^([A-Z]+)-(\d{4})$")
_DATED_ID_RE = re.compile(r"^([A-Z]+)-(\d{8})-(\d{3})$")


def parse_semantic_id(item_id: str) -> tuple[str, int] | None:
    """Parse a semantic ID `PREFIX-NNNN` → (prefix, number); else None."""
    m = _SEMANTIC_ID_RE.match(item_id)
    if not m:
        return None
    return m.group(1), int(m.group(2))


def parse_dated_id(item_id: str) -> tuple[str, str, int] | None:
    """Parse a dated ID `PREFIX-YYYYMMDD-NNN` → (prefix, date, seq); else None."""
    m = _DATED_ID_RE.match(item_id)
    if not m:
        return None
    return m.group(1), m.group(2), int(m.group(3))


def format_semantic_id(prefix: str, number: int) -> str:
    """Format `PREFIX-NNNN` (zero-padded 4 digits)."""
    if not is_known_prefix(prefix):
        raise ValueError(f"unknown prefix family: {prefix!r}")
    if number < 0 or number > 9999:
        raise ValueError(f"semantic ID number out of range [0, 9999]: {number}")
    return f"{prefix}-{number:04d}"


def format_dated_id(prefix: str, date: str, seq: int) -> str:
    """Format `PREFIX-YYYYMMDD-NNN`."""
    if not is_known_prefix(prefix):
        raise ValueError(f"unknown prefix family: {prefix!r}")
    if not re.match(r"^\d{8}$", date):
        raise ValueError(f"date must be YYYYMMDD: {date!r}")
    if seq < 1 or seq > 999:
        raise ValueError(f"dated seq out of range [1, 999]: {seq}")
    return f"{prefix}-{date}-{seq:03d}"


# ---------------------------------------------------------------------------
# Lookups & validations
# ---------------------------------------------------------------------------


def is_known_prefix(prefix: str) -> bool:
    return prefix in _PREFIX_BY_NAME


def prefix_spec(prefix: str) -> PrefixSpec | None:
    return _PREFIX_BY_NAME.get(prefix)


def spec_for_id(item_id: str) -> PrefixSpec | None:
    parsed = parse_semantic_id(item_id) or (
        (parse_dated_id(item_id)[0:1] + (None,)) if parse_dated_id(item_id) else None
    )
    if parsed is None:
        return None
    return _PREFIX_BY_NAME.get(parsed[0])


def is_graph_entity(item_id: str) -> bool:
    spec = spec_for_id(item_id)
    return bool(spec and spec.kind == IdKind.GRAPH_ENTITY)


def is_root_prefix(prefix: str) -> bool:
    return prefix in ROOT_PREFIXES


def allowed_upstream(prefix: str) -> tuple[str, ...]:
    spec = _PREFIX_BY_NAME.get(prefix)
    if spec is None:
        return ()
    return spec.allowed_upstream


def valid_edge(downstream_prefix: str, upstream_prefix: str) -> bool:
    """Return True iff downstream_prefix may derive from upstream_prefix."""
    return upstream_prefix in allowed_upstream(downstream_prefix)


def validate_id(item_id: str) -> list[str]:
    """Return a list of human-readable validation errors. Empty = OK."""
    errors: list[str] = []
    sem = parse_semantic_id(item_id)
    dated = parse_dated_id(item_id)
    if sem is None and dated is None:
        errors.append(
            f"malformed ID {item_id!r}: expected PREFIX-NNNN or PREFIX-YYYYMMDD-NNN"
        )
        return errors
    prefix = (sem or dated)[0]
    if not is_known_prefix(prefix):
        errors.append(f"unknown prefix family in {item_id!r}: {prefix!r}")
    return errors


# Convenience: contract-tier prefixes (graph entities only — exclude
# structured carriers and dated families). Used by structural eval.
GRAPH_ENTITY_PREFIXES: frozenset[str] = frozenset(
    p.prefix for p in PREFIX_FAMILIES if p.kind == IdKind.GRAPH_ENTITY
)


__all__ = [
    "Tier",
    "IdKind",
    "PrefixSpec",
    "PREFIX_FAMILIES",
    "ROOT_PREFIXES",
    "DECISION_RECORD_TYPES",
    "CONTAINER_LAYERS",
    "GRAPH_ENTITY_PREFIXES",
    "parse_semantic_id",
    "parse_dated_id",
    "format_semantic_id",
    "format_dated_id",
    "is_known_prefix",
    "prefix_spec",
    "spec_for_id",
    "is_graph_entity",
    "is_root_prefix",
    "allowed_upstream",
    "valid_edge",
    "validate_id",
]
