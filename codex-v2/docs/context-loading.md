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

When loading context for any command, follow these allocation targets:

| Slice | Budget |
| --- | --- |
| Code (generation, implementation) | 60% |
| Specs (canonical artifacts) | 30% |
| System prompt (skill, constitution, references) | 10% |

**Max recommended artifact lengths:**

| Artifact | Max tokens |
| --- | --- |
| Module spec | ≤ 3 000 |
| DM per bounded context | ≤ 1 500 |
| Root spec | ≤ 3 000 |

**Overflow strategy:** When specs exceed the 30% budget, summarize furthest-upstream artifacts first. Prefer to summarize `intent.md` before `prd.md`, `prd.md` before `usm.md`, and so on. The closest-to-code artifacts (spec, dm) should remain verbatim as long as possible.

## Base Load Set

Always load:

1. `constitution.md`
2. Root `spec.md`
3. Current module spec if the task is module-scoped
4. Derived `AGENTS.md` for the scope
5. Trace entries for the referenced IDs

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
3. summarize the furthest-upstream artifacts before summarizing the active boundary
4. never replace the owning interface or invariant with a loose paraphrase if the task depends on its exact meaning

## Escalation Rules

Escalate scope when any of these are true:

- the classifier cannot prove a narrower scope with high confidence
- multiple bounded contexts are involved
- interface ownership is ambiguous
- a task changes NFRs or deployment semantics
- a bugfix reveals that the approved workflow or invariant is wrong

## Exclusion Rules

Do not load:

- unrelated module specs without a dependency edge
- unrelated `USM` epics or `DM` bounded contexts
- large duplicated prose already available through the trace slice
- historical superseded artifacts unless the task is explicitly historical analysis

## Output

The agent should produce a context bundle summary with:

| Field | Meaning |
| --- | --- |
| `change_class` | Chosen class and confidence |
| `artifact_refs` | Files loaded |
| `item_refs` | IDs loaded |
| `escalation_reason` | Why broader scope was needed, if applicable |

This summary becomes input to the derived `plan.md`.
