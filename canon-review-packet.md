# Canon review packet

Externalized Step 2 verify for `review-canon.md`. Every finding surfaced from the cross-walk in `canon-fact-map.md`, walked against the Review checklist in `review-canon.md`.

**Total: 9 findings** (4 HIGH, 3 MEDIUM, 2 LOW). Estimated walk-time at ~3 min/finding: **~25-30 minutes**.

| Severity | Category | Count |
|---|---|---|
| HIGH | A — Separation of concerns | 2 |
| HIGH | B — Internal consistency | 2 |
| MEDIUM | C — Occam: aggressive cuts | 3 |
| LOW | D — Clarity / writing | 1 |
| LOW | E — Cross-doc citation hygiene | 1 |

---

## CANON-FIND-001 [HIGH / A — Separation of concerns]

**Location:** verification ladder per-tier check list duplicated in:
- `codæ-manifesto.html` §7 lines 1242–1244 (Rung 1/2/3 cards each list checks)
- `vibeloom-methodology.md` §14.3 lines 443–447 (Decidable/Mechanical/Heuristic table with checks per tier + trajectory)
- `vibeloom-templates.md` references/eval.md "## The verification ladder" lines 735–741 (Decidable/Mechanical/Heuristic with checks per tier)
- `vibeloom-templates.md` tasks/eval.md Steps 2–4 (lines 1579–1581) (re-states checks per tier)

**Why it's a finding:** Same per-tier check inventory ("lifecycle consistency, required fields, ID validity, reference integrity, …") appears in four places. Methodology is the canonical home (it owns the paradigm definition); manifesto should name the rungs as a philosophical climb without re-listing checks; templates should reference methodology, not re-state. Risk: lists drift apart over time.

**Proposed fix:**
- Methodology §14.3: stays canonical (already has the v0.3-vs-trajectory table — keep it).
- Manifesto §7: keep the three rung cards (Rung 1/2/3 + the climb prose), but trim the per-rung check lists to one example each + a "(see methodology §14.3 for the full check list per tier)" link.
- Templates references/eval.md: replace "## The verification ladder" check list with "see methodology §14.3" cross-reference; keep the heuristic-dimensions section (which is genuinely skill-specific detail, not duplicated elsewhere).
- Templates tasks/eval.md Steps 2–4: replace inline tier check enumeration with "follow methodology §14.3 tier definitions" + the operation-specific Steps that wrap them.

**Downstream impact:** site pages (`codae.html` if it surfaces the ladder), and any re-extraction of `templates/`. Estimated 4 file edits.

---

## CANON-FIND-002 [HIGH / A — Separation of concerns]

**Location:** `vibeloom-templates.md` references/eval.md, full "Verification Ladder + Semantic Eval Reference" block (lines 731+).

**Why it's a finding:** This reference re-defines tier semantics ("Decidable (engine, structural) — deterministic checks the engine performs without an LLM. Lifecycle consistency, required fields, …"). Tier semantics are methodology's job (§14.3); references should specialize, not re-define.

**Proposed fix:** Trim the "## The verification ladder" subsection to a 1-paragraph orientation that cites methodology §14.3, and keep the "## Heuristic dimensions" section (Faithful Representation, Naming Consistency, etc., lines 779+) which is the genuine skill-side specialization.

**Downstream impact:** Same as 001 — re-extracted templates. (CANON-FIND-001 and 002 may be applied as a single combined edit to references/eval.md.)

---

## CANON-FIND-003 [HIGH / B — Internal consistency]

**Location:** `vibeloom-methodology.md` §14.3 line 441.

**Current text:**
> Each tier is more rigorous and more expensive than the one below.

**Why it's a finding:** Tier ordering in the §14.3 table is Decidable (top) → Mechanical → Heuristic (bottom). The claim "more rigorous AND more expensive than the one below" implies Decidable > Heuristic on cost. **That's wrong.** Decidable structural eval is *cheaper* than Heuristic semantic eval (no LLM call, pure compute). Decidable is more rigorous AND cheaper; Heuristic is less rigorous AND more expensive. The sentence is both internally contradictory (rigor goes one way, cost the other) and factually inverted on cost direction.

