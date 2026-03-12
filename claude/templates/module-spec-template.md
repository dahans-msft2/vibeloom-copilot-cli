---
status: draft
owner: module-spec
approved-by:
last-reviewed: YYYY-MM-DD
upstream-refs:
  - artifact: ../../dm.md
    version-hash:
  - artifact: ../../spec.md
    version-hash:
profile: full
module-id: SPEC-MOD-xx
bounded-context: BCx
---

# Module Spec: mod-[name]

**Module ID:** SPEC-MOD-xx
**Bounded Context:** BCx — [Context Name]
**Responsibility:** <!-- One sentence -->

## Domain Entities Owned

<!-- Entities from dm.md that this module is responsible for -->

| Entity ID | Entity | Role in this module |
|-----------|--------|-------------------|
| DM-BCx-Exx | | Aggregate root / Entity / Value object |

## Interface Contract

### Exports (other modules may depend on these)

#### APIs

| ID | Signature | Description | Returns | Errors |
|----|-----------|-------------|---------|--------|
| MOD-{name}-API-01 | `functionName(param: Type) → ReturnType` | | | |

#### Events

| ID | Event | Payload | Description |
|----|-------|---------|-------------|
| MOD-{name}-EVT-01 | EventName | `{ field: Type }` | |

### Imports (this module depends on these)

| From module | Interface ID | Signature | Usage |
|-------------|-------------|-----------|-------|
| mod-{other} | MOD-{other}-API-xx | `functionName(param: Type) → ReturnType` | |

### Shared Types Used

| Type | Owner module | Used as |
|------|-------------|--------|
| | mod-{owner} | |

## Internal Architecture

### Key Components

| Component | Responsibility |
|-----------|---------------|
| | |

### Data Model

| Entity | Storage details | Key fields | Indexes |
|--------|----------------|------------|---------|
| | | | |

### Internal APIs / Routes

| Method | Path | Handler | Description | Stories |
|--------|------|---------|-------------|---------|
| | | | | USM-xx |

## Module-Specific Decisions

<!-- Any technical decisions specific to this module that differ from or elaborate on the root spec -->

## Testing Notes

<!-- Module-specific testing considerations -->

| Test type | Focus | Key scenarios |
|-----------|-------|--------------|
| Unit | | |
| Integration | | |
| Contract | Interface compliance | |
