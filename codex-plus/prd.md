---
artifact_id: ART-PRD-CODEX-PLUS
artifact_type: prd
status: draft
owner: methodology
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-INTENT-CODEX-PLUS
depends_on:
  - ART-INTENT-CODEX-PLUS
---

# Product Requirements Document: Codex Plus Methodology Package

## Overview

The product is a methodology package that enables users to build and maintain software with coding agents through a durable contract stack instead of relying on one-off prompts. It should help users sustain quality, module boundaries, and semantic coherence as the codebase and team grow.

## Users & Personas

| ID | Persona | Description | Primary goals |
| --- | --- | --- | --- |
| USR-001 | Product-oriented builder | PM or designer comfortable reviewing structured docs | Turn intent into a safe implementation workflow without writing exhaustive specs manually |
| USR-002 | Technical governor | Lead engineer or architect | Preserve semantic coherence, testing discipline, and module boundaries across time |
| USR-003 | Execution agent | Codex or similar coding agent | Receive a minimal but sufficient contract slice to implement or reconcile a change safely |

## Goals

| ID | Goal | Success signal |
| --- | --- | --- |
| GOAL-001 | Make long-lived agentic development governable | Teams can sustain contract-based incremental work over time |
| GOAL-002 | Preserve semantics across parallel change | Cross-module regressions and concept drift decrease |
| GOAL-003 | Keep specs concise enough for routine human review | Humans can review and approve artifacts without wading through boilerplate |

## Success Metrics

| ID | Metric | Target |
| --- | --- | --- |
| METRIC-001 | Percent of implemented changes with valid trace links from requirement to test | 100% for approved work |
| METRIC-002 | Number of durable projections required by the method | No more than 3 |
| METRIC-003 | Manual review burden for low-risk edits | Bounded to the touched slice plus derived operational docs |
| METRIC-004 | Cross-module ownership ambiguity incidents | 0 in approved `full` profile work |

## Functional Requirements

| ID | Requirement | Priority | Users | Acceptance criteria |
| --- | --- | --- | --- | --- |
| PRD-FR-001 | The package must define a canonical intent-first contract stack with `intent`, `prd`, `usm`, `dm`, and `spec`. | P0 | USR-001, USR-002, USR-003 | The methodology names each artifact, its authority, and its downstream role. |
| PRD-FR-002 | The package must make `USM` mandatory as the workflow and acceptance layer. | P0 | USR-001, USR-002 | Every governed project template includes `usm.md`; no profile omits it. |
| PRD-FR-003 | The package must make `DM` mandatory as the semantic layer. | P0 | USR-002, USR-003 | Every governed project template includes `dm.md`; no profile omits it. |
| PRD-FR-004 | The package must define deterministic context loading so agents use the smallest safe contract slice. | P0 | USR-002, USR-003 | The package documents always-load, conditional-load, and escalation rules. |
| PRD-FR-005 | The package must define asymmetric reconciliation after manual edits or code drift. | P0 | USR-002, USR-003 | The methodology distinguishes upstream semantic truth from downstream drift and requires explicit proposals. |
| PRD-FR-006 | The package must support greenfield initialization and brownfield import. | P0 | USR-001, USR-002 | The workflow defines both a greenfield path and an `import` bootstrap path. |
| PRD-FR-007 | The package must treat `AGENTS.md` and `plan.md` as derived operational artifacts, not canonical peers. | P0 | USR-002, USR-003 | Templates and docs describe them as derived and regenerable. |
| PRD-FR-008 | The package must support a steady-state local bugfix path for governed repos. | P1 | USR-002, USR-003 | The technical spec defines repro-first, regression-first, targeted reconcile behavior. |
| PRD-FR-009 | The package must keep machine-readable projections intentionally limited. | P1 | USR-002 | Only trace index, stale graph, and interface/schema manifests are durable outputs. |
| PRD-FR-010 | The package must provide focused help and explanation paths for methodology, profiles, evals, templates, and commands. | P1 | USR-001, USR-002, USR-003 | The skill exposes topic help and the docs provide targeted guides without bloating the skill body. |
| PRD-FR-011 | The package must provide concrete technical-design templates without sacrificing governance rules. | P1 | USR-002, USR-003 | Root and module spec templates include runtime architecture detail, ownership rules, and interface structure together. |

## Non-Functional Requirements

| ID | Requirement | Target | Measurement |
| --- | --- | --- | --- |
| NFR-001 | Human readability | Canonical artifacts remain concise and skimmable | Review pass can be done directly in Markdown |
| NFR-002 | Context efficiency | Agents load minimal sufficient context | Context-loading rules define exclusion and escalation behavior |
| NFR-003 | Traceability | Each approved item traces to upstream and downstream IDs | Structural eval verifies link completeness |
| NFR-004 | Parallel safety | Full profile changes must have explicit write ownership and interface ownership | Structural eval verifies ownership and dependency DAG rules |
| NFR-005 | Governance durability | Approved upstream changes must stale dependent artifacts predictably | Stale propagation follows explicit dependency edges |

## Scope Boundaries

### In Scope

- Methodology artifacts and templates for the Codex Plus variant
- Eval instructions
- Protocol documentation
- Technical design for a future runtime

### Out Of Scope

- Runnable command implementation
- Automation workflows
- Generated live `AGENTS.md` files
- Runtime-specific language selection

### Future Considerations

- Skill command surface and runtime implementation
- Tooling around in-memory reconcile and trace generation
- Optional integration adapters for non-Codex environments

## Risks & Open Questions

| ID | Risk / Question | Severity | Mitigation / Status |
| --- | --- | --- | --- |
| RISK-001 | Over-specification could slow routine changes | Medium | Keep universal defaults in the constitution and keep projections limited |
| RISK-002 | Artifact authority can become muddy if derived artifacts are hand-edited | High | Mark derived artifacts explicitly non-canonical and regenerable |
| RISK-003 | Brownfield import can infer the wrong semantics | High | Mark imported content with confidence and require human approval before governance begins |
