# VibeLoom Implementation

This document is the concrete implementation companion to [vibeloom-methodology.md](/Users/ilya.baimetov/Projects/vibeloom/v02/vibeloom-methodology.md). The methodology defines conceptual truth. This document defines the concrete artifact layout, metadata shape, ID schema, template inventory, runtime behavior, and engine boundary required to build a working VibeLoom skill package and local engine.

The current working draft lives at repository root as `vibeloom-implementation.md`. Once the layered skill package is scaffolded, this file moves to `docs/vibeloom-implementation.md`.

---

## Authority And Package Shape

Authority flows downward:

1. methodology defines conceptual truth
2. implementation defines concrete artifact and runtime truth
3. `assets/` define generation inputs derived from implementation
4. `references/` define distilled runtime-operational guidance derived from methodology and implementation
5. `SKILL.md` orchestrates runtime loading and command routing without redefining lower-layer truth

The future layered skill package is:

```text
/
  SKILL.md
  docs/
    vibeloom-methodology.md
    vibeloom-implementation.md
  references/
    ...
  assets/
    ...
```

This phase defines `docs/`, `assets/`, `references/`, and `SKILL.md` conceptually, but only authors the implementation doc and `assets/` templates.

---

## Engine And Skill Boundary

VibeLoom has two runtime layers:

- the **skill**, which is the natural-language and orchestration layer
- the **engine**, which is the deterministic substrate invoked by the skill

### Skill Responsibilities

The skill owns:

- natural-language interface
- operation selection
- profile and mode defaults
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

The engine does **not** decide product meaning, semantic intent, or approval outcomes. Semantic judgment remains with the agent and the human-gated workflow.

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

## References Layer

`references/` is reserved for distilled runtime-operational authority.

Its role is:

- shrink runtime context compared to loading the full canon docs
- restate methodology and implementation rules in compact operational form
- support `SKILL.md` without making `SKILL.md` itself large or duplicative

`references/` is downstream from methodology and implementation:

- it may compress or reorganize concrete rules
- it may not invent new artifact, lifecycle, ID, or graph semantics
- it is not authored in this phase unless later work requires it

---

## Governed Repo Layout

The generated governed repository layout is:

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

Concrete placement rules:

- root contract artifacts always live at repository root
- containers live as direct child directories of repository root
- components live as direct child directories of their container directory
- assistant-specific execution guidance is emitted directly into the scope it governs
- `pdr` and `adr` are standardized as repo-level ledger artifacts in `context/`
- `bdd` is standardized as a repo-level multi-file context artifact under `context/bdd/`
- narrower context scopes may be added later, but are not required in v1

The authoritative inventory of containers and components still lives in contract artifacts:

- `containers.md` is the global container inventory
- each `container.md` is the authoritative component inventory for that container

The filesystem is a navigation aid and consistency check. It is not the semantic source of truth.

---

## Artifact Mapping

The concrete output and template mapping is:

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
| root execution guidance for Codex-like agents | `/AGENTS.md` | `assets/context/root-AGENTS.md` | root |
| root execution guidance for Claude-like agents | `/CLAUDE.md` | `assets/context/root-CLAUDE.md` | root |
| container execution guidance for Codex-like agents | `/<container>/AGENTS.md` | `assets/context/container-AGENTS.md` | container |
| container execution guidance for Claude-like agents | `/<container>/CLAUDE.md` | `assets/context/container-CLAUDE.md` | container |
| component execution guidance for Codex-like agents | `/<container>/<component>/AGENTS.md` | `assets/context/component-AGENTS.md` | component |
| component execution guidance for Claude-like agents | `/<container>/<component>/CLAUDE.md` | `assets/context/component-CLAUDE.md` | component |
| `pdr` ledger | `/context/pdr.md` | `assets/context/pdr.md` | root |
| `adr` ledger | `/context/adr.md` | `assets/context/adr.md` | root |
| `bdd` | `/context/bdd/BDD-####-<behavior-slug>.md` | `assets/context/bdd.md` | root |

The body shape of each generated artifact is defined by the corresponding template in `assets/`. This document defines the metadata, IDs, path rules, and runtime behavior that the templates must obey.

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
| `status` | enum | One of `draft`, `approved`, `stale`, `superseded` |
| `version` | integer | Latest approved version number; starts at `0` until the first approval |
| `draft_revision` | integer | Optional; required when `status: draft` and content differs from the last approved version |
| `approval_mode` | enum | One of `human`, `delegated` |
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

