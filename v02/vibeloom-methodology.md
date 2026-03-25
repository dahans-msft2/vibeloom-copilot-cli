# VibeLoom Methodology

VibeLoom is a contract-driven methodology for long-lived vibe coding. It is built for codebases that must survive more than one generation step, more than one contributor, and more than one architectural revision without losing semantic coherence. It uses a **contract** - a tiered set of specifications validated for consistency and coherence - to code-generate an application.

This file is the source of truth for the methodology and artifact structure. Concrete templates, exact file names, CLI surface, and runtime behavior belong to implementation and must conform to this document.

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
- **Who** need their systems to survive repeated AI-assisted change by multiple contributors and architectural revision without semantic drift, while allowing multiple humans and agents to work on the system over time
- **VibeLoom** is a methodology for **contract-driven** development
- **That** preserves consistency and coherence across contract (intent-specs, product-specs, system-specs), context, and code through human-gated contract, agent-facing context, and continuous validation
- **Unlike** prompt-only or one-spec-fits-all AI-generation practices
- **VibeLoom** maintains consistency and coherence of the whole system as humans and agents work on it over time

A number of software engineering practices and methodologies have been invented to keep products consistent and coherent: PRD, User Story Mapping, Domain-Driven Design, Behavior-Driven Development, C4 system design, Test-Driven Development, and others. However, because they introduced extra ceremony and required extra effort, they were often underused or not used at all.

VibeLoom addresses these problems by generating a multi-tiered contract of structured specifications and treating this contract as an eval system and the durable source of truth rather than relying just on code, chat history, and agent memory.

VibeLoom turns the tables on the extra process/spec ceremony: now it is the agents that do the heavy lifting of generating, reviewing, and validating the entire contract/context/code stack for internal consistency and coherence, while humans keep the approval authority.

---

## Principles

The core principles of VibeLoom methodology are:

1. **The system is defined as a contract stack, not a set of stale one-off specs**
2. **The contract stack doubles as eval stack.**
3. **Agents are responsible for generation and validation, gated by humans.**
4. **Scoped context enables agent scaling.**

---

## Overview
Here is an overview of developing a system using VibeLoom:
- Human defines a **contract** for the system. Contract is generated interactively through a human-edits <-> agent-generation loop.
- To make the contract both consistent and coherent, the human validates specs through **review** (a critique loop over the current tier against approved upstream truth) and **eval** (more formal structural and semantic validation). Specs are checked against other specs in the same tier and against approved upstream tiers.
- First, the human defines **intent-specs** by iteratively shaping a high-level description of the system (`intent`) and the repo-wide defaults (`defaults`) that will govern the rest of the generation process.
- After the **intent-specs** are approved, **product-specs** (`prd`, `usm`, `dm`) are generated and validated using the same process.
- After the **product-specs** are approved, **system-specs** (`system`, `containers`, `container`, `component`) are generated and validated using the same process.
- Generation and validation of the **contract** is performed at the tier level
  - The entire tier (however many specs it includes) is generated as a single operation
  - The agent asks for approval of the entire tier after the tier is generated, to reduce approval steps.
  - The entire tier is reviewed, evaled, and approved as a single operation.
  - Even if a human edited individual specs, the review/eval/approval is performed for the entire tier as a whole to avoid inconsistency and incoherence across specs in the same tier.
  - Generation process can proceed to the next tier **only after** the entire tier (all specs in the tier) is approved.
- **context** (execution guidance artifacts, `pdr`, `bdd`, `adr`, and similar artifacts) is generated from the approved contract to help agents work effectively. Some context artifacts, such as `pdr`, `bdd`, and `adr`, may appear as byproducts of contract evolution; others are generated later as explicit execution context.
- Context artifacts do not carry lifecycle metadata such as `draft` or `approved`; they are assumed correct by default. Because agentic generation is still early, the workflow may pause after generating context so a human can optionally review or eval it against upstream specs.
- If context generation is poor, the recommended fix is to edit upstream **contract** and regenerate context. Direct human edits to **context** are an exceptional fallback, not the primary workflow.
- After the **context** is ready, the swarm of agents can generate the **code** - meaning the system itself that can be built and executed.

## The Contract Stack

### Overview

VibeLoom governs application development through a compact contract stack.
The application artifacts play the following roles:
- **contract**: human-gated, normative semantic truth. These artifacts - whether human-authored or generated - belong to human-gated tiers, are generated tier-by-tier as batches, and are approved only at the tier boundary.
- **context**: normative execution truth for agents. These artifacts are required primarily for code generation agents. They do not carry approval-state metadata and do not require human approval, although humans may review or edit them in exceptional cases.
- **code**: the executable result. Humans are not expected to edit it directly.

