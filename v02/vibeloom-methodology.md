# VibeLoom Methodology

VibeLoom is a contract-driven methodology for long-lived vibe coding. It is built for codebases that must survive more than one generation step, more than one contributor, and more than one architectural revision without losing semantic coherence. It uses a **contract** - a tiered set of specifications validated for consistent and coherence - to code-generate an application.

This file is the source of truth for the methodology. Implementation details such as CLI surface, template schemas, and runtime behavior are specified from and must conform to this document.

---

## The Problem

AI code generation is excellent at producing local momentum. It is weak at preserving consistency and coherence long-term.

As a vibe-coded project grows, it starts suffering from:

1. **Semantic drift.** Concepts, workflows, and invariants shift subtly with every prompt.
2. **Invisible governance.** If intent lives only in chat history, there is no durable review surface for humans.
3. **Context fragmentation.** Large codebases exceed what one agent can safely hold in context, so ownership and responsibilities become guesswork.
4. **Reconciliation failure.** Manual edits, bugfixes, and drift have no principled path back to the specification layer.

All these problems are immanent to software engineering and existed before coding agents, albeit in different forms. Large software projects have always struggled to maintain consistency and coherence across intent, specs, and code.

---

## The Solution

**Vision**
- **For** teams and solo builders creating long-lived AI-generated software systems
- **Who** need
  - their systems to survive repeated AI-assisted change by multiple contributors, and architectural revision without semantic drift
  - multiple humans and agents may work on the system over time
- **VibeLoom** is a methodology for **contract-driven** development
- **That** preserves consistency and coherence across contract (intent-specs, product-specs, system-specs), context, and code through human-gated contract, agent-facing context, and continuous validation.
- **Unlike** prompt-only or one-spec-fits-all AI-generation practices
- **VibeLoom** maintain consistency and coherence of the whole system as humans and agents work on the system over time.

A number of software engineering practices and methodologies have been invented to keep products consistent and coherent: PRD, User Story Mapping, Domain-Driven Design, Behavior-Driven Development, C4 system design, Test-Driven Development, and others. However, because they introduced extra ceremony and requied extra effort, they were often underused or not used at all.

VibeLoom addresses these problems by generating a multi-tiered contract of structured specifications and treating this contract as an eval system and the durable source of truth rather than relying just on code, chat history, and agent memory.

VibeLoom  turns the tables on the extra process/spec ceremony: now it is the agents that do the heavy lifting of generating, reviewing, and validating the entire the entire contract/context/code stack for internal consistency and coherence, while humans keep the approval authority.

---

## Principles

The core principles of VibeLoom methodology are:

1. **The system is defined as a contract stack, not a set of stale one-off specs**
2. **The contract stack doubles as eval stack.**
3. **Agents are responsible for generation and validation, gated by humans.**
4. **Scoped context enables agent scaling.**

---

## Overview
Here is an overview of developing a system using VibeLoom
- Human defines a **contract** for the system. Contract is generated interactively through a human-edits <-> agent-generation loop.
- to make the contract both consistent and coherent, the human validates specs through **review** (a higher-level detect-issue -> suggest-fix -> implement-fix loop) and **eval** (more formal structural and semantic validation). Specs are checked against other specs in the same tier and against approved upstream tiers.
- First, the human defines **intent-specs** by iteratively shaping a high-level description of the system (`intent`) and the repo-wide defaults (`defaults`) that will govern the rest of the generation process.
- after the **intent-specs** are approved, **product-specs** (`prd`, `usm`, `dm`) are generated and validated using the same process.
- after the **product-specs** are approved, **system-specs** (`system`, `containers`, `container`, `component`) are generated and validated using the same process.
- generation and validation of the **contract** is performed at a tier level
  - The entire tier (however many specs it includes) is generated as a single operation
  - The agent asks for approval of the entire tier after the tier is generated, to reduce approval steps.
  - The entire tier is validated and eval-ed as a single operation.
  - Even if human edited individual specs, the review/eval/approval is performed for the entire tier as a whole - to avoid inconsistence and incoherence across the same-tier specs
  - Generation process can proceed to the next tier **only after** the entire tier (all specs in the tier) is approved.
