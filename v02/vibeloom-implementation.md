# VibeLoom Implementation

This document is the concrete implementation companion to [vibeloom-methodology.md](/Users/ilya.baimetov/Projects/vibeloom/v02/vibeloom-methodology.md). The methodology defines conceptual truth. This document defines the concrete artifact layout, metadata shape, ID schema, template inventory for contract and context artifacts, runtime behavior, and engine boundary required to build a working VibeLoom skill package and local engine.

The current working draft lives at repository root as `vibeloom-implementation.md`. Once the layered skill package is scaffolded, this file moves to `docs/vibeloom-implementation.md`.

---

## Authority, Package Shape, And Engine Boundary

Authority flows downward: methodology → implementation → `assets/` templates → `SKILL.md`. This phase fully specifies contract and context artifacts plus code-generation orchestration, but it does not yet define concrete code templates or code-item carriers.

VibeLoom has two runtime layers:

- the **skill**, which is the natural-language and orchestration layer
- the **engine**, which is the deterministic substrate invoked by the skill

### Skill Responsibilities

The skill owns:

- natural-language interface
- operation selection
- mode selection and validation
- approval pauses and user interaction
- context loading decisions
- orchestration across tiers and scopes
- invoking the engine for deterministic work

### Engine Responsibilities

The engine owns:

- parsing artifacts and frontmatter
- assigning and validating stable IDs
- validating artifact schemas and required fields
- materializing templates into concrete artifacts
- building and querying the context graph
- computing stale propagation and impact sets
- computing status snapshots
- handling deterministic generation bookkeeping

The engine does **not** decide product meaning, semantic intent, or approval outcomes. Semantic judgment remains with the agent and the approval-gated workflow.

### Engine State

The engine may maintain regenerable local state under:

```text
/.vibeloom/
  state/
    context-graph.json
    status.json
```

These files are derived runtime state. They are not contract, context, or code truth.

---

## Governed Repo Layout

### Full Layout (`pm`, `dev`, `expert`)

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
  CLAUDE.md
  context/
    pdr.md
    adr.md
    bdd/
      BDD-####-<behavior-slug>.md
  <container>/
    container.md
    AGENTS.md
    CLAUDE.md
    <component>/
      component.md
      AGENTS.md
      CLAUDE.md
  .vibeloom/
    state/
      context-graph.json
      status.json
```

### Compact Layout (`vibe`)

```text
/
  defaults.md
  intent.md
  system.md
  AGENTS.md
  CLAUDE.md
  .vibeloom/
    state/
      context-graph.json
      status.json
```

In `vibe`, there are no container directories, no `context/` directory, and no product-specs artifacts. All system-level information lives in the single flat `system.md`. Container and component directories appear only after upgrade to pm/dev/expert.

### Placement Rules

- root contract artifacts always live at repository root
- containers live as direct child directories of repository root (full modes only)
- components live as direct child directories of their container directory (full modes only)
- assistant-specific execution guidance is emitted directly into the scope it governs (root only in `vibe`)
- `pdr` and `adr` are standardized as repo-level ledger artifacts in `context/` (full modes only)
- `bdd` is standardized as a repo-level multi-file context artifact under `context/bdd/` (full modes only)
- narrower context scopes may be added later, but are not required in v1

The authoritative inventory of containers and components still lives in contract artifacts:

- In full modes: `containers.md` is the global container inventory; each `container.md` is the authoritative component inventory for that container
- In `vibe`: the flat `system.md` contains both the container and component inventories

The filesystem is a navigation aid and consistency check. It is not the semantic source of truth.

---

## Artifact Mapping

The concrete output and template mapping for contract and context artifacts is:

#### Full Artifact Mapping (`pm`, `dev`, `expert`)

| Artifact Type | Output Path | Template Path | Scope |
| --- | --- | --- | --- |
| `intent` | `/intent.md` | `assets/intent-specs/intent.md` | root |
| `defaults` | `/defaults.md` | `assets/intent-specs/defaults.md` | root |
| `prd` | `/prd.md` | `assets/product-specs/prd.md` | root |
| `usm` | `/usm.md` | `assets/product-specs/usm.md` | root |
| `dm` | `/dm.md` | `assets/product-specs/dm.md` | root |
| `system` | `/system.md` | `assets/system-specs/system.md` | root |
| `containers` | `/containers.md` | `assets/system-specs/containers.md` | root |
| `container` | `/<container>/container.md` | `assets/system-specs/container.md` | container |
| `component` | `/<container>/<component>/component.md` | `assets/system-specs/component.md` | component |
| root execution guidance | `/AGENTS.md`, `/CLAUDE.md` | `assets/context/root-execution-guidance.md` | root |
| container execution guidance | `/<container>/AGENTS.md`, `/<container>/CLAUDE.md` | `assets/context/container-execution-guidance.md` | container |
| component execution guidance | `/<container>/<component>/AGENTS.md`, `/<container>/<component>/CLAUDE.md` | `assets/context/component-execution-guidance.md` | component |
| `pdr` ledger | `/context/pdr.md` | `assets/context/pdr.md` | root |
| `adr` ledger | `/context/adr.md` | `assets/context/adr.md` | root |
| `bdd` | `/context/bdd/BDD-####-<behavior-slug>.md` | `assets/context/bdd.md` | root |

