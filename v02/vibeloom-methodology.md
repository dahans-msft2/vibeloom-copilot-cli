# VibeLoom Methodology

VibeLoom is a contract-driven methodology for long-lived vibe coding. It is built for codebases that must survive more than one generation step, more than one contributor, and more than one architectural revision without losing semantic coherence.

This file is the source of truth for the methodology. Implementation details such as CLI surface, template schemas, and runtime behavior are derived from and must conform to this document.

---

## What VibeLoom Is

VibeLoom governs generated applications through a stack of canonical contracts and derived execution guidance.

It is designed for projects where:

- the code must survive repeated AI-assisted change
- multiple humans and agents may work on the system over time
- the cost of semantic drift is higher than the cost of maintaining a compact contract layer

VibeLoom optimizes for three things at once:

1. **Human reviewability** of intent, requirements, and architecture
2. **Traceable change propagation** from upstream meaning to downstream implementation
3. **Safe swarm execution** through explicit ownership boundaries and deterministic context scoping

Code is downstream output. The contract stack governs what the code is allowed to mean.

---

## The Problem

AI code generation is excellent at producing local momentum. It is weak at preserving clarity and quality long-term.

Four systemic failure modes appear as projects grow:

1. **Semantic drift.** Concepts, workflows, and invariants shift subtly with every prompt.
2. **Invisible governance.** If intent lives only in chat history, there is no durable review surface for humans.
3. **Context fragmentation.** Large codebases exceed what one agent can safely hold in context, so ownership and responsibilities become guesswork.
4. **Reconciliation failure.** Manual edits, bugfixes, and drift have no principled path back to the specification layer.

Even before coding agents, all these problems existed. Agents amplify them by increasing both the speed and the volume of change.

---

## Core Thesis

These principles anchor the methodology:

1. **Intent must become contracts, not remain chat history.**
2. **Structured contracts are cheaper to review than generated code.**
3. **The contract stack doubles as the eval stack.**
4. **Human approval governs canonical truth; agents accelerate production and verification.**
5. **Safe agent scaling requires explicit ownership boundaries and scoped context.**

---

## Design Principles

1. **Structure over prose**
2. **Clarity over cleverness**
3. **Explicit ownership over shared ambiguity**
4. **Stable boundaries over ad hoc decomposition**
5. **Scoped context over maximal loading**
6. **Canonical truth over derived guidance**
7. **Human authority over agent autonomy**
8. **Asymmetry over silent reconciliation**
9. **Bounded processes over infinite loops**
10. **Conciseness over ceremony**

---

## The Contract Stack

VibeLoom organizes governed applications into a compact contract stack. Root artifacts define global truth. Container and component artifacts localize technical truth for implementation and swarm work.

| Artifact | Scope | Role | Authority | Primary audience |
| --- | --- | --- | --- | --- |
| `defaults.md` | repo | Minimal constitution: global defaults, foundations, binding repo-wide rules, global technology baseline, agent defaults, quality defaults | Canonical | Tech lead + agents |
| `intent.md` | repo | Product purpose, rationale, and non-normalized user intent | Canonical | Product owner |
| `prd.md` | repo | Functional requirements and non-functional requirements | Canonical | Product + engineering leads |
| `usm.md` | repo | Epic/story/workflow structure and acceptance framing | Canonical | Product + design |
| `dm.md` | repo | Domain model: bounded contexts, aggregates, invariants, ubiquitous language | Canonical | Domain + architecture leads |
| `system.md` | repo | System context, external actors/systems, high-level trust and NFR boundaries | Canonical | Architecture lead |
| `containers.md` | repo | Global runtime/deployment topology, container inventory, communication paths, hosting/runtime choices | Canonical | Architecture + platform leads |
| `/<container>/container.md` | container | Local runtime boundary, resident bounded contexts, authoritative component inventory, local constraints | Canonical | Engineers + agents working in that container |
| `/<container>/<component>/component.md` | component | Full contract for one owned technical boundary | Canonical | Engineers + agents working on that component |
| `AGENTS.md` | root / container / component | Scoped execution guidance derived from canonical truth | Derived | Agents |

