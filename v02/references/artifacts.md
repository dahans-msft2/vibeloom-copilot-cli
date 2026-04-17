# Artifacts Reference

Artifact layout, frontmatter shapes, ID schema, and derivation rules. Authoritative semantics live in [`vibeloom-implementation.md`](../vibeloom-implementation.md). This file is a load-on-demand condensation.

---

## Governed repo layout

### Full layout (`pm`, `dev`, `expert`)

```
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
          BDD-####-<behavior-slug>.md
  .vibeloom/
    state/
      context-graph.json
      status.json
```

### Compact layout (`vibe`)

```
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

Filesystem is a navigation aid and consistency check, not the semantic source of truth.

---

## Artifact mapping (full modes)

| Artifact | Output path | Template | Scope |
|---|---|---|---|
| `intent` | `/intent.md` | `assets/intent-specs/intent.md` | root |
| `defaults` | `/defaults.md` | `assets/intent-specs/defaults.md` | root |
| `prd` | `/prd.md` | `assets/product-specs/prd.md` | root |
| `usm` | `/usm.md` | `assets/product-specs/usm.md` | root |
| `dm` | `/dm.md` | `assets/product-specs/dm.md` | root |
| `system` | `/system.md` | `assets/system-specs/system.md` | root |
| `containers` | `/containers.md` | `assets/system-specs/containers.md` | root |
| `container` | `/<container>/container.md` | `assets/system-specs/container.md` | container |
| `component` | `/<container>/<component>/component.md` | `assets/system-specs/component.md` | component |
| root `config` | `/AGENTS.md`, `/CLAUDE.md` | `assets/context/root-config.md` | root |
| container `config` | `/<container>/AGENTS.md`, `/<container>/CLAUDE.md` | `assets/context/container-config.md` | container |
| component `config` | `/<container>/<component>/AGENTS.md`, `/<container>/<component>/CLAUDE.md` | `assets/context/component-config.md` | component |
| `pdr` | `/context/pdr.md` | `assets/context/pdr.md` | root |
| `adr` | `/context/adr.md` | `assets/context/adr.md` | root |
| `bdd` | `/<container>/<component>/context/bdd/BDD-####-<slug>.md` | `assets/context/bdd.md` | component |

### Compact mapping (vibe)

| Artifact | Output path | Template | Scope |
|---|---|---|---|
| `intent` | `/intent.md` | `assets/intent-specs/vibe-intent.md` | root |
| `defaults` | `/defaults.md` | `assets/intent-specs/defaults.md` | root |
| `system` | `/system.md` | `assets/system-specs/vibe-system.md` | root |
| root `config` | `/AGENTS.md`, `/CLAUDE.md` | `assets/context/root-config.md` | root |

---

## Contract artifact frontmatter

Every contract artifact includes:

| Field | Type | Notes |
|---|---|---|
| `artifact_id` | string | Stable artifact identifier |
| `artifact_type` | enum | `intent` \| `defaults` \| `prd` \| `usm` \| `dm` \| `system` \| `containers` \| `container` \| `component` |
| `tier` | enum | `intent-specs` \| `product-specs` \| `system-specs` |
| `scope_kind` | enum | `root` \| `container` \| `component` |
| `scope_id` | string | `root` or the governing scope slug |
| `status` | enum | `draft` \| `approved` |
| `timestamp` | string | ISO 8601 of the last change |
| `approval_mode` | enum | `user` \| `delegated`. Set at approval time only; absent on drafts. |
| `derives_from` | string[] | Upstream short item IDs that materially constrain this artifact |

Additional required fields:

