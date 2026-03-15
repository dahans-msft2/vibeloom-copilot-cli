# Runtime Methodology Index

This file is the runtime summary loaded during routine skill work.

- `docs/` owns methodology truth.
- `references/` owns runtime-efficient execution guidance.
- Load `docs/` only when the user asks for deeper explanation, uses `help topic`, or another runtime reference points there.

## Authority

- Canonical artifacts: `constitution.md`, `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md`
- Derived artifacts: `AGENTS.md`, `plan.md`
- Canonical artifacts define semantic truth. Derived artifacts guide execution and never override canonical semantics.

## Runtime Invariants

- The governed stack is intent-first: `intent -> prd -> usm -> dm -> spec`
- `USM` and `DM` are mandatory in every profile.
- Only `lite` and `full` profiles exist.
- `fix issue` is the steady-state bugfix path. Do not route ordinary defects through `import repo`.

## Change Classes

| Class | Runtime meaning |
| --- | --- |
| `local` | No workflow, semantic, interface, or NFR change |
| `behavioral-in-module` | Behavior change inside one boundary |
| `boundary-changing` | Actor, workflow, concept, interface, or NFR change across boundaries |

If classification is uncertain, escalate upward.

## Reconcile Rule

- Approved upstream truth defines semantics.
- Drift produces proposals, not silent upstream rewrites.
- Bounded reconcile stays limited to one up-pass, one down-pass, and one final validation.

## Deep Docs

- `../docs/vibeloom-methodology.md`
- `../docs/profile-selection.md`
- `../docs/artifact-protocol.md`
- `../docs/context-loading.md`
