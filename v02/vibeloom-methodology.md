# VibeLoom Methodology

VibeLoom is a contract-driven methodology for long-lived vibe coding. It is built for codebases that must survive more than one generation step, more than one contributor, and more than one architectural revision without losing semantic coherence.

This file is the source of truth for the methodology. Implementation details such as CLI surface, template schemas, and runtime behavior are derived from and must conform to this document.

---

## What VibeLoom Is

VibeLoom implements AI-powered SDLC through a stack of canonical contracts and derived execution guidance.
The contract stack preserves long-term **consistency** and **coherence** across all tiers, from user intent to code.

It is designed for projects where:

- the code must survive repeated AI-assisted change
- multiple humans and agents may work on the system over time
- the cost of semantic drift is higher than the cost of maintaining a compact contract layer

VibeLoom optimizes for three things at once:

1. **Human gating** at tier boundaries: intent-specs, product-specs, system-specs, context, and code
2. **Traceable change propagation** from high-level intent to low-level implementation and back
3. **Safe swarm execution** through explicit ownership boundaries and deterministic context scoping

---

## The Problem

AI code generation is excellent at producing local momentum. It is weak at preserving clarity and quality long-term.

Four systemic failure modes appear as projects grow:

1. **Semantic drift.** Concepts, workflows, and invariants shift subtly with every prompt.
2. **Invisible governance.** If intent lives only in chat history, there is no durable review surface for humans.
3. **Context fragmentation.** Large codebases exceed what one agent can safely hold in context, so ownership and responsibilities become guesswork.
4. **Reconciliation failure.** Manual edits, bugfixes, and drift have no principled path back to the specification layer.

All these problems are immanent to software engineering and existed before coding agents, albeit in different forms. Large software projects have always struggled to maintain consistency and coherence across intent, specs, and code.

---

## The Solution

Historically, many strong software engineering methodologies were invented to keep products consistent and coherent: User Story Mapping, Domain-Driven Design, Behavior-Driven Development, C4 system design mapping, Test-Driven Development, and others. However, because they introduced additional ceremony, they were often underused.

VibeLoom addresses these problems by treating structured specifications as a multi-tier eval system and the durable source of truth rather than relying on code, chat history, and agent memory. Agents turn the tradeoff around: the methodology delegates creation, maintenance, and continuous verification of internal consistency and coherence across the entire spec+code base to the agents, while humans keep the approval authority.

---

## Principles

These principles anchor the methodology:

1. **The system is defined as a contract stack, not a set of stale one-off documents.**
2. **The contract stack is used as the eval stack.**
3. **Agents are responsible for generation and validation, gated by humans.**
4. **Scoped context enables agent scaling.**

---

## The Contract Stack

VibeLoom governs application development through a compact contract stack. Canonical specs define normative truth. Derived guidance distills that truth for execution.

### Generation Tiers

The artifact stack also groups into generation tiers. These tiers are the primary orchestration model for users and agents.

| Tier | Role | Artifacts |
| --- | --- | --- |
| intent-specs | Capture user intent and normalize repo-wide defaults | `intent`, `defaults` |
| product-specs | Turn intent into formally traceable product and domain contracts | `prd`, `usm`, `dm` |
| system-specs | Translate approved product and domain semantics into technical contracts | `system`, `containers`, per-container `container`, per-component `component` |
| context | Distill scoped execution guidance for agents | `AGENTS.md`, `CLAUDE.md`, and similar |
| code | Produce executable implementation and verification artifacts | source code, tests, runtime / ops glue |

Tiers are a generation and governance abstraction. Specs remain the fine-grained review, traceability, and dependency surfaces inside each tier.

---

### Canonical Specs

A governed application owns the following canonical specs:

| Spec | Tier | Role | Primary audience |
| --- | --- | --- | --- |
| `intent` | intent-specs | Vision-like prose description of the system; may include both product and implementation wishes | PMs |
| `defaults` | intent-specs | Minimal constitution: global defaults, foundations, binding repo-wide rules, global technology baseline, agent defaults, quality defaults | Tech leads + agents |
| `prd` | product-specs | Functional requirements and non-functional requirements | PMs + Tech leads |
| `usm` | product-specs | Epic/story/workflow structure and acceptance framing | PMs + UX designers |
| `dm` | product-specs | Domain model: bounded contexts, aggregates, invariants, ubiquitous language | PMs + Tech leads |
| `system` | system-specs | System context, external actors/systems, high-level trust and NFR boundaries | Tech leads |
| `containers` | system-specs | Global runtime/deployment topology, container inventory, communication paths, hosting/runtime choices | Tech leads |
| `container` | system-specs | Local runtime boundary, resident bounded contexts, authoritative component inventory, local constraints | Tech leads |
| `component` | system-specs | Full contract for one owned technical boundary | Tech leads |

