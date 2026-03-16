---
artifact_id: ART-SPEC-[PROJECT]
artifact_type: spec
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

<!-- This template is for a concrete governed project spec.
     It requires one selected profile.
     It is not the shape used by the checked-in VibeLoom methodology-package meta-spec. -->

# Technical Spec: [Project Name]

## Purpose

<!-- Describe the runtime and implementation design that realizes the approved
     semantics. Explain the runtime shape in 1-2 sentences.
     Example: "This spec defines a TypeScript monolith with clear module
     boundaries, PostgreSQL storage, and explicit interface ownership." -->

## Selected Profile

- `lite` or `full`:
- Why this profile is the right coordination boundary:
- Note: both profiles still use separate `intent.md`, `prd.md`, `usm.md`, `dm.md`, and `spec.md`.

## Tech Stack

| Layer | Technology | Version | Rationale |
| --- | --- | --- | --- |
| Language | | | |
| Framework | | | |
| Database | | | |
| Data access | | | |
| Auth | | | |
| Testing | | | |
| Deployment | | | |

## Runtime Architecture

### Overview

<!-- Monolith, service-oriented, client-server, worker model, or similar.
     Name the runtime boundaries and why they are sufficient for the approved
     requirements and invariants. -->

### Components

| Component | Responsibility | Technology | Stories / Requirements |
| --- | --- | --- | --- |
| | | | STORY-001, PRD-FR-001 |

### Communication Patterns

| From | To | Pattern | Notes |
| --- | --- | --- | --- |
| | | Sync API / Event / Queue | |

## Data Architecture

### Storage Mapping

| Entity ID | Storage | Table / Collection / Stream | Key fields | Notes |
| --- | --- | --- | --- | --- |
| ENT-001 | | | | |

### Data Flow

| Flow | Trigger | Steps | Consistency / Transaction Notes |
| --- | --- | --- | --- |
| FLOW-001 | STORY-001 | | |

## API And Interface Design

### External APIs

| ID | Method / Event | Path / Topic | Description | Auth | Stories |
| --- | --- | --- | --- | --- | --- |
| API-001 | | | | | STORY-001 |

### Internal Interfaces

| ID | Owner | Type | Signature / Shape | Consumers |
| --- | --- | --- | --- | --- |
| API-002 | MOD-[MODULE] | API / Event / Schema | | MOD-[OTHER] |

### Error Handling Strategy

| Scenario | Handling strategy | Trace to requirement / invariant |
| --- | --- | --- |
| validation failure | | INV-001 |
| downstream dependency failure | | NFR-001 |
| idempotent retry / duplicate submission | | STORY-001 |

## Upstream Trace Matrix

| Spec area | PRD refs | STORY refs | ENT refs | INV refs |
| --- | --- | --- | --- | --- |
| runtime architecture | PRD-FR-001 | STORY-001 | ENT-001 | INV-001 |
| data and storage | PRD-FR-001 | STORY-001 | ENT-001 | INV-001 |
| interfaces and ownership | PRD-FR-001 | STORY-001 | ENT-001 | INV-001 |
| context loading | PRD-FR-001 | STORY-001 | ENT-001 | INV-001 |
| reconcile and bugfix behavior | PRD-FR-001 | STORY-001 | ENT-001 | INV-001 |

## Security And Trust Boundaries

| Concern | Approach | Requirement / Invariant |
| --- | --- | --- |
| Authentication | | NFR-001 |
| Authorization | | PRD-FR-001 |
| Input validation | | INV-001 |
| Auditability | | NFR-002 |

## Observability

| Signal | Implementation | Requirement |
| --- | --- | --- |
| Logging | | NFR-001 |
| Metrics | | NFR-002 |
| Tracing | | NFR-003 |
| Health checks | | NFR-004 |

## Deployment Architecture

| Aspect | Approach | Notes |
| --- | --- | --- |
| Hosting | | |
| Environments | | |
| CI/CD | | |
| Scaling | | |
| Secrets management | | |

## Module And Ownership Model

### Module Responsibilities

| Module ID | Bounded Context | Responsibility | Owned write surface | Directory |
| --- | --- | --- | --- | --- |
| MOD-[MODULE] | BC-001 | | | `modules/[module]/` |

### Dependency DAG

```text
MOD-[MODULE] -> MOD-[OTHER]
```

### Interface Ownership Rules

- Each public API, event, or schema has exactly one owning module.
- Cross-module dependencies must stay acyclic.
- New shared boundaries require an explicit spec amendment before implementation.
- `lite` may collapse into one application module, but ownership is still explicit.

## Context-Loading Notes

Exact routine loading belongs in the runtime references for the active environment. Use this section to capture the intended starting slice and escalation pattern for this concrete repo rather than a second command-level load catalog.

### Default Starting Slice

- this `spec.md`
- the active module spec when a module boundary is touched
- the relevant trace slice when touched IDs, stale impact, or downstream coverage are in question
- the derived `AGENTS.md` for the task scope when it exists and reduces execution ambiguity

### Load Conditionally

- `prd.md` and `usm.md` slices for behavior changes
- `dm.md` slices for concept and invariant changes
- neighboring module specs and interface manifests for cross-boundary work

### Surface Notes

- In `code-first`, this spec and the touched module specs are the default visible layer.
- If workflow, concept, invariant, interface, or NFR ambiguity appears, surface the relevant `prd/usm/dm` slices explicitly.

### Escalate When

- ownership is ambiguous
- the change touches multiple bounded contexts
- a bugfix reveals a semantic contradiction
- an interface or invariant must be interpreted exactly and the current slice is only summarized

## Reconcile Behavior

### Inputs

- touched paths or artifacts, e.g. `spec.md`, `modules/billing/**`
- referenced IDs, e.g. `STORY-014`, `ENT-009`, `API-004`
- active profile
- current dependency or stale graph
- current approved upstream slice

### Behavior

1. classify the change
2. run one up-pass against upstream truth
3. choose one proposal path
4. run one down-pass through affected downstream artifacts
5. run one final structural validation

Approved upstream truth is authoritative. Downstream edits may challenge it, but may not silently replace it.

## Steady-State Bugfix Path

1. capture repro and expected behavior
2. add or update regression coverage
3. identify the violated or missing contract item
4. reconcile only the affected slice unless a broader semantic contradiction is discovered

## Stale Propagation Rules

- approved upstream changes stale dependent downstream artifacts through explicit dependency edges
- stale status propagates only through declared dependencies, not intuition
- downstream code drift may trigger a proposal, but may not silently rewrite approved upstream truth
- example: a changed `API-*` may stale the owning module spec, dependent module specs, and any derived contract tests that declare that interface

## Allowed Durable Projections

| Projection | Purpose |
| --- | --- |
| Trace index | Required trace links across tiers |
| Dependency/stale graph | Explicit stale propagation |
| Interface/schema manifests | Checkable boundary contracts |

## Testing Strategy

| Level | Focus | Derived from |
| --- | --- | --- |
| Structural eval | Metadata, IDs, references, lifecycle | Artifact protocol and templates |
| Semantic eval | Coverage, contradictions, ownership sanity | Canonical artifacts |
| Contract tests | Interface and schema compliance | `API-*` |
| Regression tests | Bugfix and workflow preservation | `STORY-*`, `INV-*` |
