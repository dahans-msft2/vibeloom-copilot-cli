# Runtime Methodology Index

This file is the runtime summary loaded during routine skill work.

- `docs/` owns canonical prose methodology truth.
- The root artifact stack is the structured package representation aligned to `docs/`.
- `references/` owns runtime-efficient execution guidance only.
- `templates/` is generation-only.
- `site/` is derivative marketing documentation and is not part of runtime authority.
- Load `docs/` only when the user asks for deeper explanation, uses `help`, or another runtime reference points there.

## Authority

- Canonical artifacts: `constitution.md`, `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md`
- Derived artifacts: `AGENTS.md`, `plan.md`
- Canonical artifacts define semantic truth. Derived artifacts guide execution and never override canonical semantics.

## Runtime Invariants

- The governed stack is intent-first: `intent -> prd -> usm -> dm -> spec`
- Draft `intent.md` may remain prose-first with no stable item IDs. Reconciliation may add optional `CAP-*` capability IDs when downstream item-level trace needs explicit intent references.
- `USM` and `DM` are mandatory in every profile.
- Only `lite` and `full` profiles exist.
- Surface modes are session-scoped: default `product-first`; `code-first` only changes which layer is shown first and escalates back to product/domain slices on boundary or semantic risk.
- `fix issue` is the steady-state bugfix path. Do not route ordinary defects through `import`.

## Surface Modes

Runtime surface rules:
- default surface is `product-first`
- `code-first` is an advanced engineering surface
- surface selection is session-scoped only
- do not persist surface choice to repo state
- surfaces do not change the canonical stack, approval scopes, lifecycle states, traceability rules, or reconcile asymmetry
- `code-first` must not omit, replace, or silently synthesize away `prd`, `usm`, or `dm`

When `code-first` is active, escalate to product or domain slices when:
- the change is `boundary-changing`
- workflows or actors are touched or ambiguous
- concepts, entities, invariants, interfaces, or NFR boundaries are touched or ambiguous
- semantic drift appears during `review`, `eval`, or `reconcile`
- the user explicitly asks to inspect product or domain artifacts

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