In this document:
- **human-gated** means downstream work may not rely on a tier until a human approves it.
- **normative** means it is a source of truth that downstream generation, execution, review, or eval in its scope must follow.
- **executable** means it can be run or checked directly.

### Generation Tiers

The artifact stack also groups into generation tiers. These tiers are the primary orchestration model for users and agents.

| Tier          | Content                                                                         | Artifacts                                                                    |
| ------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| intent-specs  | Capture user intent and normalize repo-wide defaults                            | `intent`, `defaults`                                                         |
| product-specs | Formally traceable product and domain contracts produced from approved intent   | `prd`, `usm`, `dm`                                                           |
| system-specs  | Technical contracts produced from approved product and domain semantics         | `system`, `containers`, per-container `container`, per-component `component` |
| context       | Distill execution guidance, decision records, and long-term agent memory        | execution guidance artifacts, `pdr`, `bdd`, `adr`, and similar |
| code          | This tier consists of executable implementation and verification artifacts      | source code, tests, runtime / ops glue                                       |

Tiers are a generation and governance abstraction. Review, eval, and approval happen at tier level. Fine-grained derivation should be represented in a context graph, and traceability, staleness, and loading should be inferred from that graph.
Governance binds to the tier semantics, not to a fixed list of specs inside the tier. A tier may gain or lose specs over time without changing the review, eval, and approval model.

---

### Contract Specs

A governed application owns the following contract specs:

The tier descriptions below define artifact structure and intent. Concrete document templates, field schemas, and formatting conventions belong to implementation.

| Spec         | Tier          | Role                                                                                                                                      | Primary audience    |
| ------------ | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| `intent`     | intent-specs  | Vision-like prose description of the system; may include both product and implementation wishes                                           | PMs                 |
| `defaults`   | intent-specs  | Minimal repo-wide constitution: binding global rules, technology baseline, and quality guardrails | Tech leads + agents |
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
| execution guidance artifacts | context | Scoped execution guidance distilled from contract specs | Agents |
| `pdr` | context | Product decision record that preserves product-level decision history without becoming contract truth | PMs + agents |
| `adr` | context | Architecture decision record that preserves technical decision history without becoming contract truth | Tech leads + agents |
| `bdd` | context | Generated non-executable behavioral scenarios used by humans and agents during implementation | PMs + tech leads + agents |

All semantic truth lives in contract specs. Context artifacts carry execution truth for agents and may be regenerated or, in exceptional cases, human-edited, but if a context artifact conflicts with a contract spec, the contract spec wins semantically. Context artifacts do not normally have approval-state metadata and are assumed correct by default, although the workflow may still pause for optional review while generation quality matures. Code is the executable result, although validation may run upward from code against every upstream tier.

---

### `intent-specs` tier
This tier captures user intent and turns repo-wide defaults into a binding constitution.

| Spec       | Description                                                                                                   |
| ---------- | ------------------------------------------------------------------------------------------------------------- |
| `intent`   | Relatively free-form prose description of the system, including product wishes and implementation preferences |
| `defaults` | Compact constitutional spec for repo-wide rules, technology baseline, and quality guardrails                  |

#### `intent` spec
`intent` is a relatively free-form prose description of the required application with two sections.

- functionality: describes, in relatively free form, what the application does.
- miscellania: Captures any other wishes from the creator that do not fit the functional description.

- `intent` may include both product-level and implementation-level wishes.
- `intent` stays prose-first rather than fully normalized.
- User-supplied technical preferences and constraints may enter through `intent`. They are promoted into `defaults` only when they become repo-wide and always-on. Otherwise, they are normalized into the narrowest downstream contract that actually owns them.

#### `defaults` spec
`defaults` is the minimal repo-wide constitution. It contains only always-on, globally binding defaults that downstream tiers and code must follow.

- Normalized global constraints belong here.
- Product rationale belongs in `intent`, not in `defaults`.
- Local scope guidance belongs in execution guidance, not in `defaults`.
- Detailed generation or runtime mechanics belong in implementation, not in `defaults`.
- Optional tactics and pattern catalogs do not belong in `defaults`.
- Downstream tiers must treat `defaults` as binding constitution.

The standard sections are:

