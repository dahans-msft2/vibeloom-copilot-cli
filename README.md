# VibeLoom

VibeLoom is a contract-driven methodology and Codex skill for long-lived vibe coding of production-quality systems.

## Package Map

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Codex skill entrypoint for the canonical `/vibeloom <verb> <noun> [tail]` grammar and documented aliases |
| `agents/` | UI metadata and explicit invocation policy |
| `references/` | Runtime-efficient operational references loaded by the skill during routine command execution |
| `assets/` | Skill icons and UI assets |
| `constitution.md` | Foundational rules that keep downstream specs concise and mechanically checkable |
| `intent.md` | Intent for the methodology-as-product |
| `prd.md` | Product requirements for the methodology package |
| `usm.md` | Workflow- and user-centered semantic layer |
| `dm.md` | Domain model for the methodology itself |
| `spec.md` | Technical design for the canonical package and future runtime protocol |
| `templates/` | Canonical templates aligned with the reconciled methodology |
| `eval/` | Structural and semantic evaluation instructions |
| `docs/` | Methodology truth and operator reading material loaded mainly through `help topic` or explicit deeper-explanation flows |
| `site/` | Derivative public documentation for `https://vibeloom.ai/` |

## Authority Model

- `docs/` owns the canonical prose methodology truth.
- The root artifact stack is the structured package representation aligned to `docs/`.
- `references/` is the skill's runtime layer. It carries only the operational guidance the skill needs to parse, route, and present results.
- `SKILL.md` is the implementation entrypoint that tells Codex how to load and apply `references/`.
- `templates/` is generation-only and must not introduce methodology truth of its own.
- `site/` is derivative public documentation and marketing material. It must not introduce new semantics.
- During routine skill execution, load `references/` first. Load `docs/` only for `help topic`, deeper explanation, or explicit escalation from a runtime reference.

## Artifact Roles

- `constitution.md` is the repo-wide governing baseline. It is normative, but it is not part of the per-project change stack.
- `intent.md`, `prd.md`, `usm.md`, `dm.md`, and `spec.md` are the canonical long-lived project artifacts for this package representation.
- Draft `intent.md` is prose-first and may remain free of stable item IDs. Reconciliation may add optional `CAP-*` capability IDs when downstream item-level trace needs them.
- `AGENTS.md` and `plan.md` are derived operational artifacts. They guide execution, but they are not source-of-truth contracts.
- Machine-readable projections are intentionally limited to three conceptual outputs: trace index, dependency/stale graph, and interface/schema manifests.

## Operator Quickstart

1. Invoke bare `$vibeloom` to get the current governed state, blockers, and next safe commands.
2. If this is your first run, use `/vibeloom help topic methodology` for the contract model and `/vibeloom help topic templates` for artifact shapes.
3. For a new governed project, start with `/vibeloom init project [intent seed]`.
4. For an existing governed repo, use `/vibeloom status repo` before changing anything.

## Phase Boundary

This repo includes the actual Codex skill plus the methodology artifacts it relies on.

- The skill interface exists in `SKILL.md`.
- No external parser or runtime binary is implemented here.
- No generated live `AGENTS.md` instances are checked in here.
- No automation or runtime code is created here.

## Additional Docs

- `docs/vibeloom-methodology.md` explains the methodology itself without runtime implementation details.
- `docs/profile-selection.md` explains Lite vs Full selection without reintroducing inline-USM Lite behavior.
- `site/` contains the public website content for `https://vibeloom.ai/`.