**Proposed fix:**
> Each tier is more rigorous than the one below it; cost runs the other direction (heuristic eval is the most expensive, decidable structural checks the cheapest).

**Downstream impact:** none beyond the methodology line itself.

---

## CANON-FIND-004 [HIGH / B — Internal consistency]

**Location:** `vibeloom-templates.md` skill/SKILL.md line 189.

**Current text:**
> **[vibeloom-methodology.md](../../vibeloom-methodology.md)** — WHAT and WHY (entities, tiers, modes, operations, approval model, derivation DAG, status taxonomy, verification ladder, decision-trace classification). If this skill file conflicts with the methodology, the methodology wins.

**Why it's a finding:** Methodology line 7 explicitly says "This document defines **what VibeLoom is**. The case for the paradigm is in the manifesto; the technical realization is in the implementation doc." So methodology is WHAT only; the manifesto is WHY. SKILL.md misattributes WHY to methodology — and silently omits the manifesto from authoritative sources.

**Proposed fix:**
> **[vibeloom-methodology.md](../../vibeloom-methodology.md)** — WHAT (entities, tiers, modes, operations, approval model, derivation DAG, status taxonomy, verification ladder, decision-trace classification). If this skill file conflicts with the methodology, the methodology wins.

(Plus see CANON-FIND-009 below for adding the manifesto as paradigm-context source.)

**Downstream impact:** re-extracted templates.

---

## CANON-FIND-005 [MEDIUM / C — Occam: aggressive cut]

**Location:** `vibeloom-methodology.md` §10 "Cognitive surface metric" lines 278–293 (whole section).

**Why it's a finding:** §10 defines a metric (`Contract cognitive surface = number of IDed contract items in the affected review cut`, `Code cognitive surface = files + classes/types + methods + endpoints + tests + integration points`, `Review compression ratio`) plus secondary metrics (review time per packet, defect-detection rate, downstream-rework frequency). Cross-walk shows: the engine never computes any of these (no §15 / §10 / §13 reference); templates never surface them; site doesn't use them. The methodology §10 even concedes "Until dogfood data lands, treat numerical ratios as targets, not proof." It's a vestigial concept that the canon defines but no consumer uses.

