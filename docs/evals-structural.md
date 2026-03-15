# Structural Checks

These checks are blocking. A canonical artifact cannot be approved while a structural check fails.

## Report Format

When these checks are surfaced through runtime commands such as `eval` or `approve`, use the mandatory 4-section response contract from `references/interaction-contract.md`:

1. `Scope`
2. `Decision / Findings`
3. `Affected IDs`
4. `Next action`

Within `Decision / Findings`, summarize each relevant structural finding with:
- `Check`: `EVAL-STRUCT-*` and check name
- `Result`: `PASS` or `FAIL`
- `Evidence`: what was inspected
- `Details`: specific failures or blocking concerns

This document defines the check criteria. It does not define an alternate top-level runtime response shape.

When useful, include a matrix such as:

```text
| Item | Expected | Actual | Status |
| ---- | -------- | ------ | ------ |
```

## Check List

### EVAL-STRUCT-001 - Metadata completeness

What to check:
- every canonical artifact includes required frontmatter
- required fields are populated or intentionally blank only where allowed

How to check:
1. inspect the artifact frontmatter
2. verify `artifact_id`, `artifact_type`, `status`, `owner`, `approved_by`, `last_reviewed`, `version`, `derived_from`, and `depends_on`
3. verify optional fields only appear where valid

Evidence:
- frontmatter block
- missing or malformed fields table when failing

Fail if:
- a required field is missing
- `artifact_type` and file role disagree
- `version` is not a positive integer

### EVAL-STRUCT-002 - Artifact authority

What to check:
- only `intent`, `prd`, `usm`, `dm`, and `spec` are treated as canonical project contracts
- `constitution.md` is treated as the governing baseline
- `AGENTS.md` and `plan.md` are derived and non-canonical

How to check:
1. read methodology docs, templates, and skill references
2. search for language that grants approval or semantic authority to derived artifacts

Evidence:
- quoted lines or file references showing artifact authority

Fail if:
- any template or doc elevates `AGENTS.md` or `plan.md` to peer semantic authority
- a canonical artifact is omitted from the stack

### EVAL-STRUCT-003 - ID grammar compliance

What to check:
- all stable IDs use approved prefixes from the constitution and artifact protocol
- duplicate IDs do not exist inside one governed scope
- draft `intent.md` is allowed to remain prose-first until reconciliation introduces optional `CAP-*`

How to check:
1. list all IDs in scope
2. compare prefixes against the constitution
3. verify one ID maps to one item only

Evidence:
- ID inventory
- duplicate or malformed ID list when failing

Fail if:
- an item uses an undefined prefix
- an expected stable item lacks an ID
- duplicate IDs exist in the same governed scope
- a draft intent artifact is failed only because it remains prose-first with no `CAP-*`

### EVAL-STRUCT-004 - Reference integrity

What to check:
- every cross-reference points to an existing ID or artifact
- downstream artifacts cite upstream items that actually exist

How to check:
1. collect all references in scope
2. resolve each reference against upstream artifacts
3. verify referenced artifacts also appear in `depends_on` where required

Evidence:
- reference matrix

Example matrix:

```text
| From item | Reference | Resolves to | Status |
| --------- | --------- | ----------- | ------ |
| STORY-014 | ENT-009   | ENT-009     | PASS   |
| STORY-021 | ENT-404   | missing     | FAIL   |
```

Fail if:
- a referenced ID does not exist
- a template references an invalid artifact type
- a downstream artifact points upstream without declaring the dependency

### EVAL-STRUCT-005 - Lifecycle correctness

What to check:
- lifecycle states are limited to `draft`, `approved`, `stale`, or `superseded`
- no alternate approval escape hatch is introduced
- approval semantics match the authority model

How to check:
1. inspect state values across artifacts and docs
2. inspect approval instructions in the skill, docs, and templates
3. explicitly search for any fifth lifecycle state or approval escape hatch

Evidence:
- state inventory
- approval rule references

Fail if:
- an unsupported state appears
- an equivalent fifth lifecycle state appears anywhere in the package
- agents are allowed to self-approve canonical artifacts
- stale behavior contradicts the dependency model

### EVAL-STRUCT-006 - Profile correctness

What to check:
- only `lite` and `full` profiles exist
- `usm.md` and `dm.md` are mandatory in both profiles
- `full` requires module and interface ownership rules

How to check:
1. inspect methodology docs
2. inspect templates and skill references
3. search for inline-USM Lite behavior or a hidden third profile

Evidence:
- profile rule excerpts

Fail if:
- a third profile appears
- Lite omits `USM` or `DM`
- Lite is described as inlining `usm.md` into `prd.md`
- Full does not require module ownership and interface ownership

### EVAL-STRUCT-007 - Traceability completeness

What to check:
- the methodology requires traceability from intent through tests

How to check:
1. inspect artifact protocol and eval docs
2. verify each tier has an expected downstream trace edge

Evidence:
- trace chain table

Expected chain:
- reconciled `CAP-*` capability -> PRD requirement
- PRD requirement -> USM story
- USM story -> DM entity or invariant
- DM entity or invariant -> spec module or interface
- changed contract item -> test

Fail if:
- a tier breaks the required chain
- a required link type is missing from the methodology
- a reconciled or downstream-traced product slice claims item-level intent trace without `CAP-*`

### EVAL-STRUCT-008 - Projection budget

What to check:
- only the allowed durable projections exist
- no external truth-bearing state file is required

How to check:
1. inspect docs, templates, and specs
2. list all persistent generated artifacts or state files they require

Evidence:
- projection inventory

Fail if:
- docs or templates require durable projections beyond:
  - trace index
  - dependency/stale graph
  - interface/schema manifests
- docs, templates, or references require an external state ledger as semantic truth

### EVAL-STRUCT-009 - Module and interface ownership

What to check:
- `full` profile requires one owner per write surface and one owner per interface
- dependencies are declared as acyclic

How to check:
1. inspect root spec and module templates
2. verify write surface, ownership, and dependency sections exist

Evidence:
- ownership matrix

Example matrix:

```text
| Surface / Interface | Owner | Status |
| ------------------- | ----- | ------ |
| modules/billing/*   | MOD-billing | PASS |
| IFACE-004           | none        | FAIL |
```

Fail if:
- ownership is ambiguous or optional
- the dependency DAG is missing where `full` requires it

### EVAL-STRUCT-010 - Stale edge validity

What to check:
- stale propagation is driven by explicit dependency edges
- reconcile remains asymmetric

How to check:
1. inspect stale propagation rules
2. inspect reconcile behavior in the spec and skill references

Evidence:
- dependency and stale rules summary

Fail if:
- upstream changes do not stale dependent artifacts
- downstream changes are allowed to overwrite approved upstream truth automatically
- reconcile is defined as an unbounded loop
