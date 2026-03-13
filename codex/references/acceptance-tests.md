# Skill Acceptance Tests

Use these scenarios when validating the skill interface or revising command routing.

## Parse Tests

### Valid core commands

```text
/vibeloom status repo
/vibeloom review artifact usm
/vibeloom develop change add annual billing
/vibeloom fix issue invite links expire too early
```

Expected:
- each command parses without guessing
- verb and noun are recognized
- freeform tail remains intact

### Valid expert commands

```text
/vibeloom generate artifact dm
/vibeloom approve scope product
/vibeloom eval scope module billing
/vibeloom help command reconcile
```

### Missing noun

```text
/vibeloom review
```

Expected:
- return the valid grammar for `review`
- do not assume `artifact`

### Invalid alias or selector

```text
/vibeloom review artifact tech
/vibeloom status module payments-api
```

Expected:
- normalize `tech` to `spec` when aliasing is allowed
- if `payments-api` is invalid, return actual module selectors from the repo

## Routing Tests

### Workflow-oriented review

Input:

```text
/vibeloom review artifact usm
```

Expected:
- lead with workflow and value language
- still cite `STORY-*`, `AC-*`, and any implied `ENT-*`

### Technical-governance review

Input:

```text
/vibeloom review artifact dm
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
- do not route to `import repo`

## UX Tests

### Bare invocation

Input:

```text
$vibeloom
```

Expected:
- return governed state
- return blockers
- return next 3 valid commands

### Adaptive summaries with IDs

Any finding must name the affected IDs explicitly, even when the wording is workflow-oriented.

## Safety Tests

- No response elevates `AGENTS.md` or `plan.md` to canonical status.
- No response omits `USM` or `DM` from the methodology.
- No response implies implicit activation; the skill remains explicit-invocation only.
