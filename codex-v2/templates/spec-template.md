---
artifact_id: ART-SPEC-[PROJECT]
artifact_type: spec
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
  - ART-DM-[PROJECT]
depends_on:
  - ART-INTENT-[PROJECT]
  - ART-PRD-[PROJECT]
  - ART-USM-[PROJECT]
  - ART-DM-[PROJECT]
profile: lite | full
---

# Technical Spec: [Project Name]

<!-- The spec is the technical implementation blueprint. It translates the
     approved semantics from upstream artifacts (intent, PRD, USM, DM) into
     concrete runtime architecture, data models, APIs, and deployment design.

     Lite profile: single module, simpler structure.
     Full profile: multi-module with interface contracts and dependency DAG. -->
<!-- Include in both Lite and Full profiles. -->

## Purpose

<!-- Describe the runtime and implementation design that realizes the approved
     semantics. 1-2 sentences.
     Example: "This spec defines the technical architecture for BookIt, a
     Next.js + PostgreSQL monolith deployed on Vercel with Supabase auth." -->

## Repository Layout

<!-- Map the key files in this governed repo and their roles. -->

| Path | Responsibility |
| --- | --- |
| `constitution.md` | Universal project rules and ID grammar |
| `intent.md` | Product vision and constraints |
| `prd.md` | Functional and non-functional requirements |
| `usm.md` | User stories organized by epic |
| `dm.md` | Domain entities, invariants, and relationships |
| `spec.md` | This file — technical architecture and design |

## Profiles

<!-- Describe what each profile means for THIS project. -->

### `lite`

<!-- Single bounded context, no module decomposition, USM inlined in prd.md. -->

-

### `full`

<!-- Multiple bounded contexts, module decomposition with interface contracts,
     separate usm.md, module-level AGENTS.md files. -->

-

## Artifact Responsibilities

<!-- Clarify the authority of each artifact in the governance chain. -->

| Artifact | Responsibility |
| --- | --- |
| `intent.md` | Captures the product vision; seed for all downstream artifacts |
| `prd.md` | Source of truth for requirements; every PRD-FR-xxx must be addressed |
| `usm.md` | Breaks requirements into stories; traces to entities and acceptance criteria |
| `dm.md` | Defines the semantic model; every entity/invariant drives data design |
| `spec.md` | Technical realization; bridges domain model to code architecture |

## Tech Stack

<!-- Choose technologies for each layer. Rationale explains WHY this choice
     over alternatives. This table is referenced by AGENTS.md for code generation. -->
<!-- Include in both Lite and Full profiles. -->

| Layer | Technology | Version | Rationale |
| --- | --- | --- | --- |
| Language | TypeScript | 5.x | Type safety, ecosystem |
| Framework | Next.js | 14.x | SSR + API routes in one repo |
| Database | PostgreSQL | 16 | Relational, ACID, mature |
| ORM / Data access | Prisma | 5.x | Type-safe queries, migrations |
| Auth | Supabase Auth | | Managed auth, social logins |
| Testing | Vitest + Playwright | | Unit + E2E coverage |
| Build / Bundle | Next.js built-in | | Zero-config |
| Deployment | Vercel | | Git-push deploys, edge functions |

## Runtime Architecture

<!-- High-level description of how the system runs: monolith vs microservices,
     client-server split, serverless functions, etc. -->

### Component Overview

<!-- List major runtime components and their responsibilities.
     Example: web client, API server, background worker, database. -->

| Component | Responsibility | Technology |
| --- | --- | --- |
| Web client | User interface, client-side routing | Next.js (React) |
| API layer | Business logic, data access | Next.js API routes |
| Database | Persistent storage | PostgreSQL |
| | | |

### Communication Patterns

<!-- How components talk to each other: REST, GraphQL, WebSockets, message queues, etc.
     Example: "The web client communicates with the API layer via REST over HTTPS.
     Background jobs are triggered via a Redis-backed queue." -->

## Data Architecture

### Data Model

<!-- Technical data model derived from dm.md. Maps domain entities to storage.
     Entity column references dm.md entity IDs for traceability. -->

| Entity (dm.md) | Storage | Table/Collection | Key fields | Indexes |
| --- | --- | --- | --- | --- |
| ENT-001 (User) | PostgreSQL | users | id, email, password_hash, role, verified | email (unique) |
| ENT-002 (Appointment) | PostgreSQL | appointments | id, start_time, end_time, status, user_id | user_id, start_time |

### Data Flow

<!-- How data moves through the system for key operations.
     Example: "Booking flow: Client POST /api/appointments → validate slot
     availability (INV-003) → insert row → emit AppointmentBooked event
     → trigger SMS reminder job." -->

## API Design

### External APIs

<!-- Public-facing APIs. Each row traces to USM stories via the Stories column. -->

| ID | Method | Path | Description | Request | Response | Auth | Stories |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SPEC-API-01 | POST | /api/auth/register | Register new user | { email, password } | { user, token } | None | STORY-001 |
| SPEC-API-02 | POST | /api/appointments | Book appointment | { slotId, notes } | { appointment } | Bearer | STORY-003 |
| SPEC-API-03 | | | | | | | STORY-xxx |

### Internal APIs (Full Profile)

