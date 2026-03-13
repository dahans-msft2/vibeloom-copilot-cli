---
artifact_id: ART-CONSTITUTION-[PROJECT]
artifact_type: constitution
# status: draft | approved | approved-with-known-issues | stale | superseded
status: draft
owner: [owner]
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from: []
depends_on: []
---

# Constitution: [Project Name]

<!-- The constitution is the governing baseline for the entire repo. It defines
     universal rules, ID grammar, lifecycle states, and quality defaults that
     every other artifact must follow.

     Keep domain-specific details out of this file — those belong in intent.md,
     prd.md, and downstream artifacts. The constitution is about HOW the
     governance works, not WHAT the product does.

     Include in both Lite and Full profiles. -->

## Purpose

<!-- State the universal rules that apply to the whole governed repo.
     Example: "This constitution defines the governance rules for the BookIt
     project. All canonical artifacts must conform to these rules. Derived
     artifacts (AGENTS.md, plan.md) are regenerated from canonical sources." -->

## Artifact Taxonomy

<!-- Classify all artifact types by authority level. This helps the Agent
     understand which files are source-of-truth vs. regenerable. -->

| Kind | Files | Authority |
| --- | --- | --- |
| Foundational rule set | `constitution.md` | Governing baseline — all other artifacts must conform |
| Canonical project contracts | `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md` | Long-lived semantic truth — human-approved |
| Derived operational artifacts | `AGENTS.md`, `plan.md` | Regenerable execution guidance — auto-generated from canonical sources |
| Durable projections | Trace index, dependency/stale graph, interface/schema manifests | Mechanically checkable support data — never edited by hand |

## Lifecycle States

<!-- Every canonical artifact moves through these states.
     Only humans can transition artifacts to "approved".
     The Agent can mark artifacts as "stale" when upstream changes. -->

| State | Meaning | Who can enter it |
| --- | --- | --- |
| `draft` | Initial state; content is being authored or generated | Agent or human |
| `approved` | Reviewed and accepted as source-of-truth | Human only |
| `approved-with-known-issues` | Approved but with documented caveats or tech debt | Human only |
| `stale` | Upstream dependency changed; needs review and possible update | Agent (automatic) or human |
| `superseded` | Replaced by a newer version; kept for history | Human only |

## Common Metadata

<!-- Required frontmatter fields for every canonical artifact in this repo. -->

<!-- All canonical artifacts must include:
     - artifact_id: unique identifier (e.g., ART-PRD-BOOKIT)
     - artifact_type: one of intent, prd, usm, dm, spec, constitution
     - status: one of the lifecycle states above
     - owner: who is responsible for this artifact
     - approved_by: who approved it (blank if draft)
     - last_reviewed: date of last review (YYYY-MM-DD)
     - version: integer version number, incremented on each approval
     - derived_from: list of artifact IDs this was generated from
     - depends_on: list of artifact IDs that must be approved before this one -->

## ID Grammar

<!-- Every traceable item gets a stable, prefixed ID. These IDs are used
     across artifacts to create the trace chain:
     PRD-FR-001 → STORY-001 → ENT-001 → IFACE-001 → TASK-001 → TEST-001

     IDs are never reused. If an item is deleted, its ID is retired. -->

| Item | Prefix | Example |
| --- | --- | --- |
| User / persona | `USR-` | USR-001 |
| Goal | `GOAL-` | GOAL-001 |
| Metric | `METRIC-` | METRIC-001 |
| Functional requirement | `PRD-FR-` | PRD-FR-001 |
| Non-functional requirement | `NFR-` | NFR-001 |
| Epic | `EPIC-` | EPIC-001 |
| Story | `STORY-` | STORY-001 |
| Acceptance criterion | `AC-` | AC-001 |
| Bounded context | `BC-` | BC-001 |
| Entity | `ENT-` | ENT-001 |
| Invariant | `INV-` | INV-001 |
| Domain event | `EVT-` | EVT-001 |
| Module | `MOD-` | MOD-001 |
| Interface contract | `IFACE-` | IFACE-001 |
| Task | `TASK-` | TASK-001 |
| Test | `TEST-` | TEST-001 |
| Eval | `EVAL-` | EVAL-001 |
| Risk | `RISK-` | RISK-001 |

## Profiles

<!-- Profiles control the complexity level of the governance artifacts.
     Choose one profile at project init and record it in spec.md frontmatter. -->

| Profile | Meaning | When to use |
| --- | --- | --- |
| `lite` | Single bounded context, USM inlined in prd.md, no module specs, no AGENTS.md per module | Small projects, solo developers, MVPs |
| `full` | Multiple bounded contexts, separate usm.md, module specs with interface contracts, per-module AGENTS.md | Team projects, multi-module systems, production apps |

## Change Classes

<!-- When a change is requested, classify it to determine the scope of
     impact and which artifacts need updating. -->

| Class | Scope | Escalation rule |
| --- | --- | --- |
| `local` | Internal implementation only; no interface or contract changes | No upstream updates needed; only plan.md and AGENTS.md regenerated |
| `behavioral-in-module` | Behavior changes within one module; may touch module spec | Update module spec and regenerate AGENTS.md; check affected stories |
| `boundary-changing` | Crosses module boundaries or modifies interface contracts | Update spec.md, affected module specs, and all downstream artifacts; requires human review |

## Traceability Rules

<!-- Define the mandatory trace chain for the repo.
     Every implementation must trace back to a requirement through this chain:
     intent → PRD-FR-xxx → STORY-xxx → ENT-xxx / INV-xxx → TASK-xxx → TEST-xxx

     The eval command verifies this chain is unbroken. -->

## Reconciliation Rules

<!-- Describe the asymmetry between upstream truth and downstream drift.
     Upstream wins: if prd.md changes, usm.md, dm.md, spec.md may become stale.
     Downstream never overrides upstream: code cannot redefine requirements.
     Stale artifacts must be reconciled before new changes can be approved. -->

## Context-Loading Rules

<!-- State what is always loaded, what is conditional, and when escalation happens.
     Always load: constitution.md, spec.md (for any task)
     Conditionally load: dm.md (if touching entities), usm.md (if touching stories)
     Escalate: if a change would affect interfaces in other modules -->

## Universal Quality Defaults

<!-- Testing, observability, accessibility, error handling, and other
     universal defaults that apply to every module and every change.
     These can be overridden in module specs with documented rationale. -->

<!-- Example defaults:
     - All new functions must have unit tests
     - All API endpoints must validate inputs with a schema
     - All mutations must emit domain events
     - Error responses must follow RFC 7807 problem details
     - Accessibility: WCAG 2.1 AA compliance
     - Logging: structured JSON, no PII in logs -->
