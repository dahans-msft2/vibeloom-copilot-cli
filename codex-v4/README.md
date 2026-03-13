# VibeLoom Codex V4 Package

This subtree contains the next merged Codex package for VibeLoom. It uses `/codex-v3` as the governance base and selectively reincorporates the best onboarding, eval-framing, and template ideas from `/codex-v2` without reopening rejected methodology decisions.

## Package Map

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Actual Codex skill entrypoint for the strict `/vibeloom ...` interface |
| `agents/` | UI metadata and explicit invocation policy |
| `references/` | On-demand operational references for the skill |
| `assets/` | Skill icons and UI assets |
| `constitution.md` | Foundational rules that keep downstream specs concise and mechanically checkable |
| `intent.md` | Intent for the methodology-as-product |
| `prd.md` | Product requirements for the methodology package |
| `usm.md` | Workflow- and user-centered semantic layer |
| `dm.md` | Domain model for the methodology itself |
| `spec.md` | Technical design for the Codex V4 package and future runtime protocol |
| `templates/` | Canonical templates aligned with the reconciled methodology |
| `eval/` | Structural and semantic evaluation instructions |
| `docs/` | Protocol notes, methodology guide, profile selection, and competitor comparison |
| `site/` | Static marketing site for `https://vibeloom.ai/` |

## Artifact Roles

- `constitution.md` is the repo-wide governing baseline. It is normative, but it is not part of the per-project change stack.
- `intent.md`, `prd.md`, `usm.md`, `dm.md`, and `spec.md` are the canonical long-lived project artifacts.
- `AGENTS.md` and `plan.md` are derived operational artifacts. They guide execution, but they are not source-of-truth contracts.
- Machine-readable projections are intentionally limited to three conceptual outputs: trace index, dependency/stale graph, and interface/schema manifests.

## Phase Boundary

This package includes the actual Codex skill plus the methodology artifacts it relies on.

- The skill interface exists in `SKILL.md`.
- No external parser or runtime binary is implemented here.
- No generated live `AGENTS.md` instances are checked in here.
- No automation or runtime code is created here.

## Relationship To Other Subtrees

- `/codex-v4` is the new merged target package.
- `/codex-v3` remains the stricter governance base and comparison point.
- `/codex-v2` remains the source of selected onboarding and template ideas.
- `/codex` and `/claude` remain intact for historical comparison.

## Additional Docs

- `docs/vibeloom-methodology.md` explains the methodology itself without runtime implementation details.
- `docs/profile-selection.md` explains Lite vs Full selection without reintroducing inline-USM Lite behavior.
- `site/` contains a static website draft for `https://vibeloom.ai/` copied from the prior package; it was not redesigned in this pass.
