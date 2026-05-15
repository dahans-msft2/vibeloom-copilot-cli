# Task: review

Interactive walk of findings from `eval`. Per finding, present the proposed fix(es), recommend one, wait for user decision, apply on Accept. Never auto-applies.

## Purpose

- Convert a static findings packet into actual edits to canon/skill/site/intent.
- Use the codæ pattern: agent proposes (with rationale and alternatives), human approves (per-item, never batched without confirmation).
- Support just-in-time variant generation: if the agent recognizes genuine ambiguity in how to fix a finding, it can offer 2-3 fix variants during the interactive loop (variants live in LLM context, not on disk).

## Inputs

- `<target>` (optional, default `canon`) — the target whose findings to walk.
- `--version <vNN>` (optional, default = latest mutable).
- Self-identified: the running agent's name (only for "which findings file to read" — see preconditions).

## Preconditions

- A findings file exists in `reports/` for this target and the current agent: `reports/eval-<target>-<this-agent>.md`.
- If the user wants to walk the OTHER agent's findings instead, they pass `--findings reports/eval-<target>-<other-agent>.md` (optional flag).
- Working tree may have unrelated dirty changes. Capture `git status --short` before starting; don't revert unrelated work.

## Steps

1. **Load the findings file.** Default: `reports/eval-<target>-<this-agent>.md`. Parse into a list ordered by severity then by id.

2. **Print walk summary.** "About to walk N findings: X Critical, Y High, Z Medium, W Low. We'll go in priority order. You can stop anytime — say 'pause' to save state and exit." (No persistent state to save in v1; saying 'pause' just exits cleanly.)

3. **For each finding** (in priority order):

   a. **Display.** Show: id, severity, location, issue, why it matters, downstream impact.

   b. **Present fix options.** Show the proposed fixes from the findings file (the eval already produced 1-3). If, on reading the finding in detail, the agent sees a better way to slice the fix space (e.g., "the eval proposed one fix but there are actually two distinct approaches"), it can extend the variants to 2-3 just-in-time. Per `references/vocabulary.md`, the user's available actions are:
      - **Accept variant N** (apply the chosen fix patch to the target artifact)
      - **Edit** (user provides their own patch)
      - **Defer** (skip this finding; record decision; move on)
      - **Reject** (mark not-a-bug or advisory→ignored; record decision; move on)

   c. **Show the recommended action.** One of the variants OR Edit OR Reject, with one-paragraph rationale. (Defer is never recommended — agents recommend a fix or rejection, not avoidance.)

   d. **Wait for user decision.** No timeout. If the user wants to discuss or modify the recommendation, do so before applying.

   e. **On Accept variant N:**
      - Apply ONLY the patch for that variant. Use the Edit tool — never Write the whole file, never auto-format unrelated areas.
      - Show the user the diff that was applied.
      - **Verify the patch landed cleanly** (the target file still parses, doesn't have garbage left over from an Edit collision).

   f. **On Edit:** the user provides their own patch (either inline or by pointing to a file they just edited manually). Show the diff. Skip the apply step (user already did it).

   g. **On Defer / Reject:** record the decision verbally in the response (no persistent decision file in v1).

   h. **After every 5 accepted/edited fixes,** suggest the user run `vibeloom-dev eval <target>` again to see if those fixes resolved related findings or introduced new ones. Don't auto-rerun; just suggest.

4. **At end of walk:**
   - Print a disposition summary: N findings walked, X accepted, Y edited, Z deferred, W rejected.
   - List the deferred items so the user has them.
   - Suggest next: `git diff` to inspect, `git add ... && git commit`, then potentially `vibeloom-dev eval <target>` for a sanity re-run, OR `vibeloom-dev generate <downstream-target>` if upstream changes warrant regenerating downstream.

## Output

- Modified files under `vNN/canon/`, `vNN/skill/`, `vNN/site/`, or `vNN/intent.md`, per the accepted fixes.
- A printed walk summary.
- No new persistent files (decisions are not persisted in v1).

## Postconditions

- Every accepted/edited fix has been applied as a single, scoped edit.
- The user has seen every finding's disposition (Accept / Edit / Defer / Reject).
- The working tree shows only the accepted edits plus any pre-existing dirty state.

## Constraints

- **Never auto-apply.** Every change requires an explicit user decision per finding. No "accept all Critical" batch mode in v1 (unless the user explicitly asks, "yes, accept all remaining Critical with the recommended fix").
- **Edit, don't Write.** Use scoped edits to avoid touching unrelated parts of the file.
- **Don't reorder findings.** Walk in the priority order from the findings file. (User can ask to skip ahead to a specific id; that's fine. But don't unilaterally reorder.)
- **Don't generate downstream as a side effect.** Even if a fix is "obviously" something that requires regenerating methodology after editing intent, don't do it. `review` only edits the target. Downstream regeneration is `generate <downstream>` followed by `reconcile <downstream>`.
- **Just-in-time variants only.** If the agent generates additional fix variants beyond what the eval proposed, those variants live in conversation, not as disk artifacts.

## Invariants

- After the walk, every finding that was Accept'd has a corresponding diff in the working tree (or was already applied if the user pre-edited).
- No finding is silently skipped — every one gets a Disposition.

## Failure modes

- **Findings file not found.** Halt: "No findings for <target>. Run `vibeloom-dev eval <target>` first."
- **Findings file is malformed.** Halt with the specific parse error and which finding it's in.
- **A proposed fix doesn't apply cleanly** (e.g., the target file changed since eval ran). Halt the loop, show the user the conflict, ask whether to: (a) rerun eval first, (b) skip this finding, (c) let the user manually resolve.
- **The accepted fix introduces a new problem** that the user spots immediately. Revert the patch (the user does this — agent doesn't auto-revert), mark the finding Edit or Defer, continue.
- **The user pauses mid-walk.** Exit cleanly. Tell the user how to resume: "Re-run `vibeloom-dev review <target>` and ask me to skip to <last finding id>."

## Validation gates

- After each accepted fix: target file still parses (HTML files: well-formed; Markdown: still valid; Python: imports cleanly).
- After the walk: `git status --short` shows changes only under `vNN/` (or the agreed target files), no unexpected modifications.
- After the walk: the printed summary's count of Accept/Edit/Defer/Reject equals the total number of findings.
