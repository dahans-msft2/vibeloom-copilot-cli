---
artifact_id: ART-SPEC-CODEX-V4
artifact_type: spec
status: draft
owner: methodology
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-INTENT-CODEX-V4
  - ART-PRD-CODEX-V4
  - ART-USM-CODEX-V4
  - ART-DM-CODEX-V4
depends_on:
  - ART-INTENT-CODEX-V4
  - ART-PRD-CODEX-V4
  - ART-USM-CODEX-V4
  - ART-DM-CODEX-V4
---

# Technical Spec: Codex V4 Methodology Package

## Purpose

This document defines the package-level technical design for Codex V4. It specifies file responsibilities, reconciliation behavior, scoped context loading, and the technical runtime boundary the package must preserve. The package is still documentation-first: it does not implement a separate runtime binary.

The exact routine command grammar, routing behavior, eval behavior, and response contract live in `references/`. This spec defines the technical rules a runtime must honor; it does not restate the routine command catalog inline.

This is a package and protocol spec, not a concrete governed repo instance. It defines what generated governed project specs must support, but it does not claim live module ownership or interface inventories for this repository itself.

Because this checked-in spec is a methodology-package meta-spec, it intentionally documents both supported profiles and generated-repo expectations. Unlike a concrete governed project `spec.md`, it does not select one active `profile` in frontmatter.

## Current Phase Boundary

- This phase ships Markdown artifacts and the Codex skill package.
- No separate executable command router is defined here beyond the skill instructions.
- Runtime language selection is deferred.

## Repository Layout

| Path | Responsibility |
| --- | --- |
| `constitution.md` | Foundational rules applied to every governed project |
| `SKILL.md` | Codex skill entrypoint that loads and applies runtime references |
| `agents/` | Skill UI metadata and invocation policy |
| `references/` | Routine runtime authority for command parsing, routing, eval behavior, and response shape |
| `intent.md` | Methodology package intent |
| `prd.md` | Methodology product requirements |
| `usm.md` | User workflow and acceptance semantics |
| `dm.md` | Methodology domain language and invariants |
| `spec.md` | Package-level technical protocol and generated-repo technical expectations |
| `templates/` | Canonical document templates |
| `docs/evals-*.md` | Detailed structural and semantic evaluation references |
| `docs/` | Supporting protocol explanations |
| `docs/profile-selection.md` | Lite vs Full guidance and transition rules |

## Supported Profiles

Generated governed project specs select one profile. This package spec documents the supported profile shapes that those concrete specs must follow.

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

## Surface Modes

Surface modes are a skill/runtime concern layered on top of the same canonical artifacts.

### `product-first`

- default session surface
- leads with `intent`, `prd`, `usm`, and `dm`
- appropriate for product framing, workflow review, and semantic clarification

### `code-first`

- advanced engineering surface
- leads with `spec.md`, module specs, interfaces, ownership, and technical boundaries
- keeps `prd`, `usm`, and `dm` stored and canonical, but collapsed until the task needs them

Rules:
- surface selection is session-scoped
- no repo-tracked surface state is written
- forced escalation surfaces upstream product/domain slices on semantic or boundary risk

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

## Upstream Trace Matrix

| Spec area | PRD refs | STORY refs | ENT refs | INV refs |
| --- | --- | --- | --- | --- |
| Package layering and authority model | PRD-FR-001, PRD-FR-010 | STORY-001, STORY-015 | ENT-001, ENT-010 | INV-003, INV-012 |
| Profiles and module/interface ownership rules | PRD-FR-011 | STORY-005, STORY-014 | ENT-007, ENT-008, ENT-009 | INV-008, INV-009, INV-010, INV-011 |
| Context loading and surface routing | PRD-FR-004, PRD-FR-010 | STORY-006, STORY-007, STORY-013, STORY-015 | ENT-006, ENT-010 | INV-007, INV-012 |
| Reconcile engine and stale propagation | PRD-FR-005, PRD-FR-008 | STORY-008, STORY-009, STORY-012 | ENT-003, ENT-004, ENT-005 | INV-004, INV-005, INV-006 |
| Import and steady-state bugfix paths | PRD-FR-006, PRD-FR-008 | STORY-009, STORY-010, STORY-011 | ENT-004, ENT-005, ENT-011 | INV-013 |
| Derived artifacts and projection restraint | PRD-FR-007, PRD-FR-009 | STORY-006, STORY-012 | ENT-001, ENT-003, ENT-010 | INV-004, INV-012 |

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
- Active surface
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

Surface overlay:
- `product-first` loads workflow/domain artifacts sooner
- `code-first` keeps the default view technical and escalates upward only when required

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

## Runtime Interface Boundary

This phase ships the runtime interface through `SKILL.md` and `references/`. It does not implement a separate runtime binary or external command router.

Runtime ownership:
- `references/command-surface.md` owns the exact command grammar, selectors, and canonical forms.
- `references/routing-and-loading.md` owns routine command routing and load selection.
- `references/evals-and-templates.md` owns routine eval and generation behavior.
- `references/interaction-contract.md` owns runtime response shape and correction patterns.

This spec owns the underlying technical rules a runtime must preserve:
- artifact layering and authority boundaries
- profile and surface semantics
- context-loading and escalation behavior
- reconcile asymmetry and stale propagation
- greenfield, import, and steady-state bugfix boundaries
- durable projection limits

Any future standalone runtime should preserve those rules. Changes to the routine command surface belong in the runtime references and acceptance tests, not as duplicated inline command tables here.

## Testing Strategy

| Level | Focus | Source |
| --- | --- | --- |
| Structural eval | Metadata, IDs, references, lifecycle correctness | Templates, artifact protocol |
| Semantic eval | Coverage, contradictions, boundary sanity | Canonical artifacts |
| Reconcile tests | Asymmetric resolution and stale propagation | Reconcile engine rules |
| Context-loading tests | Minimal sufficient slice and escalation behavior | Context-loading protocol |
