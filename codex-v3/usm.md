---
artifact_id: ART-USM-CODEX-V3
artifact_type: usm
status: draft
owner: methodology
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-INTENT-CODEX-V3
  - ART-PRD-CODEX-V3
depends_on:
  - ART-INTENT-CODEX-V3
  - ART-PRD-CODEX-V3
---

# User Story Map: Codex V3 Methodology Package

## Users

| ID | Persona | Description |
| --- | --- | --- |
| USR-001 | Product-oriented builder | Wants the system to turn intent into a durable, reviewable contract stack |
| USR-002 | Technical governor | Wants reliable semantics, ownership boundaries, and safe incremental change |
| USR-003 | Execution agent | Wants a small, relevant context slice and explicit task boundaries |

## Story Map

### Epic: EPIC-001 — Initialize A Governed Project

**Goal:** A user can start a governed project with the methodology scaffolding in place before code generation begins.

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-001 | Create a new governed project | USR-001 | initialize a project from an intent | the repo starts from a shared source of truth instead of an untracked prompt | P0 | ENT-001, ENT-006 | AC-001, AC-002 |
| STORY-002 | Approve foundational artifacts | USR-002 | review and approve the initial stack | downstream work is gated by explicit human approval | P0 | ENT-001, ENT-004, ENT-005 | AC-003 |

### Epic: EPIC-002 — Reveal User Value And Semantics

**Goal:** The methodology exposes user workflows before technical decomposition happens.

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-003 | Map user workflows with USM | USR-001 | express epics, stories, and acceptance criteria | the intended user value is easy to validate | P0 | ENT-002, ENT-003 | AC-004, AC-005 |
| STORY-004 | Derive domain concepts from workflows | USR-002 | model entities, relationships, and invariants | the system preserves ubiquitous language across implementation changes | P0 | ENT-002, ENT-007, ENT-008 | AC-006 |

### Epic: EPIC-003 — Design Safe Execution Boundaries

**Goal:** The methodology turns semantics into technical boundaries safe for Codex agents.

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-005 | Define module boundaries and interfaces | USR-002 | derive modules and owned interfaces from the approved semantics | parallel work has clear write surfaces and interface ownership | P0 | ENT-008, ENT-009 | AC-007 |
| STORY-006 | Generate derived operational guidance | USR-003 | receive a scoped `AGENTS.md` and change plan | execution uses minimal relevant context without elevating derived docs to source of truth | P0 | ENT-001, ENT-010 | AC-008 |

### Epic: EPIC-004 — Evolve A Governed Codebase

**Goal:** Approved contracts remain durable while the code and downstream artifacts continue to change.

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-007 | Classify a change before execution | USR-003 | identify whether a change is local, behavioral, or boundary-changing | the system loads only the safe context slice and applies the correct approval path | P0 | ENT-006, ENT-010 | AC-009 |
| STORY-008 | Reconcile manual edits asymmetrically | USR-002 | detect drift and choose whether semantics or implementation should change | approved upstream truth is not silently overwritten | P0 | ENT-001, ENT-004, ENT-005 | AC-010 |
| STORY-009 | Fix defects locally in governed repos | USR-002 | start from a repro and regression test | defect handling stays fast without re-importing the whole repo | P1 | ENT-004, ENT-005 | AC-011 |

### Epic: EPIC-005 — Import Existing Repositories

**Goal:** An unmanaged repo can enter the methodology with controlled uncertainty.

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-010 | Import an unmanaged codebase | USR-002 | reconstruct draft contracts from code, tests, and docs | I can bring a brownfield repo under governance | P1 | ENT-001, ENT-004, ENT-011 | AC-012 |
| STORY-011 | Review inferred confidence | USR-002 | see where the import is uncertain | I can approve or correct inferred semantics before downstream work resumes | P1 | ENT-011, ENT-005 | AC-013 |

### Epic: EPIC-006 — Teach The Operator Without Diluting The Protocol

**Goal:** The methodology stays learnable and usable without collapsing back into vague conversational guidance.

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-014 | Choose the right profile with explicit guidance | USR-002 | review clear Lite vs Full heuristics | the repo takes on only the coordination overhead it actually needs | P1 | ENT-007, ENT-010 | AC-014 |
| STORY-015 | Ask for focused help topics | USR-001 | load methodology, profile, eval, template, or command guidance on demand | the skill stays lean while the docs stay teachable | P1 | ENT-001, ENT-010 | AC-015 |

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| AC-001 | The initialized project contains the canonical contract files required by the selected profile. |
| AC-002 | The initial stack is created from intent-first inputs rather than technical design alone. |
| AC-003 | Downstream work does not proceed from an unapproved canonical contract. |
| AC-004 | Every story has a stable ID, actor, value statement, and acceptance criteria. |
| AC-005 | Stories are easy for humans to validate against user needs before technical decomposition. |
| AC-006 | Every domain entity or invariant can be traced back to one or more stories or requirements. |
| AC-007 | In `full` profile, every module owns a write surface and every interface has a single owner. |
| AC-008 | Derived operational artifacts contain only the slice needed for execution. |
| AC-009 | If change classification is uncertain, the workflow escalates to the broader scope. |
| AC-010 | Drift produces proposals and stale markers rather than silent semantic rewrites. |
| AC-011 | The steady-state bugfix path starts from repro, expected behavior, and regression coverage. |
| AC-012 | Import reconstructs draft contracts and marks low-confidence inferences for review. |
| AC-013 | The user can approve or correct inferred semantics before normal governance begins. |
| AC-014 | Profile guidance preserves separate `usm.md` and `dm.md` in both profiles. |
| AC-015 | Topic help returns targeted guidance without dumping the full methodology into every response. |

## Cross-Cutting Concerns

| ID | Story | Affects epics | Priority |
| --- | --- | --- | --- |
| STORY-012 | Maintain trace links across every tier | EPIC-001, EPIC-002, EPIC-003, EPIC-004, EPIC-005 | P0 |
| STORY-013 | Keep context slices small enough for efficient execution | EPIC-003, EPIC-004, EPIC-005 | P0 |

## Story Dependencies

| Story | Depends on | Reason |
| --- | --- | --- |
| STORY-003 | STORY-001 | Workflow modeling assumes an initialized artifact stack |
| STORY-004 | STORY-003 | Domain concepts are surfaced through validated workflows |
| STORY-005 | STORY-004 | Module boundaries are derived after semantics are modeled |
| STORY-006 | STORY-005 | Derived operational artifacts depend on technical boundaries |
| STORY-007 | STORY-005 | Change classification needs known module and interface boundaries |
| STORY-008 | STORY-002, STORY-005 | Reconciliation assumes approved upstream truth and known dependencies |
| STORY-009 | STORY-008 | Local defect handling depends on targeted reconcile rules |
| STORY-011 | STORY-010 | Confidence review follows import |
| STORY-014 | STORY-004 | Profile choice should follow semantic modeling, not precede it |
| STORY-015 | STORY-001 | Focused help assumes a governed vocabulary and command surface already exist |
