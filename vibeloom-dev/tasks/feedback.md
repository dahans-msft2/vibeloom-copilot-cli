# Task: feedback

Critique a peer agent's eval. Reads the peer's eval file, evaluates the findings, writes a critique to a peer-specific feedback file. Does NOT modify any artifacts. Eval-only in v1.

## Purpose

- Capture the value of a second perspective on the same canon/skill/site.
- Surface: what the peer got right (agree + amplify), what the peer got wrong (disagree + counter-evidence), what the peer missed (new findings the peer overlooked), where the peer's framing could be sharpened.
- Independent of consensus/synthesize — feedback is a critique, not an attempt to merge.

## Inputs

- `<peer>` (required) — the agent name whose eval you're critiquing (e.g., `claude`, `codex`, or whatever name appears in the peer's `reports/eval-<target>-<peer>.md` file). The current agent (self-identified per `references/multi-agent.md`) is the AUTHOR of the critique.
- `<target>` (required) — the target whose eval is being critiqued: one of `canon`, `intent`, `manifesto`, `methodology`, `implementation`, `skill`, `site`.
- `--version <vNN>` (optional, default = latest mutable).

## Preconditions

- The peer's eval file exists: `reports/eval-<target>-<peer>.md`.
- The current agent's own name is resolvable per `references/multi-agent.md` AND is different from `<peer>`.
- `reports/` directory exists.

## Steps

0. **Resolve own agent name.** Per `references/multi-agent.md`:
   1. If `VIBELOOM_AGENT_NAME` env var is set, use it.
   2. Else if the skill install has a hardcoded name, use it.
   3. Else ask the user: "What lowercase, hyphenated name should I use to identify my outputs in this repo? (e.g., `claude`, `codex`, `cursor`, `gemini`)". Use the answer for the session.
   Bind this to `<self>` for the rest of the task.

0.5. **Ensure `reports/` exists.** Run `mkdir -p reports/` from the repo root. Idempotent; gitignored per `/file-layout.md §5`.

1. **Validate distinctness.**
   - If `<self>` equals `<peer>`, halt: "You're <self> giving feedback on <self>'s own eval — that's a self-review, not cross-agent feedback. Use `eval <target>` to re-eval, or specify a different peer agent."

2. **Load peer's eval file.** `reports/eval-<target>-<peer>.md`. Parse findings into a list.

3. **Independently re-read the target.**
   - Resolve target → file list (same logic as `eval`).
   - Read the target files. Form your own model of the artifacts. Don't anchor purely on peer's findings.

4. **For each peer finding,** assess:
   - **Agree (+amplify)**: this finding is real; here's additional supporting evidence or a sharper way to state it.
   - **Agree (verbatim)**: this finding is correctly stated; nothing to add.
   - **Disagree (false positive)**: this finding is not real; here's the counter-evidence from the artifact.
   - **Disagree (severity wrong)**: the issue is real but the peer over- or under-rated severity; explain.
   - **Disagree (framing wrong)**: the issue points at something real but the peer's analysis misframes it (e.g., blamed the wrong file, conflated two issues); reframe.
   - **Partially agree**: real issue, but the peer's proposed fix is wrong; counter with a better fix.

5. **Generate new findings** the peer missed.
   - From your independent read in step 3, identify issues the peer didn't surface.
   - Format each per the eval finding quality bar (id, severity, location, issue, why, fixes, recommended, verification, downstream).
   - Use ids like `MISS-001`, `MISS-002` to distinguish from peer findings (which keep their original ids).

6. **Identify synthesis opportunities.**
   - Where multiple peer findings + your new findings cluster around the same root cause, note it.
   - Where peer's framing + your reframing could combine into a stronger statement, note it.
   - Don't actually write the synthesis (no consensus.md in v1) — just flag the opportunities.

7. **Write the feedback file** to `reports/feedback-<target>-<self>-on-<peer>.md`. Overwrite any existing.

   File structure:
   - Frontmatter: `self: <self>`, `peer: <peer>`, `target: <target>`, `version: vNN`, `date: <ISO timestamp>`.
   - **Summary of agreement** — % of peer findings you agree with, top 3 you most strongly agree with.
   - **Disagreements** — list, each with reason.
   - **New findings** (MISS-* ids) — full eval-format findings.
   - **Synthesis opportunities** — clusters / reframings to consider when (or if) consensus is built.

8. **Print summary to user.**
   - File written.
   - Counts: peer findings reviewed, agreed with, disagreed with, partially agreed; new findings added.
   - Suggested next: open the feedback file, then "you may also want to run `feedback <self> <target>` in <peer> for the reverse direction" OR "you have enough perspective — review the canon decisions yourself."

## Output

- `reports/feedback-<target>-<self>-on-<peer>.md`.
- A printed summary.

## Postconditions

- No artifact under `vNN/` is modified (feedback is read-only on artifacts).
- The feedback file exists and is well-formed.
- No peer file is modified (we only read peer's eval; we don't edit it).

## Constraints

- **Critique, not consensus.** Feedback states one author's view on the peer's eval. It does not produce a merged or agreed-upon list. (Synthesize / consensus is a deferred command for later versions.)
- **Independent re-read.** Step 3 is critical — don't just critique the peer's findings in isolation; form your own view from the artifact first. This catches misses.
- **Be specific.** "I disagree with finding CANON-005" is not feedback. Cite the artifact evidence that supports your disagreement.
- **No artifact edits.** Feedback proposes nothing for application. The user decides what to do with the perspectives.

## Invariants

- The feedback file's `self` field equals `<self>` (resolved in Step 0).
- The `peer` field equals the `<peer>` argument.
- For every peer finding id, there's a corresponding assessment in the feedback file (agree / disagree / partially agree).
- For every MISS-* finding, the finding meets the eval quality bar.

## Failure modes

- **Peer file not found.** Halt: "No eval from <peer> for <target>. The peer needs to run `vibeloom-dev eval <target>` first."
- **Peer file malformed.** Halt: "Peer's eval file at <path> doesn't parse. Show the user the parse error; they may need to ask the peer to re-eval."
- **`<self>` equals `<peer>`.** Halt per step 1.
- **Target files have changed since peer evaluated.** (User edited canon between eval and feedback.) Surface to user: "Target has changed since peer's eval. My critique will be against the current state, not the state peer evaluated. Proceed? (y/n)". Default: proceed but note in the feedback file's frontmatter.

## Validation gates

- After step 7: feedback file is valid markdown with required frontmatter and sections.
- The filename matches pattern `feedback-<target>-<self>-on-<peer>.md`.
- Every peer finding id appears in the file's "Summary of agreement" or "Disagreements" section (no peer finding is silently dropped).
- Every MISS-* finding has all eval-format fields.
- `git status --short reports/` shows only the new/updated feedback file.