### Derived Guidance

Derived guidance is generated from canonical specs and never outranks them.

| Artifact | Tier | Role | Primary audience |
| --- | --- | --- | --- |
| `AGENTS.md`, `CLAUDE.md`, and similar | context | Scoped execution guidance distilled from canonical truth | Agents |

All normative truth lives in canonical specs. Code is downstream implementation rather than a canonical spec, although validation may run upward from code against every upstream tier.

---

### `intent-specs` tier
This tier captures user intent and turns repo-wide defaults into a binding constitution.

| Spec | Structure |
| --- | --- |
| `intent` | Relatively free-form prose description of the system, including product wishes and implementation preferences |
| `defaults` | Compact constitutional spec for global rules, defaults, and engineering expectations |

#### `intent` spec
`intent` is a relatively free-form prose description of the required application with two sections.

| Section | Purpose |
| --- | --- |
| `functionality` | Describes, in relatively free form, what the application does. |
| `miscellania` | Captures any other wishes from the creator that do not fit the functional description. |

- `intent` may include both product-level and implementation-level wishes.
- `intent` stays prose-first rather than fully normalized.

#### `defaults` spec
`defaults` is the minimal constitution for repo-wide rules, defaults, and execution expectations.

| Section | Purpose |
| --- | --- |
| `repo defaults` | Defines repo-scoped workflow defaults, naming conventions, and operating assumptions. |
| `foundations` | States the foundational methodologies or conceptual bases the repo follows. |
| `repo-wide rules` | Records globally binding structural and engineering rules. |
| `technology baseline` | Captures repo-global technology choices that all downstream tiers should assume. |
| `agent defaults` | Defines global context-loading and execution rules for agents. |
| `code generation defaults` | Defines default implementation habits such as test-first work and boundary discipline. |
| `quality defaults` | Captures universal quality expectations that apply across the repo. |
| `toolbox note` | Lists optional tactics or patterns that may be used when they solve a concrete problem. |

- Normalized global constraints belong here.
- Project rationale belongs in `intent`, not in `defaults`.
- Downstream tiers must treat `defaults` as binding constitution.

---

### `product-specs` tier
This tier turns intent into formally traceable product and domain contracts.

| Spec | Structure |
| --- | --- |
| `prd` | Product Requirements Document defining scope, requirements, and constraints |
| `usm` | User Story Map defining activities, workflows, stories, and release slices |
| `dm` | Domain Model defining language, boundaries, and invariants |

#### `prd` spec
`prd` is the formally traceable requirements contract for the product.

| Section | Purpose |
| --- | --- |
| `scope` | Defines the product surface being specified. |
| `functional requirements` | Enumerates required behaviors and capabilities. |
| `non-functional requirements` | Captures quality attributes and operational expectations. |
| `constraints and assumptions` | Records known constraints, dependencies, and planning assumptions. |
| `out of scope` | Prevents accidental expansion of the product surface. |

- Formal traceability begins here.
- FR and NFR identifiers originate here.

#### `usm` spec
`usm` is the workflow and delivery map that organizes the product into activities, journeys, stories, and release slices.

| Section | Purpose |
| --- | --- |
| `activities / backbone` | Defines the top-level product activities or narrative backbone. |
| `workflows / journeys` | Groups user flows or end-to-end journeys under the backbone. |
| `stories` | Breaks workflows into implementable, traceable stories. |
| `acceptance framing` | States the expected behavior and acceptance intent for each story. |
| `milestones / release slices` | Organizes stories into slices that can be delivered coherently. |

- `usm` derives from `prd`.
- Stories trace to PRD requirements.
- Acceptance framing stays behavior-focused rather than technical.

#### `dm` spec
`dm` is the semantic model of the domain and the source for technical boundary derivation.

| Section | Purpose |
| --- | --- |
| `ubiquitous language` | Defines the shared domain vocabulary. |
| `bounded contexts` | Identifies semantic boundaries and ownership zones. |
| `aggregates / entities / value objects` | Defines the core domain structures and their responsibilities. |
| `invariants / business rules` | Records the rules that must always hold true in the domain. |
| `relationships / integration touchpoints` | Describes important links between concepts and external touchpoints. |

- `dm` is the semantic source for technical boundary derivation.
- Components are derived from domain semantics, not folder shape.

---

### `system-specs` tier
This tier translates approved product and domain semantics into technical contracts.

| Spec | Structure |
| --- | --- |
| `system` | System-level contract for system purpose, context, and external boundaries |
| `containers` | Global runtime and deployment topology contract |
| `container` | Local container contract for one runtime boundary |
| `component` | Smallest owned technical contract inside a container |

