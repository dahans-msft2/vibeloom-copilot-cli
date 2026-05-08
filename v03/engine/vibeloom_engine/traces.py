"""Trace I/O for the six trace families + schema-version handling (§8).

Trace families:
  approval, code-sync, generation, eval, decision, import.

Each family has its own JSONL file under `.vibeloom/traces/`. JSONL is
**append-only** — there is no in-place rewrite path. Records are validated
on read against `schema_version` per §8.7.

`id-registry.json` is the structured exception (it is mutated, not
appended); it lives in `registry.py`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from vibeloom_engine.io_ import ensure_dir, traces_dir


# Engine-known schema major. Future-major traces raise on read.
ENGINE_SCHEMA_MAJOR = 1


# Family → filename map. The trace-id prefix mirrors the filename root.
TRACE_FAMILIES: dict[str, str] = {
    "approval": "approvals.jsonl",
    "code-sync": "code-sync.jsonl",
    "generation": "generations.jsonl",
    "eval": "evals.jsonl",
    "decision": "decisions.jsonl",
    "import": "imports.jsonl",
}

# Allowed `kind` values per family — used to reject kind mismatches on read.
KIND_FOR_FAMILY: dict[str, str] = {
    "approval": "approval",
    "code-sync": "code-sync",
    "generation": "generation",
    "eval": "eval",
    "decision": "decision",
    "import": "import",
}

# Required fields per family beyond the universal {schema_version, trace_id, kind, timestamp}.
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "approval": ("approval_unit", "approval_mode", "items", "artifacts"),
    "code-sync": ("scope", "realizes", "owned_paths", "file_hashes", "validation"),
    "generation": ("task_template_id", "scope", "basis_ids", "output_artifact_ids"),
    "eval": ("target", "checks_run", "findings"),
    "decision": ("topic", "payload"),
    "import": ("evidence_summary", "candidates_proposed"),
}


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class TraceSchemaError(RuntimeError):
    """Raised when a trace record is malformed or schema-incompatible."""


# ---------------------------------------------------------------------------
# schema_version handling per §8.7
# ---------------------------------------------------------------------------


def _parse_schema_version(raw: Any) -> tuple[int, int]:
    """Parse a schema_version string → (major, minor)."""
    if not isinstance(raw, str):
        raise TraceSchemaError(f"schema_version must be a string; got {type(raw).__name__}")
    parts = raw.split(".")
    if len(parts) < 2:
        raise TraceSchemaError(f"schema_version must be 'major.minor'; got {raw!r}")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError as e:
        raise TraceSchemaError(f"schema_version not numeric: {raw!r}") from e


def _validate_record(family: str, rec: dict[str, Any]) -> None:
    """Validate a single trace record. Raises TraceSchemaError on rejection."""
    expected_kind = KIND_FOR_FAMILY[family]
    for field_name in ("schema_version", "trace_id", "kind", "timestamp"):
        if field_name not in rec:
            raise TraceSchemaError(
                f"trace family {family!r}: missing required field {field_name!r}"
            )
    if rec["kind"] != expected_kind:
        raise TraceSchemaError(
            f"trace family {family!r}: kind mismatch — expected {expected_kind!r}, got {rec['kind']!r}"
        )
    major, _ = _parse_schema_version(rec["schema_version"])
    if major > ENGINE_SCHEMA_MAJOR:
        raise TraceSchemaError(
            f"trace family {family!r}: schema_version {rec['schema_version']} has major "
            f"{major} > engine major {ENGINE_SCHEMA_MAJOR} — engine cannot parse"
        )
    # Required-field presence on read for current major (additive minor changes are OK).
    if major == ENGINE_SCHEMA_MAJOR:
        for needed in REQUIRED_FIELDS.get(family, ()):
            if needed not in rec:
                raise TraceSchemaError(
                    f"trace family {family!r} v{rec['schema_version']}: missing required field {needed!r}"
                )


# ---------------------------------------------------------------------------
# Read / write
# ---------------------------------------------------------------------------


def trace_file(repo_root: Path, family: str) -> Path:
    if family not in TRACE_FAMILIES:
        raise ValueError(f"unknown trace family: {family!r}")
    return traces_dir(repo_root) / TRACE_FAMILIES[family]


def append_trace(repo_root: Path, family: str, record: dict[str, Any]) -> Path:
    """Append a record to the family's JSONL file. Validates on write too."""
    if family not in TRACE_FAMILIES:
        raise ValueError(f"unknown trace family: {family!r}")
    # Auto-fill schema_version if missing (engine-current).
    record = dict(record)
    record.setdefault("schema_version", f"{ENGINE_SCHEMA_MAJOR}.0")
    record.setdefault("kind", KIND_FOR_FAMILY[family])
    _validate_record(family, record)

    ensure_dir(traces_dir(repo_root))
    p = trace_file(repo_root, family)
    line = json.dumps(record, separators=(",", ":"), sort_keys=True)
    # Append atomically (open in append mode, single write).
    with p.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return p


def iter_trace_records(repo_root: Path, family: str) -> Iterator[dict[str, Any]]:
    """Iterate all records in a family's JSONL file. Validates on read."""
    p = trace_file(repo_root, family)
    if not p.is_file():
        return iter(())

    def _gen() -> Iterator[dict[str, Any]]:
        with p.open("r", encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, start=1):
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError as e:
                    raise TraceSchemaError(
                        f"trace file {p} line {lineno}: malformed JSON: {e}"
                    ) from e
                _validate_record(family, rec)
                yield rec

    return _gen()


def read_all_traces(repo_root: Path, family: str) -> list[dict[str, Any]]:
    return list(iter_trace_records(repo_root, family))


# ---------------------------------------------------------------------------
# trace_id allocation (date-keyed sequence within a family)
# ---------------------------------------------------------------------------


@dataclass
class TraceIdAllocator:
    """Allocates dated trace IDs `<KIND>-YYYYMMDD-NNN`.

    Persists nothing on its own — the caller (registry.py) maintains
    `{kind: {date: next_seq}}` in `id-registry.json`. This class is a
    convenience around the format.
    """

    counters: dict[str, dict[str, int]] = field(default_factory=dict)

    def next_id(self, kind: str, today: str | None = None) -> str:
        if today is None:
            today = datetime.now(timezone.utc).strftime("%Y%m%d")
        kind_counters = self.counters.setdefault(kind, {})
        seq = kind_counters.get(today, 0) + 1
        kind_counters[today] = seq
        return f"{kind}-{today}-{seq:03d}"


__all__ = [
    "ENGINE_SCHEMA_MAJOR",
    "TRACE_FAMILIES",
    "KIND_FOR_FAMILY",
    "REQUIRED_FIELDS",
    "TraceSchemaError",
    "trace_file",
    "append_trace",
    "iter_trace_records",
    "read_all_traces",
    "TraceIdAllocator",
]
