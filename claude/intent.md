---
status: draft
owner: methodology
approved-by:
last-reviewed: 2026-03-12
upstream-refs:
  - artifact: ../intent.md
    note: original intent document, this is the expanded version
---

# Intent for the VibeLoom Contract-Driven Vibe Coding Skill

## Terminology

- **Agent** (capital A) — an AI code generation system such as Claude Code or Codex.
- **agent** (lowercase) — used more freely; meaning derived from context.
- **artifact** — a structured markdown file that is part of the contract stack.
- **contract stack** — the tiered set of artifacts from intent through code.
- **eval** — a consistency or completeness check of one artifact against another.
- **module** — a semi-independent unit of the application, scoped for one agent's context window.
- **profile** — a complexity tier (Lite or Full) that determines which artifacts and structures are required.

---

## 0. Summary

VibeLoom is a structured methodology and Claude Code / Codex skill for iterative, contract-driven vibe coding of production-quality systems. It transforms loose prose (intent) into working code via a tiered stack of structured specifications:

1. **intent** — loose-prose description of the system
2. **prd** — product requirements document (includes USM section in Lite profile)
3. **usm** — user story map (separate file in Full profile only)
4. **dm** — domain model (DDD-style, the semantic anchor of the methodology)
5. **spec** — architecture/design spec (runtime, data, security, modules, deployment)
6. **module specs** — per-module spec + AGENTS.md (Full profile only)
7. **AGENTS.md** — agent instruction files (root + per-module)

Each tier is gated by human review and approval. At each level, any spec can be edited manually, and the entire stack — both upstream and downstream — is verified against the edit for consistency and conformance.

**Main deliverable:** A Claude Code / Codex skill (`/vibeloom`) that enables a user to vibe-code, extend, and long-term maintain an application using this methodology. No external API costs — runs within the user's existing subscription.

---

## 1. Core Thesis

1. **Prompt-first generation is insufficient for long-lived systems.** Prompts are vague prose and cannot serve as contracts. Multiple semantic layers are missing between the prompt (intent) and the code — PRD, user story map, domain model, architecture/design specs.

2. **AI changes the economics of maintaining specs.** Historically, teams were not strict about maintaining a full set of high-quality artifacts — too much overhead. With Agents, the cost of generating and maintaining structured specs has dropped dramatically. This does not mean returning to gigantic specs nobody reads. It means generating concise, highly structured specs that humans can read, verify, and spot-edit.

3. **Upstream specs must act as evals for downstream work.** Every derived artifact and every implementation unit is checked against its upstream contracts. This is the enforcement mechanism that makes the methodology work — not just aspiration, but concrete, tiered evaluation with defined pass/fail criteria.

4. **Modularization enables multi-agent development.** Breaking the application into modules scoped to bounded contexts enables parallel agent work, controls context window usage, and provides clear ownership boundaries for incremental development.

---

## 2. Canonical Contract Stack

Each artifact is a `.md` file in Markdown format with YAML frontmatter for lifecycle tracking.
Each artifact has a template named `<artifact>-template.md` that is part of the skill.
Artifacts must be highly structured and **assign rigid IDs to all items** for machine-parseable cross-referencing.

### ID Format Convention

All items across all artifacts use a consistent, rigid ID format:

| Artifact | ID Format | Example |
|----------|-----------|---------|
| prd.md | `PRD-{nnn}` | `PRD-001`, `PRD-012` |
| usm.md | `USM-E{nn}-S{nn}` | `USM-E01-S03` (Epic 1, Story 3) |
| dm.md | `DM-{BC}-E{nn}` | `DM-BC1-E05` (Bounded Context 1, Entity 5) |
| spec.md | `SPEC-{section}-{nn}` | `SPEC-API-03`, `SPEC-MOD-02` |
| module spec | `MOD-{name}-{section}-{nn}` | `MOD-ORDERS-API-01` |
| NFRs | `NFR-{nn}` | `NFR-01` |

### Artifact Descriptions

