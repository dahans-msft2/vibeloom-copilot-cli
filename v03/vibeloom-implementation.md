# VibeLoom Implementation

**Status:** v03 draft. Subject to change. Companion: [`vibeloom-methodology.md`](vibeloom-methodology.md).

The methodology defines what VibeLoom is. This document specifies how to build it: a skill, a deterministic engine, an artifact and template system.

---

## 1. Runtime architecture

VibeLoom has three operational layers:

1. **Skill / orchestrator** — natural-language interface, operation routing, user interaction, semantic judgment, task dispatch, review and reconciliation loops.
2. **Engine** — deterministic substrate: parsing, schema validation, ID allocation, graph construction, affected-set computation, status, staleness, trace indexing.
3. **Validation runners** — project-specific checks invoked by the skill: typecheck, tests, static analysis, contract tests, smoke checks, deployment checks. Configured via a per-project validation registry (§7).

The engine never judges product meaning or approval outcome. The skill never hand-waves graph or state work the engine can compute.

---

## 2. Governed repo layout

### 2.1 Full-mode layout (`pm`, `dev`, `ux`, `expert`)

```text
/
  intent.md
  defaults.md
  prd.md
  usm.md
  dm.md
  ux.md
  system.md
  containers.md
  AGENTS.md
  CLAUDE.md
  validation-registry.md
  ux-specs/
    mockups/
  <container>/
    container.md
    AGENTS.md
    CLAUDE.md
    <component>/
      component.md
      AGENTS.md
      CLAUDE.md
      context/
        bdd/
  .vibeloom/
    cache/
      contract-graph.json
      status.json
    traces/
      approvals.jsonl
      generations.jsonl
      evals.jsonl
      code-sync.jsonl
      decisions.jsonl
      imports.jsonl
      id-registry.json
    runs/
      RUN-.../
        tasks/TASK-.../
          patch.diff
          summary.yaml
          files/
```

### 2.2 Compact `vibe` layout

