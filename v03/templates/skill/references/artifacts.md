# Artifacts Reference

Artifact layout, frontmatter shapes, ID schema, and derivation rules. Authoritative semantics live in [`vibeloom-implementation.md`](../../../vibeloom-implementation.md). This file is a load-on-demand condensation.

---

## Governed repo layout

### Full layout (`pm`, `dev`, `ux`, `expert`)

```
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
  decisions/
    idr/   IDR-NNNN-<slug>.md
    pdr/   PDR-NNNN-<slug>.md
    udr/   UDR-NNNN-<slug>.md
    adr/   ADR-NNNN-<slug>.md
    general/   DEC-NNNN-<slug>.md
  <container>/
    container.md          # carries layer field
    AGENTS.md
    CLAUDE.md
    <component>/
      component.md
      AGENTS.md
      CLAUDE.md
      context/
        bdd/
          BDD-####-<behavior-slug>.md
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

### Compact layout (`vibe`)

```
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

No cache, no graph, no code-sync. Approval traces remain (cheap; enable future upgrade migration).

Filesystem is a navigation aid and consistency check, not the semantic source of truth.

---

## Artifact mapping (full modes)

| Artifact | Output path | Template | Scope |
|---|---|---|---|
| `intent` | `/intent.md` | `templates/artifacts/intent-specs/intent.md` | root |
| `defaults` | `/defaults.md` | `templates/artifacts/intent-specs/defaults.md` | root |
| `prd` | `/prd.md` | `templates/artifacts/product-specs/prd.md` | root |
| `usm` | `/usm.md` | `templates/artifacts/product-specs/usm.md` | root |
| `dm` | `/dm.md` | `templates/artifacts/product-specs/dm.md` | root |
| `ux` | `/ux.md` | `templates/artifacts/ux-specs/ux.md` | root |
| `system` | `/system.md` | `templates/artifacts/system-specs/system.md` | root |
| `containers` | `/containers.md` | `templates/artifacts/system-specs/containers.md` | root |
| `container` | `/<container>/container.md` | `templates/artifacts/system-specs/container.md` | container |
| `component` | `/<container>/<component>/component.md` | `templates/artifacts/system-specs/component.md` | component |
| `validation-registry` | `/validation-registry.md` | `templates/artifacts/validation-registry.md` | root |
| root `config` | `/AGENTS.md`, `/CLAUDE.md` | `templates/artifacts/context/root-config.md` | root |
| container `config` | `/<container>/AGENTS.md`, `/<container>/CLAUDE.md` | `templates/artifacts/context/container-config.md` | container |
| component `config` | `/<container>/<component>/AGENTS.md`, `/<container>/<component>/CLAUDE.md` | `templates/artifacts/context/component-config.md` | component |
| `decision-trace` (per record) | `/decisions/<record_type>/<RECORD>-NNNN-<slug>.md` | `templates/artifacts/context/decision-trace.md` | root (one file per decision) |
| `bdd` | `/<container>/<component>/context/bdd/BDD-####-<slug>.md` | `templates/artifacts/context/bdd.md` | component |

### Compact mapping (vibe)

| Artifact | Output path | Template | Scope |
|---|---|---|---|
| `intent` | `/intent.md` | `templates/artifacts/intent-specs/vibe-intent.md` | root |
| `defaults` | `/defaults.md` | `templates/artifacts/intent-specs/defaults.md` | root |
| `system` | `/system.md` | `templates/artifacts/system-specs/vibe-system.md` | root |
| root `config` | `/AGENTS.md`, `/CLAUDE.md` | `templates/artifacts/context/root-config.md` | root |

---

## Contract artifact frontmatter

Every contract artifact includes:

