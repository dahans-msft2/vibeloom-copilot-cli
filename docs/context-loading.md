# Context-Loading Guide

This guide explains the reasoning behind VibeLoom's context-scoping model.

The canonical layer contract lives in [vibeloom-methodology.md](vibeloom-methodology.md).
Use this file for maintainer-facing deeper explanation, examples, and judgment calls rather than as a routed `help` topic or routine runtime rulebook.

## Objectives

- Load the smallest safe slice of upstream truth.
- Avoid flooding the model with unrelated modules or stories.
- Escalate predictably when scope is uncertain or cross-boundary.

## What Shapes The Slice

Context scoping usually depends on a few recurring inputs:

- requested change description
- touched paths, when known
- referenced IDs, when known
- active profile
- active surface
- dependency or stale edges
- trace links for the touched slice

The runtime references define how those signals are used during routine commands. This guide explains the intent behind that behavior.

## Stable Principles

### Start from the nearest owning boundary

The runtime references own the exact per-command load bundle. As a general rule:

- artifact review starts from the target artifact
- technical change work starts from the nearest owning technical boundary

For technical work, the first useful slice usually includes:

- the relevant root `spec.md`
- the current module spec when the task is module-scoped
- the derived `AGENTS.md` for the scope when it exists and reduces ambiguity
- trace entries for directly referenced IDs, stale impact, or downstream trace questions

That starting point is narrow on purpose. It gives the agent the local contract surface before broader product or domain context is added.

### Escalate upward, not sideways

When a task becomes semantically ambiguous, the safe move is to load the governing upstream slice:

- `prd.md` when goals, requirements, scope, or NFRs are implicated
- `usm.md` when workflows, acceptance criteria, or user-visible behavior are implicated
- `dm.md` when concepts, invariants, ownership, or bounded contexts are implicated

Only then should the slice widen sideways into neighboring modules, interfaces, or dependency edges.

### Keep unrelated material out

A disciplined slice normally excludes:

- unrelated module specs without a dependency edge
- unrelated `USM` epics or `DM` bounded contexts
- duplicated prose already recoverable from the trace slice
- historical superseded artifacts unless the task is explicitly historical

The goal is not minimalism for its own sake. The goal is to keep only the truth needed to make the current decision safely.

## How Change Class Usually Affects Scope

### `local`

A local change usually stays close to the technical boundary:

- root spec
- current module spec or relevant technical slice
- derived operational guidance for the scope

Broader `USM` or `DM` material is unnecessary unless the task stops looking purely local.

### `behavioral-in-module`

A behavioral change inside one boundary usually adds the governing product and domain slice:

- relevant `PRD-FR-*`
- touched `STORY-*` and `AC-*`
- touched `ENT-*` and `INV-*`

This is the point where "small code change" and "small semantic change" stop being the same thing.

### `boundary-changing`

A boundary-changing task usually needs the full affected chain:

- all affected module specs
- neighboring interfaces and dependency edges
- workflow and domain slices for each touched bounded context

If the task changes ownership or introduces a new shared boundary, the narrow local slice is no longer enough.

## Surface Effects

Surfaces change what is shown first, not what is true.

- `product-first` brings workflow and domain context into view sooner.
- `code-first` starts with the technical slice and escalates upward when the task stops being safely spec-local.

That means `code-first` is not permission to omit `prd.md`, `usm.md`, or `dm.md`. It only changes the order in which those layers become visible.

## Context Pressure Heuristics

When the available context gets tight, preserve the most failure-sensitive material first:

1. active code and active module spec
2. directly touched IDs
3. owning invariants, interfaces, and acceptance boundaries when exact wording matters
4. upstream prose summarized from furthest upstream toward the active boundary

Avoid treating fixed token percentages or hard token caps as durable methodology rules. Those numbers are model- and session-dependent and belong, if anywhere, in runtime tuning rather than canonical prose.

## Worked Examples

### Local bugfix in a governed module

A local bugfix usually starts from:

- root `spec.md`
- the affected module spec
- derived `AGENTS.md` when it exists and clarifies the scoped write surface
- the repro, failing test, and touched `API-*` or `INV-*`
- trace links when the violated contract or stale impact is in question

It usually does not need unrelated `USM` epics, unrelated modules, or brownfield import guidance.

### Workflow review of `usm.md`

A workflow review usually needs:

- the target `usm.md` slice
- relevant `prd.md` requirements
- only the `dm.md` slice needed to explain missing or inconsistent entities

It usually does not need full module specs unless the review has already become cross-boundary or implementation-specific.

### Boundary-changing feature in `full`

A boundary-changing feature usually starts from the owning technical boundaries, then expands:

- root `spec.md`
- all affected module specs
- touched `PRD-FR-*`, `STORY-*`, `ENT-*`, and `INV-*`
- neighboring interfaces and dependency edges

If ownership is ambiguous, a new shared boundary appears, or two bounded contexts start sharing one write surface, the slice should widen before implementation decisions continue.

## Communicating The Chosen Slice

When the operator would benefit from a scope summary, a useful explanation is:

- chosen change class and confidence
- active surface
- artifacts loaded
- key IDs loaded
- reason for any escalation

That summary helps humans audit whether the agent loaded enough truth without turning the summary itself into a new durable authority layer.
