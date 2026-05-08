"""Tests for ids.py — prefix registry, parse/format, edges."""

from vibeloom_engine.ids import (
    DECISION_RECORD_TYPES,
    GRAPH_ENTITY_PREFIXES,
    PREFIX_FAMILIES,
    ROOT_PREFIXES,
    allowed_upstream,
    format_dated_id,
    format_semantic_id,
    is_known_prefix,
    is_root_prefix,
    parse_dated_id,
    parse_semantic_id,
    prefix_spec,
    valid_edge,
    validate_id,
)


def test_root_prefixes_only_cap_and_cst():
    """Per §8.2, only CAP and CST are roots."""
    assert ROOT_PREFIXES == frozenset({"CAP", "CST"})


def test_decision_record_types():
    assert DECISION_RECORD_TYPES == frozenset({"IDR", "PDR", "UDR", "ADR", "general"})


def test_known_prefix_table_includes_v03_additions():
    """Spot-check the v0.3 prefixes added since v02."""
    assert is_known_prefix("DEF")
    assert is_known_prefix("VIEW")
    assert is_known_prefix("INT")
    assert is_known_prefix("UXC")
    assert is_known_prefix("MOCK")
    assert is_known_prefix("APPROVAL")
    assert is_known_prefix("DEC")
    assert is_known_prefix("RUN")


def test_pdr_adr_not_independent_prefixes():
    """v0.3 unifies decisions under DEC; PDR/ADR are record_types."""
    assert not is_known_prefix("PDR")
    assert not is_known_prefix("ADR")


def test_parse_format_semantic_id_roundtrip():
    assert parse_semantic_id("FR-0007") == ("FR", 7)
    assert format_semantic_id("FR", 7) == "FR-0007"


def test_parse_dated_id():
    assert parse_dated_id("APPROVAL-20260508-001") == ("APPROVAL", "20260508", 1)
    assert parse_dated_id("FR-0007") is None


def test_format_dated_id():
    assert format_dated_id("APPROVAL", "20260508", 1) == "APPROVAL-20260508-001"


def test_validate_id_malformed():
    errs = validate_id("foo")
    assert errs and "malformed" in errs[0]


def test_valid_edge_per_5_1():
    """A few canonical derivation rules from §5.1."""
    assert valid_edge("OBJ", "CAP")
    assert valid_edge("KR", "OBJ")
    assert valid_edge("FR", "CAP")
    assert valid_edge("FR", "OBJ")
    assert not valid_edge("FR", "FR")  # cycle would be invalid
    assert not valid_edge("CAP", "FR")  # roots have no upstream


def test_def_derives_from_cap_or_cst():
    """DEF normalizes from CAP/CST per §5.1 notes."""
    assert valid_edge("DEF", "CAP")
    assert valid_edge("DEF", "CST")


def test_bc_domain_layer_only_flag():
    """BC carries the methodology §6.4 invariant flag."""
    spec = prefix_spec("BC")
    assert spec is not None
    assert spec.domain_layer_only is True


def test_graph_entity_prefixes_excludes_structured_carriers():
    """IF/DEP/BEH/NOTE are structured content, not graph nodes."""
    assert "IF" not in GRAPH_ENTITY_PREFIXES
    assert "DEP" not in GRAPH_ENTITY_PREFIXES
    assert "BEH" not in GRAPH_ENTITY_PREFIXES
    assert "NOTE" not in GRAPH_ENTITY_PREFIXES
    assert "FR" in GRAPH_ENTITY_PREFIXES
    assert "BC" in GRAPH_ENTITY_PREFIXES


def test_is_root_prefix():
    assert is_root_prefix("CAP")
    assert is_root_prefix("CST")
    assert not is_root_prefix("FR")


def test_allowed_upstream_unknown_prefix_empty():
    assert allowed_upstream("FOO") == ()


def test_format_semantic_id_rejects_out_of_range():
    import pytest

    with pytest.raises(ValueError):
        format_semantic_id("FR", -1)
    with pytest.raises(ValueError):
        format_semantic_id("FR", 10000)
    with pytest.raises(ValueError):
        format_semantic_id("FOO", 1)


def test_format_dated_id_rejects_bad_inputs():
    import pytest

    with pytest.raises(ValueError):
        format_dated_id("FOO", "20260508", 1)
    with pytest.raises(ValueError):
        format_dated_id("RUN", "2026-05-08", 1)
    with pytest.raises(ValueError):
        format_dated_id("RUN", "20260508", 0)
    with pytest.raises(ValueError):
        format_dated_id("RUN", "20260508", 1000)
