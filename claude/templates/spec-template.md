---
status: draft
owner: spec
approved-by:
last-reviewed: YYYY-MM-DD
upstream-refs:
  - artifact: intent.md
    version-hash:
  - artifact: prd.md
    version-hash:
  - artifact: dm.md
    version-hash:
profile: lite | full
---

# Architecture & Design Spec: [Project Name]

## Tech Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Language | | | |
| Framework | | | |
| Database | | | |
| ORM / Data access | | | |
| Auth | | | |
| Testing | | | |
| Build / Bundle | | | |
| Deployment | | | |

## Runtime Architecture

<!-- High-level description of how the system runs: monolith vs microservices, client-server, etc. -->

### Component Overview

<!-- List major runtime components and their responsibilities -->

| Component | Responsibility | Technology |
|-----------|---------------|-----------|
| | | |

### Communication Patterns

<!-- How components talk to each other: REST, events, queues, etc. -->

## Data Architecture

### Data Model

<!-- Technical data model derived from dm.md. Maps domain entities to storage. -->

| Entity (dm.md) | Storage | Table/Collection | Key fields | Indexes |
|----------------|---------|-----------------|------------|---------|
| DM-BC1-E01 | | | | |

### Data Flow

<!-- How data moves through the system for key operations -->

## API Design

### External APIs

| ID | Method | Path | Description | Request | Response | Auth | Stories |
|----|--------|------|-------------|---------|----------|------|---------|
| SPEC-API-01 | | | | | | | USM-xx |

### Internal APIs (Full Profile)

<!-- APIs between modules — see Module Interface Contracts below -->

## Security

| Concern | Approach | NFR ref |
|---------|----------|---------|
| Authentication | | NFR-xx |
| Authorization | | NFR-xx |
| Data protection | | NFR-xx |
| Input validation | | NFR-xx |

## Observability

| Signal | Implementation | NFR ref |
|--------|---------------|---------|
| Logging | | NFR-xx |
| Metrics | | NFR-xx |
| Tracing | | NFR-xx |
| Health checks | | NFR-xx |

## Module Decomposition (Full Profile)

<!-- For Lite profile: omit this section — the whole app is one module. -->
<!-- For Full profile: list modules derived from dm.md bounded contexts. -->

| ID | Module | Bounded Context | Responsibility | Directory |
|----|--------|----------------|----------------|-----------|
| SPEC-MOD-01 | mod-{name} | BC1 | | modules/mod-{name}/ |
| SPEC-MOD-02 | mod-{name} | BC2 | | modules/mod-{name}/ |

### Dependency DAG

<!-- Which modules depend on which. Must be acyclic. -->

```
SPEC-MOD-01 → SPEC-MOD-02
SPEC-MOD-01 → SPEC-MOD-03
SPEC-MOD-03 → SPEC-MOD-02
```

### Module Interface Contracts (Full Profile)

<!-- Summary of all cross-module interfaces. Detailed contracts go in each module's spec.md. -->

| From | To | Interface | Type |
|------|----|-----------|------|
| SPEC-MOD-01 | SPEC-MOD-02 | checkAvailability() | Sync API |
| SPEC-MOD-01 | SPEC-MOD-03 | chargePayment() | Sync API |
| SPEC-MOD-01 | * | OrderPlaced event | Async event |

## Deployment Architecture

| Aspect | Approach |
|--------|----------|
| Hosting | |
| Containerization | |
| CI/CD | |
| Environments | |
| Scaling | |

## Error Handling Strategy

<!-- How errors propagate, what gets logged, what the user sees -->

## Testing Strategy

| Level | Scope | Tools | Derived from |
|-------|-------|-------|-------------|
| Unit | Individual functions/classes | | dm.md invariants |
| Integration | Module boundaries | | spec.md interfaces |
| E2E | User workflows | | usm.md stories |
| Contract | Cross-module APIs | | Interface contracts |
