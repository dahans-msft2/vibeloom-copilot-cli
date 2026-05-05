<!--
VibeLoom task template: review
Operation: review
Invoked by: SKILL.md when user runs `/vibeloom review <target>`
-->

# Task: review

## Purpose

Interactive findings loop on a single target. Surface eval findings; propose bounded fixes; user approves, edits, or rejects each; iterate until target is clean. `review` fixes the target only — it does NOT propagate changes downward (that's `generate` after approval).

## Inputs

- `<target>`: required. A specific tier (e.g. `intent-specs`) or scope (e.g. `web/search`).
- Findings from a prior `eval` invocation (or eval is invoked first if findings absent).

## Preconditions

- Target exists and is in `draft` status (review on `approved` items first auto-reopens to draft, surfacing the implication for downstream).

## Steps

1. Run `eval` on target to surface current findings.
2. Build a **review packet**:
   - Changed item IDs in scope.
   - Upstream basis (the items this target derives from).
   - Findings (blocking and advisory).
   - Proposed bounded fixes (one per finding when possible).
   - Downstream impact preview (which downstream items will become stale if this target changes).
   - Recommendation summary.
   - Evidence and trace pointers.
3. Present the packet to the user (one finding at a time or batched, per UX preference).
4. For each finding, the user picks:
   - **Accept proposed fix** → apply patch to target.
   - **Edit fix** → user provides their own patch.
   - **Defer** → mark finding as deferred (kept in trace but not blocking this review pass).
   - **Reject (mark advisory→ignored)** → record decision trace explaining why.
5. After each accepted/edited fix, re-run eval on the affected sub-scope.
6. Loop until no blocking findings remain (or user explicitly stops with deferred findings noted).
7. Emit a `generation` trace recording the review patches as a kind of in-place generation.
8. Recommend next operation: `approve <target>` if clean, or `reconcile <target>` if drift was detected during review.

## Output

- Target artifact updated (status: still draft).
- Eval trace entries for each iteration.
- Generation trace entry for the cumulative review patches.
- Decision trace entries for any deferred / ignored findings (record_type=`general` typically).

## Constraints

- `review` fixes the TARGET ONLY. Downstream is not regenerated until `generate` is invoked after approval.
- The review packet is the bounded human review surface — the user should not need to read raw whole artifacts unless they choose to drill down.
- Packet is write-capable: the user can add their own findings, modify recommendations, or note context.
- Don't auto-apply fixes without explicit user accept (codæ principle: agents propose; humans approve).

## Validation

- After each fix iteration, structural eval runs immediately.
- Heuristic eval runs once at the end of the review (not per iteration — too costly).
- `review` does NOT invoke mechanical runners on code (review is for contract-tier targets; code-tier review uses `reconcile` instead).

## Failure modes

- Findings are all blocking and proposed fixes are all rejected: surface "review cannot complete; consider `reconcile <target>` to negotiate direction."
- User edits a fix in a way that introduces NEW findings: surface them on the next iteration; loop continues.
- Target has no findings at all: complete immediately; recommend `approve <target>`.