All normative truth lives in canonical artifacts. `AGENTS.md` files are generated execution briefs and never outrank the contracts that produced them.

Code is not part of the contract stack. It is the downstream implementation governed by the stack.

### Root Canonical Artifacts

At repository root, a governed application always owns:

- `defaults.md`
- `intent.md`
- `prd.md`
- `usm.md`
- `dm.md`
- `system.md`
- `containers.md`

There is **no canonical root `components.md`**. Global deployment topology belongs in `containers.md`. Local component inventory belongs in each container's `container.md`.

---

## Generated App File Structure

The canonical generated-app layout is:

```text
/
  defaults.md
  intent.md
  prd.md
  usm.md
  dm.md
  system.md
  containers.md
  AGENTS.md

  <container>/
    container.md
    AGENTS.md
    <component>/
      component.md
      AGENTS.md
      ...
```

This layout is intentionally shallow.

- Containers live at repo root.
- Every first-class component has its own directory.
- Bounded context is **not** a path level. It is captured in metadata and container inventory.
- A first-class component must be listed in its container's `container.md` and map to a directory containing `component.md`.
- Directories without `component.md` are **not** canonical components by default.

The root stays understandable to humans, while container and component directories give agents small, stable working boundaries.

---

## Technical Structure Model

VibeLoom uses three technical description levels:

| Artifact | Answers | Does not own |
| --- | --- | --- |
| `system.md` | What system exists, who or what surrounds it, and which high-level boundaries matter | Detailed deployment topology or component inventory |
| `containers.md` | Which deployable/runtime boundaries exist, how they communicate, and where they run | Local component contracts |
| `container.md` | Which bounded contexts and components live in this container, and what local runtime constraints apply | Cross-system topology |
| `component.md` | What one owned technical boundary is responsible for, which interfaces it owns, and which code paths it governs | Whole-container or whole-system maps |

### Foundations

VibeLoom names only two foundations explicitly:

- **DDD** for semantic modeling: bounded contexts, aggregates, invariants, and ubiquitous language
- **C4** for system and container description

Everything else is derived from or subordinate to explicit VibeLoom rules.

### Containers, Bounded Contexts, and Components

These relationships are normative:

1. **The component is the primary unit of ownership, safe change, and agent work allocation.**
2. **Every component belongs to exactly one bounded context.**
3. **Every component has exactly one container home.**
4. **A bounded context must not span multiple containers.**
5. **Components from the same bounded context must be co-located in the same container.**
6. **A container may host multiple bounded contexts.**

This gives VibeLoom a clear semantic-to-runtime mapping:

- bounded context defines semantic home
- component defines owned technical change boundary
- container defines runtime and deployment home

### Component Derivation

VibeLoom does not derive components from filesystem shape or deployment shape. It derives them from semantics first, then validates them against implementation safety.

The default derivation process is:

1. Start from a bounded context in `dm.md`.
2. Identify aggregate candidates and their invariants.
3. Treat aggregate cores as the default first pass for component candidates.
4. Add **process/workflow components** when important behavior is not a natural responsibility of one aggregate.
5. Add **adapter components** where external systems, protocols, or translations must be isolated.
6. Add **query/read components** only when read complexity, ownership, or performance justifies them.
7. Merge or split candidates until each component owns a coherent write surface, clear interfaces, and a safe independent work scope.

This archetype set is a VibeLoom heuristic informed by DDD aggregates and services, plus boundary patterns such as adapters. It is **not** presented as a canonical Evans taxonomy.

### Container Inventory and Component Discovery

Agents do not discover components by guessing from folder names.

`container.md` is the authoritative component inventory for one container. At minimum, it lists for each component:

- component ID or canonical name
- folder path
- bounded context
- one-line responsibility

It may also summarize owned interfaces or direct local dependencies when that improves navigation.

Agents discover components by reading `container.md` first, then loading the matching `component.md`. The filesystem convention is a consistency check and navigation aid, not the source of truth.

### Component Metadata

`component.md` frontmatter must include at minimum:

