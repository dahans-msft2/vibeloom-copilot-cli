---
artifact_id: ART-USM-[PROJECT]
artifact_type: usm
# status: draft | approved | approved-with-known-issues | stale | superseded
status: draft
owner: [owner]
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-INTENT-[PROJECT]
  - ART-PRD-[PROJECT]
depends_on:
  - ART-INTENT-[PROJECT]
  - ART-PRD-[PROJECT]
---

# User Story Map: [Project Name]

<!-- The USM breaks PRD requirements into implementable user stories organized
     by epic. Each story traces back to a persona (USR-xxx) and forward to
     domain entities (ENT-xxx).

     Full profile: this is a standalone file (usm.md).
     Lite profile: the USM is inlined inside prd.md; this file is not used. -->
<!-- Full profile only -->

## Users

<!-- Carry forward persona IDs from prd.md. Keep descriptions in sync. -->

| ID | Persona | Description |
| --- | --- | --- |
| USR-001 | Business owner | Manages appointments and business settings |
| USR-002 | Customer | Books and manages own appointments |

## Story Map

### Epic: EPIC-001 — [Epic Name]

<!-- Each epic groups related stories around a user goal.
     The Goal sentence should complete: "Users can ___." -->

**Goal:** [one sentence describing the epic's user goal]

<!-- Story table columns:
     - ID: stable identifier, format STORY-NNN
     - Story: short name
     - As a...: persona ID from Users table
     - I want to...: action the user takes
     - So that...: value delivered
     - Priority: P0 = must-have for launch, P1 = should-have, P2 = nice-to-have
     - Entities: domain entity IDs from dm.md that this story touches
     - Acceptance criteria: comma-separated AC-xxx IDs defined in the section below -->

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-001 | User registration | USR-001 | create an account with email | I can manage my business | P0 | ENT-001 | AC-001, AC-002 |
| STORY-002 | | USR-001 | | | P0 / P1 / P2 | ENT-xxx | AC-xxx |

### Epic: EPIC-002 — [Epic Name]

**Goal:**

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-003 | | USR-002 | | | P0 / P1 / P2 | ENT-xxx | AC-xxx |

<!-- Add more epics as needed. Keep epic numbering sequential: EPIC-003, EPIC-004, ... -->

## Acceptance Criteria

<!-- Detailed, testable criteria for each story. Referenced by AC-xxx IDs above.
     Each criterion should be verifiable with a concrete pass/fail test. -->

| ID | Criterion |
| --- | --- |
| AC-001 | Given a new user, when they submit the registration form with valid email and password, then an account is created and a verification email is sent |
| AC-002 | Given a new user, when they submit an already-registered email, then they see an error message |
| AC-003 | |

## Cross-Cutting Concerns

<!-- Stories that span multiple epics: authentication, authorization, audit
     logging, notifications, error handling, analytics, etc. -->

| ID | Story | Affects epics | Priority |
| --- | --- | --- | --- |
| STORY-999 | Audit logging for all mutations | EPIC-001, EPIC-002 | P0 |

## Story Dependencies

<!-- Note any ordering constraints between stories. These inform the task
     graph in plan.md and help the Agent sequence implementation work. -->

| Story | Depends on | Reason |
| --- | --- | --- |
| STORY-002 | STORY-001 | Cannot create appointments without user accounts |
| STORY-003 | | |
