# Modes Reference

Four modes control user ownership, delegation, and contract-stack depth. Authoritative semantics live in [`vibeloom-methodology.md ## Modes`](../vibeloom-methodology.md) and [`## Generation ### Approval And Auto-Advance`](../vibeloom-methodology.md). This file is a load-on-demand condensation.

A mode controls three things:

- which contract tiers the user explicitly co-authors and approves
- which contract tiers are delegated to the agent for auto-advance
- whether the contract stack is full or compact

An approval unit is one contract tier.

---

## Full modes

`pm`, `dev`, and `expert` all maintain the full contract stack: `intent-specs` → `product-specs` → `system-specs` → `context` → `code`. They differ only in validation and approval rules.

### `expert`

- **User owns:** all three contract tiers (`intent-specs`, `product-specs`, `system-specs`).
- **Delegated:** none.
- **Public surface:** `generate`, `review`, `eval`, `reconcile`, `approve`, `status`, `help`, each accepting any target tier.
- **Normal stops:** every contract tier pauses for explicit user review and approval.

### `pm`

- **User owns:** `intent-specs`, `product-specs`.
- **Delegated:** `system-specs` auto-advances when safe.
- **Public surface:** same as `expert`.
- **Normal stops:** after `product-specs` generation; `system-specs` auto-advances unless blocking eval findings or a breaking semantic change is detected.

### `dev`

- **User owns:** `intent-specs`, `system-specs`.
- **Delegated:** `product-specs` auto-advances when safe.
- **Public surface:** same as `expert`.
- **Normal stops:** after `system-specs` generation; `product-specs` auto-advances between intent approval and system generation.

---

## Compact mode

### `vibe`

Simplified ceremony for small or early-stage projects. Contract stack collapses to `intent` + `defaults` + flat `system`.

- **Artifacts exist:** `intent` (with product summary section), `defaults`, `system` (flat), root `config`, `source`, `tests`, `runtime`.
- **Artifacts absent:** `prd`, `usm`, `dm`, `containers`, per-container `container`, per-component `component`, `pdr`, `adr`, `bdd`, container/component-scoped config.
- **Tier order:** `intent-specs` → `system-specs` → `context` (root config only) → `code`.
- **User owns:** `intent-specs` only.
- **Delegated:** `system-specs` auto-advances when structural blockers clear.
- **Public surface:**
  - `approve intent-specs`
  - `generate code`
  - `reconcile code`
  - `review intent-specs`, `eval intent-specs`
  - `review context`, `eval context`
  - `review code`, `eval code`
  - `status`, `help`
- **Normal stops:** only `intent-specs` is a public user stop. Compact `system-specs` never becomes a public approval stop.
- **System-specs handling:** the engine may target `system-specs` internally, but it is not publicly reviewable.

---

## Delegated auto-advance

In `pm` and `dev`, a delegated approval unit auto-advances only when all three conditions hold:

1. Structural eval passes (all blocking checks clear).
2. No breaking semantic change is detected against approved truth.
3. No flagged issue requires human judgment.

If any condition fails, the delegated tier escalates to explicit user review and approval before the run can complete. See [`runtime.md`](runtime.md) for the validation rules and [`../vibeloom-methodology.md ## Generation ### Breaking-Change Detection`](../vibeloom-methodology.md) for the breaking-change classification table.

In `vibe`, compact `system-specs` uses the same safety tests. Structural blockers halt downstream generation and surface through the intent-centric UX. Non-blocking advisory findings may allow best-effort continuation with findings surfaced and upgrade recommended when appropriate.

---

## Mode × command matrix (normal flow)

| Step | `vibe` | `pm` | `dev` | `expert` |
|---|---|---|---|---|
| Bootstrap | `init --mode vibe` | `init --mode pm` | `init --mode dev` | `init --mode expert` |
| Shape intent | `review intent-specs` | `review intent-specs` | `review intent-specs` | `review intent-specs` |
| Approve intent | `approve intent-specs` | `approve intent-specs` | `approve intent-specs` | `approve intent-specs` |
| Forward to product | — | `generate product-specs` | (automatic) | `generate product-specs` |
| Approve product | — | `approve product-specs` | (auto or escalated) | `approve product-specs` |
| Forward to system | (automatic) | (automatic) | `generate system-specs` | `generate system-specs` |
| Approve system | (automatic) | (auto or escalated) | `approve system-specs` | `approve system-specs` |
| Forward to code | `generate code` | `generate code` | `generate code` | `generate code` |

`(automatic)` = handled by the forward `generate` command via smart orchestration.
`(auto or escalated)` = normally delegated, but escalates if breaking change detected.
`—` = tier does not exist in this mode.

---

## Next-command suggestions

After every stop, the skill suggests the next forward command:

| After | `vibe` | `pm` | `dev` | `expert` |
|---|---|---|---|---|
| approve intent-specs | `generate code` | `generate product-specs` | `generate system-specs` | `generate product-specs` |
| approve product-specs | — | `generate code` | — | `generate system-specs` |
| approve system-specs | — | — | `generate code` | `generate code` |
| explicit `generate context` | — | `generate code` | `generate code` | `generate code` |

---

## Upgrade

`init --upgrade --mode <pm|dev|expert>` promotes a `vibe` repo to a full mode. One-way — no downgrade back to `vibe`. See [`../vibeloom-methodology.md ## Vibe-to-Full Upgrade`](../vibeloom-methodology.md).