- `status`
- `version`
- `dependencies`
- `approval_mode`
- `bounded_context`
- `container`
- `owned_paths`
- `owned_interfaces`
- `trace_to`

These fields are the minimum needed to support ownership, stale detection, approval provenance, and traceability.

---

## Workflow And Operations

VibeLoom defines methodology-level operations. Implementations may expose them through different commands or interfaces, but the logical operations stay the same.

| Operation | Direction | Meaning |
| --- | --- | --- |
| `init` | top-down | Bootstrap a governed repo and produce the first draft contract stack |
| `vibeloom` | top-down | Primary orchestrator for natural-language change requests |
| `generate` | top-down | Produce one artifact or one scoped slice of artifacts from upstream truth |
| `review` | up + lateral | Critique a scope and optionally apply bounded fixes |
| `eval` | up | Run formal structural and semantic checks for the selected scope |
| `fix` | top-down | Propagate approved upstream changes down to stale downstream artifacts |
| `approve` | gate | Move drafts to approved state, record provenance, increment version |
| `status` | read-only | Show lifecycle state, dependency health, stale propagation, and coverage gaps |
| `import` | bottom-up | Reconstruct candidate contracts from an unmanaged or drifted codebase |

### Generation Order

The normal top-down contract order is:

1. `intent.md`
2. `defaults.md`
3. `prd.md`
4. `usm.md`
5. `dm.md`
6. `system.md`
7. `containers.md`
8. affected `container.md` files
9. affected `component.md` files
10. derived `AGENTS.md` files
11. code

`defaults.md` becomes the authoritative home for normalized global constraints after intent capture. `intent.md` remains authoritative for product purpose, rationale, and non-normalized nuance.

### Profiles

Profiles control workflow rigor, not artifact scope. Both profiles use the same canonical stack.

| Profile | Classification | Approval behavior | Typical use |
| --- | --- | --- | --- |
| `lite` | Hidden internal classifier for safe scoping and escalation | One approval pause after the canonical spec stack for the current run is generated; code still waits for approved specs | Smaller or lower-risk projects |
| `full` | Explicit visible classifier | Tiered approval gates before proceeding downward | Larger, longer-lived, or parallelized systems |

`lite` is intentionally less ceremonial, not less safe. It may generate multiple spec tiers in one orchestrated run from upstream drafts created earlier in that same run.

### Lifecycle and Approval Provenance

Lifecycle states are limited to:

- `draft`
- `approved`
- `stale`
- `superseded`

There is no separate `auto-approved` lifecycle state.

Delegated approval is represented through provenance metadata:

```text
approval_mode: human | delegated
```

Delegated approval still results in `approved`. It allows orchestration to proceed while preserving the fact that a human did not directly review that artifact at that moment.

### Approval and Versioning

Only canonical artifacts are approved.

On approval:

- status becomes `approved`
- version increments
- approval provenance is recorded
- downstream artifacts may become `stale` through declared dependencies

Git history provides the long-term audit trail for approvals and amendments.

---

## Review, Eval, And Reconciliation

`review` and `eval` are related but distinct.

- `review` is human-facing critique plus optional bounded remediation.
- `eval` is structured validation of the current scope against the current rules.

### Review

VibeLoom keeps a single `review` operation. The interface may expose different options, but the methodology-level behaviors are:

- **Advisory review:** findings and proposed fixes only
- **Bounded remediation:** apply bounded fixes inside the allowed scope
- **Custom instructions:** apply explicit user instructions while staying inside review rules

Review may:

- surface contradictions, unclear assumptions, and missing links
- propose upstream or lateral corrections
- apply bounded fixes within scope

Review may **not** silently rewrite semantically meaningful upstream truth. When an upstream amendment changes meaning, the human chooses the direction and later approves the updated canonical artifact.

### Eval Tiers

VibeLoom uses two runtime eval tiers and one methodology-level behavioral tier.

| Tier | Type | Purpose | Blocking |
| --- | --- | --- | --- |
| 1 | Structural | Validate frontmatter, IDs, lifecycle rules, dependency declarations, path/spec consistency, and reference integrity | Yes |
| 2 | Semantic | Analyze requirement coverage, boundary sanity, componentization fit, contradiction with upstream truth, and context sufficiency | No |
| 3 | Behavioral | Produce on-demand Gherkin scenarios from approved contracts for later implementation | No |

