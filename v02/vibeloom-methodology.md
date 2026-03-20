# VibeLoom Methodology

VibeLoom is a contract-driven methodology for long-lived vibe coding. It is built for codebases that must survive more than one generation step, more than one contributor, and more than one architectural revision without losing semantic coherence.

This document owns conceptual methodology truth. It defines what VibeLoom means, not the concrete skill packaging or file layout that a particular implementation uses.

---

## What VibeLoom Is

VibeLoom governs generated software through a stack of canonical contracts and derived execution guidance.

It is designed for projects where:

- code must survive repeated AI-assisted change
- multiple humans and agents may work on the same system over time
- semantic drift is more dangerous than the ceremony of maintaining a compact contract layer

VibeLoom optimizes for three things at once:

1. **Human reviewability** of intent, requirements, domain meaning, and architecture
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

All of these problems predate coding agents. Agents amplify them by increasing both the speed and the volume of change.

---

## Core Thesis

These principles anchor the methodology:

1. **Intent must become contracts, not remain chat history.**
2. **Structured contracts are cheaper to review than generated code.**
3. **The contract stack doubles as the evaluation stack.**
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

## Conceptual Contract Layers

VibeLoom uses a layered contract model. Each layer stabilizes a different kind of truth.

| Layer | Purpose | Authority |
| --- | --- | --- |
| Constitutional defaults | Repo-wide foundations, global constraints, ownership rules, and universal defaults | Canonical |
| Intent | Product purpose, rationale, and non-normalized user intent | Canonical |
| Requirements | Functional requirements and non-functional requirements | Canonical |
| Workflow and story layer | User stories, workflow structure, acceptance framing, and delivery slices | Canonical |
| Domain layer | Bounded contexts, aggregates, invariants, and ubiquitous language | Canonical |
| System layer | System context, external actors and systems, and high-level trust or NFR boundaries | Canonical |
| Deployment/runtime layer | Runtime boundaries, communication topology, and deployment constraints | Canonical |
| Container layer | Local runtime boundary and the set of technical boundaries that live within it | Canonical |
| Component layer | The smallest owned technical boundary for safe implementation and change | Canonical |
| Derived execution guidance | Scoped working guidance distilled from canonical truth for a specific execution context | Derived |

All normative truth lives in canonical layers. Derived execution guidance helps agents work safely, but it never outranks the contracts that produced it.

Code is not part of the contract stack. It is the downstream implementation governed by the stack.

---

## Conceptual Technical Boundary Model

VibeLoom uses two named foundations:

- **DDD** for semantic modeling: bounded contexts, aggregates, invariants, and ubiquitous language
- **C4** for system and deployment description

Everything else is derived from or subordinate to explicit VibeLoom rules.

### Bounded Contexts, Containers, and Components

These relationships are normative:

1. **The component is the primary unit of ownership, safe change, and agent work allocation.**
2. **Every component belongs to exactly one bounded context.**
3. **Every component has exactly one container home.**
4. **A bounded context must not span multiple containers.**
5. **Components from the same bounded context must be co-located in the same container.**
6. **A container may host multiple bounded contexts.**

This gives VibeLoom a clear semantic-to-runtime mapping:

- a bounded context defines semantic home
- a component defines owned technical change boundary
- a container defines runtime and deployment home

### Component Derivation

VibeLoom does not derive components from code layout or deployment layout. It derives them from semantics first, then validates them against implementation safety.

The default derivation logic is:

1. Start from one bounded context in the domain layer.
2. Identify aggregate candidates and their invariants.
3. Treat aggregate cores as the default first pass for component candidates.
4. Add process or workflow components when important behavior is not a natural responsibility of one aggregate.
5. Add adapter components where external systems, protocols, or translations must be isolated.
6. Add query or read components only when read complexity, ownership, or performance justifies them.
7. Merge or split candidates until each component owns a coherent write surface, clear interfaces, and a safe independent work scope.

This archetype set is a VibeLoom heuristic informed by DDD aggregates and services, plus boundary patterns such as adapters. It is not presented as a canonical Evans taxonomy.

---

## Workflow Semantics And Governance

VibeLoom distinguishes between conceptual workflow semantics and concrete runtime commands. The methodology defines the logical lifecycle of governed change, not the exact command surface.

### Conceptual Lifecycle

The normal top-down flow is:

1. capture or refine intent
2. normalize global defaults
3. define requirements
4. expose workflows and stories
5. stabilize the domain model
6. define system and runtime boundaries
7. define container and component boundaries
8. generate or modify code

### Profiles

Profiles control workflow rigor, not artifact scope. Both profiles use the same conceptual stack.

- **Lite** keeps the safety logic but hides most of the workflow ceremony from the user.
- **Full** makes change classification and approval gates explicit.

Lite is intentionally less ceremonial, not less safe. Full is intended for longer-lived systems, parallel execution, or higher coordination risk.

### Lifecycle States

Canonical artifacts move through a limited lifecycle:

- draft
- approved
- stale
- superseded

There is no separate lifecycle state for delegated approval. Delegated approval is provenance about how approval happened, not a different kind of artifact state.

