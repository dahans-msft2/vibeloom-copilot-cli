---
name: vibeloom
description: 'Contract-driven governance for long-lived AI-coded projects (VibeLoom v0.2 runnable substrate). Use when the user wants to bootstrap, import, generate, evaluate, review, reconcile, approve, or check status on artifacts in a VibeLoom-governed project, or invokes /vibeloom or $vibeloom. Modes: vibe, pm, dev, expert.'
argument-hint: '[init|import|generate|eval|review|reconcile|approve|status] [target] [--mode <vibe|pm|dev|expert>]'
---

# VibeLoom (Copilot CLI / VS Code Copilot port)

VibeLoom governs long-lived AI-coded projects by generating a tiered contract of specifications (`intent-specs` → `product-specs` → `system-specs`), deriving execution context from it, and generating code from the approved stack. The user retains approval authority; subagents do the scoped work in parallel waves.

This SKILL.md is the Copilot CLI / VS Code Copilot Chat port of the original `v02/SKILL.md` (authored for Claude Code and Codex). The methodology, references, artifact templates, and engine all live under `v02/` and are reused unchanged.

## When to use this skill

Invoke on any `$vibeloom` or `/vibeloom` mention, or when the user asks to run any methodology operation: `init`, `import`, `generate`, `eval`, `review`, `reconcile`, `approve`, `status`.

## Authoritative sources (always consult before deciding)

If this file conflicts with the methodology, the methodology wins.

- **[../../../v02/vibeloom-methodology.md](../../../v02/vibeloom-methodology.md)** — WHAT and WHY (entities, tiers, modes, operations, approval model, Derivation DAG).
- **[../../../v02/vibeloom-implementation.md](../../../v02/vibeloom-implementation.md)** — HOW (artifact layout, metadata, ID schema, runtime loop, subagent dispatch, load sets).
- **[../../../v02/SKILL.md](../../../v02/SKILL.md)** — original skill body. Canonical word on routing and response shape; this file is the Copilot-side wrapper.

## Runtime references (load on demand from `v02/references/`)

- **[operations.md](../../../v02/references/operations.md)** — per-operation purpose, parameters, pre/postconditions.
- **[modes.md](../../../v02/references/modes.md)** — `vibe` / `pm` / `dev` / `expert`: tier ownership, auto-advance, public surface.
- **[runtime.md](../../../v02/references/runtime.md)** — dispatch mechanics: runtime loop, waves, load sets, late-fetch, validation.
- **[artifacts.md](../../../v02/references/artifacts.md)** — artifact layout, frontmatter, ID schema, derivation rules.
- **[eval.md](../../../v02/references/eval.md)** — semantic-eval dimensions, finding schema, severity classification.
- **[troubleshooting.md](../../../v02/references/troubleshooting.md)** — cache corruption, direct edits, breaking changes, partial wave failure.

## Templates

17 artifact templates in `v02/assets/`:

- `intent-specs/`: `intent.md`, `vibe-intent.md`, `defaults.md`
- `product-specs/`: `prd.md`, `usm.md`, `dm.md`
- `system-specs/`: `system.md`, `vibe-system.md`, `containers.md`, `container.md`, `component.md`
- `context/`: `pdr.md`, `adr.md`, `bdd.md`, `root-config.md`, `container-config.md`, `component-config.md`

Load one template at a time, for the artifact being generated.

## Engine invocation (Windows)

```powershell
$env:PYTHONPATH = "v02\engine"   # set once per session; adjust to full path if running from outside repo root
py -m vibeloom_engine parse        --repo <target-repo>
py -m vibeloom_engine graph        --repo <target-repo>
py -m vibeloom_engine eval         --repo <target-repo> [--target <tier>]
py -m vibeloom_engine affected     --repo <target-repo> --ids <IDs...>
py -m vibeloom_engine staleness    --repo <target-repo>
py -m vibeloom_engine status       --repo <target-repo>
py -m vibeloom_engine detect-edits --repo <target-repo>
```

All engine commands emit JSON on stdout. Engine makes no semantic judgments — parse / validate / report only.

## Command routing

Load `v02/references/operations.md` first, then the subset relevant to the operation:

| Operation                    | First load                                | Then                                               |
|------------------------------|-------------------------------------------|----------------------------------------------------|
| `init`, `import`             | `operations.md`, `modes.md`               | `intent` template (init) or reconstruction prompts (import) |
| `generate <target>`          | `operations.md`, `runtime.md`             | target-tier templates + graph cache                |
| `eval` / `review <target>`   | `operations.md`, `runtime.md`, `eval.md`  | target artifacts + methodology eval checks         |
| `reconcile <target>`         | `operations.md`, `runtime.md`, `eval.md`  | downstream artifacts + graph                       |
| `approve <target>`           | `operations.md`, `modes.md`, `eval.md`    | target artifacts                                   |
| `status`                     | `artifacts.md`                            | graph cache + status snapshot                      |

## Getting started

New project: `vibeloom init --mode <vibe|pm|dev|expert>`
Existing codebase: `vibeloom import --mode <mode>`

Consult `v02/references/modes.md` to help the user pick a mode.

## Copilot-specific notes

- **No `/vibeloom` slash command primitive.** Invoke naturally ("vibeloom init in pm mode") or type `/vibeloom` — Copilot will load this skill from its description match.
- **Subagent parallelism.** Use the `task` tool with `Explore` for read-only investigation and `general-purpose` for full-capability subagents. Pass each a scoped load set per `v02/references/runtime.md` — they must not load this skill or methodology docs.
- **Python launcher.** On this machine use `py` (not `python` or `python3`).

## Guardrails

- Never bypass an approval gate.
- Treat the methodology as authoritative; flag any drift.
- Do not invent entity types, ID prefixes, or derivation edges.
- Subagents receive scoped load sets only.
- Late-fetch is bounded: one re-invocation per task.
- `reconcile` is always user-initiated.

## Response shape

1. **Scope** — tier/scope touched
2. **Decision** — what was done or what the user must decide
3. **Affected** — item IDs, artifacts, scopes changed or surfaced
4. **Next** — suggested next command

## Version note

This skill ports **v0.2** (runnable). v0.3 spec is under `v03/` — consult for design-time reading only; the engine catches up in a future v0.3.x release.
