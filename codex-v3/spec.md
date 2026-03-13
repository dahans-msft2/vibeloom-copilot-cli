---
artifact_id: ART-SPEC-CODEX-V3
artifact_type: spec
status: draft
owner: methodology
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-INTENT-CODEX-V3
  - ART-PRD-CODEX-V3
  - ART-USM-CODEX-V3
  - ART-DM-CODEX-V3
depends_on:
  - ART-INTENT-CODEX-V3
  - ART-PRD-CODEX-V3
  - ART-USM-CODEX-V3
  - ART-DM-CODEX-V3
profile: full
---

# Technical Spec: Codex V3 Methodology Package

## Purpose

This document defines the package-level technical design for Codex V3. It specifies file responsibilities, reconciliation behavior, scoped context loading, and the strict command surface packaged as a Codex skill. The package is still documentation-first: it does not implement a separate runtime binary.

## Current Phase Boundary

- This phase ships Markdown artifacts and the Codex skill package.
- No separate executable command router is defined here beyond the skill instructions.
- Runtime language selection is deferred.

## Repository Layout

| Path | Responsibility |
| --- | --- |
| `constitution.md` | Foundational rules applied to every governed project |
| `SKILL.md` | Codex skill entrypoint and command interface |
| `agents/openai.yaml` | Skill UI metadata and invocation policy |
| `references/` | On-demand operational references for the skill |
| `assets/` | Skill icons and UI assets |
| `intent.md` | Methodology package intent |
| `prd.md` | Methodology product requirements |
| `usm.md` | User workflow and acceptance semantics |
| `dm.md` | Methodology domain language and invariants |
| `spec.md` | Technical protocol and future runtime behavior |
| `templates/` | Canonical document templates |
| `eval/` | Evaluation instructions |
| `docs/` | Supporting protocol explanations |
| `docs/profile-selection.md` | Lite vs Full guidance and transition rules |

## Profiles

### `lite`

- `USM` and `DM` are still mandatory.
- Single bounded context is expected.
- Module decomposition may collapse into one application module.
- Derived operational guidance remains scoped, but module DAG and interface registry may be minimal.
- Technical templates still require explicit runtime, data, and API design sections.

### `full`

- Multiple bounded contexts or coordination risk require explicit modules.
- Every module must declare write ownership and allowed dependencies.
- Cross-module interfaces must be owned and listed in the interface manifest.
- Context maps, dependency DAGs, and module-level execution guidance are expected.

## Artifact Responsibilities

| Artifact | Responsibility |
| --- | --- |
| `intent.md` | Captures the human goal, audience, constraints, and capability outline |
| `prd.md` | Defines goals, users, requirements, NFRs, and scope boundaries |
| `usm.md` | Defines epics, stories, acceptance criteria, and workflow dependencies |
| `dm.md` | Defines bounded contexts, entities, relationships, invariants, and glossary |
| `spec.md` | Defines technical architecture, module boundaries, interfaces, data/storage, policies, and execution rules |

Derived operational artifacts:
- `AGENTS.md` packages the relevant policy and context slice for execution.
- `plan.md` packages a per-change task graph, touched IDs, acceptance signals, and validation steps.

## Allowed Durable Projections

Only three machine-readable projections may persist on disk:

| Projection | Purpose |
| --- | --- |
| Trace index | Resolve upstream/downstream coverage for items and tests |
| Dependency/stale graph | Track explicit dependency edges and stale propagation |
| Interface/schema manifests | Represent APIs, events, schemas, and module ownership in checkable form |

Rules:
- No additional always-on projections are allowed without explicit methodology revision.
- Other analyses may be generated transiently during reconcile, eval, or planning.

## Reconcile Engine

### Inputs

- Touched file paths or changed artifacts
- Referenced IDs
- Current approved dependency graph
- Active profile
- Requested or inferred change class

### Behavior

