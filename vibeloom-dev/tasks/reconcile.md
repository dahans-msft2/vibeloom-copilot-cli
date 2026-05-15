# Task: reconcile

Interactive walk of changes produced by `generate <target>`. Per changed item, present 1-3 variants for what to do with it, recommend one, wait for user decision. Variants are just-in-time (LLM context only; not on disk).

## Purpose

- Let the user steer the just-generated artifact, item by item.
- Surface drift cases where the generation diverged from prior content in ways that may warrant amending upstream instead.
- Apply per-item decisions to produce the final accepted version.

## Inputs

- `<target>` (optional, default `canon`) — typically the target most recently passed to `generate`.
- `--version <vNN>` (optional, default = latest mutable).

## Preconditions

- `generate <target>` has been run recently; the target file(s) have new/updated content in the working tree.
- The user committed (or stashed) before generate; git HEAD is the stable baseline.
- Working tree may have unrelated dirty changes; capture `git status --short` before starting; don't revert unrelated changes.

## Steps

0. **Validate the baseline.**
   - Run `git diff --quiet HEAD -- <target-files>`. If the exit code is 0 (no diff vs HEAD), halt with:
     ```
     No diff vs HEAD for <target-files>. Reconcile has nothing to walk. Possible causes:
       (a) You haven't run `vibeloom-dev generate <target>` yet — run it first.
       (b) `generate` produced output identical to HEAD (rare; nothing to reconcile).
       (c) You didn't commit before `generate`, so HEAD already includes generate's output.
           Check `git log --oneline -5` to see if the most recent commit is a generate output.
           If so, you have two options:
             - Treat HEAD as the new baseline (the reconcile was effectively skipped); proceed to git's normal workflow (review the diff to the parent commit if needed).
             - Reset HEAD to before generate (`git reset --soft HEAD~1`) and re-run reconcile to walk the changes interactively.
     ```
   - Otherwise (diff is non-empty): proceed.

1. **Identify the change set.**
   - Compare current target files vs git HEAD: `git diff HEAD -- <target-files>`.
   - Parse the diff into semantic items: sections added, sections modified, sections removed. An "item" is a methodology section, an implementation subsection, a template fenced block, a site page section, etc. — granularity depends on target.
   - Order items by file → section position.

2. **Print walk summary.** "About to walk N changed items in <target>: A added, M modified, R removed. You can stop anytime — say 'pause' to exit cleanly."

3. **For each item** (in order):

   a. **Display.** Show: item identifier (file + section path), change type (add / modify / remove), the diff.

   b. **Decide variant count just-in-time.** Default: 1 variant (the generated version as-is). If the agent reading the diff sees genuine ambiguity (e.g., "this new section could be structured two different ways that are equally valid"), generate 2-3 variants in conversation. Don't persist variants.

   c. **Present options.** Per `references/vocabulary.md`:
      - **preserve_contract: variant-a** (the as-generated content; always present)
      - **preserve_contract: variant-b**, **variant-c** (only if multi-variant)
      - **amend_contract** (this change indicates upstream needs amendment; reopen the upstream artifact, edit it, then re-generate downstream)
      - **preserve_existing** (reject the generated change; keep what was in git HEAD)
      - **user_defined** (user supplies a custom patch)
      - **defer** (skip; record verbally)

   d. **Show the recommended option** with one-paragraph rationale. Recommendation is a `preserve_contract: variant-*` or `amend_contract` (never `user_defined` or `defer`).

   e. **Wait for user decision.** No timeout.

   f. **Apply the decision** (always per-section, NEVER per-file — see Constraints):
      - **preserve_contract: variant-N (where N=A is "as-generated"):** no-op for variant-A (the file already has it); for variant-B/C, swap the section with the chosen variant using the Edit tool (old_string = current section content; new_string = chosen variant).
      - **amend_contract:** section-scoped revert. Fetch HEAD's content for this section: read `git show HEAD:<file>` and locate the corresponding section by header path. Use Edit tool (old_string = current generated section; new_string = HEAD's section content). Then print: "Reverted. Now amend `<upstream>` first, then re-run `generate <target>` to regenerate downstream."
      - **preserve_existing:** section-scoped revert, identical mechanism to `amend_contract` above (read HEAD section via `git show HEAD:<file>`, Edit-replace) but without the upstream-amend note.
      - **user_defined:** user supplies a patch (inline or by pre-editing). Apply (or skip apply if user did it themselves). Confirm with diff.
      - **defer:** leave the section as-generated in the working tree (user can decide later). No persistent state.

   g. **Verify the apply landed cleanly** (target file still parses).

4. **At end of walk:**
   - Print disposition summary: N items walked, breakdown by decision verb.
   - List `amend_contract` decisions — these are the upstream items the user should edit next.
   - List `defer` items — user has them as TODO.
   - Suggested next: `git diff <target-files>` to inspect final state, then `git add ... && git commit`, then handle `amend_contract` items.

## Output

- Target files in working tree, modified per the user's per-item decisions.
- A printed walk summary.

## Postconditions

- Every changed item has a recorded disposition (visible in the walk summary).
- Target files in the working tree reflect the union of accepted variants + reverted sections + user-defined patches + deferred-as-generated sections.
- No upstream artifact is modified by reconcile (amend_contract just flags; the user does the actual amend afterwards).
- No file outside the target is modified.

## Constraints

- **Just-in-time variants only.** Variants live in the LLM's conversation context. Don't write variant-B/C to disk anywhere. If the user wants to compare two variants more carefully, copy them into the conversation, not into files.
- **Edit, don't Write.** Use scoped edits to modify just the section in question.
- **Per-section revert only — NEVER `git checkout HEAD -- <file>`.** A `preserve_existing` or `amend_contract` decision reverts just THIS section to HEAD content (using `git show HEAD:<file>` + Edit-replace). Whole-file revert would obliterate other sections in the same file that the user has already Accepted, Edited, or `user_defined`'d during this walk.
- **Don't auto-amend upstream.** amend_contract is a NOTE TO USER, not an action the skill takes. Reconcile reverts the downstream section and tells the user what upstream needs editing.
- **Don't reorder items.** Walk in file → section position order.
- **Granularity is the agent's call.** For methodology, items are typically sections (## level). For templates.md, items are fenced template blocks. For site HTML, items are <section>-level blocks. Choose the granularity that lets the user make sensible decisions; don't go too fine-grained (per-paragraph would be exhausting).

## Invariants

- After the walk: every section in the target file is either as-generated (variant-A or unchanged), or replaced with a chosen variant, or reverted to HEAD, or replaced with a user-defined patch.
- No section is in an undecided state.

## Failure modes

- **No diff vs HEAD.** Caught at Step 0. See Step 0's halt message for the three possible causes and remediation paths.
- **Conflicting concurrent edits.** Working tree has both generate's changes AND additional manual edits made after generate. Surface to the user before walking. Ask: "Working tree has manual edits beyond what generate produced. Walk all changes, or only generate's?". Default: walk all.
- **An apply fails** (e.g., the section couldn't be Edit'd because surrounding text changed). Show user the error, ask: skip, revert section, or user-define.
- **The user pauses mid-walk.** Exit cleanly. Remaining items are in the working tree as-generated. Tell user how to resume.

## Validation gates

- After each apply: target file parses (HTML well-formed; Markdown valid; Python imports).
- After the walk: `git status --short` shows changes only in target files (no unexpected modifications).
- After the walk: every item in step 2's list has a disposition recorded in the summary.
