<!--
VibeLoom task template: generate-code-component
Operation: generate (per-component code generation, the leaf task in the dispatch plan)
Invoked by: SKILL.md as a subagent task within a wave; one invocation per affected component
-->

# Task: generate-code-component

## Purpose

Generate or repair the code for one component, with bounded write scope, layer-aware codegen patterns, and full validation contract.

## Inputs

- `task_id`, `run_id`, `wave_id`, `template_version` (from subagent task header — see canonical implementation §13.4)
- `scope`: the target component, e.g. `web/search` or `notes-service/notes`
- `component_id`: CMP-#### of the target
- `container_id`, `layer`: from container.md frontmatter (drives codegen pattern)
- `load_set_refs`: items the subagent receives in its load (baseline + owned scope + foreign IF slices + relevant context)
- `foreign_refs`: IF-#### contracts of dependencies (read-only — never used to expand write scope)
- `allowed_read_paths`: globs the subagent may read
- `allowed_write_paths`: globs the subagent may write (always disjoint from other subagents in the same wave)
- `validation_contract`: list of runner_ids the orchestrator will invoke against the subagent's output
- `result_shape_id`: expected shape of the subagent's return (for orchestrator validation)
- Approved upstream: full contract for the component's lineage (CAP → FR → STORY → BC → CMP).
- Tech stack inherited from defaults.md (per layer).

## Preconditions

- `system-specs` is `approved` for the target component.
- `context` is generated and current for the component.
- Container's `layer` field is set.
- Validation registry declares the runners listed in `validation_contract`.

## Steps

1. Load the load set (baseline + owned scope + foreign IF slices + relevant context).
2. Read the container's `layer` to determine the codegen pattern:
   - **presentation**: generate UI components, pages, routes, design-token usage. Bundle target per Tech Stack.
   - **application**: generate API surfaces, request/response handlers, orchestration logic. Auth middleware per Tech Stack.
   - **domain**: generate aggregate roots, entity classes, value objects, domain events, repository interfaces. Persistence pattern per Tech Stack.
   - **infrastructure**: generate IaC declarations (Terraform / Pulumi / CDK / native). NOT application code.
3. For each owned interface (IF-####) in the component:
   - Generate the implementation respecting the contract (signature, behavior described in BEH-####).
   - Emit code in the appropriate language per Tech Stack.
4. For each owned behavior (BEH-####):
   - Generate at least one test (unit or integration, per validation registry runners).
   - Tests are evidence of contract conformance, not contract themselves.
5. For each consumed dependency (DEP-####):
   - Reference the foreign component's IF-#### contract from `foreign_refs`. Don't re-implement the foreign contract.
6. Late-fetch ONCE if a narrow missing context slice is discovered (e.g. an IF detail not in the load set). Cap is one re-invocation per task.
7. Write the patch to the staging directory at `.vibeloom/runs/<RUN-ID>/tasks/<TASK-ID>/`.
8. Run all validation runners declared in `validation_contract` inside the staging dir.
9. Return a result conforming to `result_shape_id`: patch summary, file list, validation summary, findings.

## Output

- Patch in `.vibeloom/runs/<RUN-ID>/tasks/<TASK-ID>/patch.diff`.
- Files in `.vibeloom/runs/<RUN-ID>/tasks/<TASK-ID>/files/`.
- Summary in `.vibeloom/runs/<RUN-ID>/tasks/<TASK-ID>/summary.yaml`.
- Validation results.
- Late-fetch event recorded in the parent generation trace if used.

## Constraints

- Writes are STRICTLY confined to `allowed_write_paths`. Writing outside is a hard violation.
- Reads are confined to `allowed_read_paths`. Reading outside is a soft violation surfaced as a finding.
- Late-fetch is bounded to ONE re-invocation per task. Exceeding the cap returns a failure result.
- The codegen pattern matches the layer (e.g. don't generate database schemas in a presentation container).
- Tech stack choices from defaults are binding. Don't substitute (e.g. don't generate Vue when defaults specify React).
- Any decision the subagent makes that constrains future generation MUST be emitted as a `decision` trace entry with `record_type: ADR` (or appropriate other) and `affects: [item_ids]`.

## Validation

- All runners in `validation_contract` MUST pass before patch is applied to working tree.
- Layer-aware structural checks: no presentation→domain calls (must go through application).
- Patch is rejected (subagent task fails) if any blocking validation fails.
- Cross-scope consistency check by orchestrator after the wave completes: do IFs match across scopes? do dependencies resolve? are BDD scenarios still satisfied?

## Failure modes

- Validation runner fails: patch is rejected; subagent surfaces finding; orchestrator reopens the component for another pass with the failure as additional input.
- Write outside allowed_write_paths: subagent surfaces error; task fails immediately; orchestrator escalates to user.
- Late-fetch limit exceeded: subagent fails the task with a "context insufficient" finding for human review.
- Stack constraints violated: subagent fails; orchestrator reopens with explicit stack reminder.
- Foreign IF contract changes during the run (concurrent change): wave fails; orchestrator restarts wave from current basis.