- **context** (`CLAUDE.md` / `AGENTS.md`, `pdr`, `bdd`, `adr`, and similar artifacts) is generated from the approved contract to help agents work effectively. Some context artifacts, such as `pdr`, `bdd` and `adr`, may appear as byproducts of contract evolution; others are generated later as explicit execution context.
- context artifacts do not carry lifecycle metadata such as `draft` or `approved`; they are assumed correct by default. Because agentic generation is still early, the workflow may pause after generating context so a human can optionally review or eval it against upstream specs.
- if context generation is poor, the recommended fix is to edit upstream **contract** and regenerate context. Direct human edits to **context** are an exceptional fallback, not the primary workflow.
- after the **context** is ready, the swarm of agents can generate the **code** - meaning the system itself that can be built and executed.

## The Contract Stack

VibeLoom governs application development through a compact contract stack.
The application artifacts play the following roles:
- **contract**: human-gated semantic truth. These artifacts - whether human-authored or generated - belong to human-gated tiers. They are generated tier-by-tier as batches, and the agent asks for approval only after the whole tier is generated. Approval is performed only at tier level.
- **context**: agent-facing operational truth. These artifacts are required primarily for code generation agents. They do not carry approval-state metadata, and they do not require human approval. Humans may review or edit them in exceptional cases, but the recommended fix path is to amend upstream contract and regenerate context.
- **code**: the executable result. Humans are not expected to edit it directly.
Contract defines normative truth. Context distills that truth for agents. Code implements the application based on the above.

### Generation Tiers

The artifact stack also groups into generation tiers. These tiers are the primary orchestration model for users and agents.

| Tier          | Content                                                                         | Artifacts                                                                    |
| ------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| intent-specs  | Capture user intent and normalize repo-wide defaults                            | `intent`, `defaults`                                                         |
| product-specs | Formally traceable product and domain contracts produced from approved intent   | `prd`, `usm`, `dm`                                                           |
| system-specs  | Technical contracts produced from approved product and domain semantics         | `system`, `containers`, per-container `container`, per-component `component` |
| context       | Distill scoped execution guidance, decision records, and long-term agent memory | `AGENTS.md`, `CLAUDE.md`, `pdr`, `bdd`, `adr`, and similar                   |
| code          | This tier consists of executable implementation and verification artifacts      | source code, tests, runtime / ops glue                                       |

Tiers are a generation and governance abstraction. Review, eval, and approval happen at tier level. Traceability and dependency remain as fine-grained as possible within and across tiers and should be represented in a context graph.
Governance binds to the tier semantics, not to a fixed list of specs inside the tier. A tier may gain or lose specs over time without changing the review, eval, and approval model.

### Tier Attributes

VibeLoom uses three cross-cutting tier attributes:

| Attribute     | Meaning                                                                                                   |
| ------------- | --------------------------------------------------------------------------------------------------------- |
| `human-gated` | The workflow expects explicit human review and approval before the tier is accepted as current truth. |
| `normative`   | The artifact defines the intended current meaning of the system or product.                               |
| `executable`  | The artifact runs as implementation, verification, packaging, deployment, or operational logic.           |

These attributes apply to the tiers as follows:

| Tier          | Human-gated | Normative | Executable | Notes                                                                                                           |
| ------------- | ----------- | --------- | ---------- | --------------------------------------------------------------------------------------------------------------- |
| intent-specs  | yes         | yes       | no         | Defines high-level product intent and repo-wide defaults.                                                       |
| product-specs | yes         | yes       | no         | Defines formally traceable requirements, workflows, and domain semantics.                                       |
| system-specs  | yes         | yes       | no         | Defines technical structure and runtime design intent.                                                          |
| context       | no          | no        | no         | Serves as the default source of execution truth for agents, but yields to contract specs on semantic conflicts and normally has no explicit approval-state metadata. |
| code          | no          | no        | yes        | Implements and verifies the approved contracts.                                                                 |