- **intent.md** — loose-prose description of the system, the initial prompt for the Agent.
- **prd.md** — Product Requirements Document. Defines what the system must do and for whom. In Lite profile, includes a USM section inline.
- **usm.md** — User Story Map. Enumerates epics and stories in a structured format. Reveals entities, user types, and workflows. Separate file in Full profile only; inlined in prd.md for Lite.
- **dm.md** — Domain Model (DDD-style). Defines entities, entity relationships, aggregates, and bounded contexts surfaced to all system users. Does NOT include internal technical details. This is the **central semantic anchor** of the methodology — it maintains the user value/semantics of the system regardless of design and implementation detail.
- **spec.md** — Architecture/Design Spec. Runtime architecture, data/storage, security, observability, API design, module decomposition, deployment architecture. All technical details go here. In Full profile, includes interface contracts between modules.
- **Module spec.md** — Per-module architecture spec (Full profile only). Each module has its own spec.md and AGENTS.md in its directory.
- **AGENTS.md** — Agent instruction files (root + per-module). Contains coding conventions, tech stack details, boundaries, and workflow instructions.

### Artifact Frontmatter

Every artifact has YAML frontmatter:

```yaml
---
status: draft | approved | stale | approved-with-known-issues
owner: <tier name>
approved-by: <human | empty>
last-reviewed: YYYY-MM-DD
upstream-refs:
  - artifact: <relative path>
    version-hash: <8-char content hash>
profile: lite | full  # only in spec.md and below
---
```

The `version-hash` enables mechanical stale detection: if the upstream artifact's current content hash differs from the stored ref hash, the downstream artifact is automatically marked `stale`.

---

## 3. Profiles

### Lite Profile

**Use when ALL of these are true:**
- The dm.md has ≤ ~15 entities
- All entities belong to one cohesive domain (no natural bounded context boundaries)
- The expected codebase is ≤ ~50 files
- Single developer/agent will work on it
- No independently deployable components needed

| Artifact | Required? | Notes |
|----------|-----------|-------|
| intent.md | Yes | Same as Full |
| prd.md | Yes | Includes USM as an inline section |
| usm.md | No | Inlined in prd.md |
| dm.md | Yes | Single bounded context, no context map |
| spec.md | Yes | No module decomposition — whole app is one unit |
| Module specs | No | N/A |
| AGENTS.md | Yes | Single root file |
| Interface contracts | No | N/A |

**Approval gates:** 2 — (1) intent, (2) product specs batch (prd+dm), then tech spec.

**File structure:**
```
project/
├── intent.md
├── prd.md              # includes USM section
├── dm.md
├── spec.md
├── AGENTS.md
├── src/
├── tests/
└── .vibeloom/state.md
```

### Full Profile

**Use when ANY of these are true:**
- The dm.md has natural bounded context boundaries (e.g., "billing" vs "scheduling" vs "inventory")
- Multiple agents/developers will work in parallel
- The codebase will exceed ~50 files or ~10K LOC
- Independent deployment of subsystems is needed
- Different parts of the system have different tech stacks

| Artifact | Required? | Notes |
|----------|-----------|-------|
| intent.md | Yes | Same as Lite |
| prd.md | Yes | Full detail |
| usm.md | Yes | Separate file with epic groupings |
| dm.md | Yes | Multiple bounded contexts, context map, aggregate roots |
| spec.md | Yes | Module decomposition, interface contracts, deployment arch |
| Module specs | Yes | Per-module spec.md + AGENTS.md |
| AGENTS.md | Yes | Root + per-module |
| Interface contracts | Yes | Full API surface, events, shared types, dependency DAG |

**Approval gates:** 3 — (1) intent, (2) product specs batch (prd+usm+dm), (3) root spec + module specs.

**File structure:**
```
project/
├── intent.md
├── prd.md
├── usm.md
├── dm.md
├── spec.md
├── AGENTS.md
├── modules/
│   ├── mod-{name}/
│   │   ├── spec.md
│   │   ├── AGENTS.md
│   │   ├── src/
│   │   └── tests/
│   └── shared/
│       └── types/
└── .vibeloom/state.md
```

**Profile selection:** Agent proposes based on dm.md analysis (entity count, BC boundaries), user approves or overrides. Module names are auto-derived from dm.md bounded contexts; user approves or renames.

---

## 4. Design Rules

