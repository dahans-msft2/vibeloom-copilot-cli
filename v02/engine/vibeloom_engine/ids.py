"""Short-ID prefix families and validation.

Implements the ID schema defined in vibeloom-implementation.md ## Stable ID Schema:
- Visible item IDs use uppercase PREFIX-#### with fixed-width 4-digit numbers.
- Globally unique by type across the repo.
- Numbering append-only within each prefix family.
- Deleted IDs never reused.

Also carries methodology-level metadata about each prefix:
- which artifact type typically owns items of this family
- whether the family is a graph entity or structured content
- which tier the family belongs to
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Tier(str, Enum):
    """Methodology tiers."""

    INTENT_SPECS = "intent-specs"
    PRODUCT_SPECS = "product-specs"
    SYSTEM_SPECS = "system-specs"
    CONTEXT = "context"
    CODE = "code"


class ItemKind(str, Enum):
    """Whether an item is a graph entity or structured content within an artifact."""

    GRAPH_ENTITY = "graph-entity"  # Participates in the derivation DAG
    STRUCTURED = "structured"  # Addressable content, not a graph node
    LEDGER_RECORD = "ledger-record"  # PDR/ADR record inside a ledger artifact


@dataclass(frozen=True)
class PrefixSpec:
    """Metadata about a short-ID prefix family."""

    prefix: str
    description: str
    owning_artifact: str  # The artifact where items of this family are defined
    tier: Tier
    kind: ItemKind


# Canonical prefix families per vibeloom-implementation.md ## Stable ID Schema.
# Order matches the implementation doc's table.
PREFIX_FAMILIES: tuple[PrefixSpec, ...] = (
    # intent-specs
    PrefixSpec("CAP", "intent capability", "intent", Tier.INTENT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("CST", "hard constraint in defaults or intent", "intent", Tier.INTENT_SPECS, ItemKind.GRAPH_ENTITY),
    # product-specs: prd
    PrefixSpec("OBJ", "objective", "prd", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("KR", "key result", "prd", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("MET", "metric", "prd", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("FR", "functional requirement", "prd", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("NFR", "non-functional requirement", "prd", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    # product-specs: usm
    PrefixSpec("EPIC", "epic", "usm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("FLOW", "workflow or journey", "usm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("STORY", "story", "usm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("ACC", "acceptance criterion", "usm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("MS", "milestone", "usm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    # product-specs: dm
    PrefixSpec("TERM", "ubiquitous-language term", "dm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("BC", "bounded context", "dm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("AGG", "aggregate", "dm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("ENT", "entity", "dm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("VO", "value object", "dm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("INV", "invariant", "dm", Tier.PRODUCT_SPECS, ItemKind.GRAPH_ENTITY),
    # system-specs: system
    PrefixSpec("EXT", "external actor or system", "system", Tier.SYSTEM_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("TB", "trust boundary", "system", Tier.SYSTEM_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("SNFR", "system-wide NFR boundary", "system", Tier.SYSTEM_SPECS, ItemKind.GRAPH_ENTITY),
    # system-specs: containers / container / component
    PrefixSpec("CONT", "container inventory item", "containers", Tier.SYSTEM_SPECS, ItemKind.GRAPH_ENTITY),
    PrefixSpec("CMP", "component inventory item", "container", Tier.SYSTEM_SPECS, ItemKind.GRAPH_ENTITY),
    # structured content within component specs (Boundary Principle)
    PrefixSpec("IF", "owned interface (body carrier)", "component", Tier.SYSTEM_SPECS, ItemKind.STRUCTURED),
    PrefixSpec("DEP", "component dependency (body carrier)", "component", Tier.SYSTEM_SPECS, ItemKind.STRUCTURED),
    PrefixSpec("BEH", "local technical behavior (body carrier)", "component", Tier.SYSTEM_SPECS, ItemKind.STRUCTURED),
    PrefixSpec("NOTE", "local test/runtime note (body carrier)", "component", Tier.SYSTEM_SPECS, ItemKind.STRUCTURED),
    # context
    PrefixSpec("PDR", "product decision record", "pdr", Tier.CONTEXT, ItemKind.LEDGER_RECORD),
    PrefixSpec("ADR", "architecture decision record", "adr", Tier.CONTEXT, ItemKind.LEDGER_RECORD),
    PrefixSpec("BDD", "behavioral-scenario artifact", "bdd", Tier.CONTEXT, ItemKind.GRAPH_ENTITY),
    PrefixSpec("SCN", "individual Gherkin scenario", "bdd", Tier.CONTEXT, ItemKind.GRAPH_ENTITY),
)

_PREFIX_BY_NAME: dict[str, PrefixSpec] = {p.prefix: p for p in PREFIX_FAMILIES}


# Valid ID shape: PREFIX-####
# Prefix is uppercase letters only. Number is exactly 4 digits, zero-padded.
_ID_RE = re.compile(r"^([A-Z]+)-(\d{4})$")


def valid_prefix(prefix: str) -> bool:
    """Return True if the prefix is a known family."""
    return prefix in _PREFIX_BY_NAME


def parse_id(item_id: str) -> tuple[str, int] | None:
    """Parse a short ID into (prefix, number) or None if malformed.

    Example: parse_id("FR-0001") -> ("FR", 1)
    """
    m = _ID_RE.match(item_id)
    if not m:
        return None
    prefix, num_str = m.groups()
    return prefix, int(num_str)


def format_id(prefix: str, number: int) -> str:
    """Format a short ID from prefix + integer. Zero-pads to 4 digits."""
    if not valid_prefix(prefix):
        raise ValueError(f"Unknown prefix family: {prefix!r}")
    if number < 0 or number > 9999:
        raise ValueError(f"Number out of range [0, 9999]: {number}")
    return f"{prefix}-{number:04d}"


def prefix_spec(prefix: str) -> PrefixSpec | None:
    """Return the PrefixSpec for a family, or None if unknown."""
    return _PREFIX_BY_NAME.get(prefix)


def spec_for_id(item_id: str) -> PrefixSpec | None:
    """Return the PrefixSpec for an item's prefix, or None if malformed/unknown."""
    parsed = parse_id(item_id)
    if not parsed:
        return None
    return _PREFIX_BY_NAME.get(parsed[0])


