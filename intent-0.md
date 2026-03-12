---
status: under-review
owner: methodology
approved-by:
last-reviewed: YYYY-MM-DD
upstream-refs: []
---

# Intent for the Contract-Driven Vibe Coding Skill
Terminology
- Agent with capital A - an AI code generation system such as Claude or Codex. A small case agent is used more freely and its meaning can be derived from the semantic context.

## 0. Summary
- A structured  definition of a methodology for iterative contract-driven vibe coding of production-quality systems. The methodology defines a vibe coding process that goes from intent (prose) to code via generating multiple tiers of structured specs:
  — intent
  — prd
  — user story map
  — domain model (with multiple bounded contexts if needed)
  — architecture/design spec (overall),
  — architecture/design spec (for each module),
  — AGENTS.md (both for the system and for each module)
  each spec is gated by human review and approval. At each level any spec can be edited manually, and then the entire
  stack of specs both upstream and downstream is verified against the manually edited one for consistency and conformance.
- The main deliverable is a skill for Claude and Codex that enables a user to vibe-code, extend and long-term maintain an application using this methodology.

## 1. Core Thesis
- Prompt-first generation is insufficient for long-lived systems. Prompts are usually a vague prose and by definition cannot serve as a contract. Multiple semantic layers are missing between the prompt (intent) and the code - pre, user story map, domain model, architecture/design specs and so on.
- Historically, software teams were not strict about maintaining a full set of high quality artifacts - too much overhead to create and keep them consistent. With Agents, it’s changed. It does not mean we need to return to generating gigantic specs that nobody reads. On the contrary, we need to generate a set of highly structured concise specs that humans will read, verify and spot-edit to correct the AI-generated artifacts.
- Upstream specs must act as evals for downstream work. Every derived artifact and every implementation unit is checked against its upstream contracts

## 2. Canonical Contract Stack
Each artifact is an .md file in Markdown format.
Each artifact has a template named <artifact>-template.md.
The templates are part of the skill.
Artifacts must be highly structured and assign IDs to all items defined in the artifact for better parsing by the Agent
— intent (the future prompt for the Agent) - a loose-prose description of the system
- prd (Product Requirements Document) - A typical PRD 
- usm (user story map) - enumerates epics and stories and structured them.
- dm (domain model) (with multiple bounded contexts if needed) - Domain model as in DDD (domain driver design) that defines entities and entity relationships surfaced to all system users - but not the internal technical details of the system. this is the central component of the methodology - it maintains the user value/semantics of the system regardless of the design and implementation detail
- spec (architecture/design spec) - runtime architecture/design, data/storage, security, observability, module derivation, deployment architecture, etc. all the technical details go here
— AGENTS.md (both for the system and for each module) - the usual AGENTS.md/CLAUDE.md
- plan (execution plan) - what Agent generates in planning mode, before the human approves and code generation starts.

## 3. Design Rules

- [ ] Use three profiles:
      — **Lite** (single bounded context)
      — **Full** (multiple bounded contexts).
- [ ] Select the profile from semantic shape and coordination risk, not code size.
- [ ] Treat `usm.md` as the authoritative behavior model.
- [ ] Treat `dm.md` as the authoritative semantic model.
- [ ] Treat `spec.md` as the authoritative technical design.
- [ ] Keep `plan.md` as the canonical execution brief.
- [ ] Make repeated rules mechanically checkable wherever feasible.
- [ ] Require human approval before authoritative artifacts become `approved`.
- [ ] After an approved upstream change, mark impacted downstream artifacts `stale`, regenerate them, re-evaluate them, and re-approve them.
- [ ] Prefer downstream coherence over faster initial generation.

## 4. Required Capabilities

| Capability | Method requirement |
| --- | --- |
| Safe multi-session work | Durable contracts, lifecycle states, explicit context loading |
| Safe parallel work | Domain-model-derived modules, explicit interfaces, write-surface ownership |
| Long-term maintainability | TDD, traceability, invariants, observability, regeneration after upstream changes |
| Controlled flexibility | Lite, and Full profiles, progressive dm.md formalization, conditional contracts/modules, thin wrappers |
| Human governance | Approval gates, auditable change records, explicit stale cascade |

## 5. Workflow
- A human creates a new project/application.
- The Agent clones intent-template.md into intent.md. intent.md is now in “draft” state
- The human can edit (multiple time) the intent.md - either in an editor or interactively interviewed by the Agent.
- When human approves the intent.md, its status changes to “approved” and the Agent now generates prd.md (based on the template) - in “draft” state.
- After generating prd.md, the Agent generates User Story Map. This helps to reveal entities, user types and workflow that should help generate a high-quality Domain Model (dm.md)
- After USM, the Agent generates the DM (Domain Model in dm.md)
- prd, sum and dm are generated sequentially, one is used to generate the next
- When all three are ready, the user is asked to review/approve all three of them. The user can edit any of the three, teh Agent needs to eval the other two as well as the intent.md against the changes, and present the inconsistencies to the user. The user needs to reconcile the specs until they are consistent before proceeding to generating technical specs.
- After the product-level specs are approved and reconciled, the Agent needs to decide which profile to use. Based on the chosen profile, the Agent generates spec.md that describes the application and modules. Modules are a mechanism of breaking the application into semi-independent units so that different people and different code generation agents (swarm of agents) can work on a module w/o affecting the others. Each module resides in its own folder and has its own spec.md and AGENTS.md. The shared context/info is in upstream specs (intent.md, prd.md, usm.md and the root spec.md)
- If a user edits an artifact manually. The Agent needs to eval all upstream artifact for consistency - are they still consistent with the newly updated downstream artifact. The Agent reviews the upstream artifacts and, if inconsistency is found, proposes how to update them.
- After the upstream chain is brought back to consistency by the human user, the Agent reviews the downstream artifacts and proposes updates to downstream artifacts and the code.
- The same idea repeats - after a spec/contract is generated, it’s eval-ed agains the upstream specs to ensure overall consistency. Then a user is given an opportunity to review/edit the spec. Then the Agent needs do the evals again, present inconsistencies to the user and the generation can only proceed past this step if all specs are reconciled.

## 6. Packaging
The objective is to create a tool that users (mostly technically savvy Product Managers and UX/UI Designers) can use to iteratively and interactively vibe-code and maintain/develop relatively complex applications. It is assumed that the user is technical enough to read/understand/validate the generated code.
The tool needs to be packaged so that it can be used from within Claude Code (both app and CLI) and Codex (both app and CLI). The expected workflow is that the user
- creates a folder for a new project
- runs the tool in that folder from either Claude or Codex w/o switching to the command line

## 7. Quality Disciplines

| Discipline | Required stance |
| --- | --- |
| TDD | Default implementation loop |
| BDD | Required for user-visible behavior |
| Design by Contract | Use for important invariants and pre/postconditions |
| SOLID | Apply as heuristics when they improve maintainability without distorting the domain model |
| Traceability | Required from requirements / invariants to tests and behavior |
| Observability | Tie logs and metrics to workflows and `NFR-*` |

