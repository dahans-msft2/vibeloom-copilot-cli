# Context-Loading Protocol

The methodology depends on deterministic context scoping. This document defines what a Codex agent should load for a task and when that scope must expand.

## Objectives

- Load the smallest safe slice of upstream truth.
- Avoid flooding the model with unrelated modules or stories.
- Escalate predictably when scope is uncertain or cross-boundary.

## Inputs

- Requested change description
- Touched paths, if known
- Referenced IDs, if known
- Active profile
- Dependency/stale graph
- Trace index

## Token Budget

When loading context for a task, use this default allocation:

| Slice | Budget |
| --- | --- |
| Active code and tests | 60% |
| Canonical artifacts | 30% |
| Skill, constitution, and operational references | 10% |

Recommended upper bounds:

| Artifact slice | Max tokens |
| --- | --- |
| active module spec | <= 3,000 |
| one bounded-context DM slice | <= 1,500 |
| root spec slice | <= 3,000 |

Overflow strategy:

1. keep the active code and active module spec verbatim
2. keep directly touched IDs verbatim
3. summarize furthest-upstream artifacts before summarizing the active boundary
4. never paraphrase an owning invariant or interface when the task depends on exact semantics

## Base Load Set

Always load:

1. `constitution.md`
2. Root `spec.md`
3. Current module spec if the task is module-scoped
4. Derived `AGENTS.md` for the scope
5. Trace entries for the referenced IDs

If the task is already inside an approved module boundary, prefer the module slice over the full repo.

## Conditional Loads

Load `prd.md` slices when:
- the task changes goals, requirements, scope, or NFRs
- the task introduces new user-visible behavior

Load `usm.md` slices when:
- the task changes workflows, acceptance criteria, or story ordering
- the task is user-visible, even if technically small

Load `dm.md` slices when:
- the task introduces, removes, or changes domain concepts
- the task touches invariants, ownership, or bounded contexts

Load neighboring module specs and interface manifests when:
- the task changes a public API, event, schema, or shared type
- the change may affect another module's write surface

Load import assessments when:
- the governed repo entered through `import`
- the touched items still carry unresolved confidence markers

## Change-Class Mapping

### `local`

Load:
- constitution
- root spec
- current module spec or relevant technical slice
- derived operational artifacts for the scope

Do not load broader `USM` or `DM` unless the change reveals semantic uncertainty.

### `behavioral-in-module`

Load:
- everything from `local`
- relevant `PRD-FR-*`
- touched `STORY-*` and `AC-*`
- touched `ENT-*` and `INV-*`

Avoid loading unrelated modules unless a dependency edge demands it.

### `boundary-changing`

Load:
- everything from `behavioral-in-module`
- all affected module specs
- neighboring interfaces and dependency edges
- root-level workflow and domain slices for every touched bounded context

## Escalation Rules

Escalate scope when any of these are true:

- the classifier cannot prove a narrower scope with high confidence
- multiple bounded contexts are involved
- interface ownership is ambiguous
- a task changes NFRs or deployment semantics
- a bugfix reveals that the approved workflow or invariant is wrong

When escalation happens, summarize furthest-upstream artifacts first and keep the local technical slice verbatim as long as possible.

## Exclusion Rules

Do not load:

- unrelated module specs without a dependency edge
- unrelated `USM` epics or `DM` bounded contexts
- large duplicated prose already available through the trace slice
- historical superseded artifacts unless the task is explicitly historical analysis

## Worked Examples

### Local bugfix in a governed module

Load:
- `constitution.md`
- root `spec.md`
- module spec for the affected module
- derived `AGENTS.md`
- repro, failing test, and touched `IFACE-*` or `INV-*`

Do not load:
- unrelated `USM` epics
- unrelated modules
- brownfield import guidance

### Workflow review of `usm.md`

Load:
- `usm.md`
- relevant `prd.md` requirements
- only the implied `dm.md` slice needed to explain missing or inconsistent entities

Do not load:
- full module specs
- interface manifests unless the review is already cross-boundary

### Boundary-changing feature in `full` profile

Load:
- `constitution.md`
- root `spec.md`
- all affected module specs
- touched `PRD-FR-*`, `STORY-*`, `ENT-*`, and `INV-*`
- neighboring interfaces and dependency edges

Escalate if:
- ownership is ambiguous
- the change adds a new interface
- two bounded contexts now share one write surface

## Budget Heuristics

Prefer this order when context pressure is high:

1. keep the active code and active module spec verbatim
2. keep the directly touched IDs verbatim
3. summarize upstream intent and product slices before summarizing active technical slices
4. keep the owning interface or invariant verbatim when the task depends on exact wording

## Output

The agent should produce a context bundle summary with:

| Field | Meaning |
| --- | --- |
| `change_class` | Chosen class and confidence |
| `artifact_refs` | Files loaded |
| `item_refs` | IDs loaded |
| `escalation_reason` | Why broader scope was needed, if applicable |

This summary becomes input to the derived `plan.md`.