def is_graph_entity(item_id: str) -> bool:
    """Return True if the item is a graph entity (participates in the derivation DAG)."""
    spec = spec_for_id(item_id)
    return bool(spec and spec.kind == ItemKind.GRAPH_ENTITY)


def validate_id(item_id: str) -> list[str]:
    """Return a list of human-readable validation errors (empty list = OK)."""
    errors: list[str] = []
    parsed = parse_id(item_id)
    if not parsed:
        errors.append(f"malformed ID {item_id!r}: expected PREFIX-#### with 4-digit number")
        return errors
    prefix, _ = parsed
    if not valid_prefix(prefix):
        errors.append(f"unknown prefix family in {item_id!r}: {prefix!r}")
    return errors


# --- Derivation DAG ---------------------------------------------------------

# Typed forward-derivation edges per vibeloom-methodology.md ## Context Graph ###
# Derivation DAG. Keys are downstream prefix; values are allowed upstream prefixes.
# "any" is a placeholder used by PDR/ADR which derive from any changed product-side
# or technical-side entity respectively (handled as meta-rule in eval).
DAG_EDGES: dict[str, tuple[str, ...]] = {
    "CAP": (),  # root
    "CST": (),  # root
    # "default" items are carried as CST entries in defaults.md; they derive from
    # constraint clauses in intent. The parser emits these as CST-#### with a
    # derives_from pointing at intent CST-#### items.
    "OBJ": ("CAP", "CST"),
    "KR": ("OBJ",),
    "MET": ("KR",),
    "FR": ("OBJ", "CAP"),
    "NFR": ("OBJ", "CAP", "CST"),
    "EPIC": ("FR",),
    "FLOW": ("FR",),
    "STORY": ("FR",),
    "ACC": ("FR", "NFR", "STORY"),
    "MS": ("STORY", "EPIC"),
    "TERM": ("CAP", "FR", "STORY"),
    "BC": ("FR", "STORY", "FLOW", "TERM"),
    "AGG": ("STORY", "BC"),
    "ENT": ("STORY", "BC"),
    "VO": ("ACC", "STORY"),
    "INV": ("FR", "ACC", "BC"),
    "EXT": ("FR", "NFR", "CAP"),
    "TB": ("NFR",),
    "SNFR": ("NFR",),
    "CONT": ("BC", "NFR", "SNFR"),
    "CMP": ("AGG", "ENT", "BC", "CONT", "FLOW", "VO"),
    "SCN": ("ACC", "INV", "CMP", "STORY"),
    # PDR and ADR are ledger records; their derivation references are "any changed
    # product-side entity" / "any changed technical-side entity" and are not
    # subject to typed edge validation.
}

# Root entity types — items with no derives_from are only valid if their prefix
# is a root type (per methodology's Core Graph Rules).
ROOT_PREFIXES: frozenset[str] = frozenset({"CAP", "CST"})

# Entity types that are terminal by type — their absence from downstream
# derives_from does not count as a coverage failure (per methodology's Eval
# Anchor coverage rule: "unless it is intentionally terminal").
# These are entities that nothing derives from in the DAG.
TERMINAL_BY_TYPE_PREFIXES: frozenset[str] = frozenset({"MET", "MS", "EXT", "TB", "SNFR", "SCN"})


def allowed_upstream_prefixes(downstream: str) -> tuple[str, ...]:
    """Return the tuple of prefixes a downstream prefix may derive from.

    Empty tuple means the prefix is a root entity type (no upstream allowed).
    Raises KeyError for prefixes not in the DAG (e.g., structured content).
    """
    return DAG_EDGES[downstream]


def valid_edge(downstream: str, upstream: str) -> bool:
    """Return True if downstream:upstream is an allowed typed derivation edge."""
    allowed = DAG_EDGES.get(downstream)
    if allowed is None:
        return False
    return upstream in allowed
