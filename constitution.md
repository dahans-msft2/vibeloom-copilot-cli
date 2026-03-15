---
artifact_id: ART-CONSTITUTION-CODEX-V4
artifact_type: constitution
status: draft
owner: methodology
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from: []
depends_on: []
---

# Constitution: Reconciled Contract-Driven Vibe Coding

## Purpose

This document defines the universal rules that apply to projects governed by the VibeLoom methodology. It exists so downstream artifacts can stay concise and focus on domain-specific meaning instead of repeating universal engineering defaults.

## Artifact Taxonomy

| Kind | Files | Authority |
| --- | --- | --- |
| Foundational rule set | `constitution.md` | Governing baseline for every generated project |
| Canonical project contracts | `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md` | Authoritative and long-lived |
| Derived operational artifacts | `AGENTS.md`, `plan.md` | Execution-only, derived from canonical contracts |
| Machine-readable projections | Trace index, dependency/stale graph, interface/schema manifests | Derived projections used for evals and scoped execution |

## Layer Contract

This package uses the canonical layer contract defined in `docs/vibeloom-methodology.md`.

- The root artifact stack is the normative package representation aligned to that methodology prose.
- `references/` is the routine runtime operational layer loaded by the skill during routine execution.
- `templates/` are generation-only and must not introduce independent methodology truth.
- `site/` is derivative public documentation and marketing material.

## Lifecycle States

| State | Meaning | Who can enter it |
| --- | --- | --- |
| `draft` | Editable working artifact | Human or agent |
| `approved` | Human-reviewed artifact that may govern downstream work | Human only |
| `stale` | Artifact whose upstream dependencies changed or whose references are invalidated | Agent may mark; human resolves |
| `superseded` | Historical artifact replaced by a newer approved version | Human or agent during version rotation |

Rules:
- Only a human may promote a canonical contract from `draft` or `stale` to `approved`.
- An agent may derive, lint, mark stale, and propose updates, but it may not silently rewrite approved semantics.
- Derived artifacts do not carry approval authority. They may be regenerated whenever their inputs change.

## Common Metadata

Every canonical artifact must include the following frontmatter fields:

| Field | Meaning |
| --- | --- |
| `artifact_id` | Stable identifier for the file-level artifact |
| `artifact_type` | One of `intent`, `prd`, `usm`, `dm`, `spec`, or `constitution` |
| `status` | Lifecycle state |
| `owner` | Responsible role or bounded context owner |
| `approved_by` | Human approver |
| `last_reviewed` | Date of latest human approval |
| `version` | Monotonic artifact version |
| `derived_from` | Source artifacts or inputs used to generate the current draft |
| `depends_on` | Upstream artifacts whose approved state this artifact relies on |

Optional fields:
- `profile`: `lite` or `full`
- `module_id`: for module specs
- `bounded_context`: for module-level artifacts

## ID Grammar

Every stable normative item referenced across artifacts must use a stable uppercase prefix.

| Item | Prefix |
| --- | --- |
| Artifact | `ART-` |
| Capability | `CAP-` |
| User / persona | `USR-` |
| Goal | `GOAL-` |
| Metric | `METRIC-` |
| Functional requirement | `PRD-FR-` |
| Non-functional requirement | `NFR-` |
| Epic | `EPIC-` |
| Story | `STORY-` |
| Acceptance criterion | `AC-` |
| Bounded context | `BC-` |
| Entity | `ENT-` |
| Invariant | `INV-` |
| Domain event | `EVT-` |
| Module | `MOD-` |
| Interface contract | `IFACE-` |
| Flow | `FLOW-` |
| Risk / open question | `RISK-` |
| Task | `TASK-` |
| Test | `TEST-` |
| Eval | `EVAL-` |

Rules:
- IDs must be stable once approved.
- Renames change labels, not IDs.
- Draft `intent.md` may remain prose-first and may omit stable item IDs.
- Reconciliation may introduce optional `CAP-*` capability IDs when downstream item-level trace needs explicit intent references.
- Cross-file references must point to existing IDs in approved upstream artifacts unless the referenced item is part of the same draft reconcile session.

## Profiles

Only two profiles exist:

| Profile | Meaning |
| --- | --- |
| `lite` | Single bounded context or low coordination risk. `USM` and `DM` remain mandatory, but module decomposition is shallow. |
| `full` | Multiple bounded contexts or meaningful coordination risk. Module decomposition, interface ownership, and dependency DAG are required. |

Profile selection is based on semantic shape and coordination risk, not raw code size.

## Change Classes

| Class | Scope |
| --- | --- |
| `local` | Content or implementation detail change that does not alter stories, domain concepts, invariants, interfaces, or NFRs |
| `behavioral-in-module` | Change within one bounded context or module that alters behavior but does not change cross-boundary semantics |
| `boundary-changing` | Change that introduces or modifies actors, workflows, entities, invariants, integrations, cross-module interfaces, or NFRs |

Rules:
- If classification is uncertain, escalate upward to the broader class.
- `boundary-changing` work requires upstream reconciliation before implementation can be considered complete.

## Traceability Rules

The methodology requires explicit trace links:

- Draft `intent.md` may remain prose-first until reconciliation needs explicit item-level trace.
- Reconciled `intent` capabilities may be named with optional `CAP-*` IDs.
- `CAP-*` capabilities feed `prd` goals and requirements once item-level intent trace is claimed.
- `prd` requirements map to `usm` epics and stories.
- `usm` stories map to `dm` entities and invariants.
- `dm` entities and invariants map to `spec` modules, interfaces, storage, and policies.
- `spec` elements map to `plan` tasks and implementation tests.

Only three durable projections are allowed:
- Trace index
- Dependency/stale graph
- Interface/schema manifests

All other analysis artifacts are generated on demand or in memory during reconcile.

## Reconciliation Rules

- Reconciliation is asymmetric. Approved upstream contracts define intended semantics.
- Downstream manual edits and code changes may reveal drift, but they do not silently rewrite upstream truth.
- When drift is detected, the agent must propose one of two paths:
  - amend upstream semantics, then cascade stale markers downstream
  - preserve upstream semantics, then amend downstream artifacts or code
- Humans choose the direction whenever the resolution is semantically meaningful.

## Context-Loading Rules

Agents must load the minimum contract slice that can safely govern the change.

Always load:
- this constitution
- the relevant root `spec.md`
- the relevant module spec for the touched area
- the applicable derived `AGENTS.md`
- the trace slice for referenced IDs

Load conditionally:
- touched `usm` stories and linked `prd` requirements for behavior changes
- touched `dm` bounded contexts and invariants for semantic changes
- neighboring module specs and interface manifests for cross-boundary changes

## Universal Quality Defaults

- TDD is the default implementation loop.
- BDD is required for user-visible workflows.
- Errors must be propagated or handled explicitly; swallowed failures are prohibited.
- Accessibility, validation, observability, and security defaults belong here unless a project-specific contract overrides them.
- Derived artifacts must never duplicate long sections of canonical contracts. They carry only the slice needed to execute safely.

## Non-Goals

- This methodology does not require a giant prose requirements corpus.
- It does not attempt to regenerate unlimited projections for every approval step.
- It does not treat `AGENTS.md` or `plan.md` as peer semantic contracts.