#### `system` spec
`system` defines the system as a whole and its relationship to the outside world.

| Section | Purpose |
| --- | --- |
| `system purpose and context` | Defines what the system is and where it sits in its broader environment. |
| `external actors and systems` | Identifies the people, systems, and dependencies around it. |
| `trust boundaries` | Marks important trust, security, or authority boundaries. |
| `system-wide NFR boundaries` | Captures system-level NFRs that shape the whole design. |

- Deployment topology does not live here.

#### `containers` spec
`containers` defines the global runtime topology of the system.

| Section | Purpose |
| --- | --- |
| `container inventory` | Lists the containers that make up the system. |
| `responsibilities` | Defines the role of each container in the overall design. |
| `communication paths` | Describes how containers interact with each other and with external systems. |
| `deployment / runtime choices` | Captures runtime, hosting, or platform choices at system scope. |
| `cross-container constraints` | Records constraints that apply across container boundaries. |

- `containers` owns global runtime topology, not local component detail.

#### `container` spec
`container` defines one local runtime boundary and the technical inventory inside it.

| Section | Purpose |
| --- | --- |
| `purpose and runtime boundary` | Defines what the container is for and where its runtime boundary sits. |
| `resident bounded contexts` | Lists the bounded contexts hosted inside this container. |
| `component inventory` | Lists the components that belong to this container. |
| `local interfaces and dependencies` | Summarizes key local interfaces and internal or adjacent dependencies. |
| `local NFR / operational constraints` | Captures local runtime, operational, and quality constraints. |

- `container` is the authoritative component inventory for one container.
- Components are discovered here, not inferred from folders.

#### `component` spec
`component` defines the smallest owned technical boundary inside the governed system.

| Section | Purpose |
| --- | --- |
| `responsibility` | States what the component owns and why it exists. |
| `owned paths` | Declares the code paths or assets the component is responsible for. |
| `owned interfaces` | Declares the interfaces or APIs the component owns. |
| `dependencies` | Records direct dependencies on other components, containers, or external systems. |
| `behavior / contracts` | Defines the local technical contracts and expected behavior of the component. |
| `local test / runtime notes` | Captures local test expectations and important runtime notes. |

- `component` is the smallest owned technical boundary.
- Each component belongs to exactly one bounded context.
- Each component has exactly one container home.

---

### `context` tier
This is a derived-artifacts tier that distills approved truth into scoped execution guidance.

| Artifact | Structure |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, and similar | Scoped guidance files generated for repo, container, or component work |

#### Derived guidance artifacts
Derived guidance artifacts summarize how to work safely in a specific scope.

| Section | Purpose |
| --- | --- |
| `scope and ownership` | States what the current scope owns. |
| `load-first context` | Tells the agent which upstream artifacts to load first. |
| `do-not-touch boundaries` | Marks files, contracts, or areas that are out of scope. |
| `common commands / checks` | Lists common commands, checks, or workflows for that scope. |
| `local caveats` | Captures scope-specific warnings, quirks, or operational notes. |

- Derived.
- Regenerable.
- Non-canonical.
- May exist at root, container, and component scopes.

---

### `code` tier
This tier contains downstream implementation artifacts rather than canonical specs.

| Artifact | Purpose |
| --- | --- |
| `source code` | Implements approved behavior and technical structure. |
| `tests` | Provide executable verification of behavior, contracts, and regressions. |
| `runtime / ops glue` | Handles configuration, packaging, deployment, and operational wiring. |

- Code is downstream from contracts.
- Tests are executable verification, not semantic source of truth.
- Validation may run upward from code against all upstream tiers.

---

## Technical Structure Model

VibeLoom uses three technical description levels:

| Artifact | Answers | Does not own |
| --- | --- | --- |
| `system.md` | What system exists, who or what surrounds it, and which high-level boundaries matter | Detailed deployment topology or component inventory |
| `containers.md` | Which deployable/runtime boundaries exist, how they communicate, and where they run | Local component contracts |
| `container.md` | Which bounded contexts and components live in this container, and what local runtime constraints apply | Cross-system topology |
| `component.md` | What one owned technical boundary is responsible for, which interfaces it owns, and which code paths it governs | Whole-container or whole-system maps |

### product-specs

VibeLoom relies on the following best practices and methodologies:
- **Product Requirements Document** - for `prd`
- **User Story Mapping**. for `usm`
- **Domain Driven Design** for `dm` - semantic modeling: bounded contexts, aggregates, invariants, and ubiquitous language
- **C4** for system and container description

Everything else is derived from or subordinate to explicit VibeLoom rules.

