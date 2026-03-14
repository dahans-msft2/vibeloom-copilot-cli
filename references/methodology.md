# VibeLoom Methodology Reference

Read this file first when the command meaning depends on artifact authority, change class, or reconcile direction.

## Canonical vs Derived

Canonical long-lived artifacts:
- `constitution.md`
- `intent.md`
- `prd.md`
- `usm.md`
- `dm.md`
- `spec.md`

Derived operational artifacts:
- `AGENTS.md`
- `plan.md`

Rules:
- Canonical artifacts define truth.
- Derived artifacts guide execution.
- Derived artifacts never override canonical semantics.

## Contract Stack

The governed stack is:

1. `intent`
2. `prd`
3. `usm`
4. `dm`
5. `spec`

The stack is intent-first and mandatory. `USM` and `DM` are always present.

## Generation And Approval Gates

Generation is sequential and top-down. Approval gates bracket logical groups:

- `approve scope intent` — approves intent, then triggers sequential generation of `prd` → `usm` → `dm` (each using the previous as input, all created as `draft`)
- `approve scope product` — approves the `prd + usm + dm` batch together
- `approve scope spec` — approves root spec + module specs

No intermediate approval gates exist within the product generation sequence.

## Profiles

| Profile | Meaning |
| --- | --- |
| `lite` | Single bounded context or low coordination risk |
| `full` | Multiple bounded contexts or meaningful coordination risk |

Both profiles require:
- `USM`
- `DM`

Profile-selection heuristics live in:
- `../docs/profile-selection.md`

## Change Classes

| Class | Meaning |
| --- | --- |
| `local` | No workflow, semantic, interface, or NFR change |
| `behavioral-in-module` | Behavior change inside one boundary |
| `boundary-changing` | Actor, workflow, concept, interface, or NFR change across boundaries |

If uncertain, escalate upward.

## Reconcile Asymmetry

- Upstream truth defines semantics.
- Downstream docs or code can reveal drift.
- Drift produces proposals, not silent upstream rewrites.

The agent must propose one path:
- amend upstream, then mark dependent artifacts stale
- preserve upstream, then amend downstream artifacts or code

Bounded reconcile rule:
- one up-pass
- one down-pass
- one final validation

Do not iterate automatically beyond that bounded loop.

## Import vs Fix

- `import repo` is a bootstrap path for unmanaged or heavily drifted repos.
- `fix issue` is the steady-state bugfix path for governed repos.
- Do not route ordinary defects through import.

## Source Files

When a deeper explanation is needed, read:
- `../docs/vibeloom-methodology.md`
- `../docs/profile-selection.md`
- `../docs/artifact-protocol.md`
- `../docs/context-loading.md`