| Section | Purpose |
| --- | --- |
| `repo constitution` | Records globally binding structural, workflow, and engineering rules that apply across the repo. |
| `technology baseline` | Captures repo-global technical choices that all downstream tiers should assume. |
| `quality guardrails` | Captures universal quality and correctness expectations that apply across the repo. |


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
`usm` is the User Story Map. It defines the delivery map that organizes the product into epics (use cases), flows (workflows and journeys), stories, and milestones (release slices).

| Section      | Purpose                                                            |
| ------------ | ------------------------------------------------------------------ |
| `stories`    | Breaks workflows into implementable, traceable stories.            |
| `epics`      | Defines the top-level product activities or narrative backbone.    |
| `flows`      | Groups user flows or end-to-end journeys under the backbone.       |
| `acceptance framing` | States the expected behavior and acceptance intent for each story. |
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

#### technical boundary rules
`system-specs` define the semantic-to-runtime mapping that makes technical ownership explicit.

- bounded context defines semantic home
- component defines owned technical change boundary
- container defines runtime and deployment home
- a bounded context must not span multiple containers
- components from the same bounded context must be co-located in the same container

#### component derivation
Components are derived from domain semantics first, then checked for implementation safety.

The default derivation process is:

1. Start from a bounded context in `dm`.
2. Identify aggregate candidates and their invariants.
3. Treat aggregate cores as the default first pass for component candidates.
4. Add process or workflow components when important behavior is not a natural responsibility of one aggregate.
5. Add adapter components where external systems, protocols, or translations must be isolated.
6. Add query or read components only when read complexity, ownership, or performance justifies them.
7. Merge or split candidates until each component owns a coherent write surface, clear interfaces, and a safe independent work scope.

---

### `context` tier
This tier contains agent-facing operational truth generated from approved contract, plus non-gated decision history and non-executable behavioral projections.

| Artifact | Description |
| --- | --- |
| execution guidance artifacts | Scoped guidance generated for repo, container, or component work |
| `pdr` | Product decision record generated as long-term context for product changes |
| `adr` | Architecture decision record generated as long-term context for technical changes |
| `bdd` | Generated behavioral scenarios for humans and agents to implement later |

#### execution guidance artifact
These artifacts summarize how to work safely in a specific scope.

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

##### derivation
Lists the relevant upstream requirements, stories, domain concepts, or technical contracts the scenarios are produced from.

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
- if runnable tests are generated from a `bdd` scenario, they become part of the executable test suite

#### `runtime / ops glue`
`runtime / ops glue` handles configuration, packaging, deployment, migrations, and operational wiring.

- Code is executable, not human-gated.
- Code is produced from contract, usually through context.
- Validation may run upward from code against all upstream tiers.

---

## Workflow

VibeLoom workflow governs how change moves from human request to approved contract, generated context, and executable code.

At a conceptual level, the workflow is:

1. Identify the highest affected tier.
2. Generate that tier as a batch from approved upstream truth.
3. Review, eval, and approve the tier at the tier boundary.
4. Continue downward until the required contract tiers are settled.
5. Generate context from approved contract.
6. Generate or reconcile code from approved contract and context.

Profiles and modes change workflow defaults, not tier semantics.

### Profiles

Profiles control workflow rigor, not artifact scope. Both profiles use the same contract stack.

| Profile | Meaning | Approval behavior | Typical use |
| --- | --- | --- | --- |
| `lite` | Lower-ceremony orchestration with hidden internal classification | One approval pause after the contract stack for the current run is generated; code still waits for approved specs | Smaller or lower-risk projects |
| `full` | Explicit, more ceremonial orchestration with visible tier boundaries | Tier-by-tier approval gates before proceeding downward | Larger, longer-lived, or parallelized systems |

`lite` is intentionally less ceremonial, not less safe. `full` is intentionally more explicit, not semantically different.

### Modes

Modes control working focus, not truth semantics. They are orthogonal to profiles.

| Mode | Primary focus | Typical emphasis |
| --- | --- | --- |
| `pm` | Product and contract shaping | intent, product-specs, acceptance intent, decision framing |
| `dev` | Technical realization and delivery | system-specs, context, code, bounded technical change |

Modes may change default prompts, context emphasis, or suggested operations, but they do not change the contract stack, approval model, or tier semantics.

### Lifecycle And Approval

Contract tiers move through these lifecycle states:

- `draft`
- `approved`
- `stale`
- `superseded`

Only contract artifacts are approved. Context does not normally carry approval-state metadata, and code is judged against approved upstream truth rather than approved in the same way.

