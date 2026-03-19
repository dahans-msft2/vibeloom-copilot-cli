# Evals And Templates Reference

Use this file when a command requires generation, approval, or validation.

- This file is the complete routine runtime eval contract.
- Routine `generate`, `approve`, `eval`, `develop`, and `fix` commands use this file directly.
- Current runtime evals are `structural` and `semantic` only.
- Broader methodology framing may mention behavioral or test-generation ideas, but those are not part of the current command surface unless `references/command-surface.md` says so.
- Use `help evals` when the user asks for the full structural and semantic check definitions.

## Runtime Eval Families

| Family | Meaning | Blocking |
| --- | --- | --- |
| `structural` | Mechanical verification of metadata, IDs, references, lifecycle, ownership, and projection limits | Yes |
| `semantic` | Reasoned analysis of coverage, contradictions, boundary sanity, context sufficiency, and bugfix or import correctness | No |

Runtime rules:
- run `structural` before `semantic` whenever both apply
- structural failures block approval
- structural failures block generation success when generated output is malformed
- semantic findings warn; they do not self-resolve
- semantic findings do not grant approval authority to the agent
- do not invent separate behavioral runtime commands

## Runtime Eval Targets

Approval targets, eval targets, normalization, and binding rules are defined in `references/command-surface.md` § "Targets And Selectors" and § "Normalization". This file does not restate them.

## Runtime Eval Output

Use the mandatory command response shape from `references/interaction-contract.md`:

1. `Scope`
2. `Decision / Findings`
3. `Affected IDs`
4. `Next action`

Minimum eval evidence:
- evaluated scope and eval families run
- artifacts or slices inspected
- failing or warning check IDs
- concrete upstream or downstream IDs implicated by the finding

## Runtime Check Inventory

Structural checks:
- `EVAL-STRUCT-001` - metadata completeness
- `EVAL-STRUCT-002` - artifact authority
- `EVAL-STRUCT-003` - ID grammar compliance
- `EVAL-STRUCT-004` - reference integrity
- `EVAL-STRUCT-005` - lifecycle correctness
- `EVAL-STRUCT-006` - profile correctness
- `EVAL-STRUCT-007` - traceability completeness
- `EVAL-STRUCT-008` - projection budget
- `EVAL-STRUCT-009` - module and interface ownership
- `EVAL-STRUCT-010` - stale edge validity

Semantic checks:
- `EVAL-SEM-001` - requirement to story coverage
- `EVAL-SEM-002` - story to entity coverage
- `EVAL-SEM-003` - entity and invariant necessity
- `EVAL-SEM-004` - workflow completeness
- `EVAL-SEM-005` - boundary sanity
- `EVAL-SEM-006` - context slice sufficiency
- `EVAL-SEM-007` - import confidence review
- `EVAL-SEM-008` - local bugfix path correctness
- `EVAL-SEM-009` - derived artifact restraint
- `EVAL-SEM-010` - projection restraint

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

Template loading rule:
- load only the target template or templates needed for the requested generation step

## Generation Rules

- Generate only the requested artifact or the next valid artifact implied by the command.
- Load only the target templates needed for that generation step.
- Use the smallest safe upstream slice.
- Preserve IDs when regenerating an existing governed artifact unless a human-approved semantic change requires a new item.
- Do not present `AGENTS` or `plan` as canonical.

### Generation Cascade After Approval

See `references/routing-and-loading.md` § "Post-Intent Approval: Sequential Product Generation" for the full cascade sequence and batch-approval rules.

## Eval Rules By Command

| Command | Required eval behavior |
| --- | --- |
| `approve ...` | Run structural checks first, then semantic checks on the selected approval target; block approval on structural failure |
| `eval ...` | Run structural and semantic checks on the selected eval target and return findings without approval |
| `generate ...` | Use templates, then run structural checks on generated output |
| `develop ...` | Run targeted structural and semantic checks on the touched slice after proposed changes |
| `fix ...` | Run targeted structural and semantic checks on the affected slice after regression framing |

## Detailed Eval Help

Use `help evals` for the full structural and semantic check definitions.