1. Classify the change as `local`, `behavioral-in-module`, or `boundary-changing`.
2. Build the minimum required context slice from the trace index and dependency graph.
3. Run one up-pass against approved upstream truth.
4. Detect drift and decide whether the mismatch is:
   - upstream contract drift
   - downstream artifact drift
   - code drift
   - unresolved ambiguity
5. Produce one explicit proposal:
   - amend upstream, then stale and regenerate affected downstream artifacts
   - preserve upstream, then update downstream artifacts or code
6. Run one down-pass across the affected downstream slice.
7. Run one final structural validation.
8. Require human approval whenever the proposal changes approved semantics.

Bound:
- No additional automatic reconcile loops are permitted in one session.

### Asymmetry Rule

Approved upstream contracts are source-of-truth for semantics. Downstream artifacts and code can challenge those semantics, but they cannot silently replace them.

## Greenfield Flow

1. Draft and reconcile `intent.md`.
2. Generate and reconcile `prd.md`, `usm.md`, and `dm.md`.
3. Select `lite` or `full`.
4. Generate and reconcile `spec.md`.
5. Derive operational artifacts.
6. Generate per-change `plan.md` before implementation.

## Brownfield Import

### Purpose

Bring an unmanaged or heavily drifted repo under governance.

### Behavior

1. Inspect code, tests, schemas, routes, and docs.
2. Infer draft `intent`, `prd`, `usm`, `dm`, and `spec`.
3. Attach import confidence signals to inferred items.
4. Require human approval before the repo is treated as governed.

### Constraints

- Import is a bootstrap path, not the default path for routine fixes.
- Low-confidence semantic inferences must remain visible until corrected or approved.

## Steady-State Bugfix Path

For a repo already under governance:

1. Start from a concrete repro and expected behavior.
2. Add or update regression coverage first.
3. Identify the violated or missing contract item.
4. Reconcile only the impacted slice.
5. Escalate to broader stale propagation only if the defect reveals a true semantic change or cross-boundary contradiction.

## Context-Loading Algorithm

### Always Load

- `constitution.md`
- active root `spec.md`
- active module spec when the task is module-scoped
- derived `AGENTS.md` for the task scope
- trace index slice for the referenced IDs

### Load Conditionally

- `prd` requirements and `usm` stories for behavioral work
- `dm` bounded contexts and invariants for semantic work
- neighboring module specs and interface manifests for cross-boundary work
- import assessments for imported or low-confidence artifacts

### Escalation Rules

Escalate context breadth when:
- change classification confidence is low
- multiple bounded contexts are touched
- a single module no longer owns the affected write surface
- interface ownership or invariants are ambiguous

## Stale Propagation Rules

- Changes in `constitution` may trigger package-wide review but are rare.
- Approved upstream changes mark dependent canonical artifacts `stale` according to explicit dependency edges.
- Derived operational artifacts are regenerated from the latest approved truth and are not independently marked `approved`.
- A `local` change does not stale unrelated upstream artifacts.

## Future Command Surface

This phase does not implement commands, but the future runtime is expected to support:

| Command | Purpose |
| --- | --- |
| `init` | Create a governed project from intent |
| `import` | Bootstrap governance for an existing repo |
| `generate` | Derive the next artifact or targeted downstream artifact |
| `approve` | Human approval flow for canonical artifacts |
| `develop` | Incremental change flow |
| `eval` | Structural and semantic checks |
| `reconcile` | Targeted drift resolution |
| `status` | Report artifact states and stale edges |
| `help topic` | Load focused guidance for methodology, profiles, evals, templates, or commands |

## Testing Strategy

| Level | Focus | Source |
| --- | --- | --- |
| Structural eval | Metadata, IDs, references, lifecycle correctness | Templates, artifact protocol |
| Semantic eval | Coverage, contradictions, boundary sanity | Canonical artifacts |
| Reconcile tests | Asymmetric resolution and stale propagation | Reconcile engine rules |
| Context-loading tests | Minimal sufficient slice and escalation behavior | Context-loading protocol |