Approval is always tier-level:

- the agent generates the whole tier before asking for approval
- the human reviews and evals the tier as a whole
- generation proceeds downward only after the tier is approved

Delegated approval may exist as provenance, but it does not change the lifecycle model.

---

## Generation

Generation is the contract-driven engine of the methodology. It works in two dimensions:

- **down** through the tiers
- **across** the artifacts inside one affected tier

### Tier Order

The normal top-down order is:

```text
intent-specs -> product-specs -> system-specs -> context -> code
```

Each tier is produced from approved upstream truth:

| Tier | Primary upstream basis | Output |
| --- | --- | --- |
| `intent-specs` | human request, edits, and prior repo intent | `intent`, `defaults` |
| `product-specs` | approved `intent-specs` | `prd`, `usm`, `dm` |
| `system-specs` | approved `product-specs` | `system`, `containers`, `container`, `component` |
| `context` | approved contract stack | execution guidance artifacts, decision records, behavioral projections, and other execution artifacts |
| `code` | approved contract plus relevant context | executable implementation and tests |

Generation dependencies are set-based rather than chain-based. A downstream artifact may be produced from a set of upstream inputs:

```text
X <- [y1, y2, ... yn]
```

For root intent capture, `n` may be `0`. For downstream artifacts, sections, or entities, `n` is usually one or more.

### Within-Tier Generation

An affected tier is generated as a batch rather than as individually governed fragments.

The default within-tier flow is:

1. Generate the artifacts of the tier in dependency order.
2. Run a forward pass across the tier.
3. Run a back pass if later artifacts sharpen or correct earlier artifacts.
4. Run structural and semantic validation for the tier.
5. If necessary, run one more bounded forward-back round.
6. Mark the resulting contract artifacts as `draft`.

This is the core double-pass generation model of VibeLoom.

This chapter describes generation at tier and artifact level. Finer-grained section and entity derivation belongs to the context graph.

### Intent As Persistent Context

`intent` persists as generation context across every lower tier, not only when producing `product-specs`.

This is deliberate: user wishes and constraints may survive all the way into system design and code, even when they were not fully normalized into later specs.

### Generation And Staleness

When approved upstream truth changes, dependent downstream artifacts become `stale` through explicit graph edges. Generation is therefore not only a bootstrap mechanism; it is also the way the stack is kept coherent over time.

---

## Review, Eval, And Reconciliation

These are three distinct conceptual activities:

- `review` critiques and frames the current tier against approved upstream truth
- `eval` checks structure and semantics
- `reconciliation` realigns lower layers after approved truth changes or downstream drift is detected

Review and eval use tier boundaries as governance surfaces, even though the underlying graph remains fine-grained. Reconciliation uses the same tier model to propagate approved truth downward.

### Review

Review is the human-facing critique loop for the current tier against approved upstream truth and same-tier coherence.

It may:

- surface contradictions, ambiguity, and missing links
- propose upstream or same-tier corrections
- apply bounded fixes within the currently reviewed tier

Review does not propagate approved changes downward; that belongs to reconciliation.
Review may not silently change semantically meaningful upstream truth. When meaning changes, the human chooses the direction and later approves the updated tier.

### Eval

VibeLoom uses three named eval types:

| Eval Type | Purpose | Blocking |
| --- | --- | --- |
| `structural eval` | Validate lifecycle rules, references, required fields, declared relationships, and basic stack integrity | Yes |
| `semantic eval` | Analyze coverage, contradiction with upstream truth, componentization fit, and context sufficiency | No |
| `behavioral eval` | Produce on-demand Gherkin acceptance scenarios from approved contract for later implementation | No |

Structural eval and semantic eval normally run against the tier currently under review or approval. Behavioral eval produces context artifacts rather than new contract truth.

### Reconciliation

Reconciliation is downstream realignment after approved truth changes or downstream drift becomes visible.

It is asymmetric:

- approved upstream contract defines intended meaning
- downstream artifacts and code may reveal drift
- drift triggers proposals, not silent rewriting of approved truth

When drift appears, the human chooses one of two semantic directions:

1. Amend upstream truth, then regenerate and reconcile downstream.
2. Preserve upstream truth, then correct downstream context or code.

To prevent loops, reconciliation stays bounded:

1. Review identifies and frames the drift.
2. Human chooses semantic direction when needed.
3. Reconciliation propagates the approved direction downward.
4. Eval validates the resulting state.

---

## Operations

VibeLoom defines eight methodology-level operations. Implementations may expose them through different commands or interfaces, but the logical operations stay the same.

