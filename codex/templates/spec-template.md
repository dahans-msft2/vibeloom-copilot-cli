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

# Technical Spec: [Project Name]

## Purpose

<!-- Describe the runtime and implementation design that realizes the approved semantics. -->

## Repository Layout

| Path | Responsibility |
| --- | --- |
| `constitution.md` | |
| `intent.md` | |
| `prd.md` | |
| `usm.md` | |
| `dm.md` | |
| `spec.md` | |

## Profiles

### `lite`

- 

### `full`

- 

## Artifact Responsibilities

| Artifact | Responsibility |
| --- | --- |
| `intent.md` | |
| `prd.md` | |
| `usm.md` | |
| `dm.md` | |
| `spec.md` | |

## Allowed Durable Projections

| Projection | Purpose |
| --- | --- |
| Trace index | |
| Dependency/stale graph | |
| Interface/schema manifests | |

## Reconcile Engine

### Inputs

- 

### Behavior

1. 
2. 
3. 

## Greenfield Flow

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

- 

## Future Command Surface

| Command | Purpose |
| --- | --- |
| `init` | |
| `import` | |
| `generate` | |
| `approve` | |
| `develop` | |
| `eval` | |
| `reconcile` | |
| `status` | |

## Testing Strategy

| Level | Focus | Source |
| --- | --- | --- |
| Structural eval | | |
| Semantic eval | | |
| Reconcile tests | | |
| Context-loading tests | | |