- Select the profile from semantic shape and coordination risk, not code size.
- Treat `usm.md` (or USM section in prd.md) as the authoritative behavior model.
- Treat `dm.md` as the authoritative semantic model.
- Treat `spec.md` as the authoritative technical design.
- All items in all artifacts must have rigid IDs in the defined format.
- Make eval checks mechanically performable wherever feasible.
- Require human approval before authoritative artifacts become `approved`.
- After an approved upstream change, mark impacted downstream artifacts `stale`, regenerate, re-evaluate, and re-approve them.
- Prefer downstream coherence over faster initial generation.

---

## 5. Eval Framework

Upstream specs act as evals for downstream work. Evals are performed by the Agent (no external scripts or tools required).

### Tier 1 — Structural Evals (Agent-performed, blocking)

Mechanical checks the Agent performs by reading and cross-referencing artifacts:

- **ID format compliance:** All items across all artifacts use the defined ID format.
- **Cross-reference integrity:** All IDs referenced in a downstream artifact exist in the upstream artifact they trace to.
- **Artifact completeness:** All required sections (per template) are present with content.
- **Module structure compliance (Full):** Directories and files match the module decomposition in spec.md.
- **Upstream-ref validity:** All `upstream-refs` in frontmatter point to existing, approved artifacts.

**Tier 1 failures are blocking** — generation cannot proceed until resolved.

### Tier 2 — Semantic Evals (Agent-performed, warnings)

Reasoning checks where the Agent assesses meaning and coverage:

- **Coverage matrices:** Do stories cover all requirements? Do entities cover all stories? Do modules cover all entities?
- **Contradiction detection:** Are there inconsistencies between artifact tiers?
- **Orphan detection:** Are there entities with no stories? Modules with no entities? Requirements with no stories?
- **Completeness assessment:** Does the downstream artifact fully implement its upstream contract?

**Tier 2 results are presented as warnings.** Human decides whether to fix or proceed.

### Tier 3 — Behavioral Evals (separate step, not part of spec pipeline)

Test-oriented checks, triggered by `/vibeloom generate tests`:

- **Scenario descriptions** derived from usm.md stories → test scenario .md files
- **Domain invariant checks** derived from dm.md → test specifications
- **Interface contract tests** derived from spec.md module interfaces (Full profile)
- **Actual test code generation** is a separate command, not part of the spec approval flow

### Eval Timing

- **Tier 1** runs automatically after every artifact generation or manual edit.
- **Tier 2** runs before presenting artifacts for human approval.
- **Tier 3** runs on-demand via `/vibeloom generate tests`.

---

## 6. Module Interface Contracts (Full Profile)

Each module's `spec.md` must include an Interface Contract section:

### Exports
APIs and events that other modules may depend on, with typed signatures:
```
#### Exports
- API-01: createOrder(items: CartItem[], customer: CustomerId) → OrderId
- EVT-01: OrderPlaced { orderId, customerId, total, timestamp }
```

### Imports
Dependencies on other modules' exports:
```
#### Imports
- From MOD-inventory: checkAvailability(sku: string) → AvailabilityResult
- From MOD-payments: chargePayment(customerId, amount) → PaymentResult
```

### Shared Types
Types referenced across module boundaries live in `modules/shared/types/`. Each type has an **owner module** — only the owner can change the type definition; other modules must adapt.

### Dependency Direction Rules
- The dependency graph must be a DAG (no cycles).
- The root `spec.md` defines allowed dependency directions.
- Adding a new cross-module dependency requires a `spec.md` amendment (human-approved).

### Change Propagation Protocol
When a module's interface changes:
1. Owning agent proposes the interface change in the module's `spec.md`.
2. Structural eval identifies all downstream modules that import the changed interface.
3. Those modules' specs are marked `stale`.
4. Each downstream module's agent updates to the new interface.
5. Contract tests are regenerated and run.

---

## 7. Context Loading Protocol

Each agent task gets a **context envelope** — a defined set of artifacts loaded in a specific way to fit within context window constraints.

### Context Envelope by Task Type

| Task | Loaded Verbatim | Loaded as Summary | Not Loaded |
|------|----------------|-------------------|------------|
| Generate module code | Module spec.md, module AGENTS.md, interface contracts (imports/exports) | dm.md (own BC only), root spec.md (module list + arch overview) | Other modules' code, prd.md, usm.md, intent.md |
| Fix failing test in module | Module spec.md, failing test + error, relevant source files | Module AGENTS.md | Everything else |
| Eval spec consistency | The two specs being compared | N/A | Everything else |
| Cross-module interface change | Both modules' spec.md, interface contracts, shared types | Root spec.md dependency DAG | Code, prd, usm |
| Generate root spec from dm | dm.md (full), prd.md, usm.md | intent.md | Code |

