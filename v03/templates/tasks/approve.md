<!--
VibeLoom task template: approve
Operation: approve
Invoked by: SKILL.md when user runs `/vibeloom approve <approval-unit>` (where approval-unit = one contract tier: intent-specs, product-specs, ux-specs, system-specs)
-->

# Task: approve

## Purpose

Advance a reviewed contract approval unit from `draft` to `approved`. Records an approval trace capturing per-item content fingerprints, which becomes the basis for subsequent drift detection.

## Inputs

- `<approval-unit>`: required. One contract tier: `intent-specs | product-specs | ux-specs | system-specs`.
- `--mode` (optional): `user` or `delegated` (engine fills in based on current mode + tier ownership rules).
- Approval-unit artifacts at `draft` status with structural eval clean.

## Preconditions

- Approval unit exists.
- All artifacts in the approval unit are `draft` (or already `approved` — in which case approve is a no-op).
- Structural eval passes (decidable tier of verification ladder).
- All blocking findings from semantic eval are addressed (no `blocking` findings remain in the most recent eval trace).
- For mode-delegated approval: current mode allows delegated approval for this tier (e.g. system-specs in pm mode auto-advances when conditions met).

## Steps

1. Run `eval --target <approval-unit>` to confirm clean.
2. If any blocking finding: abort, surface "approval cannot proceed; address findings first via review."
3. Compute per-item content fingerprints (SHA-256 canonical hashes) for every IDed item in the approval unit.
4. Compute per-artifact hashes alongside items.
5. Append an `approval` trace entry to .vibeloom/traces/approvals.jsonl with:
   - approval_unit (the tier)
   - approval_mode (user or delegated)
   - items: { item_id: hash } per IDed item in the unit
   - artifacts: { artifact_id: hash } per artifact in the unit
   - run_id, timestamp, author
6. Update each artifact's frontmatter status from `draft` to `approved`.
7. Refresh contract graph cache.
8. If auto-advance is configured for the next tier in current mode (and structural + semantic eval would pass for it), automatically invoke the next `generate-*` task.

## Output

- Each artifact in the approval unit: status updated to `approved`.
- New approval trace entry in .vibeloom/traces/approvals.jsonl.
- Contract graph cache refreshed.
- (Optional) Auto-advance kicked off for next tier.

## Constraints

- Approval is per-tier (the approval unit). Affected artifacts within the tier advance together. Cannot approve a single artifact in isolation.
- Approval requires all-clean structural + zero-blocking-semantic findings. False positives in advisory findings don't block.
- Approval traces are append-only and never regenerated. They are the single source of truth for "what was approved when by whom."
- Auto-advance is bounded by mode rules: e.g. in pm mode, system-specs auto-advances when its eval is clean and no breaking semantic finding is detected. Auto-advance never happens for user-owned tiers.
- Direct edits to `approved` artifacts (outside this task) auto-reopen them to `draft` per lifecycle drift rules.

## Validation

- Pre-approval: structural + semantic eval (run as part of step 1).
- Post-approval: re-run structural eval after status flips, to catch any inconsistency introduced by the approval itself (rare but possible).
- Mechanical runners not invoked at approval time (they run at generate / code-sync time).

## Failure modes

- Blocking findings: abort, surface "review first."
- Hash computation fails (non-deterministic content): surface error; user must address (typically a frontmatter formatting issue).
- Auto-advance trigger fires but the next tier has its own findings: surface findings + halt auto-advance; user resolves.
- Concurrent edit during approval (artifact mtime changes between hash and write): abort with "concurrent edit detected; re-run approve."
