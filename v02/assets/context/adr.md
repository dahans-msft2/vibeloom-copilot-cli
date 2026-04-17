<!--
VibeLoom template: adr (architecture decision record ledger)
Tier: context (full modes only; in vibe, adr is a record of change for system)
Purpose: append-only ledger of technical decisions that were triggered by contract changes but are not themselves contract truth.
Entities: ADR-#### records.
Derivation rules:
- Artifact-level derives_from is always empty ([]).
- Per-record derives_from inside each ADR-#### section is the canonical derivation link. It points at "any changed technical-side entity" that triggered the decision.

Generator guidance:
- Append-only. Never mutate past ADR records.
- Each record captures: recorded_at, derives_from, contract delta, impact, decision, why.
- Records do not participate in the forward derivation chain.
-->

---
artifact_id: adr
artifact_type: adr
tier: context
scope_kind: root
scope_id: root
timestamp: "<ISO-8601 timestamp>"
derives_from: []
---

# Architecture Decision Records

Append-only ledger of technical decisions.

## ADR-0001

<!-- One record per decision. Add new records as additional `## ADR-####` sections in chronological order. -->

- **recorded_at:**
- **derives_from:**

### Decision

<!-- What technical decision was made. -->

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
