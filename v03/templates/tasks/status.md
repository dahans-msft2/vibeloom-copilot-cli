<!--
VibeLoom task template: status
Operation: status
Invoked by: SKILL.md when user runs `/vibeloom status` or as preamble to other operations
-->

# Task: status

## Purpose

Read-only report across lifecycle, freshness, coverage, drift, and current mode. Recommends the next operation.

## Inputs

- (none — operates on current repo state)
- `--target` (optional): scope-narrow the report.
- `--verbose` (optional): include per-item detail; default is per-artifact summary.

## Preconditions

- `.vibeloom/cache/contract-graph.json` exists or can be rebuilt.
- `.vibeloom/traces/approvals.jsonl` exists (otherwise: "no approvals yet — run `/vibeloom init` to start").

## Steps

1. Build/refresh contract graph via engine `parse + graph` (cheap if cache is current).
2. Compute per-item status by category:
   - **current**: synchronized to approved basis; no findings.
   - **stale**: downstream depended on changed approved truth.
   - **uncovered**: approved upstream lacks required downstream realization.
   - **dangling**: downstream references a removed upstream item.
   - **drifted**: semantic mismatch, direct edit, or unvalidated divergence.
   - **obsolete**: upstream basis was superseded conceptually.
3. Compute per-artifact lifecycle (draft / approved).
4. Compute coverage: per upstream item, count of downstream items (uncovered if zero in scope-required tier).
5. Compute trace summary: counts per family in current run window.
6. Compute current mode + per-tier ownership.
7. Aggregate into a status report with recommended next operation.
8. Persist status snapshot to `.vibeloom/cache/status.json`.

## Output

- Status report (rendered to user).
- `.vibeloom/cache/status.json` updated.
- Recommended next operation (e.g. "review intent-specs (1 advisory finding)" or "approve product-specs (clean)" or "reconcile code (3 stale, 1 drifted)").

## Constraints

- Read-only — modifies no contract artifacts and no traces.
- May refresh `.vibeloom/cache/` files (status.json, contract-graph.json).
- Status categories are taxonomy from methodology §9 — applied per-item, not per-artifact.
- Recommendation is best-effort; never auto-invokes the recommended operation.

## Validation

- N/A.

## Failure modes

- Cache corrupt: rebuild from artifacts and traces; surface "cache rebuilt" notice.
- Approval traces missing: surface "no approvals — run init" advisory.
- Trace files unreadable: surface integrity warning; status proceeds with reduced fidelity.