#### Compact Artifact Mapping (`vibe`)

| Artifact Type | Output Path | Template Path | Scope |
| --- | --- | --- | --- |
| `intent` | `/intent.md` | `assets/intent-specs/vibe-intent.md` | root |
| `defaults` | `/defaults.md` | `assets/intent-specs/defaults.md` | root |
| `system` | `/system.md` | `assets/system-specs/vibe-system.md` | root |
| root execution guidance | `/AGENTS.md`, `/CLAUDE.md` | `assets/context/root-execution-guidance.md` | root |

The body shape of each generated contract or context artifact is defined by the corresponding template in `assets/`. This document defines the metadata, IDs, path rules, and runtime behavior that the templates must obey.

---

## Metadata Format

All generated Markdown artifacts use YAML frontmatter.

### Contract Artifact Frontmatter

Every contract artifact must include:

| Field | Type | Notes |
| --- | --- | --- |
| `artifact_id` | string | Stable artifact identifier |
| `artifact_type` | enum | One of `intent`, `defaults`, `prd`, `usm`, `dm`, `system`, `containers`, `container`, `component` |
| `tier` | enum | One of `intent-specs`, `product-specs`, `system-specs` |
| `scope_kind` | enum | One of `root`, `container`, `component` |
| `scope_id` | string | `root` or the governing container/component scope slug |
| `status` | enum | One of `draft`, `approved` |
| `version` | integer | Latest approved version number; starts at `0` until the first approval |
| `draft_revision` | integer | Optional; required when `status: draft` and content differs from the last approved version |
| `approval_mode` | enum | One of `human`, `delegated`. Set at approval time only; absent on drafts. |
| `derives_from` | string[] | Upstream short item IDs that materially constrain this artifact |

Additional required fields:

- `container.md`
  - `container_id` corresponding to the governing `CONT-####` item
- `component.md`
  - `container_id` corresponding to the governing `CONT-####` item
  - `component_id` corresponding to the governing `CMP-####` item
  - `bounded_context` corresponding to the governing `BC-####` item
  - `owned_paths`
  - `owned_interfaces`

### Context Artifact Frontmatter

Every context artifact must include:

| Field | Type | Notes |
| --- | --- | --- |
| `artifact_id` | string | Stable artifact identifier |
| `artifact_type` | enum | One of `execution-guidance`, `pdr`, `adr`, `bdd` |
| `tier` | enum | Always `context` |
| `scope_kind` | enum | One of `root`, `container`, `component` |
| `scope_id` | string | `root` or the governing scope slug |
| `derives_from` | string[] | Upstream short item IDs that constrain this artifact |

Additional required fields:

- execution guidance artifacts
  - `assistant`

Context artifacts do **not** carry `status`, `version`, or `approval_mode`.

For ledger artifacts (`pdr`, `adr`): artifact-level `derives_from` in frontmatter is always empty (`[]`). Per-record `derives_from` inside each `PDR-####` / `ADR-####` section is the canonical derivation link. The engine builds graph edges from per-record `derives_from`, not from artifact-level frontmatter.

### Versioning Rule

Contract versioning uses approved versions plus draft revisions:

- first generated draft: `version: 0`, `draft_revision: 1`
- first approved artifact: `version: 1`, no `draft_revision`
- next unapproved change: `version: 1`, `draft_revision: 2`
- next approval: `version: 2`, no `draft_revision`

