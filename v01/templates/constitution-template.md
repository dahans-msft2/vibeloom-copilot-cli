---
artifact_id: ART-CONSTITUTION-[PROJECT]
artifact_type: constitution
status: draft
owner: [owner]
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from: []
depends_on: []
---

# Constitution: [Project Name]

## Purpose

<!-- State the universal rules that apply to the whole governed repo. Keep domain specifics out of this file. -->

## Artifact Taxonomy

| Kind | Files | Authority |
| --- | --- | --- |
| Foundational rule set | `constitution.md` | Governing baseline |
| Canonical project contracts | `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md` | Long-lived semantic truth |
| Derived operational artifacts | `AGENTS.md`, `plan.md` | Regenerable execution guidance |
| Machine-readable projections | Trace index, dependency/stale graph, interface/schema manifests | Derived projections used for evals and scoped execution |

## Layer Contract

<!-- Point repo-level layering back to the canonical methodology prose.
     Keep detailed runtime-operational rules out of this file. -->

- The root artifact stack is the normative package representation aligned to the methodology prose.
- Environment-specific runtime guidance owns exact command behavior and load selection.
- `templates/` are generation-only and must not introduce independent methodology truth.
- `site/` is derivative public documentation and marketing material.

## Lifecycle States

| State | Meaning | Who can enter it |
| --- | --- | --- |
| `draft` | | |
| `approved` | | |
| `stale` | | |
| `superseded` | | |

## Common Metadata

<!-- Define required frontmatter fields for the repo. -->

## ID Grammar

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
| Interface contract | `API-` |
| Flow | `FLOW-` |
| Risk / open question | `RISK-` |
| Task | `TASK-` |
| Test | `TEST-` |
| Eval | `EVAL-` |

## Profiles

| Profile | Meaning |
| --- | --- |
| `lite` | |
| `full` | |

## Change Classes

| Class | Scope | Escalation rule |
| --- | --- | --- |
| `local` | | |
| `behavioral-in-module` | | |
| `boundary-changing` | | |

## Traceability Rules

<!-- Define the mandatory trace chain for the repo. -->

## Reconciliation Rules

<!-- Describe the asymmetry between upstream truth and downstream drift. -->

## Context-Loading Rules

Agents must load the minimum contract slice that can safely govern the change.

<!-- Preserve only universal context-loading constraints here.
     Do not define a second command-level or "always load" runtime bundle in the constitution. -->

- start from the governing artifact or technical boundary that owns the decision being made
- include trace links when referenced IDs, downstream impact, or stale implications are part of the task
- bring workflow and domain slices into view when workflows, concepts, invariants, interfaces, or NFR boundaries are implicated
- broaden upward before sideways when ambiguity appears
- keep unrelated modules, bounded contexts, and superseded artifacts out of the default slice unless explicit dependency or historical analysis requires them
- derived operational guidance may narrow execution focus, but it never replaces canonical authority

## Universal Quality Defaults

<!-- Testing, observability, accessibility, error handling, and other universal defaults. -->
