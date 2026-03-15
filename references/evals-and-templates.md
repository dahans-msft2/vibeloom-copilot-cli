# Evals And Templates Reference

Use this file when a command requires generation, approval, or validation.

- This file describes the current runtime eval surface.
- Current runtime evals are structural and semantic only.
- Broader methodology framing may mention behavioral or test-generation ideas, but those are not part of the current command surface unless `references/command-surface.md` says so.

## Eval Sources

Structural evals:
- `../eval/structural-checks.md`

Semantic evals:
- `../eval/semantic-checks.md`

Rules:
- structural failures block approval
- semantic findings warn; they do not self-resolve

## Template Sources

Canonical templates:
- `../templates/constitution-template.md`
- `../templates/intent-template.md`
- `../templates/prd-template.md`
- `../templates/usm-template.md`
- `../templates/dm-template.md`
- `../templates/spec-template.md`

Derived templates:
- `../templates/module-spec-template.md`
- `../templates/agents-template.md`
- `../templates/plan-template.md`

## Generation Rules

- Generate only the requested artifact or the next valid artifact implied by the command.
- Use the smallest safe upstream slice.
- Preserve IDs when regenerating an existing governed artifact unless a human-approved semantic change requires a new item.
- Do not present `AGENTS` or `plan` as canonical.

### Generation Cascade After Approval

When `approve scope intent` succeeds, the agent generates the product spec batch sequentially:

1. `prd.md` — from approved intent
2. `usm.md` — from approved intent + generated PRD
3. `dm.md` — from approved intent + generated PRD + generated USM

Each artifact feeds the next. All three are created as `draft`. No intermediate approval gates exist between them. The batch is approved together via `approve scope product`.

## Approval Rules

Allowed approval scopes:
- `intent`
- `product`
- `spec`
- `module`
- `change`

Normalize:
- `product` -> `prd+usm+dm`
- `spec` -> root spec plus module specs where applicable

## Eval Rules By Command

| Command | Required eval behavior |
| --- | --- |
| `approve scope ...` | Run structural checks first, then semantic checks |
| `eval scope ...` | Run requested checks and return findings without approval |
| `generate artifact ...` | Use templates, then run structural checks on generated output |
| `develop change ...` | Evaluate the touched slice after proposed changes |
| `fix issue ...` | Evaluate the affected slice after regression framing |