---

### Contract Specs

A governed application owns the following contract specs:

| Spec         | Tier          | Role                                                                                                                                      | Primary audience    |
| ------------ | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| `intent`     | intent-specs  | Vision-like prose description of the system; may include both product and implementation wishes                                           | PMs                 |
| `defaults`   | intent-specs  | Minimal constitution: global defaults, foundations, binding repo-wide rules, global technology baseline, agent defaults, quality defaults | Tech leads + agents |
| `prd`        | product-specs | Functional requirements and non-functional requirements                                                                                   | PMs + Tech leads    |
| `usm`        | product-specs | Epic/story/workflow structure and acceptance framing                                                                                      | PMs + UX designers  |
| `dm`         | product-specs | Domain model: bounded contexts, aggregates, invariants, ubiquitous language                                                               | PMs + Tech leads    |
| `system`     | system-specs  | System context, external actors/systems, high-level trust and NFR boundaries                                                              | Tech leads          |
| `containers` | system-specs  | Global runtime/deployment topology, container inventory, communication paths, hosting/runtime choices                                     | Tech leads          |
| `container`  | system-specs  | per-container: local runtime boundary, resident bounded contexts, authoritative component inventory, local constraints                    | Tech leads          |
| `component`  | system-specs  | per-component: full contract for one owned technical boundary                                                                             | Tech leads          |

### Context Artifacts

Context artifacts are generated from contract specs and are the default execution surface for agents, but they never outrank contract specs semantically.

| Artifact | Tier | Role | Primary audience |
| --- | --- | --- | --- |
| `AGENTS.md`, `CLAUDE.md`, and similar | context | Scoped execution guidance distilled from contract specs | Agents |
| `pdr` | context | Product decision record that preserves product-level decision history without becoming contract truth | PMs + agents |
| `adr` | context | Architecture decision record that preserves technical decision history without becoming contract truth | Tech leads + agents |
| `bdd` | context | Generated non-executable behavioral scenarios used by humans and agents during implementation | PMs + tech leads + agents |

All semantic normative truth lives in contract specs. Context artifacts are the default execution truth for agents and may be regenerated or, in exceptional cases, human-edited, but if a context artifact conflicts with a contract spec, the contract spec wins semantically. Context artifacts do not normally have approval-state metadata and are assumed correct by default, although implementations may still pause for optional review while generation quality matures. Code is the executable result, although validation may run upward from code against every upstream tier.

---

### `intent-specs` tier
This tier captures user intent and turns repo-wide defaults into a binding constitution.

| Spec       | Description                                                                                                   |
| ---------- | ------------------------------------------------------------------------------------------------------------- |
| `intent`   | Relatively free-form prose description of the system, including product wishes and implementation preferences |
| `defaults` | Compact constitutional spec for global rules, defaults, and engineering expectations                          |

#### `intent` spec
`intent` is a relatively free-form prose description of the required application with two sections.

- functionality: describes, in relatively free form, what the application does.
- miscellania: Captures any other wishes from the creator that do not fit the functional description.

- `intent` may include both product-level and implementation-level wishes.
- `intent` stays prose-first rather than fully normalized.

#### `defaults` spec
`defaults` is the minimal constitution for repo-wide rules, defaults, and execution expectations.
- Normalized global constraints belong here.
- Project rationale belongs in `intent`, not in `defaults`.
- Downstream tiers must treat `defaults` as binding constitution.

