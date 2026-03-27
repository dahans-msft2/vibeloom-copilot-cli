---
artifact_id: pdr
artifact_type: pdr
tier: context
scope_kind: root
scope_id: root
derives_from: []
---

# Product Decision Ledger

`pdr` is an append-only ledger of product decisions recorded after they are already reflected in contract.

## `PDR-0001`
- **recorded_at:** `2026-03-25T00:00:00Z`
- **derives_from:** `[FR-0001, Q-0001]`
<!--
Append new records as additional `## PDR-####` sections in chronological order.
Replace the ID, timestamp, and causal item IDs with the actual record values.
-->

### Decision

<What product decision was made>
<!--
Exemplar:
Keep explicit approval mandatory before any invitation grants access.
-->

### Why

<Reason, tradeoff, or trigger>
<!--
Exemplar:
Implicit access made ownership and auditability unclear, especially when invitations were retried or revoked.
-->

### Contract Delta

| changed_item_id | change |
| --- | --- |
<!--
Exemplar rows. Replace with project-specific contract deltas.
| `FR-0002` | Clarified that invite creation alone never grants access. |
| `Q-0001` | Resolved the question of whether approval is optional. |
-->

### Impact

| affected_item_id | expected_effect |
| --- | --- |
<!--
Exemplar rows. Replace with downstream impact for this decision.
| `STORY-0007` | Reconcile the story with the explicit approval rule. |
| `ACC-0003` | Regenerate acceptance framing to reflect the clarified product behavior. |
| `BDD-0004` | Regenerate behavioral scenarios for the approval flow. |
-->
