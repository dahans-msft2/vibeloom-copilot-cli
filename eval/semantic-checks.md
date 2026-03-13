# Semantic Checks

These checks are warnings. They do not self-resolve and they do not grant approval authority to the agent.

## Report Format

Use this shape:

```text
Semantic Checks
===============

Check: [name]
Result: PASS | WARNING
Evidence: [what was compared]
Details: [specific observations]
```

Use matrices when coverage or ownership is clearer in table form.

## Check List

### EVAL-SEM-001 - Requirement to story coverage

What to check:
- each `PRD-FR-*` requirement is represented by one or more `STORY-*` items
- the acceptance criteria plausibly satisfy the requirement

How to check:
1. list `PRD-FR-*` items
2. map each requirement to story IDs and acceptance criteria
3. flag uncovered or vague mappings

Evidence:
- coverage matrix

Example matrix:

```text
| Requirement | Stories | Status |
| ----------- | ------- | ------ |
| PRD-FR-004  | STORY-018, STORY-019 | PASS |
| PRD-FR-007  | none | WARNING |
```

Warn if:
- a requirement is unrepresented
- only a vague story appears to cover the requirement

### EVAL-SEM-002 - Story to entity coverage

What to check:
- each `STORY-*` item references one or more `ENT-*` items or a clearly intentional cross-cutting concern

How to check:
1. list stories in scope
2. inspect entity references
3. reason about whether missing entity coverage is intentional

Evidence:
- story-to-entity matrix

Example matrix:

```text
| Story | Entity refs | Status |
| ----- | ----------- | ------ |
| STORY-011 | ENT-004, ENT-009 | PASS |
| STORY-014 | none | WARNING |
```

Warn if:
- a semantically important story touches no domain concept

### EVAL-SEM-003 - Entity and invariant necessity

What to check:
- each `ENT-*` and `INV-*` item is justified by stories or requirements

How to check:
1. list entities and invariants
2. map them back to `STORY-*`, `PRD-FR-*`, or `NFR-*`
3. note entities that appear speculative or redundant

Evidence:
- reverse trace inventory

Warn if:
- the domain model appears over-modeled
- an invariant has no visible behavioral consequence

### EVAL-SEM-004 - Workflow completeness

What to check:
- the `USM` captures the critical end-to-end flows implied by the PRD and intent
- approval and reconcile steps are present when they are user-visible workflow concepts

How to check:
1. read the PRD goals and requirements
2. inspect whether the story map covers entry, success, exception, and completion flow

Evidence:
- short narrative of missing or complete flow segments

Warn if:
- a key transition is missing
- acceptance criteria skip a major user-visible step

### EVAL-SEM-005 - Boundary sanity

What to check:
- module boundaries in `spec.md` match domain semantics in `dm.md` and workflow slices in `usm.md`

How to check:
1. compare bounded contexts to module responsibilities
2. inspect whether one aggregate is split without good reason
3. inspect whether multiple modules claim one responsibility

Evidence:
- module-to-context ownership matrix

Example matrix:

```text
| Entity | Bounded context | Owning module | Status |
| ------ | --------------- | ------------- | ------ |
| ENT-012 | BC-billing | MOD-billing | PASS |
| ENT-014 | BC-billing | MOD-auth | WARNING |
```

Warn if:
- a module split cuts through one aggregate or invariant cluster
- several modules appear to own one domain responsibility

### EVAL-SEM-006 - Context slice sufficiency

What to check:
- the context-loading protocol includes enough upstream truth to implement safely without loading unrelated contracts

How to check:
1. inspect context-loading rules
2. test them mentally against a local change, a module change, and a boundary change

Evidence:
- scenario-by-scenario adequacy notes

Warn if:
- the slice is too narrow to be safe
- the slice is so broad that it defeats context discipline
- status or onboarding guidance implicitly depends on loading the full governed repo for routine work

### EVAL-SEM-007 - Import confidence review

What to check:
- the import path preserves uncertainty instead of presenting inferred semantics as fact

How to check:
1. inspect import workflow and templates
2. verify confidence markers or equivalent uncertainty signals are required

Evidence:
- import rule summary

Warn if:
- imported artifacts look fully authoritative before human review
- confidence or evidence is hidden

### EVAL-SEM-008 - Local bugfix path correctness

What to check:
- the steady-state bugfix path starts from repro, expected behavior, and regression coverage before broad re-import or full upstream regeneration

How to check:
1. inspect bugfix instructions
2. compare them to import instructions
3. verify the normal defect path stays local unless a broader contradiction is discovered

Evidence:
- bugfix vs import decision summary

Warn if:
- routine defect handling depends on `import`
- regression framing is missing

### EVAL-SEM-009 - Derived artifact restraint

What to check:
- `AGENTS.md` and `plan.md` remain lean, scoped, and explicitly derived

How to check:
1. inspect templates and methodology docs
2. compare derived content expectations to canonical artifact expectations

Evidence:
- derived artifact rule summary

Warn if:
- derived artifacts duplicate large canonical sections
- derived artifacts begin to carry semantic authority of their own

### EVAL-SEM-010 - Projection restraint

What to check:
- the methodology does not introduce a large persistent artifact set that would overwhelm context loading and review

How to check:
1. inspect specs, docs, and templates
2. list durable artifacts beyond the canonical stack

Evidence:
- projection inventory

Warn if:
- the design drifts toward durable artifact sprawl beyond the three allowed projections
