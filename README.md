# VibeLoom

VibeLoom is a contract-driven methodology and Codex skill for long-lived vibe coding of production-quality systems.

## Package Map

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Codex skill entrypoint for the canonical `/vibeloom <action> <target> <context>` command model |
| `agents/` | UI metadata and explicit invocation policy |
| `references/` | Runtime-efficient operational references loaded by the skill during routine command execution |
| `constitution.md` | Foundational rules that keep downstream specs concise and mechanically checkable |
| `intent.md` | Intent for the methodology-as-product |
| `prd.md` | Product requirements for the methodology package |
| `usm.md` | Workflow- and user-centered semantic layer |
| `dm.md` | Domain model for the methodology itself |
| `spec.md` | Package-level technical meta-spec for the methodology package and future runtime protocol |
| `templates/` | Canonical templates aligned with the reconciled methodology |
| `docs/evals-*.md` | Detailed structural and semantic evaluation references |
| `docs/` | Methodology truth and operator reading material loaded mainly through `help` or explicit deeper-explanation flows |
| `site/` | Derivative public documentation for `https://vibeloom.ai/` |

## Authority Model

The canonical prose layer contract lives in [docs/vibeloom-methodology.md](docs/vibeloom-methodology.md).

During routine skill execution, `references/` are the operational authority. `docs/` are loaded mainly through `help` or explicit deeper-explanation paths. `templates/` are generation-only, and `site/` is derivative public documentation.

## Artifact Roles

- `constitution.md` is the repo-wide governing baseline. It is normative, but it is not part of the per-project change stack.
- `intent.md`, `prd.md`, `usm.md`, `dm.md`, and `spec.md` are the canonical long-lived project artifacts for this package representation.
- The checked-in `spec.md` is a package-level meta-spec for this methodology repo; generated governed project specs still declare one selected profile.
- Draft `intent.md` is prose-first and may remain free of stable item IDs. Reconciliation may add optional `CAP-*` capability IDs when downstream item-level trace needs them.
- `AGENTS.md` and `plan.md` are derived operational artifacts. They guide execution, but they are not source-of-truth contracts.
- Machine-readable projections stay intentionally limited; see the methodology docs and `spec.md` for the canonical constraint.

## Operator Quickstart

1. Invoke bare `$vibeloom` to get the current governed state, blockers, and next safe commands.
2. If this is your first run, use `/vibeloom help methodology` for the contract model and `/vibeloom help templates` for artifact shapes.
3. For a new governed project, start with `/vibeloom init [intent seed]`.
4. For an existing governed repo, use `/vibeloom status` before changing anything.

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