The MANIFESTO has its own cognitive-surface visual (§5 "The mendable surface" — 108K-LOC mountain vs 24% contract column) which IS load-bearing for the case (Category C' — keep). That visual makes the case in manifesto vocabulary; the methodology §10 metric definition is the separable, vestigial part.

**Proposed fix:** Two paths:
- **(a) cut M §10 entirely**: the manifesto's visual makes the case; the metric isn't operational.
- **(b) move M §10 to roadmap.md** as an "engine-implements-and-surfaces cognitive-surface metrics" item, and remove from methodology.

I lean (b) — the metric IS a real future capability worth documenting somewhere; just not in methodology where it claims to be a paradigm element when it isn't yet operational.

**Downstream impact:** roadmap.md addition; the manifesto's §5 visual stays untouched.

---

## CANON-FIND-006 [MEDIUM / C — Occam: aggressive cut]

**Location:** `vibeloom-implementation.md` §16 "Brownfield import" lines 1191–1207.

**Why it's a finding:** §16 is an orphan section. Cross-grep shows zero references to it from anywhere in the canon. Its content (one YAML evidence shape + one line "Imported contract remains draft until reviewed and approved") is conceptually covered by I §15.8 (the full `import` operation pseudo-code) and the YAML evidence shape really belongs in §6 (Artifact frontmatter) if it's a frontmatter shape, or as a structured sub-block of §15.8 if it's an evidence shape produced by import.

**Proposed fix:** Cut §16 entirely. The YAML example is duplicative of what import already produces (§15.8 step 5 writes drafts with confidence + evidence); if a worked example is wanted, it belongs as a sub-example of §15.8.

**Downstream impact:** §-numbering shifts (§17 → §16, §18 → §17, etc.). Forward references like "§16" (none found in cross-grep) need updates; "§17" (none found) needs updates; "§18 acceptance checklist" — needs forward-reference renumbering wherever it's cited.

---

## CANON-FIND-007 [MEDIUM / C — Occam: aggressive cut]

**Location:** `vibeloom-implementation.md` §17 "UX and mockup ingestion" lines 1211–1225.

**Why it's a finding:** Same shape as 006. §17 is an orphan section. Content is one MOCK YAML record + one line "Generated obligations must become IDed items before they become contract truth." The conceptual content is fully covered by methodology §6.3 ("Mockups are critical input evidence … Mockups do not become normative truth until their extracted obligations are represented as IDed contract items"); the YAML shape belongs in §6 (Artifact frontmatter) if MOCK has a frontmatter shape, but MOCK is a structured field on `ux.md`, not a separate file with frontmatter — so the YAML in §17 is just an example, not a schema.

**Proposed fix:** Cut §17. If a worked MOCK example is wanted, it belongs as a sub-block of §6 (perhaps a new §6.5 "Body item shapes" with examples per family) OR in templates references/artifacts.md (which already has body-item shapes for other families).

**Downstream impact:** §-numbering shifts (combined with 006: §18 → §16, etc.). If accepted with 006, the §-renumber is one batch.

---

## CANON-FIND-008 [LOW / D — Clarity / writing]

**Location:** verification-ladder presentation across two tiers:
- `codæ-manifesto.html` §7 line 1242: Rung 1 = Semantic (heuristic); Rung 3 = Structural (decidable). Climb is bottom-up: Rung 1 → Rung 3.
- `vibeloom-methodology.md` §14.3 table lines 444–447: Decidable first row, Heuristic last row. Climb is described as "promote checks upward" but the table is top-to-bottom Decidable→Heuristic.

**Why it's a finding:** A careful reader who reads both could be confused about whether the ladder is "climb up = toward decidable" (manifesto) or "table top = decidable" (methodology). Both are internally consistent; the cross-doc presentation isn't.

**Proposed fix:** Align the verbal framing in both: pick "decidable is the destination" as the metaphor, present manifesto Rung 1 → Rung 3 as Heuristic → Decidable, and keep methodology table top-to-bottom Decidable → Heuristic but explicitly say "the table is top-down: Decidable is the destination, Heuristic is the entry point; promotion is upward toward Decidable."

Smaller fix: change methodology §14.3 sentence after the table from "Each tier is more rigorous than the one below" to "Decidable is the top of the ladder; Heuristic is the entry point — and the climb promotes checks upward toward Decidable."

(This finding subsumes part of CANON-FIND-003 — they share text. Apply 003 first; then 008 polishes the surrounding sentences.)

**Downstream impact:** none beyond the methodology paragraph.

---

## CANON-FIND-009 [LOW / E — Cross-doc citation hygiene]

**Location:** `vibeloom-templates.md` skill/SKILL.md "Authoritative sources" section, lines 185–190.

**Current text:** Lists vibeloom-methodology.md and vibeloom-implementation.md only.

**Why it's a finding:** The manifesto is the WHY tier of the canon (per CANON-FIND-004). SKILL.md should at least cite it as paradigm-context source, even if the runtime doesn't load it. Otherwise an agent running the skill has no pointer to the case for the paradigm — only the WHAT and HOW.

**Proposed fix:** Add a third bullet:
> - **[codæ-manifesto.html](../../codæ-manifesto.html)** — WHY (the case for contract-driven agentic engineering). Paradigm context; not loaded at runtime, but referenced when explaining the system or onboarding new contributors.

**Downstream impact:** re-extracted templates.

---

## Combined application notes

- CANON-FIND-001 + CANON-FIND-002 should be applied as a single coordinated edit to `templates/skill/references/eval.md` (both touch the same file).
- CANON-FIND-003 + CANON-FIND-008 share the same paragraph in M §14.3; apply 003 first, then 008 polishes.
- CANON-FIND-004 + CANON-FIND-009 are both edits to skill/SKILL.md — apply as one batch.
- CANON-FIND-006 + CANON-FIND-007 are both impl §-renumber concerns; apply as one batch with care for forward references.

That's 9 findings, 4 effective edit batches.