The sections of the documents are:
##### foundations
States the foundational methodologies or conceptual bases the repo follows
##### repo
Defines repo-scoped workflow defaults, naming conventions, and operating assumptions.
##### rules
Records globally binding structural and engineering rules.
##### tech
Captures repo-global technology choices that all downstream tiers should assume.
##### agents
Defines global context-loading and execution rules for agents.
##### code
Defines default implementation habits such as test-first work and boundary discipline.
##### quality
Captures universal quality expectations that apply across the repo.
##### toolbox
Lists optional tactics or patterns that may be used when they solve a concrete problem. |


---

### `product-specs` tier
This tier turns intent into formally traceable product and domain contracts.

| Spec  | Structure                                                                   |
| ----- | --------------------------------------------------------------------------- |
| `prd` | Product Requirements Document defining scope, requirements, and constraints |
| `usm` | User Story Map defining activities, workflows, stories, and release slices  |
| `dm`  | Domain Model defining language, boundaries, and invariants                  |

#### `prd` spec
`prd` is the formally traceable requirements contract for the product.

##### TL;DR
Briefly states what this product/feature is and why it's valuable (1–3 sentences)
- **What we’re building:** <1–2 sentences>
- **For whom:** <primary user / customer>
- **Why now:** <1 sentence — urgency or opportunity>
- **Expected outcome:** <1 sentence — measurable>

##### Problem Statement (The "Why")
Briefly describes the pain point or opportunity. What is broken, missing, or inefficient? Use data to back this up.

##### Strategic Value (The "So What")
Why do this now? How does this align with company OKRs or long-term strategy?
- **Strategic Alignment**:
- **Urgency**:

##### The Solution (The "What")

High-level description of the feature/product. Do not get bogged down in UI details yet.
**Core Value Proposition:**
One sentence description of the solution

**Features:**
| Feature     | Description         | Priority     |
| ----------- | ------------------- | ------------ |
| [Feature 1] | [Brief description] | P0 / P1 / P2 |
| [Feature 2] | [Brief description] | P0 / P1 / P2 |
| [Feature 3] | [Brief description] | P0 / P1 / P2 |

##### OKR
What does success look like? Define a clear, measurable outcome.
- **Objective**:
- **Key Results**:

##### Metrics

| Metric                  | Current Baseline | Target (Success) | Data Source |
| ----------------------- | ---------------- | ---------------- | ----------- |
| **Northstar Metric**    |                  |                  |             |
| **Indicative Metric 1** | 12% Conversion   | 15% Conversion   | Mixpanel    |
| **Indicative Metric N** | 12% Conversion   | 15% Conversion   | Mixpanel    |
| **Guardrail Metric 1**  | < 200ms Latency  | < 200ms Latency  | Datadog     |
| **Guardrail Metric N**  | < 200ms Latency  | < 200ms Latency  | Datadog     |

Two standard metrics for a feature with UX are

| Metric                    | Current Baseline | Target (Success) | Data Source |
| ------------------------- | ---------------- | ---------------- | ----------- |
| **TT - time-in-task**     |                  |                  |             |
| **AT - actions-in-task**  |                  |                  |             |
| **ST - %success-in-task** |                  |                  |             |

**Time-on-Task** - **time** it took the user to complete the task (e.g. schedule an appointment or skip a shipment)
**Actions-on-Task** - # of **actions** (button clicks, item selections, strings typed, etc.) it took the user to complete the task
**%Success-on-Task** - # of **percentage** of users who successfully complete the task

##### Timeline & Milestones

| Milestone       | Target Date |
| --------------- | ----------- |
| Functionality 1 | [Date]      |
| Functionality 2 | [Date]      |
| Functionality 2 | [Date]      |
| Launch          | [Date]      |

##### Risks & Open Questions

---


#### `usm` spec
`usm` is the User Story Map. It defines flows (workflows and user journeys) and delivery map that organizes the product into epics(use cases), flows(workflows and journeys), stories, and milestones(release slices).