### system-specs

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
| `vibeloom` | top-down | Primary orchestrator for natural-language change requests; determines affected tiers and cascades through them |
| `generate` | top-down | Generate one affected tier from upstream truth using a forward-pass, back-pass, and validation flow; narrower artifact regeneration is a bounded optimization |
| `review` | up + lateral | Critique one selected scope, usually a whole tier at its approval boundary, and optionally apply bounded fixes |
| `eval` | up | Run formal structural and semantic checks for the selected scope; tier-boundary evaluation is the normal gating surface |
| `fix` | top-down | Propagate approved upstream changes down to stale downstream artifacts and tiers |
| `approve` | gate | Move reviewed drafts, usually a whole tier, to approved state, record provenance, and increment version |
| `status` | read-only | Show lifecycle state, dependency health, stale propagation, and coverage gaps |
| `import` | bottom-up | Reconstruct candidate contracts from an unmanaged or drifted codebase |

### Generation Order

Generation, review, and evaluation work in two dimensions:

- **Vertically:** lower tiers are generated from higher-tier truth.
- **Horizontally:** artifacts inside one tier are generated in dependency order and reconciled back across the tier when later artifacts sharpen earlier ones.

The normal top-down tier order is:

```text
intent -> product-specs -> system-specs -> context -> code
```

Within that flow, the normal artifact order is:

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

### Tier Generation Semantics

Specs are generated down and across:

- **down** through the named tiers
- **across** the artifacts inside each affected tier

Within one affected tier, artifacts are generated and governed as a batch rather than as individually approved fragments.

The default flow is:

1. Generate the affected tier in dependency order.
2. Run a **forward pass** across the tier.
3. Run a **back pass** across the same tier if later artifacts require coherent updates to earlier artifacts.
4. Run structural and semantic validation for the generated tier.
5. If validation surfaces issues, one additional forward-back round is permitted before presenting results.
6. Mark all resulting artifacts in that tier as `draft`.
7. Review, evaluate, and approve the tier before relying on it as canonical truth.

Users are not expected to approve individual artifacts mid-tier under normal operation. The methodology-level approval surface is the generated tier.

### Intent As Persistent Context

`intent.md` is loaded as generation context at every tier, not only when generating product-specs.

This is deliberate: intent may contain user constraints that must survive all the way into system design and code. Intent is prose-first rather than ID-traced, so its authority is enforced through persistent loading plus review and semantic evaluation.

### Bottom-Up Evaluation

Consistency and coherence checks run upward.

Every downstream artifact is evaluated against its immediate upstream contracts, but the default human-facing review and approval surface is the current generated tier. This is why `review`, `eval`, and `approve` normally happen at tier boundaries even though traceability and dependency edges exist at artifact level.

### Change Propagation

When an upstream contract changes, dependent downstream artifacts become `stale` through explicit declared dependency edges. The system does not rely on intuition or chat memory to decide what must be revisited.

The approval boundary depends on profile:

- In `full`, the next tier does not begin until the current tier is approved.
- In `lite`, the orchestrator may generate the spec tiers in one run from drafts created earlier in that run, then pause once before code generation.

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

Both can target an artifact, a component, or a wider scope, but the default governance surface for spec work is the affected tier.

### Review

VibeLoom keeps a single `review` operation. The interface may expose different options, but the methodology-level behaviors are:

- **Advisory review:** findings and proposed fixes only
- **Bounded remediation:** apply bounded fixes inside the allowed scope
- **Custom instructions:** apply explicit user instructions while staying inside review rules

Review may:

- surface contradictions, unclear assumptions, and missing links
- propose upstream or lateral corrections
- apply bounded fixes within scope

In normal top-down operation, review is centered on the generated tier. Artifact-level review is a narrower override for intentionally local work, not the default review model.

Review may **not** silently rewrite semantically meaningful upstream truth. When an upstream amendment changes meaning, the human chooses the direction and later approves the updated canonical artifact.

### Eval Levels

VibeLoom uses two runtime eval levels and one methodology-level behavioral level.

| Level | Type | Purpose | Blocking |
| --- | --- | --- | --- |
| 1 | Structural | Validate frontmatter, IDs, lifecycle rules, dependency declarations, path/spec consistency, and reference integrity | Yes |
| 2 | Semantic | Analyze requirement coverage, boundary sanity, componentization fit, contradiction with upstream truth, and context sufficiency | No |
| 3 | Behavioral | Produce on-demand Gherkin scenarios from approved contracts for later implementation | No |

Levels 1 and 2 are normally run against the tier currently under review, fix, or approval. Narrower artifact-level eval is allowed when the user intentionally scopes work more tightly.

Level 3 outputs are non-canonical. They guide humans or agents who later implement tests or scenarios in code.

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
