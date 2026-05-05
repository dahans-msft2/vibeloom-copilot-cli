---
name: vibeloom
description: Contract-driven agentic engineering for long-lived AI-coded projects. Use when the user wants to bootstrap, import, generate, eval, review, reconcile, or approve artifacts in a project governed by VibeLoom (modes: vibe, pm, dev, ux, expert).
argument-hint: "[init|import|generate|eval|review|reconcile|approve|status] [target]"
---

# VibeLoom

VibeLoom is the reference instantiation of the **codæ** paradigm (contract-driven agentic engineering). It governs long-lived AI-coded projects through a tiered contract: `intent-specs` → `product-specs` ⇄ `ux-specs` → `system-specs` → `context` → `code`. Each tier derives from approved upstream truth; downstream is regenerated, never approved as its own layer. The user retains approval authority at mode-specific gates; subagents do scoped work in parallel waves.

## When to use this skill

Invoke on any `$vibeloom` or `/vibeloom` command, or when the user mentions VibeLoom, codæ, contract-driven engineering, or asks to run any methodology operation: `init`, `import`, `generate`, `eval`, `review`, `reconcile`, `approve`, `status`.

## Authoritative sources

Always consult these before making decisions:

- **[vibeloom-methodology.md](../../vibeloom-methodology.md)** — WHAT and WHY (entities, tiers, modes, operations, approval model, derivation DAG, status taxonomy, verification ladder, decision-trace classification). If this skill file conflicts with the methodology, the methodology wins.
- **[vibeloom-implementation.md](../../vibeloom-implementation.md)** — HOW (cache vs traces split, artifact layout, frontmatter shape, ID schema, runtime loop, dispatch plan + wave assembly + subagent task header schema, trace schemas, layer-aware constraints).

## Runtime references (load on demand)

- **[references/operations.md](references/operations.md)** — per-operation quick reference (purpose, parameters, preconditions, postconditions).
- **[references/modes.md](references/modes.md)** — per-mode behavior (`vibe`, `pm`, `dev`, `ux`, `expert`): tier ownership, auto-advance, public surface.
- **[references/runtime.md](references/runtime.md)** — dispatch mechanics: dispatch plan, wave assembly, parallel semantics, subagent task header, load sets, late-fetch.
- **[references/artifacts.md](references/artifacts.md)** — artifact layout, frontmatter shapes, ID schema, derivation rules, layer-aware constraints.
- **[references/eval.md](references/eval.md)** — verification ladder (decidable / mechanical / heuristic), heuristic dimensions, finding schema, severity classification.
- **[references/troubleshooting.md](references/troubleshooting.md)** — failure modes and recovery (cache corruption, lifecycle drift, breaking changes, partial wave failure, late-fetch overflow).

## Templates

### Artifact templates (under [`../artifacts/`](../artifacts/))

