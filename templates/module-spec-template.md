---
artifact_id: ART-MODULE-SPEC-[MODULE]
artifact_type: spec
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

**Module ID:** MOD-[MODULE]  
**Bounded Context:** BC-[XXX] — [Context Name]

## Responsibility

<!-- One sentence describing the module's owned capability.
     Example: "Owns user identity, authentication, and session management." -->

## Owned Write Surface

<!-- Files, routes, jobs, tables, or schema objects this module may change. -->

- `modules/[module]/...`
- [owned routes, jobs, storage objects, or files]

## Domain Ownership

<!-- Aggregate root means the module owns the consistency boundary.
     Projection means read-only data imported from another owner. -->

| Entity ID | Entity | Role |
| --- | --- | --- |
| ENT-001 | | Aggregate root / entity / projection |

## Allowed Dependencies

<!-- Keep this list minimal and justify every dependency. -->

| Module | Why |
| --- | --- |
| MOD-[OTHER] | |

## Interface Contracts

### Owned APIs

| ID | Signature | Description | Returns | Errors | Consumers |
| --- | --- | --- | --- | --- | --- |
| IFACE-001 | `functionName(param: Type) -> Result` | | | | MOD-[OTHER] |

### Owned Events

| ID | Event | Payload | Description | Consumers |
| --- | --- | --- | --- | --- |
| IFACE-002 | EventName | `{ field: Type }` | | MOD-[OTHER] |

### Owned Schemas

| ID | Schema | Purpose | Consumers |
| --- | --- | --- | --- |
| IFACE-003 | | | |

### Imported Interfaces

| From | Interface ID | Signature / Shape | Usage |
| --- | --- | --- | --- |
| MOD-[OTHER] | IFACE-004 | | |

### Shared Types Used

| Type | Owner module | Used as |
| --- | --- | --- |
| | MOD-[OTHER] | |

## Internal Architecture

### Key Components

| Component | Responsibility |
| --- | --- |
| | |

### Internal Routes / Jobs / Handlers

<!-- List internal entry points owned by this module. -->

| Type | Name | Entry point | Stories |
| --- | --- | --- | --- |
| Route / Job / Handler | | | STORY-001 |

## Data And Storage

<!-- Map owned entities to concrete storage. -->

| Entity | Storage | Key fields | Indexes / Constraints | Notes |
| --- | --- | --- | --- | --- |
| ENT-001 | | | | |

## Module-Specific Decisions

| Decision | Reason | Tradeoff |
| --- | --- | --- |
| | | |

## Testing Notes

<!-- Contract tests verify exported interfaces. Regression tests should cite
     the highest-risk user-visible or invariant-related scenarios. -->

| Test type | Focus | Key scenarios |
| --- | --- | --- |
| Unit | | |
| Integration | | |
| Contract | Owned interfaces | |
| Regression | Known bugfix risks | |
