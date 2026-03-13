---
artifact_id: ART-PRD-[PROJECT]
artifact_type: prd
# status: draft | approved | approved-with-known-issues | stale | superseded
status: draft
owner: [owner]
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-INTENT-[PROJECT]
depends_on:
  - ART-INTENT-[PROJECT]
---

# Product Requirements Document: [Project Name]

<!-- The PRD translates the Intent into structured, traceable requirements.
     Every functional requirement here becomes the source-of-truth that
     downstream artifacts (USM, DM, Spec) trace back to.
     Include in both Lite and Full profiles. -->

## Overview

<!-- Summarize what is being built, for whom, and why now. 2-3 sentences.
     Example: "BookIt is an appointment-scheduling SaaS for small-business
     owners who currently juggle spreadsheets and phone calls. It reduces
     no-shows through automated reminders and lets customers self-serve." -->

## Users & Personas

<!-- Carry forward from intent.md and elaborate. Each persona gets a stable ID
     (USR-001, USR-002, ...) that stories and requirements reference. -->

| ID | Persona | Description | Primary goals |
| --- | --- | --- | --- |
| USR-001 | Business owner | Manages appointments and business settings | Reduce no-shows, save admin time |
| USR-002 | Customer | Books and manages own appointments | Quick booking, easy rescheduling |

## Goals

<!-- High-level product goals that requirements ladder up to. -->

| ID | Goal | Success signal |
| --- | --- | --- |
| GOAL-001 | | |

## Success Metrics

<!-- Measurable indicators tied to goals. -->

| ID | Metric | Target |
| --- | --- | --- |
| METRIC-001 | | |

## Functional Requirements

<!-- Each row is a traceable requirement. Priority uses P0 (must-have for launch),
     P1 (should-have), P2 (nice-to-have). The Users column references persona IDs.
     Acceptance criteria are plain-language summaries — detailed criteria live in usm.md. -->

| ID | Requirement | Priority | Users | Acceptance criteria |
| --- | --- | --- | --- | --- |
| PRD-FR-001 | User registration with email and password | P0 | USR-001, USR-002 | User can sign up, receives verification email, can log in |
| PRD-FR-002 | Appointment booking from available slots | P0 | USR-002 | Customer sees available slots and can book one |
| PRD-FR-003 | | P0 / P1 / P2 | USR-001 | [plain-language acceptance summary] |

## Non-Functional Requirements

<!-- Performance, scalability, security, accessibility, compliance, etc.
     Each NFR gets a stable ID referenced by spec.md security/observability tables. -->

| ID | Requirement | Target | Measurement |
| --- | --- | --- | --- |
| NFR-001 | Page load time | < 2 s on 3G | Lighthouse performance score |
| NFR-002 | Uptime | 99.9 % | Monthly availability report |
| NFR-003 | | | |

## User Story Map (Lite Profile — inline)

<!-- For Lite profile, the USM is included here instead of a separate usm.md.
     For Full profile, replace this section with:
       "See [usm.md](usm.md) for the full User Story Map."
     This avoids duplication across files. -->
<!-- Full profile only: delete this section and reference usm.md instead. -->

### Epic: EPIC-001 — [Epic Name]

| ID | Story | As a... | I want to... | So that... | Priority | Entities |
| --- | --- | --- | --- | --- | --- | --- |
| STORY-001 | User registration | USR-001 | create an account | I can manage my business | P0 | ENT-001 |
| STORY-002 | | USR-001 | | | P0 / P1 / P2 | ENT-xxx |

### Epic: EPIC-002 — [Epic Name]

| ID | Story | As a... | I want to... | So that... | Priority | Entities |
| --- | --- | --- | --- | --- | --- | --- |
| STORY-003 | | USR-002 | | | P0 / P1 / P2 | ENT-xxx |

## Scope Boundaries

### In Scope

<!-- Features and capabilities included in the current version. -->

-

### Out Of Scope

<!-- Explicitly excluded to prevent scope creep. -->

-

### Future Considerations

<!-- Features deferred to a later version but worth noting now. -->

-

## Risks & Open Questions

<!-- Track uncertainties, technical risks, and decisions that need resolution.
     Severity: High = blocks launch, Medium = degrades quality, Low = cosmetic. -->

| ID | Risk / Question | Severity | Mitigation / Status |
| --- | --- | --- | --- |
| RISK-001 | Third-party SMS provider rate limits | Medium | Evaluate Twilio vs MessageBird; add retry queue |
| RISK-002 | | High / Medium / Low | |