`approval_mode` is provenance, not a declaration. Drafts do not carry `approval_mode`. At approval time, set `approval_mode: human` for explicit human approval or `approval_mode: delegated` for auto-advanced approval.

### Direct Edit Detection

When a user edits an approved contract artifact outside of skill operations:

1. The user should set `status: draft` and add `draft_revision` in frontmatter to signal the edit.
2. Alternatively, the skill detects the edit at the start of any operation by comparing artifact content against the approved state.
3. The skill confirms the transition with the user before proceeding.
4. Staleness propagation follows the same rules as any other draft transition.

### Staleness

Staleness is never written into artifact frontmatter. It is computed by the context graph by comparing each artifact's derivation basis against the latest approved upstream versions. Unapproved drafts do not trigger staleness.

---

## Stable ID Schema

Visible item IDs use short typed references:

```text
PREFIX-0001
```

Core rules:

- visible item IDs use uppercase prefix families plus fixed-width 4-digit numbers
- item IDs are globally unique by type across the repo
- numbering is append-only within each prefix family
- deleted IDs are never reused
- visible references use only short IDs; they do not encode artifact identity
- human meaning lives in adjacent labels, titles, and statements rather than in the ID itself
- overlays get IDs only when they are intentionally addressable

### Prefix Families

| Family | Meaning |
| --- | --- |
| `CAP-####` | intent capability |
| `WISH-####` | softer intent preference |
| `CST-####` | hard constraint item in defaults, intent, PRD, or system-specs |
| `FR-####` | functional requirement |
| `NFR-####` | non-functional requirement |
| `ASM-####` | assumption |
| `IN-####` | in-scope boundary item |
| `OOS-####` | out-of-scope item |
| `Q-####` | open question |
| `EPIC-####` | epic |
| `FLOW-####` | workflow or journey |
| `STORY-####` | story |
| `ACC-####` | acceptance-framing entry |
| `TERM-####` | ubiquitous-language term |
| `BC-####` | bounded context |
| `AGG-####` | aggregate |
| `ENT-####` | entity |
| `VO-####` | value object |
| `INV-####` | invariant or business rule |
| `REL-####` | domain relationship or integration touchpoint |
| `EXT-####` | external actor or system |
| `TB-####` | trust boundary |
| `SNFR-####` | system-wide NFR boundary |
| `CONT-####` | container inventory item |
| `CMP-####` | component inventory item |
| `EDGE-####` | communication path or local dependency edge |
| `IF-####` | owned interface |
| `DEP-####` | component dependency |
| `BEH-####` | local technical behavior or contract |
| `NOTE-####` | local test or runtime note |
| `PDR-####` | product decision record item inside `pdr.md` |
| `ADR-####` | architecture decision record item inside `adr.md` |
| `BDD-####` | behavioral-scenario artifact |
| `SCN-####` | individual Gherkin scenario |
| `OBJ-####` | objective overlay item when explicitly addressable |
| `KR-####` | key-result overlay item when explicitly addressable |
| `MET-####` | metric overlay item when explicitly addressable |
| `MS-####` | milestone overlay item when explicitly addressable |
| `RISK-####` | risk overlay item when explicitly addressable |

### Artifact IDs

| Artifact | ID Shape |
| --- | --- |
| root contract artifacts | fixed name: `intent`, `defaults`, `prd`, `usm`, `dm`, `system`, `containers` |
| `container.md` | `container.<container-slug>` |
| `component.md` | `component.<container-slug>.<component-slug>` |
| root `AGENTS.md` | `guidance.root.codex` |
| root `CLAUDE.md` | `guidance.root.claude` |
| container guidance | `guidance.container.<container-slug>.<assistant-slug>` |
| component guidance | `guidance.component.<container-slug>.<component-slug>.<assistant-slug>` |
| `pdr` ledger | `pdr` |
| `adr` ledger | `adr` |
| `bdd` | `BDD-####` |

Root contract artifacts keep semantic IDs because there are few of them and they are not the hot path in derivation-heavy generation. Decision ledgers keep semantic artifact IDs because the record items inside them carry the addressable identity. `bdd` artifacts use short typed artifact IDs because each behavior file is its own selectively loadable context artifact.

### Engine Identity Model

The engine resolves short visible IDs through containment and index metadata rather than by qualifying the visible ID.

For each addressable item, the engine stores:

- `item_id`
- `artifact_id`
- `section`
- `tier`
- `scope`

The engine may derive an internal composite key for storage, but visible docs and templates never expose qualified forms such as `prd#FR-0001`.

### Item Ownership And `intent`

Every addressable item is owned by exactly one artifact where it is defined.

`intent` remains prose-first. Free prose in `intent` stays un-IDed. Structured `intent` entries use only:

- `CAP-####`
- `WISH-####`
- `CST-####`

### Derivation References

The canonical relation name is `derives_from`.

Rules:

- visible `derives_from` references in docs and templates use short item IDs only
- artifact frontmatter records the smallest useful constraining set of upstream item IDs
- item-level derivation lives in the body carriers defined by the artifact template
- artifact ownership stays separate from item ID

### Brownfield Import And ID Lifecycle

Bootstrap commands are uniform across all modes:

- `init --mode <mode>` and `import --mode <mode>` are valid only before the repo becomes governed
- once bootstrap succeeds, later `init` or `import` calls are errors with guidance
- `--mode` is required on both bootstrap commands
- `init` always creates governed scaffolding, mode state, and draft `intent-specs` only
- `import` reconstructs candidate contract according to the chosen initial mode

During brownfield import:

- preserve an existing ID if it already matches the short typed family rules
- otherwise assign one new short ID and record the mapping in engine state or import metadata
- never renumber imported items after the initial mapping
- never recycle deleted IDs

`import --mode vibe` reconstructs the compact stack bottom-up from code analysis:
1. Analyze existing code to infer compact system-specs (flat system context, components, interfaces, behaviors)
2. Infer compact intent-specs (capabilities, wishes, constraints, product-summary prose) from the reconstructed flat system

`system-specs` and `intent-specs` are marked `draft` after compact reconstruction. The skill then runs bottom-up review starting at compact system-specs and proceeding upward through intent-specs before generating final root guidance and reconciling against code.

`import --mode pm|dev|expert` reconstructs the full contract stack bottom-up from code analysis:
1. Analyze existing code to infer system-specs (components, containers, interfaces, behaviors)
2. Infer product-specs (requirements, stories, domain model) from the reconstructed system-specs
3. Infer intent-specs (capabilities, wishes, constraints) from the reconstructed product-specs
4. Generate the context tier (execution guidance, decision records, BDD scenarios) from the reconstructed contract

All three contract tiers are marked `draft` after full reconstruction. The skill then runs `review` starting at system-specs and proceeding upward through product-specs and intent-specs, surfacing findings for human confirmation at each tier before moving to the next.

---

## Item Carriers And Template Rules

Templates in `assets/` are authoritative for body shape. The engine parses addressable items (short IDs) from tables and structured lists inside each artifact. Each template defines which carriers it uses.

Key exceptions to the standard table-with-IDs pattern:
- `defaults`: compact rule lists that still use `CST-####` item IDs so downstream derivation can reference individual repo-wide constraints
- `pdr` / `adr`: ledger artifacts with repeated record sections (`PDR-####` / `ADR-####`), each carrying `recorded_at`, `derives_from`, `contract delta`, `impact`, `decision`, and `why`
- `bdd`: multi-file (each `BDD-####` is its own context artifact under `/context/bdd/`) for selective loading during implementation

Templates are intentionally standalone. Small structural duplication between templates is allowed when it reduces context load at generation time.

### Table Column Conventions

Templates use these canonical column names across tiers:

| Column | Meaning | Used in |
| --- | --- | --- |
| `id` | Short typed item ID | all contract and context tables with addressable items |
| `derives_from` | Upstream short item IDs that constrain this item | all contract tiers, pdr, adr, bdd |
| `description` | What the item is or does | intent, prd, usm, dm, system, containers, container, component |
| `notes` | Additional context, rationale, or caveats | any table where supplementary commentary is useful |
| `priority` | Relative importance or sequencing | prd (FR, features, scope) |
| `measure` / `target` | Quantitative NFR specification | prd (NFR), system (SNFR) |

Domain-specific columns (e.g., `kind`, `runtime`, `rule`, `relationship`) are template-local and documented within the template that uses them.

---

## Context Graph Realization

The v1 context graph realization is built from explicit derivation plus containment across contract and context artifacts. Code does not yet participate in the explicit graph because concrete code-item carriers are not specified. In `vibe`, code drift is analyzed heuristically by the skill rather than through graph-backed code-item validation.

