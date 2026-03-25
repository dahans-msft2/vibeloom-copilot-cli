---
artifact_id: adr
artifact_type: adr
tier: context
scope_kind: root
scope_id: root
---

# Architecture Decision Ledger

`adr` is an append-only ledger of technical decisions recorded after they are already reflected in contract.

## `ADR-0001`
- **recorded_at:** `2026-03-25T00:00:00Z`
- **derives_from:** `[CMP-0001, NFR-0001]`
<!--
Append new records as additional `## ADR-####` sections in chronological order.
Replace the ID, timestamp, and causal item IDs with the actual record values.
-->

### Decision

<What technical decision was made>
<!--
Exemplar:
Isolate invitation lifecycle behavior into its own component rather than letting it spread across shared helpers.
-->

### Why

<Reason, tradeoff, or trigger>
<!--
Exemplar:
This keeps approval semantics, invariants, and executable verification inside one owned boundary instead of distributing them across unrelated code.
-->

### Contract Delta

| changed_item_id | change |
| --- | --- |
<!--
Exemplar rows. Replace with project-specific contract deltas.
| `CMP-0001` | Declared a dedicated invitation lifecycle component. |
| `NFR-0001` | Tightened the auditability and durability expectations for state transitions. |
-->

### Impact

| affected_item_id | expected_effect |
| --- | --- |
<!--
Exemplar rows. Replace with downstream impact for this decision.
| `DEP-0001` | Reconcile component dependencies with the new ownership boundary. |
| `BEH-0002` | Regenerate local behavior contracts to match the isolated component. |
| `NOTE-0001` | Re-align verification notes and tests around the new technical boundary. |
-->
