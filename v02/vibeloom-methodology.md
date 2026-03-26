# VibeLoom Methodology

VibeLoom is a contract-driven methodology for long-lived vibe coding. It is built for codebases that must survive more than one generation step, more than one contributor, and more than one architectural revision without losing semantic coherence. It uses a **contract** - a tiered set of specifications validated for consistency and coherence - to code-generate an application.

This file is the source of truth for the methodology and artifact structure. Concrete templates, exact file names, CLI surface, and runtime behavior belong to implementation and must conform to this document.

---

## The Problem

AI code generation produces local momentum but fails to preserve consistency and coherence long-term. As a project grows, it suffers from:

- **Semantic drift** — concepts and invariants shift subtly with every prompt
- **Invisible governance** — intent lives only in chat history with no durable review surface
- **Context fragmentation** — large codebases exceed one agent's context, making ownership guesswork
- **Reconciliation failure** — manual edits and drift have no principled path back to specifications

---

## The Solution

VibeLoom generates a multi-tiered contract of structured specifications and treats it as both the durable source of truth and the eval system. Agents do the heavy lifting of generating, reviewing, and validating the entire contract/context/code stack for internal consistency and coherence. Humans keep approval authority.

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
- To make the contract both consistent and coherent, the human validates specs through **review** (a critique loop over the current governance surface against approved upstream truth) and **eval** (more formal structural and semantic validation). Specs are checked against other specs in the same tier and against approved upstream tiers.
- Every run starts with **intent-specs** by iteratively shaping a high-level description of the system (`intent`) and the repo-wide defaults (`defaults`) that will govern the rest of the generation process.
- The run then proceeds downward through **product-specs** (`prd`, `usm`, `dm`) and **system-specs** (`system`, `containers`, `container`, `component`) as needed.
- Generation and validation of the **contract** use one of two governance profiles:
  - `full` uses **tier-scope approval**
  - `lite` uses **contract-scope approval** across the affected contract stack for the current run
- In `full`, each affected contract tier is generated, reviewed, evaled, and approved as one unit before the run proceeds to the next lower contract tier.
- In `lite`, the affected contract stack is generated first and then reviewed, evaled, and approved as one unit before context and code proceed.
- **context** (execution guidance artifacts, `pdr`, `bdd`, `adr`, and similar artifacts) is generated from the approved contract to help agents work effectively. Some context artifacts, such as `pdr`, `bdd`, and `adr`, may appear as byproducts of contract evolution; others are generated later as explicit execution context.
- Context artifacts do not carry lifecycle metadata such as `draft` or `approved`; they are assumed correct by default. In `full`, context is still a visible boundary and the workflow pauses before code so a human can review or eval it against upstream specs. In `lite`, context normally flows directly into code.
- If context generation is poor, the recommended fix is to edit upstream **contract** and regenerate context. Direct human edits to **context** are an exceptional fallback, not the primary workflow.
- After the **context** is ready, the swarm of agents can generate the **code** - meaning the system itself that can be built and executed.

## The Contract Stack

### Overview

VibeLoom governs application development through a compact contract stack.
The application artifacts play the following roles:
- **contract**: human-gated, normative semantic truth. These artifacts - whether human-authored or generated - belong to human-gated tiers, are generated tier-by-tier as batches, and are approved at the current governance boundary (`full`: tier scope, `lite`: contract scope across the affected contract stack for the run).
- **context**: normative execution truth for agents. These artifacts are required primarily for code generation agents. They do not carry approval-state metadata and do not require human approval, although humans may review or edit them in exceptional cases.
- **code**: the executable result. Humans are not expected to edit it directly.

In this document:
- **human-gated** means downstream work may not rely on a tier until a human approves it.
- **normative** means it is a source of truth that downstream generation, execution, review, or eval in its scope must follow.
- **executable** means it can be run or checked directly.

The contract stack separates semantic truth, execution truth, and executable result.

