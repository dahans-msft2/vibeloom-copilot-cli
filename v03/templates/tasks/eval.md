<!--
VibeLoom task template: eval
Operation: eval
Invoked by: SKILL.md when user runs `/vibeloom eval [--target <tier>]` or as part of generate / approve preconditions
-->

# Task: eval

## Purpose

Read-only validation of a target against approved upstream truth across the verification ladder. Produces findings; modifies nothing.

## Inputs

- `--target` (optional): tier or specific scope to eval (e.g. `intent-specs`, `product-specs`, `web/search`). Default: full repo.
- Approved contract via .vibeloom/cache/contract-graph.json + .vibeloom/traces/approvals.jsonl.
- Validation registry at validation-registry.md.

## Preconditions

- `.vibeloom/cache/contract-graph.json` exists or can be rebuilt.
- For mechanical-tier checks: validation runners in registry are executable.
- For heuristic-tier checks: agent has access to the items in scope.

## Steps

1. Build/refresh contract graph via engine `parse + graph`.
2. **Decidable tier (engine, structural)**: run all structural checks for target — lifecycle consistency, required fields, ID validity & registry consistency, reference integrity, tier-order/DAG validity, coverage, dangling references, ownership rules (including layer-aware: hosted_bounded_contexts must be empty in non-domain components), context sufficiency.
3. **Mechanical tier (engine + runners)**: invoke validation runners declared in registry that are in scope for the target. Aggregate pass/fail per runner.
4. **Heuristic tier (agent, semantic)**: agent runs heuristic dimensions against items in scope — faithful representation, naming consistency, implicit dependency detection, capability gaps, UX/product mismatch, mockup extraction gaps, target-platform mismatch.
5. Categorize findings: `blocking` (must address before approval) or `advisory` (worth noting, not gating).
6. Emit an `eval` trace per invocation: target, checks_run, findings (each with finding_id, severity, item_id, message), cost.
7. Return aggregated findings to caller (or surface to user if invoked directly).

## Output

- Eval trace in `.vibeloom/traces/evals.jsonl`.
- Findings list (blocking + advisory).
- Non-zero exit code if any blocking findings.

## Constraints

- Read-only — modifies no artifacts and no traces other than appending to evals.jsonl.
- False positives beat false negatives: prefer over-marking to under-marking.
- Heuristic findings are agent-judged; ambiguous cases escalate as blocking by default.
- Mechanical runners run with their declared scope; runners outside the target are skipped.

## Validation

- N/A (eval is itself the validation).

## Failure modes

- Engine parse fails: surface parse errors first; halt before structural checks.
- A mechanical runner times out: surface as advisory; the rest of the runners proceed.
- Heuristic eval cost exceeds budget: surface advisory ("eval truncated due to context budget"); the rest of decidable + mechanical results stand.
