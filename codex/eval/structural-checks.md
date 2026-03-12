# Structural Checks

These checks are blocking. A canonical artifact cannot be approved while a structural check fails.

## Report Format

Use this shape:

```text
Structural Checks
=================

Check: [name]
Result: PASS | FAIL
Details: [specific failures]
```

## Check List

### EVAL-STRUCT-001 — Metadata completeness

Verify that every canonical artifact includes:
- `artifact_id`
- `artifact_type`
- `status`
- `owner`
- `approved_by`
- `last_reviewed`
- `version`
- `derived_from`
- `depends_on`

Fail if required metadata is missing or malformed.

### EVAL-STRUCT-002 — Artifact authority

Verify that:
- only `intent`, `prd`, `usm`, `dm`, and `spec` are treated as canonical project contracts
- `constitution.md` is treated as the governing baseline
- `AGENTS.md` and `plan.md` are described as derived, regenerable, and non-canonical

Fail if any template or doc elevates `AGENTS.md` or `plan.md` to peer semantic authority.

### EVAL-STRUCT-003 — ID grammar compliance

Verify that all stable IDs use approved prefixes from the constitution and artifact protocol.

Fail if:
- an item uses an undefined prefix
- an expected stable item lacks an ID
- duplicate IDs exist in the same governed scope

### EVAL-STRUCT-004 — Reference integrity

Verify that every cross-reference points to an existing ID or artifact in scope.

Fail if:
- a referenced ID does not exist
- a template references an artifact type that is no longer valid
- a downstream artifact points to an upstream artifact that is missing from `depends_on`

### EVAL-STRUCT-005 — Lifecycle correctness

Verify that lifecycle states are limited to `draft`, `approved`, `stale`, or `superseded`.

Fail if:
- an artifact uses an unsupported state
- approval language allows agents to self-approve canonical artifacts
- stale behavior contradicts the dependency model

### EVAL-STRUCT-006 — Profile correctness

Verify that:
- only `lite` and `full` profiles exist
- `usm.md` and `dm.md` are mandatory in both profiles
- `full` profile requires module and interface ownership rules

Fail if any artifact reintroduces a third profile or omits `USM` / `DM`.

### EVAL-STRUCT-007 — Traceability completeness

Verify that the methodology requires traceability from:
- intent capabilities to PRD requirements
- PRD requirements to USM stories
- USM stories to DM entities and invariants
- DM entities and invariants to spec modules and interfaces
- changed contract items to tests

Fail if a tier breaks the required trace chain.

### EVAL-STRUCT-008 — Projection budget

Verify that only these durable projections exist:
- trace index
- dependency/stale graph
- interface/schema manifests

Fail if docs or templates require additional always-on durable projections.

### EVAL-STRUCT-009 — Module and interface ownership

Verify that the `full` profile requires:
- one owner per module write surface
- one owner per interface contract
- acyclic module dependencies

Fail if ownership is ambiguous or optional.

### EVAL-STRUCT-010 — Stale edge validity

Verify that stale propagation is driven by explicit dependency edges and asymmetric reconciliation rules.

Fail if:
- upstream changes do not stale dependent artifacts
- downstream changes are allowed to overwrite approved upstream truth automatically
