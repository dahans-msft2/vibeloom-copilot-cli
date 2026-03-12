# VibeLoom Codex Package

This subtree contains the reconciled methodology artifacts for the Codex variant of VibeLoom.

## Package Map

| Path | Purpose |
| --- | --- |
| `constitution.md` | Foundational rules that keep downstream specs concise and mechanically checkable |
| `intent.md` | Intent for the methodology-as-product |
| `prd.md` | Product requirements for the methodology package |
| `usm.md` | Workflow- and user-centered semantic layer |
| `dm.md` | Domain model for the methodology itself |
| `spec.md` | Technical design for the future Codex runtime and file protocol |
| `templates/` | Canonical templates aligned with the reconciled methodology |
| `eval/` | Structural and semantic evaluation instructions |
| `docs/` | Protocol, context-loading, and competitor comparison notes |

## Artifact Roles

- `constitution.md` is the repo-wide governing baseline. It is normative, but it is not part of the per-project change stack.
- `intent.md`, `prd.md`, `usm.md`, `dm.md`, and `spec.md` are the canonical long-lived project artifacts.
- `AGENTS.md` and `plan.md` are derived operational artifacts. They guide execution, but they are not source-of-truth contracts.
- Machine-readable projections are intentionally limited to three conceptual outputs: trace index, dependency/stale graph, and interface/schema manifests.

## Phase Boundary

This phase defines the methodology and its artifacts only.

- No runnable skill command is created here.
- No generated live `AGENTS.md` instances are checked in here.
- No automation or runtime code is created here.

## Relationship To `/claude`

`/codex` and `/claude` are parallel subtrees. This package does not reconcile, overwrite, or depend on the contents of `/claude`.
