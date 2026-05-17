# VibeLoom — Project Guidelines

This repo hosts **VibeLoom**, a contract-driven governance methodology + engine for long-lived AI-coded projects, and the public website at `vibeloom.ai`. It was originally authored for Claude Code and Codex but is fully usable from VS Code Copilot Chat and Copilot CLI.

## Repo layout (orient here first)

- `v03/` — **current spec** (codæ manifesto + VibeLoom v0.3 methodology, implementation, examples). Spec-only; engine support pending.
- `v02/` — **runnable substrate**. Methodology, skill, 17 artifact templates, and the deterministic `vibeloom-engine` Python package. Use this for actual execution.
- `v01/` — archived first cut. Don't change unless explicitly asked.
- `site/` — Cloudflare Workers static assets for `vibeloom.ai`. Auto-deploys on push to `main`.
- `.github/skills/vibeloom/` — Copilot CLI skill that wraps the v0.2 substrate for this environment.

## Authoritative sources

When working on VibeLoom itself (not the website), the methodology is the source of truth. If anything disagrees with it, the methodology wins.

- **v0.3 (spec)**: `v03/codæ-manifesto.html`, `v03/vibeloom-methodology.md`, `v03/vibeloom-implementation.md`, `v03/getting-started.md`
- **v0.2 (runnable)**: `v02/SKILL.md`, `v02/vibeloom-methodology.md`, `v02/vibeloom-implementation.md`, `v02/references/*.md`
- Artifact templates: `v02/assets/`. Engine source: `v02/engine/vibeloom_engine/`.

## Engine

The `vibeloom-engine` is pure Python 3.10+, **zero dependencies**, invoked via `py -m`. From the repo root on Windows:

```powershell
$env:PYTHONPATH = "v02\engine"
py -m vibeloom_engine --version
py -m vibeloom_engine parse --repo <target-repo>
```

Commands: `parse`, `graph`, `eval`, `affected`, `staleness`, `status`, `detect-edits`. All emit JSON on stdout. The engine makes no semantic judgments — parse / validate / report only.

## When the user asks for VibeLoom operations

If the user invokes a VibeLoom operation (`init`, `import`, `generate`, `eval`, `review`, `reconcile`, `approve`, `status`) or mentions `/vibeloom` or `$vibeloom`, load the `vibeloom` skill (`.github/skills/vibeloom/SKILL.md`) and follow its routing table.

## Coding behavioral standards

All agents that write or review code follow the [Karpathy guidelines](.github/skills/karpathy-guidelines/SKILL.md) augmented by the [Huginn-Muninn prediction ledger](.github/skills/huginn-muninn/SKILL.md). Together they form the behavioral backbone:

1. **Think before coding** — state your assumptions explicitly. If the goal is ambiguous, surface the interpretations and ask. Never pick silently.
2. **Simplicity first** — minimum code that satisfies the AC. No speculative abstractions, no configurability that wasn't requested.
3. **Surgical changes** — every changed line must trace to a subtask AC item. Mention unrelated issues; never touch them.
4. **Goal-driven execution** — success criteria must be verifiable *before* you start. If they aren't, return a `BlockerReport`.
5. **Predict → Observe → Classify → Update** — before each meaningful action, state the expected observation and confidence. After the action, compare, classify prediction error (`none|minor|scope|model|evidence|execution|safety`), and update confidence before choosing the next action.

## Guardrails (apply everywhere in this repo)

- **Never bypass an approval gate.** When a contract tier is a user stop, halt and surface findings rather than advancing.
- **Don't invent entity types, ID prefixes, or derivation edges.** Valid set is defined by the methodology's Derivation DAG (`v02/vibeloom-implementation.md`).
- **Don't auto-invoke `reconcile`.** Always user-initiated.
- **Subagent load sets are scoped.** Subagents never load this file, the skill, or methodology docs — only their target artifacts.

## Response shape for operations

For VibeLoom operations that pause for user input, use this four-section shape:

1. **Scope** — tier / scope touched
2. **Decision** — what was done or what the user must decide
3. **Affected** — item IDs, artifacts, scopes changed or surfaced
4. **Next** — suggested next command
