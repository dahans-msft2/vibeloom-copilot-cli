---
name: vibeloom
description: Use when the user explicitly invokes $vibeloom or asks to initialize, import, review, reconcile, or evolve a governed codebase through VibeLoom's strict command interface and contract stack of intent, prd, usm, dm, and spec.
metadata:
  short-description: Contract-driven vibe coding workflows
---

# VibeLoom

## When To Use

Use this skill only when the user explicitly invokes `$vibeloom` or clearly asks to operate through the VibeLoom workflow.

This skill is for governed, contract-driven work over the canonical stack:
- `intent.md`
- `prd.md`
- `usm.md`
- `dm.md`
- `spec.md`

## Authority Model

- `docs/` owns methodology truth and longer explanations.
- `references/` is the runtime layer consumed by this skill.
- `site/` is derivative public documentation and is never authoritative.
- During routine command execution, load `references/` first and `docs/` only for `help topic`, deeper explanation, or an explicit runtime escalation.

## Invocation Model

- The skill is explicit-invocation only.
- Canonical commands use `/vibeloom <verb> <noun> [tail]`.
- Normalize the documented aliases from `references/command-surface.md` before routing.
- Verbs and nouns are strict after alias normalization. The remaining tail is freeform.
- If the noun is missing or invalid, do not guess. Return the valid grammar for that verb and the closest valid forms.
- Bare `$vibeloom` with no `/vibeloom ...` command triggers state-aware triage.
- If triage finds no governed project or a clearly first-time operator, keep the first reply short and point to `help topic methodology` and `help topic templates`.

Read [references/command-surface.md](references/command-surface.md) for the full grammar, aliases, and examples.

## Command Surface

### Core Commands

| Command | Purpose |
| --- | --- |
| `/vibeloom init project [intent seed]` | Start a governed project from intent |
| `/vibeloom import repo [path-or-current]` | Bootstrap governance for an unmanaged repo |
| `/vibeloom status repo` | Report governed state, blockers, and next valid actions |
| `/vibeloom status artifact <selector>` | Report one canonical artifact |
| `/vibeloom status module <module-name>` | Report one module |
| `/vibeloom review artifact <selector>` | Review one canonical artifact |
| `/vibeloom review module <module-name>` | Review one module slice |
| `/vibeloom develop change <request>` | Run feature or enhancement flow |
| `/vibeloom fix issue <repro-or-bug>` | Run steady-state bugfix flow |
| `/vibeloom reconcile repo` | Reconcile drift across the governed repo |
| `/vibeloom reconcile artifact <selector>` | Reconcile one artifact |
| `/vibeloom reconcile module <module-name>` | Reconcile one module |

### Expert Commands

| Command | Purpose |
| --- | --- |
| `/vibeloom generate artifact <selector>` | Generate a specific artifact or derived artifact |
| `/vibeloom approve scope <selector>` | Approve an intent, product batch, spec batch, module, or change |
| `/vibeloom eval scope <selector>` | Run structural and semantic checks over a scope |
| `/vibeloom help command <verb>` | Explain valid grammar and routing for one verb |
| `/vibeloom help topic <methodology|profiles|evals|templates|commands>` | Load guided help for one documentation topic |

## Routing Rules

Start with the smallest correct reference set:

1. Read [references/methodology.md](references/methodology.md) for the runtime summary of artifact authority, change classes, and reconcile asymmetry.
2. Read [references/command-surface.md](references/command-surface.md) to parse the command shape and aliases.
3. Read [references/routing-and-loading.md](references/routing-and-loading.md) to choose the right repo slice and state-aware next actions.
4. Read [references/interaction-contract.md](references/interaction-contract.md) before presenting findings or corrections.
5. Read [references/evals-and-templates.md](references/evals-and-templates.md) when the command requires generation, approval, evals, or template loading.

Do not load `docs/` during routine commands unless the active command requires deeper explanation or a runtime reference explicitly escalates to it.

## Output Contract

Every command response must use this shape:
1. `Scope`
2. `Decision / Findings`
3. `Affected IDs`
4. `Next action`

Use `references/interaction-contract.md` for review, status, fix, triage, and error-specific phrasing.

Read [references/interaction-contract.md](references/interaction-contract.md) for examples and correction patterns.

## Safety Rules

- Never treat `AGENTS.md` or `plan.md` as canonical semantic authority.
- Never omit `USM` or `DM` from the governed methodology.
- Treat `fix issue` as distinct from `import repo`; do not route routine defects through brownfield bootstrap.
- Use canonical command forms in responses even when the input used an alias.
- If a command would violate current methodology state, explain the blocking artifact and the next allowed command.
- If a selector is invalid, discover valid selectors from the repo when possible and return them explicitly.

## Validation

When updating the skill or validating its behavior, use [references/acceptance-tests.md](references/acceptance-tests.md).
