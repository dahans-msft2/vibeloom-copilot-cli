---
name: vibeloom
description: Use when the user explicitly invokes $vibeloom or asks to initialize, import, review, fix, reconcile, or evolve a governed codebase through VibeLoom's strict command interface, surface modes, and contract stack of intent, prd, usm, dm, and spec.
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

## Entrypoint Role

`SKILL.md` is the runtime entrypoint and orchestrator. The canonical layer contract lives in [docs/vibeloom-methodology.md](docs/vibeloom-methodology.md); routine runtime authority lives in `references/`.

## Runtime Bootstrap

On each invocation, start with the smallest correct reference set:

1. Read [references/command-surface.md](references/command-surface.md) to parse the command grammar, selectors, and canonical forms.
2. Read [references/methodology.md](references/methodology.md) for runtime invariants such as authority boundaries, profiles, surfaces, change classes, and reconcile asymmetry.
3. Read [references/routing-and-loading.md](references/routing-and-loading.md) to choose the right repo slice, next valid action, and escalation path.
4. Read [references/interaction-contract.md](references/interaction-contract.md) before presenting findings, errors, triage, or corrections.
5. Read [references/evals-and-templates.md](references/evals-and-templates.md) when generation, approval, evals, or template loading is involved.

Do not load `docs/` during routine commands unless the user asks for `help`, requests deeper explanation, or a runtime reference explicitly escalates.

## Help Topic Registry

`help` is the only command family allowed to load explanatory material outside `references/`.

Topic routing:
- `methodology` -> `docs/vibeloom-methodology.md`
- `profiles` -> `docs/profile-selection.md`
- `surfaces` -> `docs/surface-modes.md`
- `evals` -> `docs/evals-structural.md`, `docs/evals-semantic.md`
- `templates` -> `templates/`
- `commands` -> `references/command-surface.md`

Rules:
- `references/` may escalate only by topic name, never by direct `docs/*` path.
- Use `help <topic>` as the canonical explanation entrypoint.
- Routine execution stays in `references/` plus required canonical artifacts and templates unless `help` is invoked.

## Skill-Specific Behavior

- The skill is explicit-invocation only.
- Bare `$vibeloom` with no `/vibeloom ...` command uses state-aware triage from [references/routing-and-loading.md](references/routing-and-loading.md).
- If triage finds no governed project or a clearly first-time operator, keep the first reply short and point to `/vibeloom help methodology` and `/vibeloom help templates`.
- Follow the reference-owned grammar and canonical command forms. Do not invent alternate command surfaces in `SKILL.md`.

## Guardrails

- Never treat `AGENTS.md` or `plan.md` as canonical semantic authority.
- Never omit `USM` or `DM` from the governed methodology.
- If a command would violate current methodology state, explain the blocking artifact and the next allowed command.
- If a selector is invalid, discover valid selectors from the repo when possible and return them explicitly.

## Validation

When updating this skill or its runtime references, validate behavior with [references/acceptance-tests.md](references/acceptance-tests.md).
