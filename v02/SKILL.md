---
name: vibeloom
description: Contract-driven governance for long-lived AI-coded projects. Use when the user wants to bootstrap, import, generate, review, reconcile, or approve artifacts in a project governed by the VibeLoom methodology (modes: vibe, pm, dev, expert).
argument-hint: "[init|import|generate|eval|review|reconcile|approve|status] [target]"
---

# VibeLoom

VibeLoom governs long-lived AI-coded projects by generating a tiered contract of specifications (`intent-specs` → `product-specs` → `system-specs`), deriving execution context from it, and generating code from the approved stack. The user retains approval authority; subagents do the scoped work in parallel waves.

## When to use this skill

Invoke on any `$vibeloom` or `/vibeloom` command, or when the user mentions VibeLoom, contract-driven governance, or asks to run any of the methodology operations (`init`, `import`, `generate`, `eval`, `review`, `reconcile`, `approve`, `status`).

## Authoritative sources

Always consult these before making decisions:

- **[vibeloom-methodology.md](vibeloom-methodology.md)** — WHAT and WHY (entities, tiers, modes, operations, approval model, derivation DAG). If this skill file conflicts with the methodology, the methodology wins.
- **[vibeloom-implementation.md](vibeloom-implementation.md)** — HOW (artifact layout, metadata shape, ID schema, runtime loop, subagent dispatch, load sets).

## Runtime references (load on demand)

- **[references/operations.md](references/operations.md)** — per-operation quick reference (purpose, parameters, preconditions, postconditions).
- **[references/modes.md](references/modes.md)** — per-mode behavior (`vibe`, `pm`, `dev`, `expert`): tier ownership, auto-advance, public surface.
- **[references/runtime.md](references/runtime.md)** — dispatch mechanics: runtime loop, waves, load sets, late-fetch, validation.
- **[references/artifacts.md](references/artifacts.md)** — artifact layout, frontmatter shapes, ID schema, derivation rules.
- **[references/eval.md](references/eval.md)** — semantic-eval dimensions, finding schema, severity classification (what the agent checks on top of the engine's structural eval).
- **[references/troubleshooting.md](references/troubleshooting.md)** — failure modes and recovery (cache corruption, direct edits, breaking changes, partial wave failure).

## Templates

The 17 artifact templates live under [`assets/`](assets/):

- `intent-specs/`: `intent.md`, `vibe-intent.md`, `defaults.md`
- `product-specs/`: `prd.md`, `usm.md`, `dm.md`
- `system-specs/`: `system.md`, `vibe-system.md`, `containers.md`, `container.md`, `component.md`
- `context/`: `pdr.md`, `adr.md`, `bdd.md`, `root-config.md`, `container-config.md`, `component-config.md`

Load one template at a time for the artifact being generated.

## Engine

The [`engine/`](engine/) directory contains the Python package that implements the deterministic substrate described in `vibeloom-implementation.md`. **Zero install, zero dependencies** — Python 3.10+ is the only requirement. Invoke the engine via `python -m` with `PYTHONPATH` pointing at `engine/`:

```bash
PYTHONPATH=<skill-root>/engine python3 -m vibeloom_engine <command> --repo <target-repo>
```

`<skill-root>` is the directory containing this `SKILL.md`. Available commands:

| Engine command | Purpose |
|---|---|
| `python3 -m vibeloom_engine parse --repo <path>` | Parse all artifacts; emit JSON inventory |
| `python3 -m vibeloom_engine graph --repo <path>` | Build + persist `.vibeloom/state/context-graph.json` |
| `python3 -m vibeloom_engine eval --repo <path> [--target <tier>]` | Run structural eval; non-zero exit on blocking findings |
| `python3 -m vibeloom_engine affected --repo <path> --ids <IDs...>` | Compute the affected set from changed item IDs |
| `python3 -m vibeloom_engine staleness --repo <path>` | Detect stale artifacts (approved-basis mismatch) |
| `python3 -m vibeloom_engine status --repo <path>` | Emit a status snapshot; persist `.vibeloom/state/status.json` |
| `python3 -m vibeloom_engine detect-edits --repo <path>` | Detect direct edits on approved contract artifacts (mtime fast-path, per-item hash confirmation) |

All engine commands emit JSON on stdout. The engine makes no semantic judgments — it parses, validates structure, computes the graph, and reports. Semantic judgment and user interaction remain with the skill.

> Optional: `pip install -e engine` puts a shorter `vibeloom-engine` command on `PATH`. Not required for skill operation.

## Command routing

On any operation invocation, load `references/operations.md` first for parameters and preconditions, then load the subset of `references/` relevant to the operation:

| Operation | First load | Then |
|---|---|---|
| `init`, `import` | `operations.md`, `modes.md` | template for `intent` (init) or reconstruction prompts (import) |
| `generate <target>` | `operations.md`, `runtime.md` | target-tier templates + graph cache |
| `eval <target>`, `review <target>` | `operations.md`, `runtime.md`, `eval.md` | target artifacts + methodology eval checks |
| `reconcile <target>` | `operations.md`, `runtime.md`, `eval.md` | downstream artifacts + graph |
| `approve <target>` | `operations.md`, `modes.md`, `eval.md` | target artifacts |
| `status` | `artifacts.md` | graph cache + status snapshot |

## Getting started

If the repo has no VibeLoom governance yet, the user typically starts with `init --mode <vibe|pm|dev|expert>` (new project) or `import --mode <mode>` (existing codebase). Consult `references/modes.md` to help the user pick a mode.

## Guardrails

- Never bypass an approval gate. When a contract tier is a user stop in the current mode, halt and surface findings rather than advancing.
- Treat the methodology as authoritative. If this file or a reference disagrees with the methodology, follow the methodology and flag the drift.
- Do not invent entity types, ID prefixes, or derivation edges. The valid set is defined by the methodology's Derivation DAG.
- Subagents receive scoped load sets only. They never load the skill or the methodology docs.
- Late-fetch is bounded: one re-invocation per task; exceed means a finding and task exit.
- `reconcile` is always user-initiated. Never auto-invoke it.

## Response shape

Keep responses tight. For operations that pause for user input, use a four-section structure:

1. **Scope** — what tier/scope this operation touched
2. **Decision** — what the skill did or is asking the user to decide
3. **Affected** — item IDs, artifacts, and scopes changed or surfaced
4. **Next** — the suggested next command
