# Example: brownfield import

A team inherits a six-year-old TypeScript invoicing application — about 50,000 lines, no specs, partial documentation, original authors gone. They want to bring it under VibeLoom governance without rewriting it.

## 1. Import analysis

```text
$ vibeloom init --mode pm
✓ Created stub layout

$ vibeloom import
ℹ Scanning 1,247 files across 8 directories...
ℹ Detected 4 candidate containers, 11 candidate components, 23 candidate bounded contexts.
✓ Wrote draft contract to repo root + per-component drafts.
✓ Import trace IMP-0001 written.
→ Next: vibeloom review intent-specs
```

The engine produces a draft contract with confidence scores per item:

```yaml
id: FR-0027
kind: functional_requirement
description: "User can export invoices as CSV."
confidence: 0.91
evidence:
  - file: billing/routes/export.ts
  - test: billing/tests/export_csv.test.ts
uncertainty: []

id: FR-0042
kind: functional_requirement
description: "User can schedule recurring invoices."
confidence: 0.58
evidence:
  - file: billing/jobs/scheduler.ts
uncertainty:
  - "No tests found for scheduling logic."
  - "Cron expressions use unusual format; intent unclear."

id: BC-0008
kind: bounded_context
description: "Tax calculation"
confidence: 0.34
evidence:
  - file: billing/tax/*.ts
uncertainty:
  - "Three different tax-calculation strategies coexist."
  - "Likely the result of a half-finished migration."
  - "User input needed to choose canonical strategy."
```

## 2. Top-down review

User runs `review intent-specs`. The packet shows the inferred capabilities and constraints. User reads and edits — most are right; a few need rewording or merging.

```text
$ vibeloom approve intent-specs
✓ intent-specs approved.
ℹ Auto-advanced product-specs (no semantic findings).
→ Next: vibeloom review product-specs
```

Product-specs review is heavier. Low-confidence items (`FR-0042`, `BC-0008`) get user attention:

```yaml
packet_type: review
target: product-specs
findings:
  advisory:
    - "FR-0042 (recurring invoices): confidence 0.58. Tests missing.
       Recommend: write a few BDD scenarios before approving, or mark
       as best-effort and revisit."
    - "BC-0008 (tax calculation): confidence 0.34. Three coexisting
       strategies. Recommend: choose canonical strategy as part of
       this approval."
recommendation: address_advisory_then_approve
```

User picks one tax strategy as canonical, marks the other two as obsolete (status `obsolete`), writes scenarios for `FR-0042`, then approves.

## 3. Code reconciliation

After full contract approval, existing code is reconciled against it:

```text
$ vibeloom status
Code reconciliation:
  current:    873 files
  drifted:    14 files
  obsolete:   3 files (deprecated tax strategies)
  uncovered:  2 components (no test coverage; explicit FR but no SYNC trace)
```

User runs `reconcile code` for the 14 drifted files. Half are minor (variable renames the agent flags but doesn't trust); the other half are real conflicts where the code does something the contract didn't capture. For each conflict, the user picks direction (`preserve_contract_regenerate_code` for outdated implementations, `amend_contract_to_preserve_downstream_behavior` for behaviors the team wants to keep).

The 3 obsolete files are deleted with a `decision` trace recording the choice.

## 4. Going forward

The repo is now a governed brownfield project. Future feature work starts from the approved contract. The team didn't rewrite anything; they spent ~4 days on the import + review cycle and now have:

- a clear `dm.md` describing all 23 bounded contexts in unambiguous terms,
- a `prd.md` that names every functional requirement with traceable evidence,
- code-sync traces for every kept file,
- 14 reconciliation traces documenting why specific divergences were preserved.

## What this example illustrates

- **Confidence + evidence makes brownfield tractable.** Without confidence scores, every inferred item would need equal review attention. With them, the team can triage.
- **Obsolete is a real category.** The deprecated tax strategies needed to disappear from the active surface without literally deleting them from the code first.
- **Reconciliation captures decisions.** The 14 reconciliation traces are the answer to "why does this code do this weird thing?" six months from now when the next person asks.
- **Import is a one-time operation.** After it, normal governance takes over.
