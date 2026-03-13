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

### BC-001 — [Context Name]

**Description:** [one sentence]

**Aggregate roots:** ENT-001

#### Entities

| ID | Entity | Description | Key attributes | Invariants |
| --- | --- | --- | --- | --- |
| ENT-001 | | | | INV-001 |

#### Invariants

| ID | Invariant | Applies to | Driven by stories / requirements |
| --- | --- | --- | --- |
| INV-001 | | ENT-001 | STORY-001, PRD-FR-001 |

#### Relationships

| From | Relationship | To | Cardinality | Description |
| --- | --- | --- | --- | --- |
| ENT-001 | | ENT-002 | | |

#### Domain Events

| ID | Event | Triggered by | Data | Consumers |
| --- | --- | --- | --- | --- |
| EVT-001 | | | | |

### BC-002 — [Context Name]

<!-- Repeat only when the project genuinely has another semantic boundary. -->

## Context Map (Full Profile)

| Upstream BC | Downstream BC | Relationship | Integration pattern |
| --- | --- | --- | --- |
| BC-001 | BC-002 | Customer-Supplier / Partnership / Conformist | API / Event / Shared schema |

## Glossary

| Term | Definition |
| --- | --- |
| | |
