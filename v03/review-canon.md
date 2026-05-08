# Review the canon

A prompt for Claude Code (or any equivalent agentic coding tool). Reads the canonical source-of-truth set and runs an interactive review loop with the user — surfacing findings, proposing bounded fixes, applying or deferring per user direction.

This prompt is itself codæ-shaped and reuses the interactive loop from [`tasks/review.md`](vibeloom-templates.md). The criteria the agent surfaces against live in **§ Review checklist** below — that's the human-editable surface; everything else is the loop machinery.

**Time budget.** Half-day to a day; ~2–5 min per finding.

---

## Purpose

Audit the canonical source-of-truth set — `codæ-manifesto.html`, `vibeloom-methodology.md`, `vibeloom-implementation.md`, `vibeloom-templates.md` — against the **Review checklist** below. Apply changes in place via the interactive loop. Produce a downstream-propagation list naming every derived doc that needs re-sync.

## Inputs

| File | Tier | Question it answers |
|---|---|---|
| `v03/codæ-manifesto.html` | WHY | "why does this paradigm exist?" |
| `v03/vibeloom-methodology.md` | WHAT | "what does the paradigm contain?" |
| `v03/vibeloom-implementation.md` | HOW | "how is the paradigm implemented?" |
| `v03/vibeloom-templates.md` | MATERIALIZATION | "what files / templates / SKILL.md ship?" |

## Preconditions

- All four input files exist; working tree is clean (recommend a checkpoint commit).
- The user is committing time for an interactive session, not a fire-and-forget run.

## Architecture sketch

```text
codæ-manifesto.html        → WHY
        │
vibeloom-methodology.md    → WHAT (tiers, modes, operations, status, traces, eval ladder)
        │
vibeloom-implementation.md → HOW (schemas, IDs, dispatch, trace I/O)
        │
vibeloom-templates.md      → MATERIALIZATION (artifact + task templates, SKILL.md, references)
```

**One fact, one tier.** When a fact appears in two tiers, the **lower** tier (closer to materialization) is canonical; the upper tier should reference, not restate.

## Steps

1. **Read the canon — three passes per doc, in tier order.** (a) Skim §s, copy heading outline. (b) Read each § slowly, mark every fact (definition, schema, rule, invariant, claim) and where it lives. (c) Cross-walk: for each fact, check whether it appears elsewhere and where it should canonically live.
   **Verify:** write `canon-fact-map.md` at repo root listing the major facts and their canonical home tier (one line per fact).

2. **Build the canon review packet.** Walk every item in the **Review checklist** below. For each surfaced finding: location (file + section), current text (verbatim quote), why it's a finding, proposed bounded fix (concrete diff), downstream-impact preview.
   **Verify:** `canon-review-packet.md` at repo root with the full categorized list before the loop starts.

3. **Surface the packet to the user as a summary first** — counts by severity, total findings, estimated walk-time. Confirm scope: walk all High? include Medium? skip Low? User may re-prioritize before drilling in.

4. **Walk findings in priority order.** For each:
   - Quote location + current text.
   - Explain why (one sentence).
   - Propose the fix (concrete `old_string` / `new_string`).
   - User picks: **Accept** / **Edit** / **Defer** / **Reject**.
   - On Accept / Edit: apply the edit, log the result, move on.
   - On Defer / Reject: log decision + rationale, move on.
   - After every batch (default 5 fixes, or one-per-doc-section): re-walk the relevant Review-checklist items on the affected sub-scope to surface any new findings.

5. **After all findings: re-walk the full Review checklist on the full canon.** Surface any new items that emerged from the cumulative edits.

6. **Produce `canon-review-report.md`** per § Final report.

## Review checklist

**This is the human-editable surface — adjust bullets as project priorities shift.** The agent surfaces a finding for any item that fails on inspection.

### A — Separation of concerns (HIGH)

- No fact stated in two tiers without an explicit `(canonical: X)` cross-reference.
- Methodology never specifies engine internals (those live in implementation).
- Implementation never explains motivation (that lives in manifesto).
- Templates never define concepts (those live in methodology).
- Manifesto never reaches into implementation details to make its case (uses methodology vocabulary only).

### B — Internal consistency (HIGH)

- Every manifesto promise is delivered in implementation.
- Methodology and implementation agree on every shared fact (e.g. mode list, trace family list, status taxonomy).
- Templates only assert what methodology or implementation specifies.
- Every forward reference (`see §X`, `per §X`, `methodology §Y`) resolves to existing content with a heading at the cited section.
- Concepts are named consistently across tiers (e.g. always "approval unit", never "approval scope").

### C — Occam's razor: aggressive cuts (MEDIUM)

