# Skill Acceptance Tests

Use these scenarios when validating the skill interface or revising command routing.

## Parse Tests

### Valid core commands

```text
/vibeloom status
/vibeloom review usm
/vibeloom develop add annual billing
/vibeloom fix issue invite links expire too early
```

Expected:
- each command parses without guessing
- action and required target shape are recognized
- freeform tail remains intact

### Concise canonical commands

```text
/vibeloom init build a recruiting platform
/vibeloom import .
/vibeloom status
/vibeloom develop add annual billing
/vibeloom reconcile
/vibeloom generate dm
/vibeloom review usm
/vibeloom approve product
/vibeloom eval module billing
/vibeloom help surfaces
```

Expected:
- each command parses as written with no extra structural keyword
- follow-up messages and suggested commands use the same concise canonical forms

### Valid expert commands

```text
/vibeloom generate dm
/vibeloom help command review
/vibeloom approve product
/vibeloom eval module billing
/vibeloom surface code-first
```

### Missing target

```text
/vibeloom review
```

Expected:
- return the valid grammar for `review`
- do not assume `artifact` or `module`

### Invalid target or selector

```text
/vibeloom help overview
/vibeloom review profiles
/vibeloom status module payments-api
/vibeloom generate tests
```

Expected:
- accept documented direct topic and artifact targets only when the trailing token is valid
- reject unsupported command forms such as `/vibeloom generate tests`
- for `review`, do not guess `module`; non-artifact review still requires `review module <module-name>`
- if `payments-api` is invalid, return actual module selectors from the repo

## Routing Tests

### Workflow-oriented review

Input:

```text
/vibeloom review usm
```

Expected:
- lead with workflow and value language
- still cite `STORY-*`, `AC-*`, and any implied `ENT-*`

### Technical-governance review

Input:

```text
/vibeloom review dm
```

Expected:
- lead with entity, invariant, or ownership language
- cite `ENT-*`, `INV-*`, and related upstream items

### Bugfix routing

Input:

```text
/vibeloom fix issue invite links expire too early
```

Expected:
- route to repro-first bugfix flow
- do not route to `import`

### Import routing boundary

Input:

```text
/vibeloom import .
```

Expected:
- use runtime import rules from `references/`
- inspect repo evidence directly rather than loading root `spec.md` as an operational dependency
- mark inferred semantics as draft with visible confidence or uncertainty

## UX Tests

### Bare invocation

Input:

```text
$vibeloom
```

Expected:
- return governed state
- return current surface
- return blockers
- return profile when known
- return next 3 valid commands
- give state-aware command suggestions instead of the full catalog

### Init interview

Input:

```text
/vibeloom init build a recruiting platform
```

Expected:
- if the seed is underspecified, ask only for missing product facts
- do not jump straight to downstream artifacts
- keep the next action focused on drafting `intent.md`

### Prose-first draft intent

Expected:
- draft `intent.md` may remain prose-first and omit stable item IDs
- the draft remains valid until reconciliation or downstream trace needs explicit item-level intent references

### Reconciled capability index

Expected:
- reconciliation may add optional `CAP-*` capability IDs to `intent.md`
- when product artifacts claim item-level intent trace, `PRD-FR-*` items reference one or more `CAP-*`

### Profile recommendation

Input:

```text
/vibeloom approve product
```

Expected:
- use the approved `dm.md` shape to recommend `lite` or `full`
- explain the recommendation with bounded-context and entity-count reasoning
- keep the recommendation session-local rather than writing it to an external state file

### Topic help

Input:

```text
/vibeloom help evals
```

Expected:
- route only to eval documentation
- summarize the structural and semantic tiers concisely
- avoid dumping the whole methodology

### Runtime loading boundary

Routine commands such as:

```text
/vibeloom status
/vibeloom develop add annual billing
/vibeloom approve product
/vibeloom eval spec
/vibeloom surface code-first
```

Expected:
- load `references/` first
- do not pull `docs/` unless a deeper explanation is requested or a runtime reference explicitly escalates
- for routine `approve` and `eval`, use `references/evals-and-templates.md` instead of the detailed eval docs
- for `surface`, use runtime surface rules from `references/`, not `docs/surface-modes.md`
- keep `help` as the primary direct path to `docs/`

### Adaptive summaries with IDs

Any finding must name the affected IDs explicitly, even when the wording is workflow-oriented.

## Safety Tests

- No response elevates `AGENTS.md` or `plan.md` to canonical status.
- No response omits `USM` or `DM` from the methodology.
- No response implies implicit activation; the skill remains explicit-invocation only.
- No response introduces a fifth approval state, collapses the USM into the PRD for Lite, or requires an external truth-bearing state ledger.
- No response introduces removed long forms or undocumented shorthand.
- No runtime rule requires stable item IDs in draft intent before reconciliation introduces optional `CAP-*`.
