# Semantic Checks

These checks are warnings. They do not self-resolve and they do not grant approval authority to the agent.

## Report Format

Use this shape:

```text
Semantic Checks
===============

Check: [name]
Result: PASS | WARNING
Details: [specific observations]
```

## Check List

### EVAL-SEM-001 — Requirement to story coverage

Check that each `PRD-FR-*` requirement is represented by one or more `STORY-*` items and that the story acceptance criteria can plausibly satisfy the requirement.

Warn if a requirement is unrepresented or only covered by a vague story.

### EVAL-SEM-002 — Story to entity coverage

Check that each `STORY-*` item references one or more `ENT-*` items or a clearly intentional cross-cutting concern.

Warn if a story appears semantically important but touches no domain concept.

### EVAL-SEM-003 — Entity and invariant necessity

Check that each `ENT-*` and `INV-*` item is justified by one or more upstream stories or requirements.

Warn if the domain model appears over-modeled or if an invariant has no visible behavioral consequence.

### EVAL-SEM-004 — Workflow completeness

Check that the `USM` captures the critical end-to-end flows implied by the PRD and intent, including approval and reconcile steps when they are user-visible workflow concepts.

Warn if the workflow model skips a key transition that the product requirements assume.

### EVAL-SEM-005 — Boundary sanity

Check that module boundaries in `spec.md` match domain semantics in `dm.md` and workflow slices in `usm.md`.

Warn if a module split appears to cut across a single aggregate or if multiple modules appear to own the same responsibility.

### EVAL-SEM-006 — Context slice sufficiency

Check that the context-loading protocol includes enough upstream truth to implement safely without loading unrelated contracts.

Warn if the slice looks too narrow to be safe or too broad to be practical.

### EVAL-SEM-007 — Import confidence review

Check that the import path preserves uncertainty instead of presenting inferred semantics as authoritative fact.

Warn if imported artifacts lack visible confidence or if the import flow bypasses human review.

### EVAL-SEM-008 — Local bugfix path correctness

Check that the steady-state bugfix path starts from repro, expected behavior, and regression coverage before broad re-import or full upstream regeneration.

Warn if routine defect handling appears to depend on bootstrapping behavior meant for unmanaged repos.

### EVAL-SEM-009 — Derived artifact restraint

Check that `AGENTS.md` and `plan.md` remain lean, scoped, and explicitly derived from upstream truth.

Warn if derived artifacts duplicate large sections of canonical contracts or begin to carry semantic authority of their own.

### EVAL-SEM-010 — Projection restraint

Check that the methodology does not introduce a large set of persistent generated artifacts that would overwhelm context loading and review.

Warn if the design drifts toward artifact sprawl beyond the three allowed durable projections.
