"""Tests for traces.py — round-trip, append, schema-version handling."""

import json
from pathlib import Path

import pytest

from vibeloom_engine.traces import (
    ENGINE_SCHEMA_MAJOR,
    TRACE_FAMILIES,
    TraceSchemaError,
    append_trace,
    iter_trace_records,
    read_all_traces,
    trace_file,
)


def _approval_record():
    return {
        "trace_id": "APPROVAL-20260508-001",
        "timestamp": "2026-05-08T00:00:00Z",
        "run_id": "RUN-20260508-001",
        "approval_unit": "product-specs",
        "approval_mode": "user",
        "items": {"FR-0001": "sha256:abc"},
        "artifacts": {"prd": "sha256:def"},
    }


def _generation_record():
    return {
        "trace_id": "GEN-20260508-001",
        "timestamp": "2026-05-08T00:01:00Z",
        "run_id": "RUN-20260508-001",
        "task_template_id": "generate-product-specs",
        "scope": "root:product-specs",
        "basis_ids": ["CAP-0001"],
        "output_artifact_ids": ["prd"],
        "result_status": "ok",
    }


def _eval_record():
    return {
        "trace_id": "EVAL-20260508-001",
        "timestamp": "2026-05-08T00:02:00Z",
        "target": "product-specs",
        "checks_run": ["structural"],
        "findings": [],
    }


def _decision_record():
    return {
        "trace_id": "DEC-20260508-001",
        "timestamp": "2026-05-08T15:00:00Z",
        "topic": "test",
        "payload": "stuff",
    }


def _import_record():
    return {
        "trace_id": "IMP-20260508-001",
        "timestamp": "2026-05-08T00:00:00Z",
        "evidence_summary": {"files_scanned": 1},
        "candidates_proposed": {"CAP": 1},
    }


def _code_sync_record():
    return {
        "trace_id": "SYNC-20260508-001",
        "timestamp": "2026-05-08T00:00:00Z",
        "scope": "component:web",
        "realizes": ["CMP-0001"],
        "owned_paths": ["web/src/**"],
        "file_hashes": {"web/src/index.ts": "sha256:abc"},
        "validation": {"typecheck": "passed"},
    }


@pytest.mark.parametrize(
    "family,record",
    [
        ("approval", _approval_record()),
        ("generation", _generation_record()),
        ("eval", _eval_record()),
        ("decision", _decision_record()),
        ("import", _import_record()),
        ("code-sync", _code_sync_record()),
    ],
)
def test_round_trip_each_family(fresh_repo: Path, family, record):
    append_trace(fresh_repo, family, record)
    out = read_all_traces(fresh_repo, family)
    assert len(out) == 1
    assert out[0]["trace_id"] == record["trace_id"]
    assert out[0]["schema_version"] == "1.0"
    assert out[0]["kind"] == family


def test_append_preserves_prior(fresh_repo: Path):
    rec1 = _approval_record()
    append_trace(fresh_repo, "approval", rec1)
    rec2 = {**rec1, "trace_id": "APPROVAL-20260508-002"}
    append_trace(fresh_repo, "approval", rec2)
    out = read_all_traces(fresh_repo, "approval")
    assert len(out) == 2


def test_future_major_raises(fresh_repo: Path):
    """schema_version major > engine major should raise per §8.7."""
    rec = _decision_record()
    rec["schema_version"] = f"{ENGINE_SCHEMA_MAJOR + 1}.0"
    rec["kind"] = "decision"
    p = trace_file(fresh_repo, "decision")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    with pytest.raises(TraceSchemaError):
        read_all_traces(fresh_repo, "decision")


def test_kind_mismatch_raises(fresh_repo: Path):
    rec = _decision_record()
    rec["schema_version"] = "1.0"
    rec["kind"] = "approval"  # wrong
    p = trace_file(fresh_repo, "decision")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    with pytest.raises(TraceSchemaError):
        read_all_traces(fresh_repo, "decision")


def test_missing_required_field_raises(fresh_repo: Path):
    rec = _approval_record()
    del rec["approval_unit"]
    rec["schema_version"] = "1.0"
    rec["kind"] = "approval"
    p = trace_file(fresh_repo, "approval")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    with pytest.raises(TraceSchemaError):
        read_all_traces(fresh_repo, "approval")


def test_minor_version_with_unknown_field_OK(fresh_repo: Path):
    """Future minor — additive — should be silently accepted."""
    rec = _approval_record()
    rec["schema_version"] = f"{ENGINE_SCHEMA_MAJOR}.99"
    rec["kind"] = "approval"
    rec["future_field_added_in_1_99"] = "ok"
    p = trace_file(fresh_repo, "approval")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    out = read_all_traces(fresh_repo, "approval")
    assert out[0]["future_field_added_in_1_99"] == "ok"


def test_unknown_family_raises(fresh_repo: Path):
    with pytest.raises(ValueError):
        list(iter_trace_records(fresh_repo, "nope"))


def test_schema_version_must_be_string(fresh_repo: Path):
    rec = _decision_record()
    rec["schema_version"] = 1.0  # not a string
    rec["kind"] = "decision"
    p = trace_file(fresh_repo, "decision")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    with pytest.raises(TraceSchemaError):
        read_all_traces(fresh_repo, "decision")


def test_malformed_json_raises(fresh_repo: Path):
    p = trace_file(fresh_repo, "decision")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{not json\n", encoding="utf-8")
    with pytest.raises(TraceSchemaError):
        read_all_traces(fresh_repo, "decision")


def test_trace_families_inventory():
    assert set(TRACE_FAMILIES.keys()) == {
        "approval", "code-sync", "generation", "eval", "decision", "import"
    }
