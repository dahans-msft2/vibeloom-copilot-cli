---
artifact_id: ART-MODULE-SPEC-[MODULE]
artifact_type: spec
# status: draft | approved | approved-with-known-issues | stale | superseded
status: draft
owner: [module-owner]
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-SPEC-[PROJECT]
  - ART-DM-[PROJECT]
depends_on:
  - ART-SPEC-[PROJECT]
  - ART-DM-[PROJECT]
profile: full
module_id: MOD-[MODULE]
bounded_context: BC-[XXX]
---

# Module Spec: [Module Name]

<!-- A module spec details one module from the root spec.md Module Decomposition
     table. It owns a slice of the domain (one bounded context) and defines
     its interface contracts so other modules can depend on it safely.

     This file is used in Full profile only. Lite profile projects have a
     single implicit module and do not need module specs. -->
<!-- Full profile only -->

**Module ID:** MOD-[MODULE]
**Bounded Context:** BC-[XXX] — [Context Name]

## Responsibility

<!-- One sentence describing the module's owned capability.
     Example: "Owns user identity, authentication, and session management." -->

## Owned Write Surface

<!-- Files and directories this module is allowed to create or modify.
     The AGENTS.md for this module enforces these boundaries. -->

- `modules/[module]/...`
- [owned schema, routes, jobs, or files]

## Domain Ownership

<!-- Entities from dm.md that this module is responsible for.
     Role: Aggregate root = consistency boundary entry point.
     Entity = owned but accessed through an aggregate root.
     Projection = read-only view of another module's entity. -->

| Entity ID | Entity | Role |
| --- | --- | --- |
| ENT-001 | User | Aggregate root |
| ENT-002 | UserProfile | Entity |
| ENT-003 | | Aggregate root / entity / projection |

## Allowed Dependencies

<!-- Other modules this module may import from. Keep this list minimal.
     If you need to add a dependency, check that it does not create a cycle
     in the root spec.md Dependency DAG. -->

| Module | Why |
| --- | --- |
| MOD-[OTHER] | Need user context for authorization checks |

## Interface Contracts

### Owned Interfaces

<!-- Interfaces this module exports for other modules to consume.
     Changing these requires updating all consumers and their module specs. -->

| ID | Type | Signature / Shape | Consumers |
| --- | --- | --- | --- |
| IFACE-001 | API | `getCurrentUser(token: string) → User` | MOD-booking |
| IFACE-002 | Event | `UserRegistered { userId, email, role }` | MOD-notification |
| IFACE-003 | Schema | `User { id, email, role, verified }` | MOD-booking (read-only) |

### Imported Interfaces

<!-- Interfaces this module consumes from other modules. -->

| From | Interface ID | Usage |
| --- | --- | --- |
| MOD-[OTHER] | IFACE-xxx | [how this module uses the imported interface] |

## Data And Storage

<!-- Technical storage details for the entities this module owns.
     Derived from dm.md entities → spec.md data model. -->

| Entity | Storage | Key fields | Notes |
| --- | --- | --- | --- |
| ENT-001 | PostgreSQL `users` table | id, email, password_hash, role | email unique index |
| ENT-002 | PostgreSQL `user_profiles` table | id, user_id, display_name | FK to users |

## Internal Architecture

<!-- Implementation details specific to this module.
     These are NOT part of the interface contract. -->
<!-- Full profile only -->

### Key Components

| Component | Responsibility |
| --- | --- |
| AuthService | Login, registration, token validation |
| UserRepository | Data access for User and UserProfile entities |

### Internal APIs / Routes

<!-- Routes handled by this module. Stories column traces to usm.md. -->

| Method | Path | Handler | Description | Stories |
| --- | --- | --- | --- | --- |
| POST | /api/auth/register | AuthService.register | Create new user account | STORY-001 |
| POST | /api/auth/login | AuthService.login | Authenticate and return token | STORY-002 |

## Module-Specific Decisions

<!-- Any technical decisions specific to this module that differ from or
     elaborate on the root spec. Document the WHY, not just the WHAT. -->

## Testing Notes

<!-- Module-specific testing considerations. Contract tests verify that
     this module's owned interfaces behave as documented above. -->

| Test type | Focus | Key scenarios |
| --- | --- | --- |
| Unit | Domain invariants | INV-001: email uniqueness; INV-002: password strength |
| Integration | Database operations | CRUD for users and profiles; concurrent registration |
| Contract | Interface compliance | IFACE-001 returns correct User shape; IFACE-002 event payload |