<!-- APIs between modules — see Module Interface Contracts below. -->
<!-- Full profile only -->

## Security

<!-- Map security concerns to approaches and trace to NFR IDs from prd.md. -->

| Concern | Approach | NFR ref |
| --- | --- | --- |
| Authentication | JWT via Supabase Auth | NFR-001 |
| Authorization | Role-based (owner, customer, admin) | NFR-002 |
| Data protection | AES-256 at rest, TLS 1.3 in transit | NFR-003 |
| Input validation | Zod schemas on all API inputs | NFR-004 |

## Observability

<!-- How the system is monitored. Trace to NFR IDs. -->

| Signal | Implementation | NFR ref |
| --- | --- | --- |
| Logging | Structured JSON logs via Pino | NFR-xxx |
| Metrics | Vercel Analytics + custom counters | NFR-xxx |
| Tracing | OpenTelemetry spans on API routes | NFR-xxx |
| Health checks | GET /api/health returning DB status | NFR-xxx |

## Allowed Durable Projections

<!-- Mechanically checkable data derived from canonical artifacts.
     These are NOT canonical — they can be regenerated at any time. -->

| Projection | Purpose |
| --- | --- |
| Trace index | Maps story IDs → code locations for coverage checks |
| Dependency/stale graph | Tracks which artifacts are stale when upstream changes |
| Interface/schema manifests | Auto-generated API schemas and type definitions |

## Module Decomposition (Full Profile)

<!-- For Lite profile: omit this section — the whole app is one module.
     For Full profile: list modules derived from dm.md bounded contexts.
     Each module gets its own directory and module-spec. -->
<!-- Full profile only -->

| ID | Module | Bounded Context | Responsibility | Directory |
| --- | --- | --- | --- | --- |
| MOD-001 | mod-auth | BC-001 | User identity and authentication | modules/mod-auth/ |
| MOD-002 | mod-booking | BC-002 | Appointment scheduling and management | modules/mod-booking/ |

### Dependency DAG

<!-- Which modules depend on which. Must be acyclic.
     If you find a cycle, refactor or extract a shared module. -->

```
MOD-002 → MOD-001 (booking needs auth context)
```

### Module Interface Contracts (Full Profile)

<!-- Summary of all cross-module interfaces. Detailed contracts go in each
     module's module-spec. -->

| From | To | Interface | Type |
| --- | --- | --- | --- |
| MOD-002 | MOD-001 | getCurrentUser() | Sync API |
| MOD-001 | * | UserRegistered event | Async event |

## Reconcile Engine

<!-- How the system detects and resolves drift between artifacts. -->

### Inputs

-

### Behavior

1.
2.
3.

## Greenfield Flow

<!-- Steps for bootstrapping a new project from scratch. -->

1.
2.
3.

## Brownfield Import

### Purpose

<!-- Bootstrap governance for unmanaged codebases. -->

### Behavior

1.
2.
3.

## Steady-State Bugfix Path

<!-- How bugs are traced back to stories/requirements and fixed. -->

1.
2.
3.

## Context-Loading Algorithm

### Always Load

-

### Load Conditionally

-

### Escalation Rules

-

## Stale Propagation Rules

<!-- When an upstream artifact changes, which downstream artifacts become stale. -->

-

## Deployment Architecture

<!-- Include in both Lite and Full profiles. -->

| Aspect | Approach |
| --- | --- |
| Hosting | Vercel (serverless) |
| Containerization | None (serverless functions) |
| CI/CD | GitHub Actions → Vercel deploy |
| Environments | dev, staging, production |
| Scaling | Auto-scale via Vercel |

## Error Handling Strategy

<!-- How errors propagate, what gets logged, what the user sees.
     Example: "API errors return RFC 7807 problem details. Unexpected errors
     log full stack via Pino and return generic 500 to client." -->

## Future Command Surface

<!-- CLI commands the governance tooling will support. -->

| Command | Purpose |
| --- | --- |
| `init` | Scaffold a new governed project |
| `import` | Bootstrap governance for existing codebase |
| `generate` | Generate downstream artifacts from upstream |
| `approve` | Mark an artifact as approved |
| `develop` | Generate plan and AGENTS.md for a change |
| `eval` | Run structural and semantic checks |
| `reconcile` | Detect and fix drift between artifacts |
| `status` | Show artifact states and stale edges |

## Testing Strategy

<!-- Map test levels to their sources in the governance chain.
     Unit tests derive from dm.md invariants.
     Integration tests derive from spec.md interfaces.
     E2E tests derive from usm.md stories and acceptance criteria. -->
<!-- Include in both Lite and Full profiles. -->

| Level | Focus | Source |
| --- | --- | --- |
| Structural eval | Artifact schema compliance | constitution.md rules |
| Semantic eval | Cross-artifact consistency | Trace chain integrity |
| Unit | Individual functions / invariants | dm.md invariants (INV-xxx) |
| Integration | Module boundaries / APIs | spec.md interfaces (SPEC-API-xxx) |
| E2E | User workflows | usm.md stories (STORY-xxx) |
| Contract | Cross-module APIs | Module interface contracts (IFACE-xxx) |
| Reconcile tests | Drift detection accuracy | Stale propagation rules |
| Context-loading tests | Correct artifact loading | Context-loading algorithm |