### Human Governance

Only canonical contracts are approved. Humans remain the authority over semantically meaningful truth even when agents draft, critique, or reconcile artifacts.

When approval is delegated through a chosen workflow mode, the artifact may still become approved for orchestration purposes, but the distinction between direct human review and delegated approval must remain visible.

---

## Review, Eval, And Reconciliation

Review and evaluation are related but distinct.

- **Review** is human-facing critique plus optional bounded remediation.
- **Evaluation** is structured validation of the current scope against the current rules.

### Review

Review may:

- surface contradictions, unclear assumptions, and missing links
- propose upstream or lateral corrections
- apply bounded fixes within the allowed scope

Review may **not** silently rewrite semantically meaningful upstream truth. When an upstream amendment changes meaning, a human chooses the direction and later approves the updated canonical contract.

### Evaluation Tiers

VibeLoom uses three conceptual evaluation tiers:

| Tier | Type | Purpose | Blocking |
| --- | --- | --- | --- |
| 1 | Structural | Validate identity, lifecycle, declared dependencies, and reference integrity | Yes |
| 2 | Semantic | Analyze coverage, contradiction, boundary sanity, and context sufficiency | No |
| 3 | Behavioral | Derive behavioral scenarios from approved contracts for later implementation | No |

Behavioral outputs are not canonical truth. They guide later implementation and verification.

### Asymmetric Reconciliation

Reconciliation is asymmetric:

- approved upstream contracts define intended semantics
- downstream contracts and code may reveal drift
- drift triggers proposals, not silent rewriting of approved truth

When drift appears, one of two directions is chosen:

1. Amend upstream truth, then propagate change downward
2. Preserve upstream truth, then correct downstream artifacts or code

Humans choose whenever the resolution changes meaning.

### Bounded Reconciliation

To prevent endless loops:

1. review identifies and frames the drift
2. human chooses the semantic direction when needed
3. downstream artifacts are repaired or regenerated
4. evaluation validates the resulting state

---

## Constitutional Defaults vs Derived Guidance

VibeLoom distinguishes between two different kinds of execution support:

- **constitutional defaults**, which are canonical and repo-wide
- **derived execution guidance**, which is scoped, regenerable, and non-canonical

The constitutional layer exists to answer:

- which foundations govern the project
- which global constraints are binding
- which ownership and boundary rules are universal
- which universal quality and execution defaults always apply

Derived execution guidance exists to answer:

- what this current scope owns
- what should be loaded first
- what should not be touched
- which local caveats matter right now

This distinction matters because agents need small working briefs, but those briefs must never become semantic truth.

---

## Context Principles

Agents have finite attention. VibeLoom therefore uses deterministic context scoping.

### Global Grounding

Execution should always remain grounded by the constitutional layer. Repo-wide rules and global constraints must stay in view even when the active work scope is narrow.

### Intent Loading

Intent should accompany:

- generative work
- review
- repo-wide architectural decisions

It does not have to be loaded for every purely local execution step once approved downstream contracts already capture the necessary constraints.

### Scope-First Loading

For technical work:

1. start from the smallest owned technical boundary if one specific boundary is being changed
2. start from the local runtime boundary if the question is about local inventory or local structure
3. load only the relevant requirements, workflow, or domain slices needed to understand touched semantics
4. escalate to broader system or deployment context when external interfaces, runtime boundaries, or NFR boundaries matter

Derived execution guidance may summarize scope, but it never substitutes for canonical truth.

### Escalation Rule

If an agent is unsure whether a change stays within one component, one bounded context, or one container, it must escalate scope upward rather than under-scope the context.

---

## Traceability

Formal traceability begins at the requirements layer. Intent remains prose-first and authoritative, but it is not ID-traced.

The core conceptual chain is:

```text
requirement -> story/workflow -> bounded context / aggregate / invariant -> system/runtime/container/component boundary -> behavioral scenario -> code
```

This chain enables:

- impact analysis
- coverage verification
- stale detection
- grounded evaluation findings

Every traced canonical item below intent should carry stable identity and dependency declarations appropriate to its layer.

When approved upstream truth changes, dependent downstream artifacts become stale through explicit declared edges rather than intuition or chat memory.

---

## Brownfield Import vs Governed Bugfix

VibeLoom treats these as different paths.

- **Import** is the bootstrap path for unmanaged or heavily drifted systems. It reconstructs candidate contracts from code and marks uncertainty explicitly for human review.
- **Governed bugfix** is the steady-state path for already governed systems. It starts from repro, expected behavior, the violated or missing contract, and regression coverage.

Once a system is governed, routine defects should be resolved against the approved stack rather than by re-inferring semantics from code on every fix.

---

## Summary

VibeLoom is strongest where prompt-only generation stops being reliable.

It works by:

- turning intent into a durable contract stack
- making semantic and technical boundaries explicit enough for humans and agents to share
- separating canonical truth from derived execution guidance
- allowing agents to move fast without losing semantic ownership, reviewability, and traceability

The methodology is intentionally stricter than ad hoc AI coding because safe speed requires explicit boundaries, explicit authority, and explicit context rules.