### Context Budget Heuristic
- Reserve **60%** of context window for code being generated/modified
- Reserve **30%** for spec artifacts (verbatim + summaries)
- Reserve **10%** for system prompt, AGENTS.md, tool definitions
- If spec load exceeds 30%, promote artifacts from verbatim to summary (furthest upstream first)

### Summary Generation
- Summaries are generated by the tool and cached alongside the full artifact in `.vibeloom/state.md`.
- A summary includes: artifact ID, status, last-modified date, all item IDs with one-line descriptions, and all interface signatures.
- Summaries are regenerated when the source artifact changes.
- Summaries are structured markdown (parseable, not prose).

### Max Recommended Artifact Lengths
- **Lite:** dm.md ≤ 2K tokens, spec.md ≤ 4K tokens
- **Full:** dm.md per BC ≤ 1.5K tokens, module spec.md ≤ 3K tokens, root spec.md ≤ 3K tokens

Exceeding these limits is a signal that the module decomposition is too coarse.

---

## 8. Workflow

### Initial Generation

1. Human creates a new project folder.
2. `/vibeloom init` scaffolds `intent.md` from template (status: `draft`) and `.vibeloom/` metadata directory.
3. Human edits `intent.md` — either in an editor or interactively interviewed by the Agent.
4. `/vibeloom approve intent` — marks intent.md as `approved`, Agent generates product specs (prd.md, usm.md if Full, dm.md) sequentially as drafts. Each uses the prior to improve the next.
5. Human reviews/edits all product specs. If any are edited, Agent runs reconciliation (eval all product specs + intent for consistency, present inconsistencies).
6. `/vibeloom approve` — runs Tier 1 + Tier 2 evals, then marks product specs as `approved`. Agent selects profile (Lite/Full), proposes it; human approves/overrides.
7. Agent generates `spec.md` (+ module specs if Full) as drafts.
8. Human reviews/edits tech specs. Agent runs evals.
9. `/vibeloom approve spec` — marks tech specs as `approved`, generates AGENTS.md.
10. `/vibeloom generate code` — generates source code. `/vibeloom generate tests` — generates tests.

### Incremental Development

1. `/vibeloom develop "add CSV export"` — user describes change in natural language.
2. Agent maps the change to affected specs (which stories, entities, modules are impacted).
3. Agent proposes spec-level changes first.
4. User chooses: review spec changes separately then generate code, OR batch approve spec+code together.
5. Agent runs bounded reconciliation if needed.
6. Agent generates code changes scoped to affected modules.
7. Agent runs evals on generated code against updated specs.

### Reconciliation (after manual spec edit)

Bounded protocol — maximum **1 up-pass + 1 down-pass + 1 validation**:

1. **Up-pass:** Agent checks edited artifact against all upstream specs. Produces inconsistency report.
2. **Human resolves** upstream inconsistencies (may edit upstream specs).
3. **Down-pass:** Agent checks all downstream specs against reconciled upstream. Produces inconsistency report.
4. **Human resolves** downstream inconsistencies.
5. **Final validation:** Tier 1 structural evals across full stack.
6. If Tier 1 passes → proceed. If Tier 1 fails → human must manually fix remaining issues.

**Escape hatch:** `status: approved-with-known-issues` — human can force-approve a spec with documented inconsistencies. These are tracked and surfaced in every subsequent eval until resolved.

### Import Existing Project

1. `/vibeloom import` — Agent analyzes existing codebase in the current directory.
2. Agent generates specs bottom-up: dm.md (from models/types) → prd.md + USM (from routes/UI/tests) → spec.md (current architecture as-is).
3. All generated specs are in `draft` status reflecting what the code currently does (not necessarily what it should do).
4. Human reviews and corrects. Standard approval flow continues from there.

---

## 9. Command Interface

Root command: `/vibeloom <command> [params]`

### Core Workflow Commands

