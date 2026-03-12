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
- [owned schema, routes, jobs, or files]

## Domain Ownership

| Entity ID | Entity | Role |
| --- | --- | --- |
| ENT-001 | | Aggregate root / entity / projection |

## Allowed Dependencies

| Module | Why |
| --- | --- |
| MOD-[OTHER] | |

## Interface Contracts

### Owned Interfaces

| ID | Type | Signature / Shape | Consumers |
| --- | --- | --- | --- |
| IFACE-001 | API / Event / Schema | | MOD-[OTHER] |

### Imported Interfaces

| From | Interface ID | Usage |
| --- | --- | --- |
| MOD-[OTHER] | IFACE-002 | |

## Data And Storage

| Entity | Storage | Key fields | Notes |
| --- | --- | --- | --- |
| ENT-001 | | | |

## Testing Notes

| Test type | Focus |
| --- | --- |
| Unit | |
| Integration | |
| Contract | |
