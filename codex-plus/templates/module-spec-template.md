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

## Responsibility

<!-- One sentence describing the module's owned capability. -->

## Owned Write Surface

- `modules/[module]/...`
- [owned routes, jobs, storage objects, or files]

## Domain Ownership

| Entity ID | Entity | Role |
| --- | --- | --- |
| ENT-001 | | Aggregate root / entity / projection |

## Allowed Dependencies

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

| Type | Name | Entry point | Stories |
| --- | --- | --- | --- |
| Route / Job / Handler | | | STORY-001 |

## Data And Storage

| Entity | Storage | Key fields | Indexes / Constraints | Notes |
| --- | --- | --- | --- | --- |
| ENT-001 | | | | |

## Module-Specific Decisions

| Decision | Reason | Tradeoff |
| --- | --- | --- |
| | | |

## Testing Notes

| Test type | Focus | Key scenarios |
| --- | --- | --- |
| Unit | | |
| Integration | | |
| Contract | Owned interfaces | |
| Regression | Known bugfix risks | |
