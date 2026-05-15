# Task: review

Interactive walk of findings from `eval`. Per finding, present the proposed fix(es), recommend one, wait for user decision, apply on `preserve_contract`. Never auto-applies. Uses the unified decision vocabulary defined in `references/vocabulary.md`.

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
      - **`preserve_contract: variant-N`** (apply the chosen fix variant to the target artifact)
      - **`amend_contract`** (the finding points at an upstream defect; don't fix the downstream artifact — flag for upstream amendment and revert this artifact if any edit was speculatively applied)
      - **`preserve_existing`** (reject the fix; mark not-a-bug or advisory→ignored; keep current state unchanged)
      - **`user_defined`** (user supplies their own patch, inline or pre-edited)
      - **`defer`** (skip this finding; no decision recorded persistently in v1; move on)

   c. **Show the recommended action.** One of the `preserve_contract: variant-N` options OR `amend_contract`, with one-paragraph rationale. Per `references/vocabulary.md`, recommendations are NEVER `preserve_existing`, `user_defined`, or `defer` — those are user-initiated exceptions, not agent suggestions.

   d. **Wait for user decision.** No timeout. If the user wants to discuss or modify the recommendation, do so before applying.

   e. **On `preserve_contract: variant-N`:**
      - Apply ONLY the patch for that variant. Use the Edit tool — never Write the whole file, never auto-format unrelated areas.
      - Show the user the diff that was applied.
      - **Verify the patch landed cleanly** (the target file still parses, doesn't have garbage left over from an Edit collision).

   f. **On `amend_contract`:**
      - Do NOT modify the target artifact. The finding indicates the upstream is wrong, not the downstream.
      - Print: "Flagged for upstream amendment. Edit `<upstream artifact>` (intent / manifesto / methodology / implementation as applicable), then re-run `generate <downstream>` followed by `reconcile <downstream>`."
      - Continue to next finding.

   g. **On `user_defined`:** the user provides their own patch (either inline or by pointing to a file they just edited manually). Show the diff. Skip the apply step (user already did it).

   h. **On `preserve_existing` or `defer`:** record the decision verbally in the response (no persistent decision file in v1).

   i. **After every 5 applied fixes** (`preserve_contract:variant-N` or `user_defined`), suggest the user run `vibeloom-dev eval <target>` again to see if those fixes resolved related findings or introduced new ones. Don't auto-rerun; just suggest.

4. **At end of walk:**
   - Print a disposition summary: N findings walked, broken down by decision verb: `preserve_contract:variant-N`, `amend_contract`, `preserve_existing`, `user_defined`, `defer`.
   - List the `amend_contract` items — these are the upstream artifacts the user should edit and regenerate from.
   - List the `defer` items so the user has them as TODO.
   - Suggest next: `git diff` to inspect applied fixes, `git add ... && git commit`, then potentially `vibeloom-dev eval <target>` for a sanity re-run, OR `vibeloom-dev generate <downstream-target>` if upstream changes (via `amend_contract` or otherwise) warrant regenerating downstream.

## Output

- Modified files under `vNN/canon/`, `vNN/skill/`, `vNN/site/`, or `vNN/intent.md`, per the `preserve_contract` / `user_defined` decisions.
- A printed walk summary.
- No new persistent files (decisions are not persisted in v1).

## Postconditions

- Every `preserve_contract` / `user_defined` fix has been applied as a single, scoped edit.
- The user has seen every finding's disposition (one of the five verbs from `references/vocabulary.md`).
- The working tree shows only the applied edits plus any pre-existing dirty state.

## Constraints

- **Never auto-apply.** Every change requires an explicit user decision per finding. No "accept all Critical" batch mode in v1 (unless the user explicitly asks, "yes, accept all remaining Critical with the recommended fix").
- **Edit, don't Write.** Use scoped edits to avoid touching unrelated parts of the file.
- **Don't reorder findings.** Walk in the priority order from the findings file. (User can ask to skip ahead to a specific id; that's fine. But don't unilaterally reorder.)
- **Don't generate downstream as a side effect.** Even if a fix is "obviously" something that requires regenerating methodology after editing intent, don't do it. `review` only edits the target. Downstream regeneration is `generate <downstream>` followed by `reconcile <downstream>`.
- **Just-in-time variants only.** If the agent generates additional fix variants beyond what the eval proposed, those variants live in conversation, not as disk artifacts.

## Invariants

- After the walk, every finding with disposition `preserve_contract:variant-N` or `user_defined` has a corresponding diff in the working tree.
- No finding is silently skipped — every one gets exactly one of the five vocabulary-defined dispositions.

## Failure modes

- **Findings file not found.** Halt: "No findings for <target>. Run `vibeloom-dev eval <target>` first."
- **Findings file is malformed.** Halt with the specific parse error and which finding it's in.
- **A proposed fix doesn't apply cleanly** (e.g., the target file changed since eval ran). Halt the loop, show the user the conflict, ask whether to: (a) rerun eval first, (b) `defer` this finding, (c) `user_defined` (user resolves manually).
- **The applied fix introduces a new problem** that the user spots immediately. The user reverts the patch manually (agent doesn't auto-revert), the finding's disposition becomes `user_defined` (user fixed it differently) or `defer` (skipping for now), continue.
- **The user pauses mid-walk.** Exit cleanly. Tell the user how to resume: "Re-run `vibeloom-dev review <target>` and ask me to skip to <last finding id>."

## Validation gates

- After each `preserve_contract:variant-N` or `user_defined` fix: target file still parses (HTML files: well-formed; Markdown: still valid; Python: imports cleanly).
- After the walk: `git status --short` shows changes only under `vNN/` (or the agreed target files), no unexpected modifications.
- After the walk: the sum of dispositions across all five verbs equals the total number of findings.