| Field | Type | Notes |
|---|---|---|
| `artifact_id` | string | Stable artifact identifier |
| `artifact_type` | enum | `intent` \| `defaults` \| `prd` \| `usm` \| `dm` \| `ux` \| `system` \| `containers` \| `container` \| `component` |
| `tier` | enum | `intent-specs` \| `product-specs` \| `ux-specs` \| `system-specs` |
| `scope_kind` | enum | `root` \| `container` \| `component` |
| `scope_id` | string | `root` or the governing scope slug |
| `status` | enum | `draft` \| `approved` |
| `timestamp` | string | ISO 8601 of the last change |
| `approval_mode` | enum | `user` \| `delegated`. Set at approval time only; absent on drafts. |
| `derives_from` | string[] | Upstream short item IDs that materially constrain this artifact |

Additional required fields:

- **`container.md`**: `container_id` (CONT-####), **`layer` (presentation \| application \| domain \| infrastructure)** — required, drives layer-aware constraints.
- **`component.md`**: `container_id`, `component_id` (CMP-####), `bounded_context` (BC-#### — required for domain-layer components, empty/null for others), `owned_paths`, `owned_interfaces`.

`owned_interfaces` and `owned_paths` in frontmatter are **summary indexes**; the body's `IF-####` table and explicit path declarations are the source of truth. Frontmatter is regenerated from body carriers.

---

## Context artifact frontmatter

Every context artifact includes:

| Field | Type | Notes |
|---|---|---|
| `artifact_id` | string | Stable artifact identifier |
| `artifact_type` | enum | `config` \| `bdd` |
| `tier` | enum | Always `context` |
| `scope_kind` | enum | `root` \| `container` \| `component` |
| `scope_id` | string | `root` or the governing scope slug |
| `timestamp` | string | ISO 8601 of the last change |
| `derives_from` | string[] | Upstream short item IDs that constrain this artifact |

Extras:

- **`config`** artifacts: `assistant` (e.g., `claude`, `codex`)

Context artifacts do **not** carry `status` or `approval_mode`.

---

## Decision-trace frontmatter

Decision traces are persisted in the append-only stream at `.vibeloom/traces/decisions.jsonl`. Per-record markdown files in `decisions/<record_type>/` are the human-readable rendering. Frontmatter shape:

| Field | Type | Notes |
|---|---|---|
| `trace_id` | string | `<RECORD>-<YYYYMMDD>-<NNNN>` (e.g. `ADR-20260512-0007`) |
| `kind` | string | Always `decision` |
| `record_type` | enum | `IDR` \| `PDR` \| `UDR` \| `ADR` \| `general` (default `general`) |
| `load_bearing` | bool | Whether decision still informs future generation. Default `false`. |
| `affects` | string[] | Contract item IDs constrained by this decision (recommended). Empty for `general`. |
| `topic` | string | Short slug or title |
| `author` | string | email or handle |
| `timestamp` | string | ISO 8601 |

---

## Stable ID schema

Visible item IDs use short typed references: `PREFIX-####` (fixed-width 4-digit). Globally unique by type across the repo, append-only within each family, deleted IDs never reused.

### Prefix families

| Family | Meaning |
|---|---|
| `CAP-####` | intent capability |
| `CST-####` | hard constraint in defaults or intent |
| `DEF-####` | repo-wide default (Tech Stack entries also use this) |
| `OBJ-####` | objective |
| `KR-####` | key result |
| `MET-####` | metric |
| `FR-####` | functional requirement |
| `NFR-####` | non-functional requirement |
| `EPIC-####` | epic |
| `FLOW-####` | workflow or journey |
| `STORY-####` | story |
| `ACC-####` | acceptance criterion |
| `MS-####` | milestone |
| `TERM-####` | ubiquitous-language term |
| `BC-####` | bounded context |
| `AGG-####` | aggregate |
| `ENT-####` | entity |
| `VO-####` | value object |
| `INV-####` | invariant |
| `VIEW-####` | UX view |
| `INT-####` | UX interaction |
| `UXC-####` | UX constraint |
| `MOCK-####` | mockup reference |
| `EXT-####` | external actor/system |
| `TB-####` | trust boundary |
| `SNFR-####` | system-wide NFR boundary |
| `CONT-####` | container inventory item |
| `CMP-####` | component inventory item |
| `IF-####` | owned interface (body carrier) |
| `DEP-####` | component dependency (body carrier) |
| `BEH-####` | local technical behavior (body carrier) |
| `NOTE-####` | local test/runtime note (body carrier) |
| `BDD-####` | behavioral-scenario artifact |
| `SCN-####` | individual Gherkin scenario |
| `RUN-`, `TASK-`, `PLAN-` | run, task, dispatch plan IDs |
| `APPROVAL-`, `SYNC-`, `GEN-`, `EVAL-`, `DEC-`, `IMP-` | trace IDs |

`IF-####`, `DEP-####`, `BEH-####`, `NOTE-####` are structured content within component/container specs — not independent graph nodes.

`ADR`, `PDR`, `UDR`, `IDR` are NOT separate ID families in v0.3 — they are `record_type` values on the unified decision-trace ID family (`DEC-`).

### Artifact IDs

| Artifact | ID shape |
|---|---|
| root contract | fixed name: `intent`, `defaults`, `prd`, `usm`, `dm`, `ux`, `system`, `containers` |
| `container.md` | `container.<container-slug>` |
| `component.md` | `component.<container-slug>.<component-slug>` |
| root config | `config.root.<assistant-slug>` (e.g., `config.root.claude`) |
| container config | `config.container.<container-slug>.<assistant-slug>` |
| component config | `config.component.<container-slug>.<component-slug>.<assistant-slug>` |
| validation-registry | `validation-registry` |
| `bdd` | `BDD-####` |
| decision trace | `<RECORD>-<YYYYMMDD>-<NNNN>` (e.g. `ADR-20260512-0007`) |

---

## Layer-aware constraints

Containers carry a required `layer` field. The layer drives:

- **Bounded contexts**: ONLY allowed in `domain`-layer containers.
- **Components**: presentation/application/infrastructure components have empty `bounded_context`; domain components have a required `bounded_context`.
- **Tech stack inheritance**: each container inherits the matching layer's section from `defaults.md` Tech Stack.
- **Deployment target**: each container's deployment pattern is layer-typical (presentation → static bundle on Cloudflare/Vercel/etc.; application → BFF on Lambda/Cloud Run/Workers; domain → service workload on ECS/Cloud Run/EKS; infrastructure → IaC declarations).

---

## Derivation rules

- The canonical relation is `derives_from`.
- Every non-root entity must derive from one or more upstream entities allowed by the methodology's Derivation DAG.
- Visible `derives_from` references use short item IDs only.
- Artifact frontmatter records the smallest useful constraining set of upstream item IDs.
- Item-level derivation lives in body carriers per the template.
- `capability` and `constraint` are the only root entity types.
- `default` (DEF) becomes universally binding once derived; it may be referenced by any downstream entity without requiring an additional typed edge.

See [`vibeloom-methodology.md`](../../../vibeloom-methodology.md) §8 for the full edge table.

---

## Ownership mapping (scope)

- **Repo-scoped:** `intent`, `defaults`, `prd`, `usm`, `dm`, `ux`, `system`, `containers`, `validation-registry`, decision-trace records (per record_type sub-folder)
- **Container-scoped:** `container`, container-level `config`
- **Component-scoped:** `component`, component-level `config`, `bdd`

Scope is the governance boundary: **repo** (global), **container** (one runtime unit), or **component** (one technical boundary).

---

## Table column conventions

Canonical column names across templates:

| Column | Meaning | Used in |
|---|---|---|
| `id` | short typed item ID | all tables with addressable items |
| `derives_from` | upstream short item IDs | all contract tiers, decision trace, bdd |
| `description` | what the item is or does | intent, prd, usm, dm, ux, system, containers, container, component |
| `notes` | additional context or rationale | any table |
| `priority` | relative importance | prd (FR, scope) |
| `measure` / `target` | NFR/SNFR quantitative spec | prd (NFR), system (SNFR) |

Domain-specific columns (e.g., `kind`, `runtime`, `rule`, `mockup_refs`) are template-local.
