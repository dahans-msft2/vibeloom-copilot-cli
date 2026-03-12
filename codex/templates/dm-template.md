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

| ID | Invariant | Applies to |
| --- | --- | --- |
| INV-001 | | ENT-001 |

#### Relationships

| From | Relationship | To | Cardinality | Description |
| --- | --- | --- | --- | --- |
| ENT-001 | | ENT-002 | | |

## Domain Events

| ID | Event | Triggered by | Data | Consumers |
| --- | --- | --- | --- | --- |
| EVT-001 | | | | |

## Glossary

| Term | Definition |
| --- | --- |
| | |