### Explicitly Stored

The engine stores:

- artifact metadata from contract and context frontmatter
- item IDs parsed from contract and context templates
- item-level `derives_from` references
- an index from short item IDs to owning artifact, section, tier, and scope
- containment:
  - item -> section
  - section -> artifact
  - artifact -> tier

### Inferred Views

See methodology for conceptual definitions of traceability, staleness, loading, and artifact impact. In v1, the engine computes all four from contract and context artifacts only. Staleness is computed in the graph only, never written to artifact frontmatter. The loading view is used to compute agent load sets — given a scope, the graph returns the minimum set of execution guidance and contract artifacts a worker agent needs.

### Agent Load Sets

The context graph computes the load set for each worker agent. The orchestrator (skill) queries the graph and passes the result to each spawned worker. Workers receive both execution guidance and the governing contract slice.

#### Full Modes (`pm`, `dev`, `expert`)

| Worker scope | Execution guidance | Contract artifacts | Always included |
| --- | --- | --- | --- |
| component | component + container guidance | component spec, container spec | `defaults` |
| container | container + root guidance | container spec, system + containers spec | `defaults` |
| root | root guidance | system, containers | `defaults` |

#### Compact Mode (`vibe`)

All workers load root guidance + flat `system.md` + `defaults`.

#### Overhead Budget

Generated guidance and contract artifacts total approximately 6,000–12,000 tokens per worker (2–5% of a 256K context window). The orchestrator additionally loads the skill (~5,000 tokens), status, and graph. Workers never load the skill or methodology.

### Graph Cache

The engine materializes a regenerable graph cache at:

```text
/.vibeloom/state/context-graph.json
```

The cache is rebuilt whenever:

- a contract artifact changes
- a context artifact is regenerated
- status or derivation metadata changes

### Status Snapshot

The engine may materialize a derived status view at:

```text
/.vibeloom/state/status.json
```

This file summarizes:

- latest approved contract versions
- stale downstream artifacts
- unresolved draft tiers
- graph health warnings

---

## Generation And Runtime Behavior

### Tier Order

See methodology for tier semantics and derivation rules. The concrete tier order depends on mode:

Full tier order (`pm`, `dev`, `expert`):
```text
intent-specs -> product-specs -> system-specs -> context -> code
```

Compact tier order (`vibe`):
```text
intent-specs -> system-specs -> context (execution guidance only) -> code
```

Within a contract tier, artifacts are generated in this order:

1. root artifacts in the tier
2. local `container.md` files for affected containers (full modes only)
3. local `component.md` files for affected components (full modes only)

### Scope Of Regeneration

Within a tier, only artifacts whose derivation basis includes changed upstream items are regenerated. Artifacts with unchanged upstream bases are not regenerated. When the double-pass back-pass identifies cross-artifact effects within the tier, those additional artifacts enter the regeneration set.

### Double-Pass Generation

See methodology for the conceptual double-pass model. The concrete steps per contract tier are:

1. generate artifacts in dependency order
2. forward pass across the tier
3. back pass if later artifacts sharpen earlier artifacts
4. structural eval + semantic eval
5. one additional bounded forward-back round if needed
6. emit as `draft`
7. pause or auto-advance for review, eval, and approval according to mode and delegated-approval rules

### Operation Contracts

| Operation | Required Inputs | Output |
| --- | --- | --- |
| `init` | project brief, initial mode | governed scaffolding, mode state, and initial `intent-specs` draft |
| `generate` | target tier, scope, approved upstream basis, mode | regenerated tier artifacts |
| `review` | current approval unit, or `intent-specs` in public `vibe` mode, scope, review style | interactive loop: eval → findings → fixes → user chooses (loop / eval-only / approve) |
| `eval` | current approval unit, or `intent-specs` in public `vibe` mode, scope | structural and semantic findings |
| `reconcile` | approved upstream change set, downstream floor scope | interactive loop: detect drift → propose fixes → apply → eval → user chooses (loop / eval-only / approve) |
| `approve` | current approval unit, approval mode | approved approval unit and updated versions |
| `status` | scope | current lifecycle and stale summary |
| `import` | unmanaged repo scope, initial mode | candidate contract drafts and context appropriate to the chosen initial mode |

