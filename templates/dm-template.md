---
artifact_id: ART-DM-[PROJECT]
artifact_type: dm
status: draft
owner: [owner]
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-INTENT-[PROJECT]
  - ART-PRD-[PROJECT]
  - ART-USM-[PROJECT]
depends_on:
  - ART-INTENT-[PROJECT]
  - ART-PRD-[PROJECT]
  - ART-USM-[PROJECT]
---

# Domain Model: [Project Name]

## Bounded Contexts

<!-- The domain model is the semantic anchor of the methodology.
     Every entity here should trace backward to stories and forward to
     technical ownership in spec.md. -->

### BC-001 — [Context Name]

**Description:** [one sentence]

**Aggregate roots:** ENT-001

<!-- Aggregate roots define the main consistency boundaries. Other entities
     in the bounded context should usually be reached through them. -->

#### Entities

<!-- Key attributes should capture the important business shape, not the full
     technical schema. -->

| ID | Entity | Description | Key attributes | Invariants |
| --- | --- | --- | --- | --- |
| ENT-001 | | | | INV-001 |

#### Invariants

<!-- Invariants are business rules that must never be violated. -->

| ID | Invariant | Applies to | Driven by stories / requirements |
| --- | --- | --- | --- |
| INV-001 | | ENT-001 | STORY-001, PRD-FR-001 |

#### Relationships

<!-- Cardinality examples: 1:1, 1:N, N:M. -->

| From | Relationship | To | Cardinality | Description |
| --- | --- | --- | --- | --- |
| ENT-001 | | ENT-002 | | |

#### Domain Events

<!-- Domain events capture meaningful state changes, not implementation noise. -->

| ID | Event | Triggered by | Data | Consumers |
| --- | --- | --- | --- | --- |
| EVT-001 | | | | |

### BC-002 — [Context Name]

<!-- Repeat only when the project genuinely has another semantic boundary.
     In `lite`, keep one bounded context unless the semantics clearly split. -->

## Context Map (Full Profile)

<!-- Full profile only. Explain how bounded contexts relate and how they
     integrate: API, event, or shared schema. -->

| Upstream BC | Downstream BC | Relationship | Integration pattern |
| --- | --- | --- | --- |
| BC-001 | BC-002 | Customer-Supplier / Partnership / Conformist | API / Event / Shared schema |

## Glossary

<!-- Keep definitions crisp and stable. This table prevents language drift
     across PRD, USM, spec, and code. -->

| Term | Definition |
| --- | --- |
| | |