- `intent-specs/`: `intent.md`, `vibe-intent.md`, `defaults.md` (with Tech Stack section per layer)
- `product-specs/`: `prd.md`, `usm.md`, `dm.md`
- `ux-specs/`: `ux.md` (peer to product-specs; mockup-evidence pattern)
- `system-specs/`: `system.md`, `vibe-system.md`, `containers.md`, `container.md` (with `layer` field + per-layer deployment guidance), `component.md` (layer-aware bounded_context constraint)
- `context/`: `bdd.md`, `decision-trace.md` (single template parameterized by record_type — replaces v02's separate adr/pdr), `root-config.md`, `container-config.md`, `component-config.md`
- `validation-registry.md` (project-level meta artifact)

Load one artifact template at a time for the artifact being generated.

### Task templates (under [`../tasks/`](../tasks/))

One task template per operation, following Inputs / Preconditions / Steps / Output / Constraints / Validation / Failure modes structure:

- `init.md`, `import.md`
- `generate-intent-specs.md`, `generate-product-specs.md`, `generate-product-specs-from-ux.md`, `generate-ux-specs.md`, `generate-system-specs.md`, `generate-context.md`, `generate-code-component.md`
- `eval.md`, `review.md`, `reconcile.md`, `approve.md`, `status.md`

Load the task template for the operation being invoked.

### Subagent prompt template

[`subagent-prompt.md`](subagent-prompt.md) — the body shape that wraps the canonical subagent task header (per implementation §13.4) into a working prompt. Used by the orchestrator when dispatching subagents within a wave.

## Engine

The engine is a deterministic Python package at the repo root (`engine/`). **Zero install, zero dependencies** beyond Python 3.10+. Invoke via `python -m`:

```bash
PYTHONPATH=<skill-root>/engine python3 -m vibeloom_engine <command> --repo <target-repo>
```

Available commands:

| Engine command | Purpose |
|---|---|
| `parse --repo <path>` | Parse all artifacts; emit JSON inventory |
| `graph --repo <path>` | Build + persist `.vibeloom/cache/contract-graph.json` |
| `eval --repo <path> [--target <tier>]` | Run structural checks; non-zero exit on blockers |
| `affected --repo <path> --ids <IDs...>` | Compute affected set from changed item IDs |
| `staleness --repo <path>` | Per-item hash diff vs approval traces; forward DAG walk |
| `detect-edits --repo <path>` | mtime fast-filter + per-item hash confirmation |
| `dispatch --repo <path> --affected <IDs>` | Build dispatch plan with wave assembly |
| `status --repo <path>` | Emit + persist status across all axes |

All engine commands emit JSON on stdout. The engine makes NO semantic judgments — it parses, validates structure, computes the graph, plans dispatch, and reports. Semantic judgment and user interaction remain with the skill.

> Optional: `pip install -e engine` puts a shorter `vibeloom-engine` command on `PATH`. Not required.

## Substrate

The cooperating substrate at `.vibeloom/` is split:

- **`.vibeloom/cache/`** — regenerable state (contract graph, status). Safe to delete; engine rebuilds.
- **`.vibeloom/traces/`** — durable provenance (append-only JSONL). Never silently regenerated; missing traces require explicit re-baselining.

Trace families: `approval`, `generation`, `eval`, `code-sync`, `decision`, `import`, plus the `id-registry.json` structured exception. See implementation §8 for schemas.

Decision traces classify by `record_type`: `IDR` (intent-specs), `PDR` (product-specs), `UDR` (ux-specs), `ADR` (system-specs), or `general` (process / methodology / operational decisions that don't change the contract). The active load-bearing subset is a queried view, not a duplicated folder.

## Command routing

On any operation invocation, load `references/operations.md` first for parameters and preconditions; then load the relevant subset of references and the task template:

| Operation | First load | Then |
|---|---|---|
| `init`, `import` | `operations.md`, `modes.md` | `tasks/init.md` or `tasks/import.md` + initial templates |
| `generate <target>` | `operations.md`, `runtime.md` | `tasks/generate-<target>.md` + target-tier templates + graph cache |
| `eval <target>`, `review <target>` | `operations.md`, `runtime.md`, `eval.md` | `tasks/eval.md` or `tasks/review.md` + target artifacts |
| `reconcile <target>` | `operations.md`, `runtime.md`, `eval.md` | `tasks/reconcile.md` + downstream artifacts + graph + traces |
| `approve <target>` | `operations.md`, `modes.md`, `eval.md` | `tasks/approve.md` + target artifacts |
| `status` | `artifacts.md` | `tasks/status.md` + graph cache |

## Getting started

If the repo has no VibeLoom governance yet, start with:

- `init --mode <vibe|pm|dev|ux|expert>` (new project), or
- `import --mode <mode>` (existing codebase).

Consult `references/modes.md` to help the user pick a mode. Default recommendation: start in `vibe` for prototypes; one-way upgrade to `pm` / `dev` / `ux` / `expert` when the project earns the ceremony.

## Guardrails

- **Approval gates**: never bypass. When a contract tier is a user stop in the current mode, halt and surface findings.
- **Methodology authoritative**: if this skill file disagrees with the methodology, follow the methodology and flag the drift.
- **No invented schema**: don't introduce entity types, ID prefixes, or derivation edges. The valid set is in the methodology's DAG.
- **Layer-aware**: containers carry a `layer` field (presentation / application / domain / infrastructure). Bounded contexts ONLY in domain-layer containers. Tech stack inherited from `defaults.md` per layer.
- **Decisions live in traces**: ADRs / PDRs / UDRs / IDRs are decision-trace entries with `record_type`. There is no `context/decisions/` folder. Active "decision context" is a queried view over traces filtered by `load_bearing: true`.
- **Subagent load sets**: scoped only — never load the skill, methodology, or implementation docs into a subagent's context. Subagents see baseline + owned scope + foreign IF slices + relevant context.
- **Late-fetch bounded**: one re-invocation per task; exceeding the cap surfaces a finding and exits the task.
- **`reconcile` is user-initiated**: never auto-invoke.
- **`approve` requires structural eval clean + zero blocking semantic findings**.
- **Auto-advance is bounded**: in delegated modes, a tier auto-advances only when structural eval passes AND no breaking semantic change is detected.
- **Decision provenance**: any subagent decision that constrains future generation MUST emit a decision trace with `record_type` and `affects: [item_ids]`.

## Response shape

Keep responses tight. For operations that pause for user input, use this structure:

1. **Scope** — what tier/scope this operation touched.
2. **Decision** — what the skill did or is asking the user to decide.
3. **Affected** — item IDs, artifacts, and scopes changed or surfaced.
4. **Next** — the suggested next command.
