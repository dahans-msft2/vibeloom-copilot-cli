<!--
VibeLoom template: pdr (product decision record ledger)
Tier: context (full modes only; in vibe, pdr is a record of change for intent)
Purpose: append-only ledger of product-level decisions that were triggered by contract changes but are not themselves contract truth.
Entities: PDR-#### records.
Derivation rules:
- Artifact-level derives_from is always empty ([]).
- Per-record derives_from inside each PDR-#### section is the canonical derivation link. It points at "any changed product-side entity" that triggered the decision.

Generator guidance:
- Append-only. Never mutate past PDR records.
- Each record captures: recorded_at, derives_from (item IDs that triggered it), contract delta, impact, decision, why.
- Records do not participate in the forward derivation chain — they are a history, not a source of truth.
-->

---
artifact_id: pdr
artifact_type: pdr
tier: context
scope_kind: root
scope_id: root
timestamp: "<ISO-8601 timestamp>"
derives_from: []
---

# Product Decision Records

Append-only ledger of product decisions.

## PDR-0001

<!-- One record per decision. Add new records as additional `## PDR-####` sections in chronological order. -->

- **recorded_at:**
- **derives_from:**

### Decision

<!-- What product decision was made. -->

### Why

<!-- Rationale, trigger, or tradeoff. -->

### Contract delta

<!-- Which contract items changed as a result of this decision. -->

| changed_item_id | change |
|---|---|
| | |

### Impact

<!-- Downstream items expected to be affected. -->

| affected_item_id | expected_effect |
|---|---|
| | |