```mermaid
graph TD
    H[Human Request] --> T1

    subgraph T1 [intent-specs]
        direction LR
        intent[intent] --> defaults[defaults]
    end
    T1 --- A1([approved])

    A1 --> T2
    subgraph T2 [product-specs]
        direction LR
        prd[prd] --> usm[usm] --> dm[dm]
    end
    T2 --- A2([approved])

    A2 --> T3
    subgraph T3 [system-specs]
        direction LR
        system[system] --> containers[containers] --> container[container] --> component[component]
    end
    T3 --- A3([approved])

    A3 --> T4
    subgraph T4 [context]
        direction LR
        exec_guidance[execution guidance] ~~~ pdr[pdr] ~~~ adr[adr] ~~~ bdd[bdd]
    end

    T4 --> T5
    subgraph T5 [code]
        direction LR
        source[source code] ~~~ tests[tests] ~~~ ops[runtime / ops glue]
    end

    style T1 fill:#e8f4fd,stroke:#1a73e8
    style T2 fill:#e8f4fd,stroke:#1a73e8
    style T3 fill:#e8f4fd,stroke:#1a73e8
    style T4 fill:#fff3e0,stroke:#e65100
    style T5 fill:#e8f5e9,stroke:#2e7d32
```

### Generation Tiers

The artifact stack also groups into generation tiers. These tiers are the primary orchestration model for users and agents.

| Tier          | Content                                                                         | Artifacts                                                                    |
| ------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| intent-specs  | Capture user intent and normalize repo-wide defaults                            | `intent`, `defaults`                                                         |
| product-specs | Formally traceable product and domain contracts produced from approved intent   | `prd`, `usm`, `dm`                                                           |
| system-specs  | Technical contracts produced from approved product and domain semantics         | `system`, `containers`, per-container `container`, per-component `component` |
| context       | Distill execution guidance, decision records, and long-term agent memory        | execution guidance artifacts, `pdr`, `bdd`, `adr`, and similar |
| code          | This tier consists of executable implementation and verification artifacts      | source code, tests, runtime / ops glue                                       |

Tiers are a generation and governance abstraction. In `full`, review, eval, and approval act at tier scope. In `lite`, review, eval, and approval act at contract scope across the affected contract tiers for the current run. Fine-grained derivation should be represented in a context graph, and traceability, staleness, and loading should be inferred from that graph.
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

All semantic truth lives in contract specs. Context artifacts carry execution truth for agents and may be regenerated or, in exceptional cases, human-edited, but if a context artifact conflicts with a contract spec, the contract spec wins semantically. Context artifacts do not normally have approval-state metadata and are assumed correct by default. In `full`, the workflow pauses at the context boundary before code. In `lite`, context normally flows directly into code. Code is the executable result, although validation may run upward from code against every upstream tier.

---

### `intent-specs` tier
Captures user intent and normalizes repo-wide defaults.

| Spec | Contract entities | Key rules |
| --- | --- | --- |
| `intent` | CAP-#### (capabilities), WISH-#### (wishes) | Prose-first; may include both product and implementation wishes. Preferences become `defaults` only when repo-wide and always-on. |
| `defaults` | CST-#### (constraints) | Minimal repo-wide constitution. Only always-on, globally binding constraints. Downstream tiers treat `defaults` as binding. |

---

### `product-specs` tier
Turns approved intent into formally traceable product and domain contracts.

| Spec | Contract entities | Derives from | Key rules |
| --- | --- | --- | --- |
| `prd` | FR-#### (functional requirements), NFR-#### (non-functional requirements) | CAP-####, WISH-#### | Every FR and NFR traces to at least one capability or wish. |
| `usm` | EPIC-#### (epics), FLOW-#### (flows), STORY-#### (stories), ACC-#### (acceptance criteria), MS-#### (milestones) | FR-#### | Every STORY traces to at least one FR. Every EPIC has at least one FLOW; every FLOW has at least one STORY. Acceptance framing stays behavior-focused. |
| `dm` | TERM-#### (ubiquitous language terms), BC-#### (bounded contexts), AGG-#### (aggregates), ENT-#### (entities), VO-#### (value objects), INV-#### (invariants) | FR-####, NFR-#### | `dm` is the semantic source for technical boundary derivation. Components come from domain semantics, not folder shape. |

---

### `system-specs` tier
Translates approved product and domain semantics into technical contracts.