| Section      | Purpose                                                            |
| ------------ | ------------------------------------------------------------------ |
| `stories`    | Breaks workflows into implementable, traceable stories.            |
| `epics`      | Defines the top-level product activities or narrative backbone.    |
| `flows`      | Groups user flows or end-to-end journeys under the backbone.       |
| `bdd`        | States the expected behavior and acceptance intent for each story. |
| `milestones` | Organizes stories into slices that can be delivered coherently.    |

- `usm` derives from `prd`.
- Stories trace to PRD requirements.
- Acceptance framing stays behavior-focused rather than technical.

#### `dm` spec
`dm` is the Domain Model as in DDD (Domain Driven Development)
It’s a semantic model of the domain and the source for technical boundary derivation.

| Section | Purpose |
| --- | --- |
| `ubiquitous language` | Defines the shared domain vocabulary. |
| `bounded contexts` | Identifies semantic boundaries and ownership zones. |
| `aggregates / entities / value objects` | Defines the core domain structures and their responsibilities. |
| `invariants / business rules` | Records the rules that must always hold true in the domain. |
| `relationships / integration touchpoints` | Describes important links between concepts and external touchpoints. |

- `dm` is the semantic source for technical boundary derivation.
- Components come from domain semantics, not folder shape.

---

### `system-specs` tier
This tier translates approved product and domain semantics into technical contracts.

| Spec | Description |
| --- | --- |
| `system` | System-level contract for system purpose, context, and external boundaries |
| `containers` | Global runtime and deployment topology contract |
| `container` | Local container contract for one runtime boundary |
| `component` | Smallest owned technical contract inside a container |

#### `system` spec
`system` defines the system as a whole and its relationship to the outside world.

##### system purpose and context
Defines what the system is and where it sits in its broader environment.

##### external actors and systems
Identifies the people, systems, and dependencies around it.

##### trust boundaries
Marks important trust, security, or authority boundaries.

##### system-wide NFR boundaries
Captures system-level NFRs that shape the whole design.

- Deployment topology does not live here.

#### `containers` spec
`containers` defines the global runtime topology of the system.

##### container inventory
Lists the containers that make up the system.

##### responsibilities
Defines the role of each container in the overall design.

##### communication paths
Describes how containers interact with each other and with external systems.

##### deployment / runtime choices
Captures runtime, hosting, or platform choices at system scope.

##### cross-container constraints
Records constraints that apply across container boundaries.

- `containers` owns global runtime topology, not local component detail.

#### `container` spec
`container` defines one local runtime boundary and the technical inventory inside it.

##### purpose and runtime boundary
Defines what the container is for and where its runtime boundary sits.

##### resident bounded contexts
Lists the bounded contexts hosted inside this container.

##### component inventory
Lists the components that belong to this container.

##### local interfaces and dependencies
Summarizes key local interfaces and internal or adjacent dependencies.

##### local NFR / operational constraints
Captures local runtime, operational, and quality constraints.

- `container` is the authoritative component inventory for one container.
- Components are discovered here, not inferred from folders.

#### `component` spec
`component` defines the smallest owned technical boundary inside the governed system.

##### responsibility
States what the component owns and why it exists.

##### owned paths
Declares the code paths or assets the component is responsible for.

##### owned interfaces
Declares the interfaces or APIs the component owns.

##### dependencies
Records direct dependencies on other components, containers, or external systems.

##### behavior / contracts
Defines the local technical contracts and expected behavior of the component.

##### local test / runtime notes
Captures local test expectations and important runtime notes.

- `component` is the smallest owned technical boundary.
- Each component belongs to exactly one bounded context.
- Each component has exactly one container home.

---

### `context` tier
This tier contains agent-facing operational truth generated from approved contract, plus non-gated decision history and non-executable behavioral projections.

| Artifact | Description |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, and similar | Scoped guidance files generated for repo, container, or component work |
| `pdr` | Product decision record generated as long-term context for product changes |
| `adr` | Architecture decision record generated as long-term context for technical changes |
| `bdd` | Generated behavioral scenarios for humans and agents to implement later |