`review` only acts on the current approval unit, checking upward against approved upstream truth. In the public `vibe` UX, this narrows to `review intent-specs` and `eval intent-specs`: heuristic, read-only checks of compact intent/defaults against downstream compact system and current code drift. These checks are outside graph-backed code-item analysis and rely on agent reasoning over repo files under a small-codebase assumption. `reconcile` only acts downward, checking downstream artifacts against approved upstream changes. Both are interactive loops: each cycle ends with the user choosing to loop, eval-only (after out-of-band edit), or approve and proceed. The symmetry: `review` is to `eval` as `reconcile` is to `generate`.

### Standard Operation Parameters

Implementations should standardize these parameter names even if the user-facing CLI or skill phrasing differs:

| Parameter | Meaning |
| --- | --- |
| `target_tier` | One of `intent-specs`, `product-specs`, `system-specs`, `context`, `code` |
| `scope` | One of `root`, `container:<container-slug>`, `component:<container-slug>/<component-slug>` |
| `mode` | One of `vibe`, `pm`, `dev`, `expert` |
| `review_style` | One of `advisory`, `bounded`. `advisory` surfaces findings without modifying artifacts. `bounded` surfaces findings and applies fixes within the current approval unit that do not change approved upstream meaning. |

| `approval_mode` | One of `human`, `delegated` |
| `affected_set` | Items, artifacts, tiers, and scopes reachable by walking derivation edges downward from every changed item in the context graph |

These parameters are the internal engine vocabulary behind the methodology-level operations. Public skill commands may expose a narrower surface than the engine, especially in `vibe`.

### Mode-Driven Approval Behavior

Implementations should enforce the same stop behavior described in methodology:

| Mode | Contract depth | Approval unit | Normal human contract stop | Delegated auto-advance by default |
| --- | --- | --- | --- | --- |
| `pm` | full (3 tiers) | each affected contract tier | `product-specs` | `system-specs` |
| `dev` | full (3 tiers) | each affected contract tier | `system-specs` | `product-specs` |
| `expert` | full (3 tiers) | each affected contract tier | every contract tier | none |
| `vibe` | compact (2 tiers) | each affected contract tier | intent-specs only | system-specs |

In `vibe`, `pm`, and `dev`, delegated auto-advance is allowed only when:

- structural eval passes
- no **breaking semantic change** is detected against approved truth
- no flagged issue requires human judgment

If a delegated approval unit is blocked or flagged, explicit human review and approval become required before the run can complete.

### Public Skill Surfaces

Full modes (`pm`, `dev`, `expert`) expose one uniform public surface:

- `generate <target>`
- `review`
- `eval`
- `reconcile`
- `approve`
- `status`
- `configure`
- `help`

`vibe` exposes a simplified public surface:

- `approve intent-specs`
- `generate code`
- `reconcile code`
- `review intent-specs`
- `eval intent-specs`
- `status`
- `configure`
- `help`

In `vibe`, `review intent-specs` and `eval intent-specs` are heuristic compact governance checks over compact intent/defaults, downstream compact system, and current code. `generate` and `reconcile` accept only `code` as the public target. Unsupported public commands or targets in `vibe` return a mode-aware explanation and, when useful, an upgrade suggestion. Bare `review` / `eval` aliases may be added later, but they are not part of the current public spec.

### Smart Orchestration

In full modes, `generate <target>` orchestrates the full path from the current state to the target tier, following mode rules. The "normal forward surface" (see methodology) lists the commands the skill should suggest to the user after each stop.

1. Check all upstream tiers are approved.
2. For any upstream tier in draft: if it is **delegated** in the current mode → auto-advance (eval, approve, continue).
3. For any upstream tier in draft: if it is a **human stop** in the current mode → stop and ask for review/approval before continuing.
4. Generate the target tier.
5. If the target tier is a human stop → stop for review/approval.
6. If the target tier is delegated → auto-advance and continue toward the original target.

Concrete behavior for full-mode public targets:

