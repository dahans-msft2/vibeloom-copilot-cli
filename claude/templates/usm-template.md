---
status: draft
owner: usm
approved-by:
last-reviewed: YYYY-MM-DD
upstream-refs:
  - artifact: intent.md
    version-hash:
  - artifact: prd.md
    version-hash:
---

# User Story Map: [Project Name]

<!-- This file is used in Full profile only. In Lite profile, the USM is inlined in prd.md. -->

## Users

| ID | Persona | Description |
|----|---------|-------------|
| USR-01 | | |
| USR-02 | | |

## Story Map

### Epic: E01 — [Epic Name]

**Goal:** <!-- One sentence describing the epic's user goal -->

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
|----|-------|---------|-------------|-----------|----------|----------|---------------------|
| USM-E01-S01 | | USR-xx | | | P0/P1/P2 | DM-xx | |
| USM-E01-S02 | | USR-xx | | | P0/P1/P2 | DM-xx | |

### Epic: E02 — [Epic Name]

**Goal:**

| ID | Story | As a... | I want to... | So that... | Priority | Entities | Acceptance criteria |
|----|-------|---------|-------------|-----------|----------|----------|---------------------|
| USM-E02-S01 | | USR-xx | | | P0/P1/P2 | DM-xx | |

<!-- Add more epics as needed -->

## Cross-Cutting Concerns

<!-- Stories that span multiple epics: auth, notifications, audit logging, etc. -->

| ID | Story | Affects epics | Priority |
|----|-------|--------------|----------|
| USM-CC-S01 | | E01, E02 | P0/P1/P2 |

## Story Dependencies

<!-- Note any ordering constraints between stories -->

| Story | Depends on | Reason |
|-------|-----------|--------|
| USM-E02-S01 | USM-E01-S01 | |