| Operation | Direction | Meaning |
| --- | --- | --- |
| `init` | top-down | Bootstrap a governed repo and produce the first draft contract stack |
| `generate` | top-down | Generate one affected tier from approved upstream truth using the forward-pass / back-pass model |
| `review` | current + up | Critique the current generated tier against approved upstream truth and optionally apply bounded fixes within that tier |
| `eval` | up | Run structural, semantic, or behavioral evaluation for the current tier |
| `reconcile` | down | Propagate approved upstream changes downward into stale downstream tiers, context, or code |
| `approve` | gate | Move a reviewed contract tier from `draft` to `approved` and record approval provenance |
| `status` | read-only | Show lifecycle state, graph health, stale propagation, and coverage gaps |
| `import` | bottom-up | Reconstruct candidate contract from an unmanaged or heavily drifted codebase |

Exact parameters, flags, file formats, and CLI surfaces belong to implementation, not to methodology.

---

## Context Graph

VibeLoom relies on an explicit context graph rather than on implicit chat memory.

The graph connects addressable items defined inside contract, context, and code artifacts so humans and agents can answer:

- what is produced from what
- what becomes stale if something changes
- what must be loaded for a given task
- how downstream work can be traced back to upstream truth

The only item-to-item relationship in the graph is the primary relation `derivation`.

### Derivation

Each downstream item records the set of upstream inputs it is produced from:

```text
downstream_item <- [input1, input2, ... inputn]
```

This allows one downstream section or entity to depend on multiple semantic inputs without forcing the methodology into artificial `1:n` or `n:n` terminology.

For root intent capture, `n` may be `0`. For downstream items, `n` is usually one or more.

### Containment And Ownership

Items are owned by the artifact in which they are defined.

Conceptually:

```text
item -> section -> artifact -> tier
```

Ownership therefore comes from containment, not from a separate item-to-item graph relation.

### Derived Views

Several useful views are inferred from derivation plus containment:

- **traceability:** walk derivation upward or downward to explain where an item came from and what it influences
- **staleness:** if an upstream item changes, mark all reachable downstream items and their containing artifacts as stale
- **loading:** load the smallest artifact or scope that contains the required downstream item and its upstream inputs
- **artifact impact:** summarize item-level derivations upward into affected sections, artifacts, and tiers

### Context Loading

Context loading is graph traversal, not guesswork.

The conceptual rules are:

- always start from the smallest scope that still preserves the required truth
- load governing contract before relying on context artifacts
- use context artifacts to accelerate execution, never to override contract
- escalate upward when it is unclear whether a change stays within one component, bounded context, or container
- keep generation and review aware of persistent intent when that intent still constrains the change

### Why The Graph Matters

The context graph is what makes VibeLoom scalable for swarms of agents and long-lived repos.

It supports:

- minimal safe context loading
- impact analysis
- stale detection
- eval grounding
- ownership clarity through containment
- parallel work allocation

---

## Defaults vs Execution Guidance

At the conceptual level, these artifacts solve different problems.

- `defaults` is contract. It records the always-on constitutional defaults of the repo.
- `execution guidance` is context. It records scope-specific guidance generated from approved truth.

So:

- `defaults` says what is globally binding across the repo
- `execution guidance` says how to work safely and effectively in this scope right now

If execution guidance conflicts with contract, contract wins semantically.

Exact file layouts, metadata formats, and generation mechanics belong to implementation.

---

## Brownfield Import vs. Steady-State Bugfix

VibeLoom treats these as different conceptual paths.

- **Brownfield import** is the bootstrap path for unmanaged or heavily drifted repos. It reconstructs candidate contract from existing code and marks uncertainty explicitly for human review.
- **Steady-state bugfix** is the governed path for repos already under VibeLoom. It starts from repro, expected behavior, the violated or missing contract, and regression coverage.

Once a repo is governed, routine defects should be resolved against approved contract truth rather than by re-inferring semantics from code on every fix.

---

## Summary

VibeLoom is strongest where prompt-only generation stops being reliable.

It works by:

- turning intent into a durable contract stack
- generating that stack tier-by-tier with human gating at tier boundaries
- using context as agent-facing execution truth without letting it outrank contract
- reconciling downstream artifacts when approved truth changes
- relying on an explicit context graph instead of chat-memory guesswork

The methodology is intentionally stricter than ad hoc AI coding because safe speed requires explicit boundaries, explicit authority, explicit generation flow, and explicit context management.