#### `AGENTS.md` / `CLAUDE.md` / similar
These files summarize how to work safely in a specific scope.

##### scope and ownership
States what the current scope owns.

##### load-first context
Tells the agent which upstream artifacts to load first.

##### do-not-touch boundaries
Marks files, contracts, or areas that are out of scope.

##### common commands / checks
Lists common commands, checks, or workflows for that scope.

##### local caveats
Captures scope-specific warnings, quirks, or operational notes.

#### `pdr` spec
`pdr` records product-level decisions after they have already been made in contract.

##### decision
States what product-level decision was made.

##### why
Records the reason, tradeoff, or trigger for the decision.

##### contract delta
Notes which contract artifacts or sections changed because of the decision.

##### impact
Summarizes the expected downstream effect on context or code generation.

#### `adr` spec
`adr` records architecture and technical decisions after they have already been made in contract.

##### decision
States what technical decision was made.

##### why
Records the reason, tradeoff, or trigger for the decision.

##### contract delta
Notes which system-specs or product-specs changed because of the decision.

##### impact
Summarizes the expected downstream effect on context or code generation.

#### `bdd` artifact
`bdd` contains generated, non-executable Gherkin descriptions of acceptance tests for both epics and stories, produced from approved contract.

##### feature / capability
States which epic, workflow, story, or behavior the scenarios cover.

##### scenarios
Describes the generated scenarios in Gherkin form for humans or agents to implement later.

##### traceability
Links scenarios back to the relevant requirements, stories, or technical contracts.

- Context artifacts are generated from contract specs.
- Context artifacts are not human-gated and normally do not have approval-state metadata.
- Humans may review or eval context artifacts against upstream contract.
- Humans may edit context artifacts when the projection of contract is poor, but the normal fix path is still to amend contract and regenerate context.
- If a context artifact conflicts with contract, contract wins semantically.
- Context artifacts may exist at root, container, and component scopes.
- Gherkin belongs to context until it becomes executable test code.

---

### `code` tier
This tier contains executable implementation and verification artifacts.

| Artifact | Description |
| --- | --- |
| `source code` | Implements approved behavior and technical structure. |
| `tests` | Provide executable verification of behavior, contracts, and regressions. |
| `runtime / ops glue` | Handles configuration, packaging, deployment, and operational wiring. |

#### `source code`
`source code` implements approved behavior and technical structure.

#### `tests`
`tests` provide executable verification of behavior, regressions, and contract compliance.

- unit tests, integration tests, and executable BDD tests belong here
- if a runnable tests are generated from the `bdd` scenario, they become part of the executable test suite (code)

#### `runtime / ops glue`
`runtime / ops glue` handles configuration, packaging, deployment, migrations, and operational wiring.

- Code is executable, not human-gated.
- Code is produced from contract, usually through context.
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

Everything else is produced from or subordinate to explicit VibeLoom rules.

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

This archetype set is a VibeLoom heuristic informed by DDD aggregates and services, plus boundary patterns such as adapters. It is **not** presented as an Evans taxonomy.

### Container Inventory and Component Discovery

Agents do not discover components by guessing from folder names.

`container.md` is the authoritative component inventory for one container. At minimum, it lists for each component:

- component ID or official name
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
| `review` | up + lateral | Critique the current generated tier at its governance boundary and optionally apply bounded fixes within that tier |
| `eval` | up | Run formal structural and semantic checks for the current tier; tier-boundary evaluation is the normal and only governance surface |
| `fix` | top-down | Propagate approved upstream changes down to stale downstream artifacts and tiers |
| `approve` | gate | Move a reviewed contract tier from `draft` to `approved`, record provenance, and increment version |
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
10. generated `AGENTS.md` files
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
7. Review, evaluate, and approve the tier before relying on it as approved contract truth.

Approval is performed only at tier level. Individual artifacts may still be edited while shaping a tier, but the methodology-level approval surface is always the generated tier.