| Spec | Contract entities | Derives from | Key rules |
| --- | --- | --- | --- |
| `system` | SYS-#### (system context items) | BC-####, NFR-#### | Defines system purpose, external actors, trust boundaries, system-wide NFRs. Deployment topology does not live here. |
| `containers` | CONT-#### (containers), EDGE-#### (communication paths) | BC-####, SYS-#### | Global runtime topology. Every CONT appears in the topology. Communication paths reference valid CONT endpoints. |
| `container` | (references CONT-####, lists component inventory) | CONT-#### | Authoritative component inventory for one runtime boundary. Components are discovered here, not inferred from folders. |
| `component` | CMP-#### (components), IF-#### (interfaces), BEH-#### (behaviors), DEP-#### (dependencies) | BC-####, CONT-#### | Smallest owned technical boundary. Each component belongs to exactly one BC and one container. |

**Technical boundary rules:**
- Bounded context (BC) defines semantic home
- Component (CMP) defines owned technical change boundary
- Container (CONT) defines runtime and deployment home
- A bounded context must not span multiple containers
- Components from the same bounded context must be co-located in the same container

---

### `context` tier
Agent-facing operational truth generated from approved contract. Context artifacts do not carry lifecycle metadata and are assumed correct by default.

| Artifact | Purpose | Key entities |
| --- | --- | --- |
| execution guidance | Scoped guidance for repo, container, or component work | (no addressable IDs — prose guidance) |
| `pdr` | Product decision history | PDR-#### (product decision records) |
| `adr` | Architecture decision history | ADR-#### (architecture decision records) |
| `bdd` | Generated non-executable behavioral scenarios | BDD-#### (behavior files), SCN-#### (Gherkin scenarios) |

- Context is generated from contract. If context conflicts with contract, contract wins.
- Humans may review or eval context against upstream contract.
- The normal fix path for poor context is to amend contract and regenerate.
- Gherkin belongs to context until it becomes executable test code.

---

### `code` tier
Executable implementation and verification artifacts.

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

1. Start from `intent-specs` and identify the affected contract stack for the current run.
2. Generate the affected contract tiers as batches from approved upstream truth.
3. In `full`, review, eval, and approve each affected tier at tier scope before moving downward.
4. In `lite`, review, eval, and approve the affected contract stack as one contract-scope unit.
5. Generate context from approved contract.
6. In `full`, pause at the context boundary before code. In `lite`, continue into code by default.
7. Generate or reconcile code from approved contract and context.

Profiles change governance granularity and pause topology. Modes, applicable only in `full`, change who meaningfully reviews which non-intent contract tier by default. Neither changes artifact semantics or the contract/context/code ontology.

```mermaid
flowchart TD
    H["Human Request / Edits"]
    I["Start From Intent Specs"]
    D["Identify Affected Contract Stack"]
    G["Generate Affected Contract Tiers<br/>Using Double-Pass Model"]

    H --> I --> D --> G

    G --> R
    G --> E

    subgraph REV["Review"]
        direction TB
        R["Critique Governance Surface"]
        R1["Surface Issues, Propose Fixes"]
        R2["Apply Bounded Same-Tier Fixes"]
        R --> R1 --> R2
    end

    subgraph EVL["Eval"]
        direction TB
        E["Structural, Semantic,<br/>Behavioral Checks"]
    end

    R2 --> A["Approve<br/>At Governance Surface"]
    E --> A

    A --> C["Generate Context"]
    C --> B["Context Boundary<br/>Full: Pause, Lite: Continue"]
    B --> K["Generate Or Reconcile Code"]

    K -.-> Q
    subgraph REC["Reconciliation"]
        direction TB
        Q["Detect Downstream Drift"]
        Q1["Human Chooses Direction"]
        Q2["Propagate Downward"]
        Q --> Q1 --> Q2
    end
```

### Profiles

Profiles are run-time-switchable governance profiles. Both profiles use the same contract stack.

| Profile | Meaning | Approval behavior | Typical use |
| --- | --- | --- | --- |
| `lite` | Lower-ceremony orchestration that treats the affected contract stack for the current run as one governance surface | Contract-scope approval of the affected contract stack, followed by direct context-to-code flow by default | Clearly simple systems with one semantic bounded context and limited business logic |
| `full` | Explicit orchestration that keeps contract tiers and the context boundary visible | Tier-scope approval of each affected contract tier, plus a mandatory pause after context before code | Larger, longer-lived, parallelized, or semantically richer systems |

`lite` is intentionally less ceremonial, not less safe. `full` is intentionally more explicit, not semantically different.

Default to `lite` only when the system is clearly simple: one semantic bounded context, limited business logic, and modest technical complexity. Typical examples include a desktop utility, small internal tool, or simple SMB website. Default to `full` otherwise, especially when multiple bounded contexts are present or likely, workflows are non-trivial, boundaries matter materially, or multiple people or agents may work in parallel.

### Modes

Modes are run-time-switchable review-ownership defaults inside `full`. They do not apply conceptually in `lite`, where the contract is approved as one human-governed unit.

Regardless of mode, `intent-specs` stay explicitly human-owned and every run still begins from `intent-specs`. Mode determines which non-intent contract tier the current human is expected to review meaningfully by default.

| Mode | Meaningful human review | Default delegated approval | Typical emphasis |
| --- | --- | --- | --- |
| `pm` | `intent-specs` and `product-specs` | `system-specs` | requirements, workflows, acceptance intent, decision framing |
| `dev` | `intent-specs` and `system-specs` | `product-specs` | technical boundaries, dependencies, and executable impact |

`pm` is the default mode. Modes may change default prompts, context emphasis, or suggested operations, but they do not change the contract stack, the contract/context/code ontology, or the requirement that the contract stack be approved before context and code proceed.

Modes do not eliminate review of the non-owned contract tier. They only make it rarer.

- Delegated review of the other tier is the default only for additive or otherwise non-semantic changes.
- If generation introduces a **breaking semantic change** in the other tier, explicit review and approval of that tier becomes required before the run can complete.
- That explicit review may be performed by the current human or delegated onward to the appropriate teammate.

A **breaking semantic change** is a change to existing approved meaning, not simple addition of new material consistent with approved truth.

Examples:

- product-side: changed scope, workflow meaning, acceptance semantics, NFR target, or domain meaning
- system-side: changed bounded-context placement, ownership, interface semantics, dependency semantics, or other approved technical meaning

### Lifecycle And Approval

Contract artifacts have two lifecycle states:

- `draft` — generated or regenerated, awaiting review and approval
- `approved` — human or delegated approval recorded

Staleness is not an artifact state. It is a computed property of the context graph, inferred by comparing each downstream artifact's derivation basis against the latest approved upstream versions. The `status` command surfaces staleness; `reconcile` resolves it by regenerating affected artifacts (which return to `draft`). Supersession is implicit in git history and the `version` integer.

Only contract artifacts are approved. Context does not carry lifecycle metadata, and code is judged against approved upstream truth rather than approved in the same way.

`intent-specs` are always explicitly human-owned. Approval scope follows profile (see Profiles above). Delegated approval is mode-driven provenance — it does not change the lifecycle model, remove explicit human ownership of `intent-specs`, or override the breaking-change escalation rule.

---

## Generation

Generation is the contract-driven engine of the methodology. It works in two dimensions:

- **down** through the tiers
- **across** the artifacts inside one affected tier

### Tier Order

Every run starts from `intent-specs` and proceeds downward. Each tier is produced from approved upstream truth:

| Tier | Primary upstream basis | Output |
| --- | --- | --- |
| `intent-specs` | human request, edits, and prior repo intent | `intent`, `defaults` |
| `product-specs` | approved `intent-specs` | `prd`, `usm`, `dm` |
| `system-specs` | approved `product-specs` | `system`, `containers`, `container`, `component` |
| `context` | approved contract stack | execution guidance artifacts, decision records, behavioral projections, and other execution artifacts |
| `code` | approved contract plus relevant context | executable implementation and tests |

### Within-Tier Generation

Each affected tier is generated as a batch using a bounded double-pass cycle. In `full`, each tier pauses after this cycle for review, eval, and approval. In `lite`, the affected contract tiers are all produced first and then reviewed together at contract scope.

```mermaid
flowchart TD
    T["Choose Affected Contract Tier"]
    O["Generate Artifacts In Dependency Order"]
    F["Run Forward Pass Across The Tier"]
    B["Run Back Pass If Later Artifacts<br/>Sharpen Earlier Ones"]
    V["Run Structural And Semantic Validation"]
    R["Run One More Bounded<br/>Forward-Back Round If Needed"]
    D["Emit Contract Artifacts As Draft"]

    T --> O --> F --> B --> V --> R --> D
```

### Intent As Persistent Context

`intent` persists as generation context across every lower tier, not only when producing `product-specs`.

This is deliberate: user wishes and constraints may survive all the way into system design and code, even when they were not fully normalized into later specs.

### Generation And Staleness

When approved upstream truth changes, dependent downstream artifacts become stale as computed by the context graph. Generation is therefore not only a bootstrap mechanism; it is also the way the stack is kept coherent over time. Staleness is never written into artifact frontmatter — it is inferred from version comparisons in the graph and surfaced by the `status` command.

---

## Review, Eval, And Reconciliation

These are three distinct conceptual activities:

- `review` critiques and frames the current governance surface against approved upstream truth
- `eval` checks structure and semantics
- `reconciliation` realigns lower layers after approved truth changes or downstream drift is detected

Review and eval use the current governance surface, even though the underlying graph remains fine-grained: tier scope in `full`, contract scope across the affected contract stack in `lite`. Reconciliation uses the same tier model to propagate approved truth downward.

Review, eval, and reconciliation are shown together in the Workflow diagram above.

### Review

Review is the human-facing critique loop for the current governance surface against approved upstream truth and same-tier coherence.

It may:

- surface contradictions, ambiguity, and missing links
- propose upstream or same-tier corrections
- apply bounded fixes within the currently reviewed governance surface

Review does not propagate approved changes downward; that belongs to reconciliation.
Review may not silently change semantically meaningful upstream truth. When meaning changes, the human chooses the direction and later approves the updated tier.

### Eval

VibeLoom uses three named eval types:

| Eval Type | Purpose | Blocking |
| --- | --- | --- |
| `structural eval` | Validate lifecycle rules, references, required fields, declared relationships, and basic stack integrity | Yes |
| `semantic eval` | Analyze coverage, contradiction with upstream truth, componentization fit, and context sufficiency | No |
| `behavioral eval` | Produce on-demand Gherkin acceptance scenarios from approved contract for later implementation | No |

Structural eval and semantic eval normally run against the governance surface currently under review or approval. Behavioral eval produces context artifacts rather than new contract truth.

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

The context graph combines item derivation with containment and derives traceability, staleness, loading, and artifact impact.

```mermaid
flowchart TD
    U1["Upstream Item A"]
    U2["Upstream Item B"]
    D["Downstream Item"]

    U1 -- "Derivation" --> D
    U2 -- "Derivation" --> D

    D -- "Contained In" --> S["Section"]
    S -- "Contained In" --> A["Artifact"]
    A -- "Contained In" --> T["Tier"]

    D -.-> TV["Traceability"]
    D -.-> SV["Staleness"]
    D -.-> LV["Loading"]
    D -.-> IV["Artifact Impact"]
```

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
- **staleness:** if an upstream item changes, flag all reachable downstream items and their containing artifacts as stale in the graph (not in artifact frontmatter)
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

- `defaults` is **contract** — always-on, globally binding repo-wide constraints
- `execution guidance` is **context** — scope-specific operational guidance generated from approved truth

If they conflict, contract wins.

---

## Brownfield Import vs. Steady-State Bugfix

VibeLoom treats these as different conceptual paths.

- **Brownfield import** is the bootstrap path for unmanaged or heavily drifted repos. It reconstructs candidate contract from existing code and marks uncertainty explicitly for human review.
- **Steady-state bugfix** is the governed path for repos already under VibeLoom. It starts from repro, expected behavior, the violated or missing contract, and regression coverage.

Once a repo is governed, routine defects should be resolved against approved contract truth rather than by re-inferring semantics from code on every fix.

Brownfield import reconstructs contract bottom-up; steady-state bugfix updates approved truth top-down.

```mermaid
flowchart TD
    S["Change Starting Point"]

    S --> BROWN
    S --> STEADY

    subgraph BROWNFIELD["Brownfield Import"]
        direction TB
        B1["Start From Unmanaged<br/>Or Heavily Drifted Codebase"]
        B2["Reconstruct Candidate Contract Bottom-Up"]
        B3["Review / Eval / Approve<br/>Reconstructed Contract"]
        B4["Generate Context From Approved Contract"]
        B5["Reconcile Or Regenerate Code<br/>Against Approved Truth"]

        B1 --> B2 --> B3 --> B4 --> B5
    end

    subgraph BUGFIX["Steady-State Bugfix"]
        direction TB
        S1["Start From Existing Approved Contract"]
        S2["Identify Highest Affected Tier"]
        S3["Update Affected Contract Truth Top-Down"]
        S4["Generate Context From Approved Contract"]
        S5["Reconcile Or Regenerate Code"]

        S1 --> S2 --> S3 --> S4 --> S5
    end
```

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
