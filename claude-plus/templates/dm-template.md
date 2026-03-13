---
artifact_id: ART-DM-[PROJECT]
artifact_type: dm
# status: draft | approved | approved-with-known-issues | stale | superseded
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

<!-- The domain model defines entities and relationships as seen by system
     users — NOT internal technical details. This is the semantic anchor of
     the methodology: every entity here is traced forward into spec.md data
     tables and backward from usm.md story Entities columns.

     Lite profile: single bounded context, no context map.
     Full profile: multiple bounded contexts with a context map. -->
<!-- Include in both Lite and Full profiles. -->

## Bounded Contexts

<!-- For Lite profile: use a single bounded context (BC-001).
     For Full profile: add multiple bounded contexts with a context map below. -->

### BC-001 — [Context Name]

**Description:** <!-- One sentence describing what this context owns.
     Example: "Owns user identity, authentication, and profile management." -->

**Aggregate roots:** ENT-001
<!-- List entity IDs that serve as aggregate roots — entry points for
     consistency boundaries. Other entities in this BC are accessed
     through their aggregate root. -->

#### Entities

<!-- Each entity gets a stable ID used by usm.md stories and spec.md data tables.
     Key attributes: list the most important fields (not an exhaustive schema).
     Invariants: reference INV-xxx IDs defined in the Invariants table below. -->

| ID | Entity | Description | Key attributes | Invariants |
| --- | --- | --- | --- | --- |
| ENT-001 | User | Registered system user | email, passwordHash, role, verified | INV-001 |
| ENT-002 | Appointment | A booked time slot | startTime, endTime, status, userId | INV-002, INV-003 |
| ENT-003 | | | | |

#### Invariants

<!-- Business rules that must NEVER be violated. These drive unit tests and
     validation logic. Each invariant references the entities it constrains. -->

| ID | Invariant | Applies to |
| --- | --- | --- |
| INV-001 | Email must be unique across all users | ENT-001 |
| INV-002 | Appointment endTime must be after startTime | ENT-002 |
| INV-003 | No two appointments for the same provider may overlap | ENT-002 |

#### Relationships

<!-- How entities relate. Cardinality: 1:1, 1:N, N:M.
     These drive database schema design in spec.md. -->

| From | Relationship | To | Cardinality | Description |
| --- | --- | --- | --- | --- |
| ENT-001 | has many | ENT-002 | 1:N | A user can have many appointments |
| ENT-002 | belongs to | ENT-001 | N:1 | Each appointment belongs to one user |

## Domain Events

<!-- Events that capture meaningful state changes in the domain.
     Triggered by: what action causes the event.
     Consumers: who/what reacts to it (other modules, notification service, etc.). -->
<!-- Include in both Lite and Full profiles. -->

| ID | Event | Triggered by | Data | Consumers |
| --- | --- | --- | --- | --- |
| EVT-001 | UserRegistered | User signs up | { userId, email } | Notification service |
| EVT-002 | AppointmentBooked | Customer books slot | { appointmentId, userId, slot } | Calendar sync, SMS reminder |
| EVT-003 | | | | |

<!-- Full profile only: add more bounded contexts below -->
<!-- ### BC-002 — [Context Name] -->
<!-- ... same structure as BC-001 ... -->

## Context Map (Full Profile Only)

<!-- How bounded contexts relate to each other.
     Relationship types: Customer-Supplier, Shared Kernel, Anticorruption Layer, etc.
     Integration pattern: API calls, async events, shared DB (avoid if possible). -->
<!-- Full profile only -->

| Upstream BC | Downstream BC | Relationship | Integration pattern |
| --- | --- | --- | --- |
| BC-001 | BC-002 | Customer-Supplier | REST API |

## Glossary

<!-- Domain terms with precise definitions to prevent ambiguity.
     Critical for aligning the team and the Agent on terminology. -->

| Term | Definition |
| --- | --- |
| Slot | A bookable time window defined by start and end times |
| No-show | An appointment where the customer did not arrive and did not cancel |