### Intent As Persistent Context

`intent.md` is loaded as generation context at every tier, not only when generating product-specs.

This is deliberate: intent may contain user constraints that must survive all the way into system design and code. Intent is prose-first rather than ID-traced, so its authority is enforced through persistent loading plus review and semantic evaluation.

### Bottom-Up Evaluation

Consistency and coherence checks run upward.

Every downstream artifact is evaluated against its immediate upstream contracts, but the human-facing governance surface is the current generated tier. This is why `review`, `eval`, and `approve` happen at tier boundaries even though traceability and dependency edges remain fine-grained and should be captured in a context graph.

### Change Propagation

When an upstream contract changes, dependent downstream artifacts become `stale` through explicit declared dependency edges. The system does not rely on intuition or chat memory to decide what must be revisited.

The approval boundary depends on profile:

- In `full`, the next tier does not begin until the current tier is approved.
- In `lite`, the orchestrator may generate the spec tiers in one run from drafts created earlier in that run, then pause once before code generation.

### Profiles

Profiles control workflow rigor, not artifact scope. Both profiles use the same contract stack.

| Profile | Classification | Approval behavior | Typical use |
| --- | --- | --- | --- |
| `lite` | Hidden internal classifier for safe scoping and escalation | One approval pause after the contract stack for the current run is generated; code still waits for approved specs | Smaller or lower-risk projects |
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

Only contract artifacts are approved.

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

Both operate on the affected tier as the governance surface for spec work.

### Review

VibeLoom keeps a single `review` operation. The interface may expose different options, but the methodology-level behaviors are:

- **Advisory review:** findings and proposed fixes only
- **Bounded remediation:** apply bounded fixes inside the allowed scope
- **Custom instructions:** apply explicit user instructions while staying inside review rules

Review may:

- surface contradictions, unclear assumptions, and missing links
- propose upstream or lateral corrections
- apply bounded fixes within scope

In normal top-down operation, review is performed at the generated tier boundary. Traceability and dependency analysis may still drill into individual specs and edges, but human review remains tier-level.

Review may **not** silently rewrite semantically meaningful upstream truth. When an upstream amendment changes meaning, the human chooses the direction and later approves the updated contract artifact.

### Eval Types

VibeLoom uses three named eval types.

| Eval Type | Purpose | Blocking |
| --- | --- | --- |
| Structural eval | Validate frontmatter, IDs, lifecycle rules, dependency declarations, path/spec consistency, and reference integrity | Yes |
| Semantic eval | Analyze requirement coverage, boundary sanity, componentization fit, contradiction with upstream truth, and context sufficiency | No |
| Behavioral eval | Produce on-demand Gherkin scenarios from approved contracts for later implementation | No |

Structural eval and semantic eval run against the tier currently under review, fix, or approval. The methodology-level eval surface remains the tier even when the underlying traceability and dependency graph is finer-grained.

Behavioral eval outputs belong to context, not contract. They guide humans or agents who later implement tests or scenarios in code.

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

`defaults.md` is a contract artifact: repo-scoped, durable, and always loaded. It is a **minimal constitution**, not a handbook and not a buzzword list.

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
9. Contract-based technical work must be scoped through `container.md` and `component.md`, not inferred from code alone.
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

`AGENTS.md` is regenerable context execution guidance.

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
3. Use `container.md` to discover components. Do not infer contract components from arbitrary folders.
4. Load only the relevant `dm.md`, `usm.md`, or `prd.md` slices needed to understand the touched semantics.
5. Load `containers.md` or `system.md` slices when container boundaries, deployment constraints, external interfaces, or NFR boundaries matter.

### Context Guidance

Load `AGENTS.md` only when it exists and reduces ambiguity. It helps execution, but it never substitutes for contract truth.

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

Every traced contract item below intent carries stable IDs or references appropriate to its layer.

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
