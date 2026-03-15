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
| Durable projections | Trace index, dependency/stale graph, interface/schema manifests | Mechanically checkable support data |

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
| Interface contract | `IFACE-` |
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

<!-- State what is always loaded, what is conditional, and when escalation happens. -->

## Universal Quality Defaults

<!-- Testing, observability, accessibility, error handling, and other universal defaults. -->
