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

## Invocation Model

- The skill is explicit-invocation only.
- Once active, parse commands in the form `/vibeloom <verb> <noun> [tail]`.
- Verbs and nouns are strict. The remaining tail is freeform.
- If the noun is missing or invalid, do not guess. Return the valid grammar for that verb and the closest valid forms.
- Bare `$vibeloom` with no `/vibeloom ...` command triggers the **Smart Entry Point** (see below).

Read [references/command-surface.md](references/command-surface.md) for the full grammar, aliases, and examples.

## Smart Entry Point (bare invocation)

When `$vibeloom` is invoked with no `/vibeloom ...` command, detect the current project state and present contextual actions.

1. Scan the current directory for VibeLoom artifacts: `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md`, `AGENTS.md`, `modules/`, `.vibeloom/`
2. Read frontmatter `status` from each artifact found
3. Determine project state and present available actions:

| State | Detection | Actions to Offer |
| --- | --- | --- |
| No project | No `intent.md` | `init project`, `import repo`, `help command init` |
| Intent draft | `intent.md` exists, status: draft | `review artifact intent`, `approve scope intent` |
| Product drafts | prd/usm/dm exist, any has status: draft | `review artifact prd`, `approve scope product` |
| Spec draft | spec.md exists, status: draft | `review artifact spec`, `approve scope spec` |
| Ready for code | All specs approved, no src/ | `generate artifact`, `develop change` |
| Active development | Source code + approved specs | `develop change`, `fix issue`, `reconcile` |

Present options concisely with numbered choices. Let the user choose.

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
| `/vibeloom help topic <methodology\|profiles\|evals\|templates\|commands>` | Load guided help for one documentation topic |

## Routing Rules

Start with the smallest correct reference set:

1. Read [references/methodology.md](references/methodology.md) for artifact authority, profiles, change classes, and reconcile asymmetry.
2. Read [references/command-surface.md](references/command-surface.md) to parse the command shape and aliases.
3. Read [references/routing-and-loading.md](references/routing-and-loading.md) to choose the right repo slice and state-aware next actions.
4. Read [references/interaction-contract.md](references/interaction-contract.md) before presenting findings or corrections.
5. Read [references/evals-and-templates.md](references/evals-and-templates.md) when the command requires generation, approval, evals, or template loading.

Only load additional methodology docs or templates when the active command requires them.

## Init Interview Mode

When routing to `init project`, after scaffolding `intent.md` and `.vibeloom/`, ask the user:

> "Would you like me to interview you about your project to populate the intent, or will you edit intent.md directly?"

If interview: ask structured questions one at a time:
1. What is the application you want to build?
2. Who are the primary users?
3. What are the 3-5 most important things it must do?
4. Are there technologies you want to use or avoid?
5. Any non-functional requirements (performance, scale, compliance)?

Populate `intent.md` from answers and show the result for review.

## Token Budget Guidance

When loading context for any command, follow these allocation targets:

| Slice | Budget |
| --- | --- |
| Code (generation, implementation) | 60% |
| Specs (canonical artifacts) | 30% |
| System prompt (skill, constitution, references) | 10% |

**Max recommended artifact lengths:**

| Artifact | Max tokens |
| --- | --- |
| Module spec | ≤ 3 000 |
| DM per bounded context | ≤ 1 500 |
| Root spec | ≤ 3 000 |

When specs exceed budget, summarize furthest-upstream artifacts first (intent before prd, prd before usm, etc.).

## Status Emoji Indicators

When producing `status` output, use these indicators:

| Emoji | Meaning |
| --- | --- |
| ✅ | Approved |
| ✏️ | Draft |
| ⚠️ | Stale or approved-with-known-issues |
| ⏳ | Not yet generated |

## Approved-With-Known-Issues Escape Hatch

In any `approve` or `reconcile` flow, if the user wants to proceed despite unresolved eval warnings or reconciliation issues, offer the `approved-with-known-issues` status:

- Set frontmatter `status: approved-with-known-issues`
- Document the known issues in `.vibeloom/state.md` under the artifact entry
- These issues are surfaced in **every subsequent eval** that touches the artifact
- Only a human may enter this state

## Output Contract

Every command response must use this shape:

1. `Scope`
2. `Decision / Findings`
3. `Affected IDs`
4. `Next action`

Adaptive summary rules:
- For `review artifact prd|usm`, lead with workflow and value language, but always cite `PRD-FR-*`, `STORY-*`, `AC-*`, and any implied `ENT-*`.
- For `review artifact dm|spec`, `eval`, and `reconcile`, lead with technical governance language and always cite `ENT-*`, `INV-*`, `MOD-*`, `IFACE-*`, and stale implications when relevant.
- For `fix issue`, always start from repro, expected behavior, violated or missing contract, and regression impact.

Read [references/interaction-contract.md](references/interaction-contract.md) for examples and correction patterns.

## Safety Rules

- Never treat `AGENTS.md` or `plan.md` as canonical semantic authority.
- Never omit `USM` or `DM` from the governed methodology.
- Treat `fix issue` as distinct from `import repo`; do not route routine defects through brownfield bootstrap.
- If a command would violate current methodology state, explain the blocking artifact and the next allowed command.
- If a selector is invalid, discover valid selectors from the repo when possible and return them explicitly.

## Validation

When updating the skill or validating its behavior, use [references/acceptance-tests.md](references/acceptance-tests.md).
