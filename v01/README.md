# VibeLoom v01

VibeLoom v01 is the current contract-driven methodology package and Codex skill for long-lived vibe coding of production-quality systems.

## Package Map

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Codex skill entrypoint for the `/vibeloom` surface over the canonical `<action> <target> <context>` command model |
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

## Authority Model

The canonical prose layer contract lives in [docs/vibeloom-methodology.md](docs/vibeloom-methodology.md). Runtime command behavior lives in `references/`. This README keeps only the package-local map.

## Workspace Context

This package now lives in `v01/` under the workspace root. The public website is no longer part of the package layout; it lives in the sibling `../site/` workspace and deploys independently.

## Artifact Roles

- `constitution.md` is the package-wide governing baseline, not part of the per-project approval stack.
- `intent.md`, `prd.md`, `usm.md`, `dm.md`, and `spec.md` are the canonical long-lived artifacts for this package representation.
- The checked-in `spec.md` is a package-level meta-spec for this methodology repo; generated governed project specs still declare one selected profile.
- `AGENTS.md` and `plan.md` are derived operational artifacts, not source-of-truth contracts.

## Operator Quickstart

1. Invoke bare `$vibeloom` to get the current governed state, blockers, and next safe commands.
2. If this is your first run, use `/vibeloom help methodology` for the contract model and `/vibeloom help templates` for artifact shapes.
3. For a new governed project, start with `/vibeloom init [intent seed]`.
4. For an existing governed repo, use `/vibeloom status` before changing anything.

## Phase Boundary

This package ships the Codex skill plus the methodology artifacts it relies on. It does not ship a separate runtime binary, checked-in generated `AGENTS.md` instances, or automation code.

## Additional Docs

- `docs/vibeloom-methodology.md` explains the methodology itself without runtime implementation details.
- `docs/profile-selection.md` explains Lite vs Full selection.
- The public website lives in the sibling `../site/` workspace.

## Public Site

The public site is no longer part of the v01 package layout. See [../site/README.md](../site/README.md) for the site-local deployment setup and Cloudflare instructions.