See [methodology §5.1](vibeloom-methodology.md#51-vibe-is-intentionally-minimal) for the design rationale (vibe as a *different operating point*, not a stripped-down full mode). The on-disk layout is:

```text
/
  intent.md
  defaults.md
  system.md
  AGENTS.md
  CLAUDE.md
  .vibeloom/
    traces/
      approvals.jsonl
      decisions.jsonl
```

No `cache/`, no graph state, no code-sync trace. Approval traces remain — cheap and useful even at vibe scale, and the substrate the future upgrade migration runs on.

---

## 3. Cache vs traces

### 3.1 Cache (`.vibeloom/cache/`)

Regenerable state. If deleted, the engine rebuilds it from artifacts and traces.

```text
.vibeloom/cache/contract-graph.json
.vibeloom/cache/status.json
```

### 3.2 Traces (`.vibeloom/traces/`)

Durable provenance. Append-oriented JSONL (with `id-registry.json` as the one structured exception). Never silently regenerated from current state. Missing traces degrade governance integrity; the user must explicitly re-baseline.

```text
.vibeloom/traces/approvals.jsonl
.vibeloom/traces/generations.jsonl
.vibeloom/traces/evals.jsonl
.vibeloom/traces/code-sync.jsonl
.vibeloom/traces/decisions.jsonl
.vibeloom/traces/imports.jsonl
.vibeloom/traces/id-registry.json
```

---

## 4. Engine responsibilities

The engine owns:

- artifact discovery,
- frontmatter parsing,
- item extraction,
- schema validation,
- stable ID allocation and registry,
- derivation DAG validation,
- graph indexing,
- affected-set computation,
- status computation including `obsolete` heuristics,
- direct-edit detection,
- stale / uncovered / dangling / drifted / obsolete classification,
- trace reading and writing for deterministic events,
- patch staging and atomic application (see §6).

The engine does not own:

- semantic equivalence,
- product or UX judgment,
- approval decisions,
- freeform generation,
- user conversation,
- final task decomposition judgment.

---

## 5. Stable IDs and registry

### 5.1 ID prefix registry

Every governed semantic item carries a stable ID of the form `PREFIX-NNNN` (zero-padded 4-digit, fixed width). Globally unique by prefix across the repo, append-only within each family, retired IDs never reused.

The table below is the **canonical** ID prefix registry. It defines every prefix VibeLoom recognizes, its tier, where it is materialized, its scope, and any layer or derivation constraints. Skill references (the `skill/references/artifacts.md` template inside `vibeloom-templates.md`) and templates derive from this table; if any of them disagree, this table wins.

| Prefix | Name | Tier | Source artifact | Scope | Notes (constraints, derivation) |
| --- | --- | --- | --- | --- | --- |
| `CAP` | capability | intent-specs | `intent.md` | root | Root entity; no upstream basis. |
| `CST` | hard constraint | intent-specs | `intent.md` or `defaults.md` | root | Root entity; no upstream basis. |
| `DEF` | repo-wide default | intent-specs | `defaults.md` | root | Universally binding once derived; downstream may reference without an explicit typed edge. Tech Stack entries also use `DEF`. |
| `OBJ` | objective | product-specs | `prd.md` | root | Derives from `CAP`. |
| `KR` | key result | product-specs | `prd.md` | root | Derives from `OBJ`. |
| `MET` | metric | product-specs | `prd.md` | root | Derives from `KR`, `FR`, or `NFR`. |
| `FR` | functional requirement | product-specs | `prd.md` | root | Derives from `CAP`; optionally from `OBJ`/`STORY`. EARS allowed as structured field. |
| `NFR` | non-functional requirement | product-specs | `prd.md` | root | Derives from `CST` or `OBJ`. EARS allowed. |
| `EPIC` | epic | product-specs | `usm.md` | root | Derives from `CAP`/`OBJ`. |
| `FLOW` | workflow / journey | product-specs | `usm.md` | root | Derives from `EPIC`. |
| `STORY` | story | product-specs | `usm.md` | root | Derives from `EPIC`/`FLOW`. |
| `ACC` | acceptance criterion | product-specs | `usm.md` | per-`STORY` | Derives from `STORY`. EARS allowed. |
| `MS` | milestone | product-specs | `usm.md` | root | Groups `STORY`s for delivery. |
| `TERM` | ubiquitous-language term | product-specs | `dm.md` | root | Domain vocabulary; consumed by `BC`/`AGG`/`ENT`. |
| `BC` | bounded context | product-specs | `dm.md` | root | **Hosted only by `domain`-layer components.** Derives from `CAP`/`STORY`. |
| `AGG` | aggregate | product-specs | `dm.md` | per-`BC` | Lives inside one `BC`. |
| `ENT` | entity | product-specs | `dm.md` | per-`AGG` | Lives inside one `AGG`. |
| `VO` | value object | product-specs | `dm.md` | per-`AGG` | Lives inside one `AGG`. |
| `INV` | invariant | product-specs | `dm.md` | per-`AGG` | Domain rule scoped to an `AGG`. |
| `VIEW` | UX view | ux-specs | `ux.md` | root | Optionally cites `MOCK`. |
| `INT` | UX interaction | ux-specs | `ux.md` | per-`VIEW` | Per-view interaction. |
| `UXC` | UX constraint | ux-specs | `ux.md` | root | Cross-view design constraint. |
| `MOCK` | mockup reference | ux-specs | `ux.md` | root | Pointer to file under `ux-specs/mockups/`. |
| `EXT` | external actor / system | system-specs | `system.md` | root | System context; outside trust boundaries. |
| `TB` | trust boundary | system-specs | `system.md` | root | Crosses one or more `CONT`s. |
| `SNFR` | system-wide NFR boundary | system-specs | `system.md` | root | Global cross-cutting NFR. |
| `CONT` | container | system-specs | `containers.md` (inventory) + per-container `container.md` | root + per-container | Carries required `layer` field (`presentation` / `application` / `domain` / `infrastructure`). |
| `CMP` | component | system-specs | `container.md` (inventory) + per-component `component.md` | per-`CONT` | Belongs to exactly one `CONT`. Layer inherited from parent `CONT`. |
| `IF` | owned interface | system-specs (body carrier) | `component.md` | per-`CMP` | Structured content; not an independent graph node in v0.3. |
| `DEP` | component dependency | system-specs (body carrier) | `component.md` | per-`CMP` | Structured content. |
| `BEH` | local technical behavior | system-specs (body carrier) | `component.md` | per-`CMP` | Structured content. |
| `NOTE` | local test/runtime note | system-specs (body carrier) | `component.md` | per-`CMP` | Structured content. |
| `BDD` | behavioral-scenario artifact | context | `bdd.md` (one file per behavior) | per-`CMP` | One file per behavior; lives under `<container>/<component>/context/bdd/`. |
| `SCN` | Gherkin scenario | context | `bdd.md` body | per-`BDD` | Inside a `BDD` artifact. |
| `RUN` | run | runtime | `.vibeloom/runs/RUN-.../` | per-invocation | Append-only ID family; one per `generate`/`reconcile` invocation. |
| `TASK` | subagent task | runtime | `.vibeloom/runs/RUN-.../tasks/TASK-.../` | per-task | Append-only. |
| `PLAN` | dispatch plan | runtime | `.vibeloom/runs/RUN-.../plan.yaml` | per-`RUN` | Append-only. |
| `APPROVAL` | approval trace | trace | `.vibeloom/traces/approvals.jsonl` | append-only | One entry per `approval_unit` flip from `draft` → `approved`. Schema §8.1. |
| `SYNC` | code-sync trace | trace | `.vibeloom/traces/code-sync.jsonl` | append-only | Source-map-shaped. Schema §8.2. |
| `GEN` | generation trace | trace | `.vibeloom/traces/generations.jsonl` | append-only | One per task result (success or failure). Schema §8.3. |
| `EVAL` | eval trace | trace | `.vibeloom/traces/evals.jsonl` | append-only | Per-eval-run. Schema §8.4. |
| `DEC` | decision trace | trace | `.vibeloom/traces/decisions.jsonl` | append-only | Carries `record_type` (`IDR` / `PDR` / `UDR` / `ADR` / `general`). Schema §8.5. |
| `IMP` | import trace | trace | `.vibeloom/traces/imports.jsonl` | append-only | One per `import` invocation. Schema §8.6. |

`IDR`, `PDR`, `UDR`, `ADR` are **not** independent ID prefixes — they are `record_type` values inside the unified `DEC-` family. See methodology §11.1.

`IF` / `DEP` / `BEH` / `NOTE` are structured content within `component.md` rather than independent graph nodes; the engine indexes them but does not require them to carry their own derivation edges.

### 5.2 Registry

Allocation state lives at `.vibeloom/traces/id-registry.json`:

```json
{
  "FR": {"next": 42, "retired": ["FR-0007"]},
  "CMP": {"next": 12, "retired": []}
}
```

The registry is engine state, not LLM context. Subagents **propose** new semantic items; the orchestrator/engine allocates final IDs. Retired IDs are never reused.

---

## 6. Artifact frontmatter

### 6.1 Contract artifact

```yaml
---
artifact_id: prd
artifact_type: prd
tier: product-specs
approval_unit: product-specs       # which bundle this artifact participates in
scope_kind: root
scope_id: root
status: draft
timestamp: 2026-05-02T00:00:00Z
derives_from: [CAP-0001, CST-0002]
---
```

`approval_unit` is structural — it names the bundle in which this artifact is approved as a single transaction (e.g. `prd.md`, `usm.md`, and `dm.md` all share `approval_unit: product-specs`, so they are reviewed and approved together). `approval_mode` (`user` | `delegated`) is event-level and lives on the approval trace (§8.1), not on the artifact — the orchestrator computes the required mode from the current methodology mode + tier (§5).

### 6.2 Context artifact

```yaml
---
artifact_id: config.component.web.search
artifact_type: config
tier: context
scope_kind: component
scope_id: web/search
timestamp: 2026-05-02T00:00:00Z
derives_from: [CMP-0012, IF-0042]
---
```

Context artifacts do not carry `status` or `approval_mode`.

### 6.3 Container frontmatter

```yaml
---
artifact_id: container.notes-api
artifact_type: container
tier: system-specs
approval_unit: system-specs       # containers/components share the system-specs bundle
scope_kind: container
scope_id: notes-api
layer: application                # presentation | application | domain | infrastructure
status: approved
timestamp: 2026-05-02T00:00:00Z
derives_from: [CONT-0002]
---
```

The `layer` field is required and carries an enum from the DDD architectural layers. The orchestrator and eval use it to determine generation rules and per-layer constraints (see methodology §6.5).

### 6.4 Component frontmatter

```yaml
component_id: CMP-0012
container_id: CONT-0002
owned_paths:
  - web/src/search/**
owned_interfaces:
  - IF-0042
hosted_bounded_contexts:
  - BC-0003
  - BC-0008
```

Rules (see methodology §6.5):

- container may host multiple components,
- component belongs to exactly one container,
- component may host multiple bounded contexts (only in `domain`-layer containers),
- bounded context belongs to exactly one component,
- `hosted_bounded_contexts` must be empty for components in non-`domain` layers.

---

## 7. Validation registry

Each project declares its validation runners once, at the root, in `validation-registry.md`. Code-sync traces reference registered runners by ID.

The file is a markdown document with YAML frontmatter and a fenced YAML body. Concretely:

````markdown
---
artifact_type: validation-registry
tier: meta
---

# Validation registry

Project-specific validation runners. The orchestrator invokes these by `runner_id` during `eval` and after task patches are staged.

```yaml
- runner_id: typecheck
  command: tsc --noEmit
  scope: workspace
  inputs:  [src/**]
  outputs: [status, logs]

- runner_id: unit
  command: npm test --workspace ${component}
  scope: component
  inputs:  [owned_paths, generated_tests]
  outputs: [status, logs, evidence_refs]

- runner_id: contract-conformance
  command: vibeloom contract-test --component ${component}
  scope: component
  inputs:  [generated_bdd, owned_paths]
  outputs: [status, logs]

- runner_id: bdd
  command: cucumber-js component/${component}/context/bdd
  scope: component

- runner_id: lint
  command: eslint
  scope: workspace
```
````

Parser: frontmatter is parsed as YAML; the body's first ```yaml fence is parsed as a list of runner records. Subsequent fenced blocks (e.g. usage notes or per-runner explanations) are ignored by the engine and serve human readers only.

Runner families to consider:

- typecheck,
- lint and static analysis,
- unit tests,
- integration tests,
- generated BDD or contract tests,
- interface conformance,
- security checks,
- smoke or deployment checks.

VibeLoom is not TDD. It requires **contract-conformance evidence** — and tests, static analysis, and runtime contract checks are all valid forms.

---

## 8. Trace schemas

Trace families are defined in [methodology §11](vibeloom-methodology.md#11-traces). This section specifies the **schema** for each trace type. All schemas share a `schema_version` field; extension is additive (new optional fields can be added in any minor version; required fields can only be added in a major version). Older traces remain readable.

Every trace also carries `trace_id`, `kind`, and `timestamp`. These are omitted from per-schema fields for brevity.

**Reconstructability principle.** Each trace family carries the metadata to promote its implied graph relationships into actual nodes/edges later (roadmap CGKG-B). Concretely: approval traces carry per-item content fingerprints; generation traces carry `basis_ids` + `output_item_ids`; code-sync traces are source-map-shaped; eval traces carry per-finding `item_id`; decision traces carry `record_type` + `affects` + `load_bearing`; import traces summarize aggregates, with per-candidate evidence living in the resulting draft artifacts. v0.3 keeps the contract graph as a knowledge graph (instantiated ontology only); promotion is deferred, never blocked by lossy schemas.

### 8.1 Approval trace

```json
{
  "schema_version": "1.0",
  "trace_id": "APPROVAL-20260502-001",
  "kind": "approval",
  "timestamp": "2026-05-02T12:00:00Z",
  "run_id": "RUN-20260502-001",
  "approval_unit": "product-specs",
  "approval_mode": "user",
  "items": {
    "FR-0007": "sha256:...",
    "STORY-0019": "sha256:..."
  },
  "artifacts": {
    "prd": "sha256:...",
    "usm": "sha256:..."
  }
}
```

Approval traces are the non-regenerable approval baseline — durable across schema versions, never silently rebuilt from current state.

### 8.2 Code-sync trace

```json
{
  "schema_version": "1.0",
  "trace_id": "SYNC-20260502-001",
  "kind": "code-sync",
  "timestamp": "2026-05-02T13:00:00Z",
  "run_id": "RUN-20260502-004",
  "scope": "component:web/search",
  "realizes": ["CMP-0012", "IF-0042", "BEH-0031", "VIEW-0006"],
  "basis_hashes": {
    "CMP-0012": "sha256:...",
    "IF-0042": "sha256:...",
    "VIEW-0006": "sha256:..."
  },
  "owned_paths": ["web/src/search/**", "web/tests/search/**"],
  "file_hashes": {
    "web/src/search/index.ts": "sha256:...",
    "web/tests/search.test.ts": "sha256:..."
  },
  "validation": {
    "typecheck": "passed",
    "unit": "passed",
    "contract-conformance": "passed",
    "bdd": "passed"
  }
}
```

Source-map-shaped: connects generated code to contract IDs, file hashes, validation evidence. v03 doesn't require deep function-level graph carriers — this trace bridges them.

### 8.3 Generation trace

```json
{
  "schema_version": "1.0",
  "trace_id": "GEN-20260502-007",
  "kind": "generation",
  "timestamp": "2026-05-02T13:30:00Z",
  "run_id": "RUN-20260502-004",
  "task_template_id": "generate-product-specs",
  "task_template_version": "0.3.1",
  "scope": "root:product-specs",
  "basis_ids": ["CAP-0001", "CST-0002"],
  "output_artifact_ids": ["prd", "usm", "dm"],
  "output_item_ids": ["FR-0007", "FR-0008", "STORY-0019", "BC-0003"],
  "result_status": "ok",
  "late_fetch_events": [
    {"target_scope": "component:web/search", "kind": "interface", "ids": ["IF-0007"]}
  ],
  "validation_summary": {"structural": "passed", "semantic": "1 advisory"},
  "cost": {"tokens_in": 12450, "tokens_out": 3120, "wall_ms": 14200, "usd": 0.18}
}
```

Together, `basis_ids` + `output_artifact_ids` + `output_item_ids` let any item trace back to the generation event that produced it — and from there to the upstream basis. This closes the provenance loop for future graph promotion. Generation traces also feed [late-fetch → context proposals](roadmap.md#d1-late-fetch--context-proposal) and cost reporting.

### 8.4 Eval trace

```json
{
  "schema_version": "1.0",
  "trace_id": "EVAL-20260502-019",
  "kind": "eval",
  "timestamp": "2026-05-02T14:00:00Z",
  "run_id": "RUN-20260502-005",
  "target": "product-specs",
  "checks_run": ["structural", "semantic"],
  "findings": [
    {"finding_id": "FIND-0007", "severity": "advisory", "item_id": "ACC-0014", "message": "Acceptance criterion lacks measurable outcome."}
  ],
  "cost": {"tokens_in": 4200, "tokens_out": 1100, "wall_ms": 5800, "usd": 0.06}
}
```

Eval traces capture every read-only check that ran, with severity and item association. Required for [trace-derived learning](roadmap.md#d-trace-derived-learning) and for the eventual contract debugger.

### 8.5 Decision trace

```json
{
  "schema_version": "1.0",
  "trace_id": "DEC-20260502-003",
  "kind": "decision",
  "record_type": "ADR",
  "timestamp": "2026-05-02T15:00:00Z",
  "author": "ilya@vibeloom.ai",
  "topic": "tax-calculation-strategy",
  "load_bearing": true,
  "affects": ["BC-0008", "FR-0042"],
  "payload": "Selected progressive bracket calculation over flat-rate. Rejected: flat-rate (oversimplifies state-level variance), per-jurisdiction lookup (too brittle to maintain)."
}
```

Schema fields:

- `record_type` (optional, enum: `IDR | PDR | UDR | ADR | general`, default `general`) — classifies the decision by primary contract tier (intent-specs / product-specs / ux-specs / system-specs respectively). `general` is for process, methodology, or operational decisions that don't change the contract. See [methodology §11.1](vibeloom-methodology.md#111-decision-trace-classification).
- `affects` (optional, recommended) — list of contract item IDs this decision constrains. Captures multi-tier impact regardless of `record_type`. For `general` decisions this is typically empty.
- `load_bearing` (default `false`) — flag for whether the decision still informs future generation. Active "decision context" is a queried view filtering decision traces by `load_bearing: true`.
- `payload` — freeform YAML or markdown. Naturally accommodates the Nygard ADR template (Context / Decision / Consequences) or any equivalent.

Decision traces are the single home for human-authored decision history (ADR/PDR/UDR/IDR/general). Promote truly normative decisions to IDed contract items; the trace entry stays immutable. `affects` and `record_type` let a future release (roadmap CGKG-B) promote load-bearing decisions to graph nodes without re-mining prose.

#### 8.5.1 Per-record markdown rendering

The JSONL stream above is canonical. Each entry is also materialized as a per-record markdown file under `/decisions/<record_type>/<TRACE_ID>-<slug>.md` (e.g. `/decisions/adr/ADR-20260502-003-tax-calculation-strategy.md`). The markdown is a **derived view** — the engine regenerates it from the JSONL whenever the trace is appended.

Why two presentations: the JSONL is the append-only event log (machine-parseable, schema-versioned); the markdown is git-friendly (per-decision blame), human-readable (open in any editor), and ecosystem-compatible (`adr-tools`, `log4brains`, Structurizr ADR plugins all expect a folder of markdown files).

File frontmatter mirrors a subset of the JSONL fields:

```yaml
---
trace_id: DEC-20260502-003
kind: decision
record_type: ADR
timestamp: 2026-05-02T15:00:00Z
author: ilya@vibeloom.ai
topic: tax-calculation-strategy
load_bearing: true
affects: [BC-0008, FR-0042]
---

# ADR-20260502-003 — Tax calculation strategy

## Context
...

## Decision
Selected progressive bracket calculation over flat-rate.

## Consequences
- Rejected: flat-rate (oversimplifies state-level variance)
- Rejected: per-jurisdiction lookup (too brittle to maintain)
```

Body shape is the Nygard ADR template (Context / Decision / Consequences) by default; users may amend the body for human readability without affecting the JSONL trace (the JSONL `payload` carries the raw decision content; body prose is regenerated from `payload` on first materialization, then preserved on subsequent regenerations of *other* fields). When `load_bearing` flips to `false`, the file remains on disk with frontmatter updated.

The markdown files are regenerable: `vibeloom decisions render` rebuilds the entire `/decisions/` tree from `decisions.jsonl`. Drop the tree, run the command, identical files come back.

### 8.6 Import trace

```json
{
  "schema_version": "1.0",
  "trace_id": "IMP-20260502-001",
  "kind": "import",
  "timestamp": "2026-05-02T16:00:00Z",
  "evidence_summary": {"files_scanned": 1247, "tests_indexed": 312, "languages": ["typescript", "python"]},
  "candidates_proposed": {"CAP": 7, "FR": 42, "BC": 23, "CMP": 11, "VIEW": 0},
  "confidence_distribution": {"high": 38, "medium": 31, "low": 14},
  "payload": {"notes": "No UX evidence (no Figma export found, no design tokens). Recommend ux mode upgrade after first product-spec review."}
}
```

One import trace per `import` invocation. The aggregate counts above are the *summary*; per-candidate evidence (which files supported inferring `BC-0003`, what confidence each inference had) lives in the produced artifacts' frontmatter `derives_from` and free-form `evidence` fields. Trace + artifacts form a complete reconstructable record. Import traces also support audit ("how was this contract derived?") and the eventual import-quality learning capability.

### 8.7 Schema extension policy

- Every trace carries `schema_version` (semver string).
- New optional fields may be added in any minor version (`1.0` → `1.1`); existing parsers ignore unknown fields.
- Required fields may only be added in a major version (`1.x` → `2.0`); parsers must explicitly opt into the new major.
- Older traces remain readable forever — vibeloom never silently rewrites them.
- The engine validates trace files on load and surfaces version mismatches as a status finding instead of crashing.

### 8.8 Trace-derived learning (deferred)

Trace-derived proposals (e.g., late-fetch frequency suggesting active-context additions, repeated reconcile choices suggesting ADR proposals) are deferred to v04+. The schemas above are designed so the substrate exists when the capabilities ship. See [roadmap §D](roadmap.md#d-trace-derived-learning).

---

## 9. Graph cache

`.vibeloom/cache/contract-graph.json`:

```json
{
  "artifacts": {},
  "items": {},
  "edges": [],
  "ownership": {},
  "scope_index": {},
  "trace_index": {}
}
```

`trace_index` maps contract IDs to code-sync traces, approval traces, generation runs, and eval evidence. Derived from durable traces; rebuildable.

`status.json` is the cached output of `status` computation.

---

## 10. Status computation

Status categories and their *meanings* are defined in [methodology §9](vibeloom-methodology.md#9-status-categories): `current` / `stale` / `uncovered` / `dangling` / `drifted` / `obsolete`. This section specifies the **computation rules** the engine uses to assign categories.

`status` reports per contract tier and per scope:

- lifecycle state,
- categories per item (using the methodology §9 definitions),
- affected artifacts and scopes,
- direct-edit detection,
- code-sync state,
- validation state,
- current mode,
- recommended next operation.

Computation rules:

| Category | Engine trigger |
| --- | --- |
| `current` | item's `derives_from` hashes match the latest approval trace for its basis, AND no eval finding exists |
| `stale` | item's `derives_from` hashes do not match the latest approval trace for its basis (basis was reapproved with changes) |
| `uncovered` | a downstream artifact is required by template/derivation rules but does not exist; OR an upstream item has no downstream realization where one is mandated |
| `dangling` | item's `derives_from` references an ID that is no longer live — the ID is retired in the registry, or was never allocated |
| `drifted` | item's content hash differs from its expected hash given basis (semantic mismatch flagged by eval), OR a direct edit was detected (file mtime + hash diff without a generation trace) |
| `obsolete` | user-marked, OR all downstream consumers are themselves obsolete or absent (heuristic) |

`obsolete` requires either explicit user marking via `vibeloom mark-obsolete <id>` or a heuristic signal. The engine surfaces obsolete candidates in `status` but never auto-marks.

---

## 11. Operation packets

### 11.1 Review packet

```yaml
packet_type: review
packet_id: REVIEW-20260502-001
target: product-specs
basis:
  approved_upstream: [CAP-0001, CST-0002]
changes:
  added: [FR-0042]
  modified: [STORY-0017]
  removed: []
findings:
  blocking: []
  advisory:
    - finding_id: FIND-0007
      item_id: ACC-0014
      summary: "Acceptance criterion lacks measurable outcome."
impact:
  uncovered_downstream: [FR-0042]
recommendation: proceed_to_approve
user_notes: |
  (free-form notes the user can add before deciding)
```

### 11.2 Reconciliation packet

```yaml
packet_type: reconciliation
packet_id: RECON-20260502-001
target: code
scope: component:web/search
stale_items: [CMP-0012, IF-0042]
drift_cases:
  - drift_id: DRIFT-0003
    evidence: "Generated code still implements old search ranking."
    directions:
      - preserve_contract_regenerate_code
      - amend_contract_to_preserve_downstream_behavior
      - user_defined
recommended_direction: preserve_contract_regenerate_code
user_notes: |
  (free-form notes the user can add before deciding)
```

Packets are write-capable: the user can add findings, modify recommendations, or annotate decisions before deciding.

---

## 12. Task templates

Task templates are structured operation instructions for subagents. **They are markdown documents, not YAML wrappers around prose.** Each template uses a consistent section structure so the engine can extract what it needs and the agent reads it as prose.

The standard task template inventory (assets shipped with vibeloom):

```text
assets/tasks/
  generate-intent-specs.md
  generate-product-specs.md
  generate-product-specs-from-ux.md   # ux mode variant
  generate-ux-specs.md
  generate-system-specs.md
  generate-component-code.md
  eval-target.md
  review-target.md
  reconcile-code.md
  reconcile-contract.md
  infer-capabilities.md               # import-time inference task family
  infer-functional-requirements.md
  infer-bounded-contexts.md
  infer-components.md
```

### 12.1 Structure

Every task template follows the canonical Design-by-Contract structure (an hommage to Meyer, consistent with the codæ manifesto §7):

```text
# <task name>

## Purpose
One-paragraph statement of what this task does and why it exists.

## Inputs
Concrete list of inputs the orchestrator must provide before invoking this task.

## Preconditions
What must be true about the world before this task runs (caller's responsibility — the orchestrator gates on these).

## Steps
Numbered, prose-form steps the agent should follow.

## Output
The shape and required fields of the result the agent must return (data structure).

## Postconditions
State-of-the-world guarantees after the task succeeds (callee's responsibility — what the task promises).

## Constraints
Hard rules the agent must follow during the task; the orchestrator will enforce on the result.

## Invariants
Properties that must hold both before and after the task (often task-specific; system-wide invariants from §13.4 also apply).

## Validation
What the orchestrator runs against the result before accepting it.

## Failure modes
Known failure modes and recovery handoffs (typically points to `references/troubleshooting.md`).
```

The orchestrator validates the result against the constraints, invariants, and validation rules. Postconditions are the structural-eval target — when the orchestrator can deterministically check a postcondition, it promotes it from heuristic to mechanical to structural per the verification ladder (§14.3). The template itself is an artifact — versioned, mendable, and tracked in `.vibeloom/traces/generations.jsonl` via `task_template_version` when changed.

### 12.2 Example: `generate-product-specs.md`

```markdown
# Generate product-specs

## Inputs
- Approved intent-specs (intent.md, defaults.md)
- Optional: ux evidence or mockup extraction summary
- Optional: existing prd.md, usm.md, dm.md (if regenerating)

## Steps
1. Read approved capabilities and constraints.
2. Derive objectives, requirements (with EARS where applicable), and metrics into prd.md.
3. Derive epics, flows, stories, acceptance criteria into usm.md.
4. Derive ubiquitous-language terms, bounded contexts, aggregates, entities, value objects, and invariants into dm.md.
5. Cite the upstream basis for every IDed item.
6. Propose item labels — do not assign final IDs.

## Output
Return a `product-generation-summary` with:
- created_items: list of {proposed_id, kind, label, derives_from}
- modified_items: list of {item_id, before_hash, summary_of_change}
- removed_items: list of item_ids
- unresolved_assumptions: list of strings
- recommended_review_findings: list of finding strings

## Constraints
- Preserve upstream meaning.
- Cite at least one approved upstream item per derived item.
- Do not assign final IDs.
- Do not modify intent-specs.

## Validation
- structural eval on draft product-specs
- semantic eval against approved intent
```

### 12.3 Versioning

Task templates change over time. Each template carries a `task-template-version` field at the bottom; engine logs template changes in `.vibeloom/traces/generations.jsonl` so a future user can answer "which version of `generate-product-specs` was used for this artifact?"

---

## 13. Dispatch and subagent execution

This section defines the orchestrator-to-subagent contract that makes parallel agent generation work. The dispatch plan, the wave-assembly rules, the parallel semantics, and the subagent task header are the load-bearing pieces.

### 13.1 Dispatch plan structure

`engine.dispatch_plan(affected)` returns a plan in this shape:

```yaml
plan_id: PLAN-20260502-004
affected_set: [CAP-0001, FR-0007, STORY-0019, CMP-0012, IF-0042, VIEW-0006, BEH-0031]
waves:
  - wave_id: W1
    scopes:
      - scope_id: product-specs
        kind: product-specs
        owned_paths: ["prd.md", "usm.md", "dm.md"]
        allowed_read_paths: ["intent.md", "defaults.md"]
        task_template_id: generate-product-specs
    dependencies: []
  - wave_id: W2
    scopes:
      - scope_id: ux-specs
        kind: ux-specs
        owned_paths: ["ux.md"]
        allowed_read_paths: ["intent.md", "prd.md", "usm.md", "ux-specs/mockups/**"]
        task_template_id: generate-ux-specs
      - scope_id: system-specs
        kind: system-specs
        owned_paths: ["system.md", "containers.md"]
        allowed_read_paths: ["intent.md", "prd.md", "usm.md", "ux.md"]
        task_template_id: generate-system-specs
    dependencies: [{from: W1, to: W2}]
  - wave_id: W3
    scopes:
      - scope_id: component:web/search
        kind: component-code
        owned_paths: ["web/src/search/**", "web/tests/search/**"]
        allowed_read_paths: ["**/component.md", "**/AGENTS.md"]
        task_template_id: generate-component-code
      - scope_id: component:search-api
        kind: component-code
        owned_paths: ["search-api/src/**", "search-api/tests/**"]
        allowed_read_paths: ["**/component.md", "**/AGENTS.md"]
        task_template_id: generate-component-code
    dependencies: [{from: W2, to: W3}]
```

The plan is build once per `generate` invocation and is itself a logged artifact (`.vibeloom/runs/RUN-.../plan.yaml`).

### 13.2 Wave assembly rules

The engine assembles waves deterministically from the affected set:

1. **Disjoint ownership.** Two scopes can be in the same wave iff their `owned_paths` are disjoint (no overlap). This guarantees per-wave parallel execution does not produce write conflicts.
2. **Derivation precedence.** Scope B is in a strictly later wave than scope A iff B's `derives_from` references items owned by A. The DAG of derivation determines minimum wave count.
3. **Concurrency cap.** Wave size is bounded by `orchestrator_concurrency_policy.max_wave_size` (default: 5 subagents per wave). Excess scopes spill to the next wave even when topologically eligible.
4. **Reconciliation singletons.** Reconciliation tasks always go in singleton waves (one subagent per wave). Reconciliation may need to read state the orchestrator just applied; isolating it prevents read/write surprises.
5. **Eval ordering.** Read-only eval tasks may run alongside generation tasks in the same wave only if they target a different scope. Otherwise eval runs as a separate wave after.

### 13.3 Parallel semantics: `execute_plan(plan)`

`execute_plan(plan)` is the single primitive that turns a dispatch plan into committed work and traces. `generate` and `reconcile` both invoke it; nothing else in the engine touches subagents directly.

```pseudo
execute_plan(plan):
  for wave in plan.waves:
    pending = []
    for scope in wave.scopes:
      template = task_template_for(scope.kind)
      header   = build_subagent_header(scope, wave, run, plan)
      future   = subagent.spawn(header)              # runs concurrently
      pending.append({"future": future, "scope": scope, "template": template})

    # all tasks in this wave run in parallel
    completed = await all([p["future"] for p in pending])

    # process results in deterministic scope_id order — reproducible run-to-run
    for p, r in sorted(zip(pending, completed), key=lambda x: x[1].scope_id):
      scope, template = p["scope"], p["template"]
      orchestrator.validate_summary(r, template)   # against template.output_shape
      orchestrator.validate_scope(r.patch, scope.allowed_paths)
      orchestrator.stage(r.patch)
      validation = orchestrator.run_validators(scope, r)
      if not validation.passed:
        traces.write("generations", FAILED, r, validation)
        continue                                     # peers in this wave still apply
      orchestrator.apply_atomic(r.patch)             # see §14
      traces.write("generations", OK, r, validation)
      if scope.is_code:
        traces.write("code-sync", build_sync_record(r, validation))
```

Key properties:
- `subagent.spawn(header)` returns a future. Runtime concurrency is bounded by `max_wave_size`.
- Each result is paired with the `scope` and `template` that produced it (via `pending`); validation, trace writing, and code-sync emission all use that pair, never values from a different scope.
- Results are processed in deterministic `scope_id` order even though they completed in arbitrary order, so the working-tree state is reproducible run-to-run for the same plan.
- A failed task does not block the wave — successful peers still apply atomically. Failure is recorded in the generation trace.
- Same-wave outputs are not input to other same-wave tasks. Cross-wave handoff happens only between waves (W1's patches are committed before W2's load sets are assembled).

### 13.4 Subagent task header schema

The orchestrator constructs and passes this header to each subagent. It is the **only** orchestrator-to-subagent contract; everything the subagent sees is in this header or in files referenced by it.

```yaml
task_id: TASK-20260502-014
run_id: RUN-20260502-004
wave_id: W2
template_id: generate-ux-specs
template_version: 0.3.1
scope:
  scope_id: ux-specs
  kind: ux-specs
  owned_paths: ["ux.md"]
load_set_refs:
  contract:
    - intent.md
    - prd.md
    - usm.md
  context:
    - AGENTS.md
  evidence:
    - ux-specs/mockups/01-checkout-empty.png
    - ux-specs/mockups/02-checkout-payment.png
foreign_refs: []           # cross-scope reads, if any
allowed_read_paths: ["intent.md", "prd.md", "usm.md", "ux-specs/mockups/**", "AGENTS.md"]
allowed_write_paths: ["ux.md"]
validation_contract:
  - structural-eval-on-output
  - semantic-eval-against-basis
result_shape_id: ux-generation-summary
budget:
  max_tokens: 50000
  max_wall_ms: 60000
```

`result_shape_id` references the task template's `## Output` section by name (matching the template's `task_template_id` plus a result-kind suffix, e.g. `ux-generation-summary` for `generate-ux-specs`). The orchestrator's `validate_summary(r, template)` checks that the returned result matches the field structure and required fields specified there. When a task template's `## Output` changes incompatibly, bump `template_version` (§12.3) — `result_shape_id` is stable across compatible changes.

Mendable means schema'd. Changing how the orchestrator prompts subagents means versioning this header — same policy as trace schemas (§8.7).

### 13.5 No direct subagent communication

Subagents do not communicate directly. The orchestrator mediates all context, patches, validation, and acceptance. If subagent A needs something subagent B is producing, that's a wave-ordering issue — A should be in a later wave.

---

## 14. Patch-based writes

Write-capable subagents do not write directly to the working tree. They write staged output:

```text
.vibeloom/runs/RUN-.../
  tasks/TASK-.../
    patch.diff
    summary.yaml
    files/
```

The orchestrator:

1. validates the result summary against the task template,
2. validates write scope against allowed paths,
3. applies the patch to a staging tree,
4. runs registered validation runners,
5. on success, applies atomically to the working tree (single commit, all-or-nothing),
6. emits generation and code-sync traces.

On failure, the staged output stays in `.vibeloom/runs/.../` for inspection. The working tree is untouched.

---

## 15. Operation implementation

This section gives brief pseudocode for each operation. Algorithms are intentionally simple and explicit; the engine is the only place where deterministic logic lives.

### 15.1 `generate`

```pseudo
generate(target_or_scope):
  affected = engine.affected_set(target_or_scope, include=["stale", "uncovered"])
  plan     = engine.dispatch_plan(affected)
  execute_plan(plan)        # §13.3 — wave assembly, validation, traces, failure handling
  status.recompute()
```

### 15.2 `eval`

```pseudo
eval(target):
  findings = []
  findings += engine.structural_eval(target)
  if target.requires_semantic_eval():
    findings += subagent.semantic_eval(target, basis=engine.upstream_basis(target))
  if target.is_code_or_context():
    runners = registry.runners_for(target.scope)
    for runner in runners:
      result = orchestrator.run(runner, target)
      findings += runner.findings_from(result)
  traces.write("evals", target, findings)
  return findings  # read-only; nothing applied
```

### 15.3 `review`

```pseudo
review(target):
  loop:
    findings = eval(target)
    packet   = engine.build_review_packet(target, findings)
    decision = user.show(packet)                    # may add notes, accept, reject, edit
    if decision.action == "approve":
      return packet
    if decision.action == "exit":
      return packet                                 # findings remain
    # decision.action == "propose_fix"
    for fix in decision.fixes:
      subagent.apply_bounded_fix(target, fix)       # only edits target; no propagation
    # loop re-evaluates
```

`review` fixes the target in place. It does not propagate downward.

### 15.4 `reconcile`

Reconcile is interactive and bounded. It walks the affected set one drift case at a time, presents the user a packet with direction options, and applies the chosen direction. Each step emits a trace.

```pseudo
reconcile(target_or_scope):
  affected = engine.affected_set(
    target_or_scope,
    include=["stale", "drifted", "dangling", "obsolete"]
  )

  if affected.empty:
    user.show("Nothing to reconcile in scope.")
    return

  while not affected.empty:
    case = engine.pick_next_case(affected)         # ranked by severity, then by upstream depth

    packet = engine.build_reconciliation_packet(case)
    # packet contains: case_id, drift_kind, evidence (file refs, hashes),
    #                  upstream basis, downstream items, direction options,
    #                  recommended direction with rationale, user_notes field.

    decision = user.show(packet)                   # may add notes; choose direction; or skip/exit

    if decision.action == "skip":
      affected.mark_skipped(case)
      continue
    if decision.action == "exit":
      traces.write("decision", topic="reconcile-session-end", payload=session_summary)
      return

    direction = decision.direction

    if direction == "preserve_contract":
      # regenerate downstream from approved upstream basis; bounded to this case's scope
      sub_plan = engine.dispatch_plan(case.downstream_scope)
      execute_plan(sub_plan)                       # runs generate semantics for affected scope only

    elif direction == "amend_contract":
      # open the upstream target for human edit + review + approve
      review(case.upstream_target)                 # interactive
      approve(case.upstream_target)                # writes approval trace
      # downstream regeneration follows in the next reconcile loop iteration as it becomes stale

    elif direction == "preserve_downstream_behavior":
      # amend contract to capture what the code already does; needs user judgment on which item
      proposal = subagent.propose_contract_amendment(case)
      review(proposal.target_artifact)             # user reviews proposed amendment
      approve(proposal.target_artifact)

    elif direction == "user_defined":
      # apply a user-specified fix bounded to this case
      subagent.apply_user_directed_fix(case, decision.spec)

    # always re-eval after applying a direction
    findings = eval(case.scope)
    traces.write("decision", topic="reconcile-case", payload={
      "case_id": case.id, "direction": direction,
      "findings_after": findings.summary
    })

    # recompute remaining affected set; the chosen direction may have closed multiple cases
    affected = engine.affected_set(
      target_or_scope,
      include=["stale", "drifted", "dangling", "obsolete"]
    )

  user.show("Reconciliation complete.")
```

### 15.5 `approve`

```pseudo
approve(approval_unit):
  findings = engine.structural_eval(approval_unit)
  blocking = [f for f in findings if f.severity == "blocking"]
  if blocking:
    raise ApprovalBlocked(blocking)
  trace = build_approval_trace(approval_unit, items_with_hashes(approval_unit))
  traces.write("approvals", trace)
  engine.set_lifecycle(approval_unit, APPROVED)
  status.recompute()
```

### 15.6 `status`

```pseudo
status():
  if cache.fresh:
    return cache.status
  graph = engine.parse_or_load(artifacts)
  traces_index = engine.read(traces)
  per_item_state = {}
  for item in graph.items:
    per_item_state[item.id] = classify(item, graph, traces_index)
    # current / stale / uncovered / dangling / drifted / obsolete
  report = compose_report(per_item_state, graph, current_mode)
  report.next = recommend_next(report)
  cache.write(report)
  return report
```

### 15.7 `init`

```pseudo
init(mode, intent_seed=None):
  scaffold_layout_for(mode)             # see §2.1 / §2.2
  if mode == "vibe":
    create("intent.md", "system.md", "AGENTS.md", "CLAUDE.md")
  else:
    create_full_layout(mode)            # ux mode adds ux.md + ux-specs/mockups/
  registry.initialize(.vibeloom/traces/id-registry.json)
  traces.write("decision", topic="init", payload={"mode": mode})
  if intent_seed:
    write("intent.md", intent_seed)     # one-line description from CLI, if provided
```

### 15.8 `import`

Brownfield import is the most evidence-heavy operation. Subagents propose; the engine ranks; the user reviews top-down.

```pseudo
import(mode, root_path):
  # 1. Scan and aggregate evidence from the existing repo
  evidence = engine.scan_codebase(root_path)
  # evidence contains: file inventory, language detection, test detection,
  #                    framework detection, possible UI surfaces (Figma exports,
  #                    storybook configs, design tokens), entry points, deps.

  # 2. Plan the inference work: one task per kind, dispatched in waves
  inference_plan = engine.import_dispatch_plan(evidence, mode)
  # mode shapes the inference: ux mode prioritizes UX evidence; dev mode
  # prioritizes architectural evidence; pm mode prioritizes user-facing surfaces.

  # 3. Run inference subagents wave by wave
  candidates_by_kind = {}
  for wave in inference_plan.waves:
    tasks = []
    for scope in wave.scopes:
      header = build_subagent_header(scope, wave, run, inference_plan)
      tasks.append(subagent.spawn(header))   # e.g. infer-capabilities, infer-fr, infer-bc, infer-cmp
    results = await all(tasks)
    for r in results:
      candidates_by_kind[r.kind] = r.candidates

  # 4. Score confidence per-candidate (rule-based + cross-evidence corroboration)
  for kind, candidates in candidates_by_kind.items():
    for c in candidates:
      c.confidence = compute_confidence(c, evidence)
      c.evidence_refs = link_evidence(c, evidence)
      c.uncertainty = collect_uncertainty(c, evidence)
      c.lifecycle = DRAFT

  # 5. Write drafts in tier order so review can proceed top-down
  write_drafts("intent-specs", candidates_by_kind["CAP"], candidates_by_kind["CST"])
  write_drafts("product-specs", candidates_by_kind["FR"], candidates_by_kind["NFR"], ...)
  if mode == "ux":
    write_drafts("ux-specs", candidates_by_kind.get("VIEW", []), candidates_by_kind.get("MOCK", []))
  write_drafts("system-specs", candidates_by_kind["CONT"], candidates_by_kind["CMP"], ...)

  # 6. Emit a single import trace summarizing the evidence and candidate distribution
  traces.write("import", {
    "evidence_summary": evidence.summary(),
    "candidates_proposed": {k: len(v) for k, v in candidates_by_kind.items()},
    "confidence_distribution": confidence_histogram(candidates_by_kind),
    "mode": mode
  })

  user.show("Import complete. Run `review intent-specs` to begin top-down approval.")
```

---

## 16. Brownfield import

Import analysis must attach evidence and confidence to inferred items.

```yaml
id: FR-0027
kind: functional_requirement
description: "User can export invoices as CSV."
confidence: 0.74
evidence:
  - file: billing/routes/export.ts
  - test: billing/tests/export_csv.test.ts
uncertainty:
  - "No UI flow found."
```

Imported contract remains `draft` until reviewed and approved.

---

## 17. UX and mockup ingestion

Mockups are input evidence. They may seed product and UX generation.

A `MOCK-####` record:

```yaml
id: MOCK-0011
source: figma://...
snapshot: ux-specs/mockups/checkout-empty.png
evidence_for: [VIEW-0012, INT-0041, STORY-0031]
notes: "Shows empty-cart state, disabled checkout CTA, and sign-in prompt."
```

Generated obligations must become IDed items (`VIEW`, `INT`, `UXC`, `STORY`, `ACC`) before they become contract truth. The mockup itself stays as evidence; it does not become normative.

---

## 18. Acceptance checklist for v03 implementation

- [ ] `.vibeloom/cache/` and `.vibeloom/traces/` are separated.
- [ ] Approval baseline is trace-backed (JSONL append-only), not snapshot-backed.
- [ ] ID registry persists retired IDs and next counters.
- [ ] Trace families (§8.1–§8.6) have schemas with `schema_version` field.
- [ ] Code-sync traces connect contract IDs to file hashes and validation evidence.
- [ ] Review and reconciliation packets exist with user-notes write capability.
- [ ] Task templates use markdown structure (Inputs / Steps / Output / Constraints / Validation), not YAML wrappers.
- [ ] Subagent writes are patch-staged in `.vibeloom/runs/`, validated, then applied atomically.
- [ ] Dispatch plan structure, wave-assembly rules, and parallel semantics match §13.1–§13.3.
- [ ] Subagent task header schema (§13.4) is the only orchestrator-to-subagent contract.
- [ ] Validation registry (`validation-registry.md`) is parsed and runners are invokable.
- [ ] Product/UX peer generation supports mockup evidence with `MOCK-####` records.
- [ ] `ux` mode supported as a fifth top-level mode (designer-led, PM peer reviewer).
- [ ] Verification ladder (decidable / mechanical / heuristic) reflected in eval routing.
- [ ] Component / container / bounded-context rules match methodology §6.5.
- [ ] `status` distinguishes `current`, `stale`, `uncovered`, `dangling`, `drifted`, and `obsolete`.
- [ ] Each operation has explicit, traceable execution semantics (§15.1–§15.8).
- [ ] Vibe layout is genuinely minimal (no graph cache, no code-sync trace) — not a stripped full mode.
- [ ] Templates exist only as fenced blocks in `vibeloom-templates.md`; the on-disk template tree (`templates/`, gitignored) is a build artifact materialized on demand by `extract-templates.py`. CI runs `--check` to confirm round-trip parses.

---

## 19. Templates

Every template, skill reference, and skill manifest is specified canonically in [`vibeloom-templates.md`](vibeloom-templates.md). **Templates do not exist as source files.** The on-disk template tree is a build artifact, materialized on demand by [`extract-templates.py`](extract-templates.py) into `templates/` (gitignored). The repo's source tree contains only the canonical markdown source plus the extractor.

### 19.1 Build-time workflow

```
edit vibeloom-templates.md          ← only canonical source
       │
       ▼
python3 extract-templates.py        ← materializes templates/ on demand
       │
       ▼
templates/  (gitignored)            ← consumed by the skill at runtime;
                                      regenerable, never committed
```

There is no on-disk template tree to keep in sync. All template edits go directly into `vibeloom-templates.md`. Skill bundling at release time (or any local development pass that needs the materialized tree) runs the extractor.

CI runs `python3 extract-templates.py --check` against a freshly extracted tree to confirm that the source is parseable and round-trip-clean. There is no "drift" to detect at the spec level — the canonical source is a single file by construction.

### 19.2 Extractor protocol

A template block opens with **four** backticks immediately followed by `template:<relative-path>` and closes with a line of exactly four backticks. Four (not three) so that ordinary 3-backtick fences inside the body — `​`​`​`yaml`, `​`​`​`text`, etc. — do not prematurely close the outer block.

````markdown
````template:tasks/init.md
# Initialize

```yaml
inputs: ...
```
````
````

The extractor writes everything between the opener and closer, verbatim, to `<dest>/<relative-path>` (default `templates/<relative-path>`). Idempotent. `--check` mode diffs and exits non-zero on drift.

### 19.3 Inventory and contracts

`vibeloom-templates.md` defines 41 templates in five families. Each family has a contract: a set of structural rules every template in that family must satisfy. Templates may add prose, examples, and craft beyond the contract; they may not omit what the contract requires.

| Family | Path prefix (in extracted tree) | Count | Contract (every template in this family must…) |
| --- | --- | --- | --- |
| Skill manifest | `skill/SKILL.md` | 1 | YAML frontmatter with `name: vibeloom`, `description`, `argument-hint`. Body lists when-to-use, authoritative sources, runtime references, templates, command routing, guardrails. |
| Subagent prompt | `skill/subagent-prompt.md` | 1 | Body shape that wraps the canonical subagent task header (§13.4) into a working prompt; includes load-set, allowed-paths, validation-contract sections. |
| Skill references | `skill/references/*.md` | 6 | Load-on-demand condensations of methodology + implementation. Each is self-contained for its operation; canonical-source pointer in the header. Files: `operations.md`, `modes.md`, `runtime.md`, `artifacts.md`, `eval.md`, `troubleshooting.md`. |
| Task templates | `tasks/*.md` | 14 | Canonical Design-by-Contract structure (10 sections): `## Purpose`, `## Inputs`, `## Preconditions`, `## Steps` (numbered), `## Output` (named result shape with required fields), `## Postconditions`, `## Constraints`, `## Invariants`, `## Validation`, `## Failure modes`. See §12.1. Trailer carries `task-template-version`. |
| Artifact templates | `artifacts/**/*.md` | 18 | YAML frontmatter (`artifact_type`, `tier`, `scope_kind`, `scope_id`, `derives_from`, plus contract-artifact-only `status` and `approval_unit`). Body uses the prefix families defined in §5.1. Tables for IDed items use canonical column conventions (see the `skill/references/artifacts.md` template). |
| Project-level meta | `artifacts/validation-registry.md`, plus README | 2 | Validation registry per §7. README documents the directory layout. |

When adding a new template:
1. Add the body inside a fenced block in `vibeloom-templates.md` (with a TOC entry up top).
2. Run `python3 extract-templates.py` to verify the source parses and the new file extracts cleanly.
3. Verify the new template satisfies its family contract above.
4. Update §19.3's count.

When changing a template's family contract, the structural change should be reflected in the relevant implementation section first (§5, §6, §7, §12, etc.); the template body in `vibeloom-templates.md` is then updated to match.

---

## 20. See also

- [`vibeloom-methodology.md`](vibeloom-methodology.md) — what VibeLoom is
- [`vibeloom-templates.md`](vibeloom-templates.md) — canonical source for every template (extracted to `templates/` on demand via `extract-templates.py`; never committed)
- [`codæ-manifesto.html`](codæ-manifesto.html) — the case for contract-driven agentic engineering
- [`vibeloom-comparison.html`](vibeloom-comparison.html) — VibeLoom vs Kiro, Spec Kit, BMAD
- [`getting-started.md`](getting-started.md) — 30-minute on-ramp for new users
- [`roadmap.md`](roadmap.md) — features and capabilities considered for v04+
- [`examples/`](examples/) — worked examples (greenfield, brownfield, ux-led, multi-component reconciliation, parallel dispatch)