Tier 3 outputs are non-canonical. They guide humans or agents who later implement tests or scenarios in code.

### Asymmetric Reconciliation

Reconciliation is built into `review` and `fix`.

The rule is asymmetric:

- approved upstream contracts define intended semantics
- downstream artifacts and code may reveal drift
- drift triggers proposals, not silent rewriting of approved truth

When drift appears, the agent proposes one of two directions:

1. Amend upstream truth, then stale and fix downstream artifacts
2. Preserve upstream truth, then correct downstream artifacts or code

Humans choose whenever the resolution changes meaning.

### Bounded Reconciliation

To prevent endless loops:

1. `review` identifies and frames the drift
2. human chooses the semantic direction when needed
3. `fix` propagates approved upstream changes downward
4. `eval` validates the resulting state

---

## Defaults vs AGENTS

`defaults.md` and `AGENTS.md` solve different problems.

### `defaults.md`

`defaults.md` is canonical, repo-scoped, durable, and always loaded. It is a **minimal constitution**, not a handbook and not a buzzword list.

It contains these sections:

1. `Repo Defaults`
2. `Foundations`
3. `Repo-Wide Rules`
4. `Technology Baseline`
5. `Agent Defaults`
6. `Code Generation Defaults`
7. `Quality Defaults`
8. `Toolbox Note`

`defaults.md` is also the authoritative home for normalized global constraints after intent capture.

### Foundations

The only named foundations are:

- `DDD`
- `C4`

They explain where the contract model comes from. They do not replace explicit VibeLoom rules.

### Repo-Wide Rules

The binding structural rules in `defaults.md` are:

1. The component is the primary unit of ownership, safe change, and agent work allocation.
2. Every component belongs to exactly one bounded context.
3. A bounded context must not span multiple containers.
4. Components from the same bounded context must be co-located in the same container.
5. A container may host multiple bounded contexts, but each component has exactly one container home.
6. Cross-component interaction must occur through explicit owned interfaces.
7. External systems and infrastructure must be isolated behind adapter boundaries rather than leaking into core component logic.
8. Component naming and contracts must follow the bounded context's ubiquitous language.
9. Canonical technical work must be scoped through `container.md` and `component.md`, not inferred from code alone.
10. Dependency and trace metadata must be explicit enough to support stale detection and impact analysis.

### Technology Baseline

Repo-global technology choices belong in `defaults.md` only when they truly apply across the whole governed application.

Examples:

- language and runtime baseline
- primary framework choices
- datastore baseline
- cloud or hosting default
- repo-wide testing or tooling defaults

Local exceptions belong in `container.md` or `component.md`, not in the constitution.

### Agent Defaults

`defaults.md` records the repo-wide rules that agents must always respect:

- what is always loaded
- how context escalation works
- which ownership rules are non-negotiable
- how approval provenance is interpreted

### Code Generation Defaults

This subsection translates approved contracts into executable implementation behavior.

It should stay compact and operational:

1. For behavior changes, prefer test-first delivery: write or update unit, component, contract, or scenario tests before implementation when practical.
2. Use the smallest test scope that can prove the behavior: unit tests inside one component first, broader workflow tests only when the change crosses explicit boundaries.
3. Implement from the owned component boundary inward. Do not widen scope unless an explicit interface or contract change requires it.
4. Keep domain logic inside the owning component and keep infrastructure-specific logic behind adapters.
5. If behavior is semantically unclear, generate or refine scenarios first rather than inventing behavior in code.

### Quality Defaults

Only truly universal quality defaults belong here:

1. Changes to a component should include or update test or scenario coverage appropriate to that component's risk.
2. Retryable handlers, jobs, and integrations should be idempotent by default.
3. Mutating component boundaries should emit sufficient logging or audit signals when the domain requires accountability.
4. Security, authorization, and NFR constraints captured upstream are binding on downstream design and code.