- **`container.md`**: `container_id` (CONT-####)
- **`component.md`**: `container_id`, `component_id` (CMP-####), `bounded_context` (BC-####), `owned_paths`, `owned_interfaces`

`owned_interfaces` and `owned_paths` in frontmatter are **summary indexes**; the body's `IF-####` table and explicit path declarations are the source of truth. Frontmatter is regenerated from body carriers.

---

## Context artifact frontmatter

Every context artifact includes:

| Field | Type | Notes |
|---|---|---|
| `artifact_id` | string | Stable artifact identifier |
| `artifact_type` | enum | `config` \| `pdr` \| `adr` \| `bdd` |
| `tier` | enum | Always `context` |
| `scope_kind` | enum | `root` \| `container` \| `component` |
| `scope_id` | string | `root` or the governing scope slug |
| `timestamp` | string | ISO 8601 of the last change |
| `derives_from` | string[] | Upstream short item IDs that constrain this artifact |

Extras:

- **`config`** artifacts: `assistant` (e.g., `claude`, `codex`)

Context artifacts do **not** carry `status` or `approval_mode`.

For ledgers (`pdr`, `adr`): artifact-level `derives_from` is always `[]`; per-record `derives_from` inside each `PDR-####`/`ADR-####` section is the canonical derivation link.

---

## Stable ID schema

Visible item IDs use short typed references: `PREFIX-0001` (fixed-width 4-digit). Globally unique by type across the repo, append-only within each family, deleted IDs never reused.

### Prefix families

| Family | Meaning |
|---|---|
| `CAP-####` | intent capability |
| `CST-####` | hard constraint in defaults or intent |
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
| `EXT-####` | external actor/system |
| `TB-####` | trust boundary |
| `SNFR-####` | system-wide NFR boundary |
| `CONT-####` | container inventory item |
| `CMP-####` | component inventory item |
| `IF-####` | owned interface (body carrier) |
| `DEP-####` | component dependency (body carrier) |
| `BEH-####` | local technical behavior (body carrier) |
| `NOTE-####` | local test/runtime note (body carrier) |
| `PDR-####` | product decision record |
| `ADR-####` | architecture decision record |
| `BDD-####` | behavioral-scenario artifact |
| `SCN-####` | individual Gherkin scenario |

`IF-####`, `DEP-####`, `BEH-####`, `NOTE-####` are structured content within component/container specs — not independent graph nodes.

### Artifact IDs

| Artifact | ID shape |
|---|---|
| root contract | fixed name: `intent`, `defaults`, `prd`, `usm`, `dm`, `system`, `containers` |
| `container.md` | `container.<container-slug>` |
| `component.md` | `component.<container-slug>.<component-slug>` |
| root config | `config.root.<assistant-slug>` (e.g., `config.root.claude`) |
| container config | `config.container.<container-slug>.<assistant-slug>` |
| component config | `config.component.<container-slug>.<component-slug>.<assistant-slug>` |
| `pdr` | `pdr` |
| `adr` | `adr` |
| `bdd` | `BDD-####` |

---

## Derivation rules

- The canonical relation is `derives_from`.
- Every non-root entity must derive from one or more upstream entities allowed by the methodology's Derivation DAG.
- Visible `derives_from` references use short item IDs only.
- Artifact frontmatter records the smallest useful constraining set of upstream item IDs.
- Item-level derivation lives in body carriers per the template.
- `capability` and `constraint` are the only root entity types.
- `default` becomes universally binding once derived; it may be referenced by any downstream entity without requiring an additional typed edge.

See [`vibeloom-methodology.md ## Context Graph ### Derivation DAG`](../vibeloom-methodology.md) for the full edge table.

---

## Ownership mapping (scope)

- **Repo-scoped:** `intent`, `defaults`, `prd`, `usm`, `dm`, `system`, `containers`, `pdr`, `adr`
- **Container-scoped:** `container`, container-level `config`
- **Component-scoped:** `component`, component-level `config`, `bdd`

Scope is the governance boundary: **repo** (global), **container** (one runtime unit), or **component** (one technical boundary).

---

## Table column conventions

Canonical column names across templates:

| Column | Meaning | Used in |
|---|---|---|
| `id` | short typed item ID | all tables with addressable items |
| `derives_from` | upstream short item IDs | all contract tiers, pdr, adr, bdd |
| `description` | what the item is or does | intent, prd, usm, dm, system, containers, container, component |
| `notes` | additional context or rationale | any table |
| `priority` | relative importance | prd (FR, scope) |
| `measure` / `target` | NFR/SNFR quantitative spec | prd (NFR), system (SNFR) |

Domain-specific columns (e.g., `kind`, `runtime`, `rule`) are template-local.