- Every methodology concept is implemented in the engine OR realized in templates OR cited as load-bearing in the manifesto.
- No implementation §s specify behavior no operation needs.
- No template fields no agent ever consumes.
- No multiple ways of saying the same thing within a tier.
- Any subsection that, if removed, would not break a downstream consumer, is a candidate for cut.

### C' — Occam's razor: but not simpler (MEDIUM)

- Don't cut a concept that's load-bearing for the manifesto's case, even if the engine doesn't implement it yet — surface as a roadmap item instead.
- Don't cut a definition the user-facing site or skill depends on.

### D — Clarity / writing (LOW)

- Long sentences split where natural.
- Active voice over passive.
- Specific over vague ("various", "appropriate", "as needed" → concrete).
- Tables vs lists chosen for readability.
- Walls of prose split into numbered procedures where applicable.

### E — Cross-doc citation hygiene (LOW)

- Citations cite the specific section (`methodology §6.4`, not `methodology §6`).
- Forward references use current section names (rename-aware).
- Citation form is consistent (`methodology §6.4` everywhere, not mixed forms like `methodology section 6.4`).

## Output

- Edits applied in place across the four canon files (per Accept / Edit decisions).
- `canon-fact-map.md` — Step 1 verify.
- `canon-review-packet.md` — Step 2 verify.
- `canon-review-report.md` — final disposition + downstream-propagation list.

## Postconditions

- Every checklist item walked; every finding resolved (Accept / Edit / Defer / Reject) with rationale logged.
- Cross-cutting re-walk after each batch surfaced no un-handled findings.
- Downstream-propagation list names every derived doc that needs re-sync.

## Constraints

- **Agents propose; humans approve.** Never auto-apply a fix.
- **One fact, one tier.** When in doubt, the lower tier is canonical.
- **No silent rewrites.** Every edit lands via the interactive loop.
- **Don't fix the spec to match implementation.** Conflicts surface as findings (Category B); the user picks direction.
- **Don't propagate downstream during this prompt.** Site / skill re-syncs are scheduled, not edited inline.

## Invariants

- Canon hierarchy preserved: manifesto → methodology → implementation → templates.
- After review, no fact appears in two tiers without `(canonical: X)`.
- Templates remain a faithful materialization of methodology + implementation.
- Manifesto continues to make a coherent case using only methodology vocabulary.

## Validation (exit gates)

- Every Review-checklist item has been considered (or explicitly skipped, with the skip recorded in the report).
- Every accepted/edited finding has been applied to the canon files in place.
- Every applied finding has a `downstream-impact: [...]` line in the report.
- The final report has been produced.
- A reference commit SHA marks the canon state at session end.

## Failure modes

- **Conflict between docs (Category B).** Surface with both citations; user picks direction. Never auto-resolve.
- **User runs out of patience mid-review.** Save `canon-review-resume.md` with remaining findings + decisions so far; resume in next session.
- **Cascading impact too large** (>10 dependent findings on one accepted edit). Pause; recommend the user batch decisions on the cascade.
- **Spec-bug surfaced.** Out of scope to fix. Surface as Category B High; user decides whether to address now or defer.
- **Vestigial concept the user wants to keep.** Accept the call; record as "keep — user rationale: …" so a future review knows it was already considered.

## Anti-patterns

- Auto-applying any fix.
- Editing across docs in one finding when the right answer is one finding per doc.
- Inventing new sections when the right answer is moving existing content.
- Suggesting "consider rephrasing" without proposing the actual rephrasing.
- Walking findings out of priority order because Low-severity ones happen to be in the same section.

## Final report

`canon-review-report.md` at repo root:

1. **Summary table:** N findings; M applied, K modified, D deferred, R rejected; by Category × Severity.
2. **Per-finding detail.** ID (`CANON-FIND-001`…), location, severity, category, current quote, why, proposed fix, user decision, applied diff (if Edit), rationale (if Defer/Reject), `downstream-impact: [...]`.
3. **Cross-cutting re-walk results.**
4. **Downstream-propagation list:** consolidated, deduplicated, grouped by doc.
5. **Deferred items.**
6. **Reference commit SHA** at session end.

## Checkpointing

Commit after each batch — group by doc + category (e.g. `canon: methodology — separation-of-concerns`). If interrupted, resume from the most recent checkpoint.

## After this review

- Walk the downstream-propagation list. Schedule [`review-site.md`](review-site.md) and [`review-skill.md`](review-skill.md) for derived docs.
- If spec-vs-impl conflicts require an engine change, flag for the next [`build-engine.md`](build-engine.md) iteration.
- If the manifesto changed materially, the codæ page on the site needs an updated narrative — flag for `review-site.md`.
- Tag a reference canon commit so downstream review prompts have a stable target.