| Command | `pm` | `dev` | `expert` |
| --- | --- | --- | --- |
| `generate intent-specs` | reshape intent (preserving user's semantic intent), regenerate defaults, stop for approval | same | same |
| `generate product-specs` | generate, stop (human) | auto-advance product (delegated) | generate, stop (human) |
| `generate system-specs` | auto-advance system (delegated) | auto-advance product if needed (delegated), generate system, stop (human) | generate, stop (human) |
| `generate context` | auto-advance downstream, generate context, stop (explicit target) | auto-advance downstream, generate context, stop (explicit target) | generate context, stop (explicit target) |
| `generate code` | auto-advance system (delegated), generate context + code | auto-advance product if needed (delegated), generate system (stop, human), after approval generate context + code | generate context + code (all upstream must be approved) |

Intent-specs are never delegated. `generate intent-specs` uses the user's current `intent.md` content as authoritative semantic input, reshapes it for structural consistency (IDs, table formatting), and regenerates `defaults.md` to stay aligned. The user's semantic intent is never overridden by generation. Always stops for explicit human approval regardless of mode. In `vibe`, the public skill does not expose `generate intent-specs`; the same normalization step runs implicitly during bootstrap and before approving draft intent.

`vibe` public command behavior:

| Command | Behavior |
| --- | --- |
| `generate code` | if `intent-specs` is still draft, stop for explicit `approve intent-specs`; otherwise generate delegated compact `system-specs`, root execution guidance, and code |
| `reconcile code` | interactive downward drift review between approved compact intent/defaults and current downstream state; if `intent-specs` is draft, normalize if needed and stop for explicit `approve intent-specs` before reconciling compact `system-specs` and code |
| `review intent-specs` | heuristic read-only review of compact intent/defaults against downstream compact system and current code drift; uses agent reasoning over filesystem layout, exported interfaces, routes or commands, tests, key strings, and owned-path comparisons |
| `eval intent-specs` | heuristic read-only eval of compact intent/defaults against downstream compact system and current code drift; runs structural checks on the compact contract plus lightweight non-graph code-drift checks |

### Next-Command Suggestions

After every stop (approval, escalation, explicit `generate context` in full modes), the skill suggests the next forward command:

| After | `vibe` | `pm` | `dev` | `expert` |
| --- | --- | --- | --- | --- |
| approve intent-specs | `generate code` | `generate product-specs` | `generate system-specs` | `generate product-specs` |
| approve product-specs | — | `generate code` | — | `generate system-specs` |
| approve system-specs | — | — | `generate code` | `generate code` |
| explicit `generate context` | — | `generate code` | `generate code` | `generate code` |

### Mode × Command Matrix (Normal Flow)

| Step | `vibe` | `pm` | `dev` | `expert` |
| --- | --- | --- | --- | --- |
| Bootstrap | `init --mode vibe` | `init --mode pm` | `init --mode dev` | `init --mode expert` |
| Shape intent | edit `intent.md` directly; normalization runs during bootstrap/approval | `generate intent-specs` (if defaults need regen) | same | same |
| Approve intent | `approve intent-specs` | `approve` | `approve` | `approve` |
| Forward to product | — | `generate product-specs` | (automatic) | `generate product-specs` |
| Approve product | — | `approve` | (auto or escalated) | `approve` |
| Forward to system | (automatic) | (automatic) | `generate system-specs` | `generate system-specs` |
| Approve system | (automatic) | (auto or escalated) | `approve` | `approve` |
| Forward to code | `generate code` | `generate code` | `generate code` | `generate code` |

`(automatic)` = handled by the forward `generate` command via smart orchestration / delegation. `(auto or escalated)` = normally delegated, but escalates to explicit approval if breaking change detected. `—` = tier does not exist in this mode.

### Utility Commands

These are skill-level commands that do not correspond to methodology operations:

| Command | Purpose |
| --- | --- |
| `configure` | Change runtime settings: `mode` (`vibe` / `pm` / `dev` / `expert`) and any future skill-level options. Switching from `vibe` to any other mode triggers a one-way upgrade (see Upgrade Mechanics below). Switching back to `vibe` is not allowed. Other mode changes take effect on the next operation. |
| `help` | Explain any VibeLoom concept, operation, or workflow by referencing methodology and implementation docs. Does not modify artifacts or state. Use `help --explain <topic>` for detailed explanations (e.g., `help --explain generate`, `help --explain modes`). |

Bootstrap-specific command rules:

- `init --mode <mode>` and `import --mode <mode>` are the only valid bootstrap entrypoints
- both require explicit `--mode`
- both are valid only before the repo becomes governed
- after bootstrap succeeds, later `init` or `import` calls return an error with guidance

### Context Generation

Context generation happens after the required contract tiers are approved.

#### Full Context Generation (`pm`, `dev`, `expert`)

Generation order inside context:

1. execution guidance artifacts for affected scopes (root, container, component)
2. decision records if the change introduced product or architecture decisions
3. `bdd` scenarios are created both (a) automatically when `generate system-specs` produces BEH-#### items and (b) on-demand in full modes via `generate context`

Generated execution guidance should include concrete project-specific pointers — artifact IDs, interface names, owned paths, and test commands — so that worker agents can orient quickly within their scope without loading the full context graph.

#### Compact Context Generation (`vibe`)

In `vibe`, context generation produces only root-level execution guidance (`AGENTS.md`, `CLAUDE.md`). No decision records or BDD scenarios are generated. These become available after upgrade to pm/dev/expert.

Context is assumed correct by default. When context is the explicit target (`generate context`), generation stops after context in all full modes. When the target is `generate code`, context is generated implicitly and the run continues into code. In `vibe`, context is generated only implicitly during `generate code` or during compact import.

### Upgrade Mechanics

When the user runs `configure mode pm|dev|expert` while in `vibe` mode, the skill performs a one-way upgrade:

1. **Snapshot:** Copy vibe artifacts (`intent.md`, `defaults.md`, `system.md`) to `.vibeloom/vibe-snapshot/` as read-only reference.
2. **Generate full contract stack** from the compact artifacts:
   - Vibe `intent` (product summary section) → regular `intent` (narrowed to vision + capabilities + wishes + constraints) + `prd` + `usm` + `dm`
   - Vibe `system` (flat) → regular `system` + `containers` + per-container `container` + per-component `component`
   - `defaults` stays as-is.
3. **Mark all new artifacts as `draft`.** Normal approval flow for the target mode takes over.
4. **Rearrange source code** into the container/component directory structure defined by the generated system-specs.
5. **Generate full context** (execution guidance at all scopes, decision records, BDD scenarios as applicable).
6. The skill informs the user that the upgrade is complete and suggests the next command for the target mode.

The transition is one-way. `configure mode vibe` from any other mode is rejected with an explanation.

---

## Template System

The v1 `assets/` tree is:

```text
assets/
  intent-specs/
    intent.md            # full modes
    vibe-intent.md       # vibe mode
    defaults.md          # all modes
  product-specs/
    prd.md               # full modes only
    usm.md               # full modes only
    dm.md                # full modes only
  system-specs/
    system.md            # full modes
    vibe-system.md       # vibe mode
    containers.md        # full modes only
    container.md         # full modes only
    component.md         # full modes only
  context/
    pdr.md               # full modes only
    adr.md               # full modes only
    bdd.md               # full modes only
    root-execution-guidance.md        # all modes
    container-execution-guidance.md   # full modes only
    component-execution-guidance.md   # full modes only
```

Template rules:

- templates are split by artifact type and scope
- templates are standalone and loadable in isolation
- templates contain required sections, optional sections, and brief local guidance
- templates do not contain runtime logic
- templates may duplicate small structural fragments when that materially reduces context load
- code templates are out of scope in this phase

---

## Validation Checklist

The implementation is valid only if all of the following hold:

- every contract and context artifact in scope for this phase has a concrete output path and template mapping
- every templated artifact has a YAML frontmatter shape
- every visible addressable item uses a short typed `PREFIX-####` ID
- every visible derivation reference uses short item IDs only
- item numbering is fixed-width, append-only, and non-recycling within each family
- root contract artifact IDs remain semantic where specified
- every contract artifact has stable artifact IDs and item carriers
- every context artifact has stable artifact IDs and short derivation references
- `bdd` is context, not contract
- execution guidance is assistant-specific and scope-specific
- contract approval follows the mode-defined approval unit and delegated-auto-advance rules
- `review` and structural/semantic `eval` act on the current approval unit plus approved upstream truth
- `reconcile` remains downstream only
- the context graph can be rebuilt from artifact metadata and item carriers without hidden prompt-only state
- brownfield import preserves compatible short IDs and records one-time remaps for incompatible legacy IDs
- bootstrap commands require an initial mode and are rejected once the repo is already governed
- full modes expose one uniform public command surface while `vibe` exposes the restricted compact surface
- the skill can load one narrow template at a time rather than one large combined template

This document is sufficient to author the future `SKILL.md`, `references/`, and the v1 contract/context engine without inventing new artifact rules. Concrete code templates and code-item carriers remain out of scope in this phase.