Additional required fields:

- execution guidance artifacts
  - `assistant`

Context artifacts do **not** carry `status`, `version`, or `approval_mode`.

### Versioning Rule

Contract versioning uses approved versions plus draft revisions:

- first generated draft: `version: 0`, `draft_revision: 1`
- first approved artifact: `version: 1`, no `draft_revision`
- next unapproved change: `version: 1`, `draft_revision: 2`
- next approval: `version: 2`, no `draft_revision`

Downstream staleness is computed from the latest approved upstream version, not from unapproved drafts.

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
| `CST-####` | hard constraint item in intent, PRD, or system-specs |
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

During brownfield import:

- preserve an existing ID if it already matches the short typed family rules
- otherwise assign one new short ID and record the mapping in engine state or import metadata
- never renumber imported items after the initial mapping
- never recycle deleted IDs

---

## Item Carriers And Template Rules

Templates are authoritative for body shape. The engine parses addressable items from the carriers standardized below:

| Artifact | Primary Item Carrier |
| --- | --- |
| `intent` | structured bullets or tables with `CAP-####`, `WISH-####`, and `CST-####` only where entries are addressable |
| `defaults` | compact tables and rule lists; v1 does not require per-rule item IDs |
| `prd` | tables with short IDs for core requirements and for optional overlays only when they are addressable |
| `usm` | tables with short IDs for epics, flows, stories, acceptance entries, and milestones |
| `dm` | tables with short IDs for bounded contexts, aggregates, entities, value objects, invariants, and relationships |
| `system` | tables with short IDs for actors, external systems, trust boundaries, and system-wide constraints |
| `containers` | container inventory plus edge and constraint tables with short IDs; descriptive responsibility/runtime notes may remain un-IDed |
| `container` | component inventory with `CMP-####`; resident bounded contexts are referenced by `BC-####`; local edges and constraints use short IDs |
| `component` | interface, dependency, behavior, and note tables with short IDs; owned paths may remain un-IDed |
| execution guidance | bullets and tables keyed by scope; any cited upstream items use short IDs |
| `pdr` / `adr` | ledger artifacts with repeated `PDR-####` / `ADR-####` record sections; each record carries `recorded_at`, `derives_from`, `contract delta`, and `impact` |
| `bdd` | artifact ID plus scenario IDs with short `derives_from` references |

For `pdr` and `adr`, each record section is the addressable unit:

- `id` is `PDR-####` or `ADR-####`
- `recorded_at` is required per record and must be ISO 8601 UTC
- `derives_from` records the upstream cause/input items that led to the decision
- `contract delta` records the directly changed contract item IDs plus a short explanation
- `impact` records downstream affected item IDs plus the expected effect or required reconciliation
- `decision` and `why` are required prose sections

`bdd` is intentionally different:

- each `BDD-####` file is its own context artifact
- BDD remains multi-file because behavioral scenario sets benefit from selective loading during implementation and review
- BDD files always live under `/context/bdd/`

The templates in `assets/` are intentionally standalone. Small structural duplication between templates is allowed when it reduces context load at generation time.

---

## Context Graph Realization

The context graph is built from explicit derivation plus containment.

### Explicitly Stored

The engine stores:

- artifact metadata from frontmatter
- item IDs parsed from templates
- item-level `derives_from` references
- an index from short item IDs to owning artifact, section, tier, and scope
- containment:
  - item -> section
  - section -> artifact
  - artifact -> tier

### Inferred Views

The engine derives:

- **traceability** by walking `derives_from` upward or downward
- **staleness** by reverse traversal from changed approved items
- **loading slices** by selecting the smallest artifact scope that contains the target item and its upstream closure
- **artifact impact** by summarizing affected items upward into sections, artifacts, and tiers

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

The concrete tier order is:

```text
intent-specs -> product-specs -> system-specs -> context -> code
```

Within a contract tier, artifacts are generated in this order:

1. root artifacts in the tier
2. local `container.md` files for affected containers
3. local `component.md` files for affected components

### Double-Pass Generation

For contract tiers:

1. generate artifacts in dependency order
2. run a forward pass across the tier
3. run a back pass if later artifacts sharpen earlier artifacts
4. run structural eval
5. run semantic eval
6. run one additional bounded forward-back round if needed
7. emit the tier as `draft`
8. pause for tier-level review, eval, and approval according to profile

### Profiles

`lite`:

- hidden internal classification
- may generate multiple contract tiers in one run from drafts produced earlier in that run
- pauses once before code generation
- may pause after context generation if explicitly requested or if generation quality checks fail

`full`:

- visible tier boundary handling
- pauses for approval after each contract tier
- pauses after context generation before code generation

### Modes

`pm` defaults:

- emphasize `intent-specs` and `product-specs`
- load product-oriented context first
- bias review toward requirements, workflows, acceptance intent, and decision framing

`dev` defaults:

- emphasize `system-specs`, context, and code
- load technical scope first
- bias review toward technical boundaries, dependencies, and executable impact

### Operation Contracts

| Operation | Required Inputs | Output |
| --- | --- | --- |
| `init` | project brief, profile, mode | initial `intent-specs` draft |
| `generate` | target tier, scope, approved upstream basis, profile, mode | regenerated tier artifacts |
| `review` | current tier, scope, review style | findings and optional bounded same-tier fixes |
| `eval` | current tier, eval type, scope | structural, semantic, or behavioral findings |
| `reconcile` | approved upstream change set, downstream floor scope | refreshed stale downstream artifacts |
| `approve` | current contract tier, approval mode | approved tier and updated versions |
| `status` | scope | current lifecycle and stale summary |
| `import` | unmanaged repo scope, target ceiling tier | candidate contract drafts |

`review` only acts on the current tier and approved upstream truth.
`reconcile` only acts downward.

### Standard Operation Parameters

Implementations should standardize these parameter names even if the user-facing CLI or skill phrasing differs:

| Parameter | Meaning |
| --- | --- |
| `target_tier` | One of `intent-specs`, `product-specs`, `system-specs`, `context`, `code` |
| `scope` | One of `root`, `container:<container-slug>`, `component:<container-slug>/<component-slug>` |
| `profile` | One of `lite`, `full` |
| `mode` | One of `pm`, `dev` |
| `review_style` | One of `advisory`, `bounded` |
| `eval_type` | One of `structural`, `semantic`, `behavioral` |
| `approval_mode` | One of `human`, `delegated` |
| `pause_after_context` | Boolean override for pausing between context and code |

These parameters are the concrete implementation vocabulary behind the methodology-level operations.

### Context Generation

Context generation happens after the required contract tiers are approved.

Generation order inside context:

1. execution guidance artifacts for affected scopes
2. decision records if the change introduced product or architecture decisions
3. `bdd` scenarios when behavior projections are requested or produced by behavioral eval

Context is assumed correct by default, but implementations may pause after context generation for optional human review.

---

## Template System

The v1 `assets/` tree is:

```text
assets/
  intent-specs/
    intent.md
    defaults.md
  product-specs/
    prd.md
    usm.md
    dm.md
  system-specs/
    system.md
    containers.md
    container.md
    component.md
  context/
    pdr.md
    adr.md
    bdd.md
    root-AGENTS.md
    root-CLAUDE.md
    container-AGENTS.md
    container-CLAUDE.md
    component-AGENTS.md
    component-CLAUDE.md
```

Template rules:

- templates are split by artifact type and scope
- templates are standalone and loadable in isolation
- templates contain required sections, optional sections, and brief local guidance
- templates do not contain runtime logic
- templates may duplicate small structural fragments when that materially reduces context load
- code templates are out of scope in this phase

`references/` is reserved for future runtime-operational authority. This phase defines its role but does not require authoring it.

---

## Validation Checklist

The implementation is valid only if all of the following hold:

- every methodology artifact has a concrete output path and template mapping
- every templated artifact has a YAML frontmatter shape
- every visible addressable item uses a short typed `PREFIX-####` ID
- every visible derivation reference uses short item IDs only
- item numbering is fixed-width, append-only, and non-recycling within each family
- root contract artifact IDs remain semantic where specified
- every contract artifact has stable artifact IDs and item carriers
- every context artifact has stable artifact IDs and short derivation references
- `bdd` is context, not contract
- execution guidance is assistant-specific and scope-specific
- contract approval remains tier-level
- `review` remains current-tier plus upstream
- `reconcile` remains downstream only
- the context graph can be rebuilt from artifact metadata and item carriers without hidden prompt-only state
- brownfield import preserves compatible short IDs and records one-time remaps for incompatible legacy IDs
- the skill can load one narrow template at a time rather than one large combined template

This document is sufficient to author the future `SKILL.md`, `references/`, and local engine without inventing new artifact rules.
