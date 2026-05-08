# Review the skill

A prompt for Claude Code (or any equivalent agentic coding tool). Reads the skill bundle (canonical source: `vibeloom-templates.md`) and runs an interactive review loop with the user — surfacing findings, proposing bounded fixes, applying or deferring per user direction.

This prompt is itself codæ-shaped and reuses the interactive loop from [`tasks/review.md`](vibeloom-templates.md). The criteria the agent surfaces against live in **§ Review checklist** below — that's the human-editable surface.

**Time budget.** Half-day; ~2–4 min per finding.

---

## Purpose

Audit the skill bundle — every fenced block under `vibeloom-templates.md` (SKILL.md, references, task templates, artifact templates) — against the **Review checklist** below. Apply changes in place via the interactive loop. Recommend the next operation (re-extract templates? re-run [`build-skill.md`](build-skill.md)?).

## Inputs

| Source | Role |
|---|---|
| `v03/vibeloom-templates.md` | **Canonical** — every template, reference, and SKILL.md lives here as a fenced block. Edits land here, not in the extracted tree. |
| `v03/templates/` (if extracted) | Extracted state. Read-only during this review. Useful for spot-checking `extract-templates.py` output. |
| `v03/vibeloom-methodology.md` | Source of truth for paradigm vocabulary and operations the skill must support |
| `v03/vibeloom-implementation.md` | Source of truth for engine behavior the skill orchestrates against |

Canon is **read-only**. Skill contradictions are skill bugs (Category B). Canon issues belong in [`review-canon.md`](review-canon.md).

## Preconditions

- `v03/vibeloom-templates.md` exists and parses (fenced blocks well-formed).
- `v03/vibeloom-methodology.md` and `v03/vibeloom-implementation.md` exist (read-only).
- Working tree is clean (recommend a checkpoint commit).
- The user is committing time for an interactive session.

## Architecture sketch — skill bundle layout

```text
vibeloom-templates.md   (canonical fenced blocks)
        │
        ├── skill/SKILL.md           ← entry point: command routing, manifest
        ├── skill/references/        ← reference docs the agent late-fetches
        ├── tasks/                   ← per-operation task templates (10-section codæ)
        └── artifacts/               ← per-tier artifact templates with frontmatter
```

Every command in `SKILL.md` routing must point at a real task template. Every task template must reference its source operation in `vibeloom-implementation.md` §15. Every artifact template must match the frontmatter shape in `vibeloom-implementation.md` §6.

## Steps

1. **Read the skill bundle + skim the canon.** (a) Skill only — `SKILL.md` first (command routing as the index), then references, then tasks, then artifact templates. (b) Canon — refresh on impl §6 (artifact frontmatter), §8 (trace schemas), §13 (dispatch), §15 (operation pseudocode). (c) Cross-walk: for every command in SKILL.md, locate its task template; for every task template, locate its impl §15 source; for every artifact template, locate its impl §6 frontmatter shape.
   **Verify:** write `skill-coverage-map.md` at repo root with three tables: (1) command → task template, (2) task template → impl §15 operation, (3) artifact template → impl §6 frontmatter. Empty cells are Category A findings.

2. **Build the skill review packet.** Walk every item in the **Review checklist** below. For each surfaced finding: location (file + fenced-block name + section), current text (verbatim quote), why it's a finding, proposed bounded fix (concrete diff against the fenced block in `vibeloom-templates.md`), affected templates if the fix cascades.
   **Verify:** `skill-review-packet.md` at repo root.

3. **Surface the packet to the user as a summary first** — counts by severity, total findings, estimated walk-time. Confirm scope.

4. **Walk findings in priority order.** For each:
   - Quote location + current text.
   - Explain why.
   - Propose the fix.
   - User picks: **Accept** / **Edit** / **Defer** / **Reject**.
   - On Accept / Edit: apply to `vibeloom-templates.md`, log, move on.
   - On Defer / Reject: log + rationale, move on.
   - After every batch (default: one per template, OR every 5 fixes): re-verify the coverage map (Step 1 verify) to surface any new gaps the edit may have introduced.

5. **After all findings: re-walk the full Review checklist on the full skill bundle.** If `extract-templates.py --check` is available, run it to confirm `vibeloom-templates.md` is internally well-formed.

6. **Produce `skill-review-report.md`** per § Final report.

## Review checklist

**This is the human-editable surface — adjust bullets as project priorities shift.** The agent surfaces a finding for any item that fails on inspection.

### A — Coverage gaps (HIGH)

- Every command in `SKILL.md` routing has a task template.
- Every operation in `vibeloom-implementation.md` §15 has a realizing task template.
- Each of the five modes (`vibe`, `pm`, `dev`, `ux`, `expert`) has a coherent path through the templates (init, generate, etc. all support the mode).
- Every artifact tier in canon has a corresponding artifact template.

### B — Spec misalignment (HIGH)

- No skill template asserts behavior the implementation doesn't deliver.
- Every artifact template's frontmatter has only fields that exist in impl §6 (no extras, no missing required).
- No task template's Validation or Constraints cite behavior diverging from impl semantics.
- Every trace shape produced by a task template matches impl §8.
- Every operation referenced by name uses the canonical name (e.g. `regenerate`, not the older `recompile`).

### C — Template completeness (MEDIUM)

- Every task template carries all 10 codæ sections (Purpose / Inputs / Preconditions / Steps / Output / Postconditions / Constraints / Invariants / Validation / Failure modes).
- No task template has placeholder or TODO Steps.
- Every task template's Steps include a verify gate.
- No reference template is orphaned (each must be cited by at least one task template).
- No reference template summarizes the canon without adding skill-specific operational detail.