### Toolbox Note

Optional tactics such as adapters, selective CQRS, SOLID heuristics, and familiar design-pattern catalogs may be used when they solve a concrete problem. They do **not** have equal normative status to `DDD`, `C4`, or explicit VibeLoom rules.

### `AGENTS.md`

`AGENTS.md` is derived, regenerable, non-canonical execution guidance.

Generated governed applications may produce it at:

- repo root
- container level
- component level

Its job is to answer:

- what this scope owns
- what to load first
- what not to touch
- which checks or commands are common here
- which local caveats matter during execution

`defaults.md` says what is globally true or globally preferred. `AGENTS.md` says how to work safely in this scope right now.

---

## Context Loading

Agents have finite attention. VibeLoom therefore uses deterministic context scoping.

### Always Loaded

`defaults.md` is always loaded.

### Usually Loaded

`intent.md` is loaded for:

- generation
- review
- repo-wide architectural decisions

It does not have to be loaded for every purely local execution step once approved downstream contracts already capture the necessary constraints.

### Scope-First Loading

For technical work:

1. Start from the target `component.md` if one component is being changed.
2. Start from `container.md` if container-local structure or inventory is the question.
3. Use `container.md` to discover components. Do not infer canonical components from arbitrary folders.
4. Load only the relevant `dm.md`, `usm.md`, or `prd.md` slices needed to understand the touched semantics.
5. Load `containers.md` or `system.md` slices when container boundaries, deployment constraints, external interfaces, or NFR boundaries matter.

### Derived Guidance

Load `AGENTS.md` only when it exists and reduces ambiguity. It helps execution, but it never substitutes for canonical truth.

### Escalation Rule

If an agent is unsure whether a change stays within one component, one bounded context, or one container, it must escalate scope upward rather than under-scope the context.

---

## Traceability

Formal traceability starts at the PRD. `intent.md` remains prose-first and authoritative, but it is not ID-traced.

The core chain is:

```text
PRD requirement -> USM story/workflow -> DM bounded context / aggregate / invariant -> system/container/component -> Gherkin scenario / code test
```

This chain enables:

- impact analysis
- coverage verification
- stale detection
- eval grounding

### Dependency Metadata

Every traced canonical item below intent carries stable IDs or references appropriate to its layer.

Artifacts declare enough dependency metadata to answer:

- which upstream truth they depend on
- which downstream artifacts become stale if they change
- which code paths and interfaces they own

When an approved upstream artifact changes version, dependent downstream artifacts become `stale` through explicit declared edges.

### Example

| Layer | Example |
| --- | --- |
| `PRD` | `PRD-FR-004` workspace sharing requires explicit invite approval |
| `USM` | `STORY-018` owner approves a workspace invite |
| `DM` | `BC-collaboration`, `AGG-invite`, `INV-009` invite must be pending before approval |
| `containers` | `CONT-app` collaboration container |
| `component` | `CMP-invite-lifecycle` in `app/invite-lifecycle/` |
| `behavioral` | `SCN-INVITE-003` invite approval scenario |

This is why the stack is more than documentation. The contracts are the eval surfaces.

---

## Brownfield Import vs. Steady-State Bugfix

VibeLoom treats these as different paths.

- **Import** is a bootstrap path for unmanaged or heavily drifted repos. It reconstructs candidate contracts from code and marks uncertainty explicitly for human review.
- **Bugfix** is the steady-state path for governed repos. It starts from repro, expected behavior, the violated or missing contract, and regression coverage.

Once a repo is governed, routine defects should be resolved against the approved stack rather than by re-inferring semantics from code on every fix.

---

## Summary

VibeLoom is strongest where prompt-only generation stops being reliable.

It works by:

- turning intent into a durable contract stack
- making containers and components explicit enough for humans and agents to share
- keeping `defaults.md` small but binding
- deriving `AGENTS.md` as scoped execution guidance rather than treating it as truth
- allowing agents to move fast without losing semantic ownership and traceability

The methodology is intentionally stricter than ad hoc AI coding because safe speed requires explicit boundaries, explicit authority, and explicit context rules.
