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

## Profiles

| Profile | Meaning |
| --- | --- |
| `lite` | Single bounded context or low coordination risk |
| `full` | Multiple bounded contexts or meaningful coordination risk |

Both profiles require:
- `USM`
- `DM`

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

## Import vs Fix

- `import repo` is a bootstrap path for unmanaged or heavily drifted repos.
- `fix issue` is the steady-state bugfix path for governed repos.
- Do not route ordinary defects through import.

## Source Files

When a deeper explanation is needed, read:
- `../docs/vibeloom-methodology.md`
- `../docs/artifact-protocol.md`
- `../docs/context-loading.md`