| Command | Parameters | Description |
|---------|-----------|-------------|
| `init` | — | Scaffold new project (intent.md + .vibeloom/). Offers interview mode. |
| `import` | — | Analyze existing codebase, generate specs bottom-up in draft status. |
| `generate` | `[artifact]` | Generate next artifact in stack (auto-detects), or specific: `prd`, `dm`, `spec`, `code`, `tests`. |
| `approve` | `[artifact]` | Approve draft artifact(s) after running evals. Blocks on Tier 1 failures. |
| `develop` | `<description>` | Incremental change: maps to affected specs → proposes spec changes → user chooses batch or separate → generates code. |

### Review & Quality Commands

| Command | Parameters | Description |
|---------|-----------|-------------|
| `eval` | `[artifact]` | Run Tier 1 structural + Tier 2 semantic evals. Full stack or specific artifact. |
| `review` | `[artifact]` | Interactive walkthrough of artifact(s), highlights decisions and issues. |
| `reconcile` | — | After manual edits: bounded 1 up + 1 down + 1 validation loop. |

### Info Commands

| Command | Parameters | Description |
|---------|-----------|-------------|
| `status` | — | All artifacts with statuses, profile, eval results, module health. |
| `help` | `[topic]` | Commands, methodology, profiles, evals, templates. |

When `/vibeloom` is invoked with no command, the Agent detects project state and presents contextually relevant actions — acting as a smart entry point.

---

## 10. Required Capabilities

| Capability | Method |
|------------|--------|
| Safe multi-session work | Durable contracts in markdown files, lifecycle states in frontmatter, content hashing for stale detection, explicit context loading protocol |
| Safe parallel work | Domain-model-derived modules, interface contracts with typed signatures, dependency DAG, write-surface ownership per module |
| Long-term maintainability | TDD, traceability via rigid IDs, domain invariants in dm.md, observability tied to NFRs, regeneration after upstream changes |
| Controlled flexibility | Lite and Full profiles with defined selection heuristics, progressive dm.md formalization, approved-with-known-issues escape hatch |
| Human governance | Approval gates per tier, bounded reconciliation protocol, auditable change records via git-tracked frontmatter |

---

## 11. Quality Disciplines

| Discipline | Integration with Contract Stack |
|------------|-------------------------------|
| TDD | Default implementation loop. Tests are generated from specs via `/vibeloom generate tests`. |
| BDD | Behavioral scenarios derived from usm.md stories. Scenario descriptions in .md format (not Gherkin). |
| Design by Contract | Domain invariants from dm.md become assertions/property tests. Interface contracts enforce module boundaries. |
| SOLID | Applied as heuristics when they improve maintainability without distorting the domain model. |
| Traceability | Rigid IDs enable tracing: PRD requirement → USM story → DM entity → SPEC module → code → test. |
| Observability | Logs and metrics tied to workflows and `NFR-*` IDs. |

---

## 12. Packaging

- **Deployment:** Claude Code / Codex skill. SKILL.md + markdown templates + eval instructions + guides.
- **No external dependencies.** Everything is markdown files + Agent intelligence.
- **No API costs beyond subscription.** Users run the skill inside their existing Claude Code or Codex environment.
- **State tracking** via `.vibeloom/state.md` — git-tracked markdown file with content hashes, eval history, profile choice, artifact summaries.
- **Cross-platform:** Works identically in Claude Code (app + CLI) and Codex (app + CLI).

### Skill File Structure
```
claude/
├── SKILL.md
├── templates/
│   ├── intent-template.md
│   ├── prd-template.md
│   ├── usm-template.md
│   ├── dm-template.md
│   ├── spec-template.md
│   ├── module-spec-template.md
│   └── agents-template.md
├── eval/
│   ├── structural-checks.md
│   └── semantic-checks.md
├── docs/
│   ├── vibeloom-methodology.md
│   └── profile-selection.md
└── site/
    ├── index.html
    └── learn-more.html
```

---

## 13. HTML Manual (vibeloom.ai "Learn More" Page)

A standalone HTML page for the vibeloom.ai website:
- Modern SaaS design: clean, minimal, light background, subtle gradients
- Target audience: technically savvy PMs and engineering managers
- Overview-first with expandable/collapsible sections for detail
- Self-contained HTML + inline CSS + vanilla JS (no external frameworks)
- Responsive (desktop + tablet)
- Inline SVG workflow diagram showing the full contract stack with generation flow (top-down), eval flow (bottom-up), human approval gates, and module decomposition branching