### D — Inter-template consistency (MEDIUM)

- Vocabulary aligned across templates (one term, one meaning — e.g. always "approval unit", never "approval scope").
- Section ordering consistent across parallel templates.
- Example shapes consistent across templates (all example traces use the same shape; all example packets use the same shape).
- Late-fetch budget assumptions consistent (or with explicit per-template rationale where they differ).
- Tone consistent across parallel templates (all prescriptive OR all suggestive — not mixed for templates that do parallel work).

### E — Clarity / writing (LOW)

- Long Steps split where natural.
- Step "what to do" separated from "why."
- Verify gates specific, not vague ("the result should look right" → concrete check).
- Failure modes actionable, not generic.

### F — Test scenarios (DEFERRED)

- Coverage of mode + operation combinations (vibe-init, pm-generate, ux-import, expert-reconcile, etc.).
- Coverage of edge cases (init in non-empty dir, approve on already-approved item, generate with no approved upstream).
- **Note:** behavioral testing is the job of `test-skill.md`, which doesn't exist yet — it requires a working engine (v0.4+). Surface scenario gaps here as informational; defer the actual test build until the engine ships.

## Output

- Edits applied in place inside `vibeloom-templates.md` (per Accept / Edit decisions).
- `skill-coverage-map.md` — three coverage tables (Step 1 verify).
- `skill-review-packet.md` — Step 2 verify.
- `skill-review-report.md` — final disposition + recommended next operation.

## Postconditions

- Every checklist item walked; every finding resolved with rationale logged.
- Coverage map shows no empty cells (or any remaining are flagged as deferred with rationale).
- `vibeloom-templates.md` parses; `extract-templates.py` (if present) produces a clean tree.

## Constraints

- **Edits land in `vibeloom-templates.md`, not in the extracted tree.** Extracted tree is a build artifact; editing it is futile.
- **Agents propose; humans approve.** Never auto-apply a fix.
- **Canon is the source of truth.** Skill contradictions are skill bugs; flag for [`review-canon.md`](review-canon.md) if the canon needs to change.
- **Coverage before clarity.** Walk High before Low.
- **Don't invent new commands or operations the canon doesn't sanction.** If a finding suggests a missing capability, surface as "needs canon support."
- **Late-fetch policy is part of skill quality** — templates that exceed the budget or fail to surface "context insufficient" are findings (Category D).

## Invariants

- Every command in `SKILL.md`'s routing block resolves to a real task template.
- Every task template carries the codæ 10-section structure.
- Every artifact template's frontmatter matches `vibeloom-implementation.md` §6.
- Every reference is cited by at least one task template.
- Vocabulary in skill templates matches methodology vocabulary.

## Validation (exit gates)

- Every Review-checklist item considered (or explicitly skipped, recorded in report).
- Every accepted/edited finding applied to `vibeloom-templates.md` in place.
- Coverage map refreshed and clean (or deferred items rationalized).
- `extract-templates.py --check` passes (if available).
- Final report produced.
- Reference commit SHA at session end.

## Failure modes

- **Skill template asserts behavior the engine doesn't implement.** Two paths: (a) edit template to match impl, or (b) flag for impl change via [`review-canon.md`](review-canon.md). User picks.
- **Coverage gap that requires net-new template content.** Out of scope. Flag as "needs `build-skill.md` re-run after canon stabilization."
- **User wants a major template restructure.** Out of scope. Note; recommend a separate design pass.
- **Cascading impact too large** (>10 dependent findings on one accepted edit). Pause; recommend batched decisions.
- **`vibeloom-templates.md` failed to parse.** Stop the review; surface parse error; user fixes; resume.

## Anti-patterns

- Editing the extracted `templates/` tree instead of `vibeloom-templates.md`.
- Auto-applying any fix.
- Inventing new commands or operations the canon doesn't sanction.
- Skipping the coverage-map verify after edits — coverage can regress.
- Suggesting "consider rephrasing" without the actual rephrasing.
- Treating reference orphans as ignorable (orphans signal either dead reference or missing citation).

## Final report

`skill-review-report.md` at repo root:

1. **Summary table:** N findings; M applied, K modified, D deferred, R rejected; by Category × Severity.
2. **Coverage map:** the three tables, refreshed after edits — every cell now filled (or flagged as deferred).
3. **Per-finding detail.** ID (`SKILL-FIND-001`…), location (fenced-block name + section), severity, category, current quote, why, proposed fix, user decision, applied diff (if Edit), rationale (if Defer/Reject), `affected templates: [...]`.
4. **Cross-cutting re-walk results.**
5. **Items flagged for canon update:** input for the next [`review-canon.md`](review-canon.md) session.
6. **Deferred items**, including all Category F (test scenarios) as future inputs to `test-skill.md`.
7. **Recommended next operation:** re-extract templates only? Re-run [`build-skill.md`](build-skill.md)? Schedule [`review-canon.md`](review-canon.md) first?
8. **Reference commit SHA** at session end.

## Checkpointing

Commit after each batch — group by template or category (e.g. `skill: tasks/generate.md — coverage`).

## After this review

- If findings flagged for canon update, schedule [`review-canon.md`](review-canon.md) first.
- If no canon-side cascades, re-run `extract-templates.py` to materialize the updated bundle, then re-run [`build-skill.md`](build-skill.md) for a fresh skill release tarball.
- **Once engine v0.4 ships,** graduate deferred Category F findings into a new `test-skill.md` prompt that drives behavioral testing on a scratch repo.
