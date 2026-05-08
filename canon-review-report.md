# Canon review report

Final report for the `review-canon.md` session run on 2026-05-07.

Walked: **11 findings** (9 from initial packet + 2 surfaced during the walk).
Result: **10 Accepted, 1 Deferred-as-resolved, 0 Rejected.**

---

## 1. Summary

| Severity | Category | Surfaced | Accepted | Deferred | Rejected |
|---|---|---:|---:|---:|---:|
| HIGH | A — Separation of concerns | 2 | 2 (001 + 002 merged) | 0 | 0 |
| HIGH | B — Internal consistency | 4 | 4 (003, 004, 010, 011) | 0 | 0 |
| MEDIUM | C — Occam: aggressive cuts | 3 | 3 (005, 006, 007) | 0 | 0 |
| LOW | D — Clarity / writing | 1 | 0 | 1 (008) | 0 |
| LOW | E — Citation hygiene | 1 | 1 (009) | 0 | 0 |
| **TOTAL** | | **11** | **10** | **1** | **0** |

Plus **4 cascade cleanups** discovered and applied during Step 5 (re-walk).

---

## 2. Per-finding detail

### CANON-FIND-001 [HIGH / A] — Verification ladder check-list dedup
**Decision:** Accept (with revised scope — left manifesto enumerations as persuasive flavor).
**Applied:**
- `vibeloom-templates.md` references/eval.md "## The verification ladder" — replaced ~5-line per-tier check inventory with single cross-reference paragraph pointing at methodology §14.3.
- `vibeloom-templates.md` tasks/eval.md Steps 2–4 — removed inline check enumerations, replaced with "the engine knows what to run" + cross-references to methodology §14.3 / §14.2 / references/eval.md.

**downstream-impact:** templates re-extraction (one fenced-block file modified).

### CANON-FIND-002 [HIGH / A] — Templates references/eval.md re-defines tier semantics
**Decision:** Auto-resolved by 001 (same target).
**Applied:** see 001.

### CANON-FIND-003 [HIGH / B] — Methodology §14.3 inverted cost claim
**Decision:** Accept.
**Applied:** `vibeloom-methodology.md` §14.3 — replaced "Each tier is more rigorous and more expensive than the one below" with explicit "Decidable is the most rigorous and the cheapest (pure compute, no LLM); heuristic is the least rigorous and the most expensive (LLM-judged)" + added the "cheap-and-rigorous share grows over time" framing on the trajectory.

**downstream-impact:** none beyond the methodology line.

### CANON-FIND-004 [HIGH / B] — SKILL.md misattributes methodology as "WHAT and WHY"
**Decision:** Accept.
**Applied:** `vibeloom-templates.md` skill/SKILL.md authoritative-sources block — methodology bullet now says "WHAT" (was "WHAT and WHY"). Plus snuck in "contract graph" → "Contract Graph" in the same line as cascade-prep for 010.

**downstream-impact:** templates re-extraction.

### CANON-FIND-005 [MEDIUM / C] — Cognitive surface metric vestigial
**Decision:** Accept (b) — replace M §10 with stub + add roadmap A4.
**Applied:**
- `vibeloom-methodology.md` §10 — replaced 16-line metric definition with 3-line stub citing manifesto §5 (visual case) + roadmap A4 (engine instrumentation).
- `roadmap.md` — new entry **A4. Cognitive-surface instrumentation** under Theme A (toolchain capabilities), with full What/Justification/With-vs-Without per the roadmap format.
- Bonus catch: fixed "derivation graph" → "Contract Graph" in roadmap A3 as cascade-prep for 010.

**downstream-impact:** roadmap A4 added (new entry); methodology §10 reduced from 16 lines to 3.

### CANON-FIND-006 + CANON-FIND-007 [MEDIUM / C] — Implementation §16 + §17 orphan sections
**Decision:** Accept (revised) — cut headings + intro/closing prose; migrate YAML examples as worked outputs of `import` step 5 in §15.8; renumber §18→§16, §19→§17, §20→§18; sweep cross-refs.
**Applied:**
- `vibeloom-implementation.md` §15.8 — added "Worked examples — what step 5 produces" subsection with the FR-#### and MOCK-#### YAML samples preserved.
- `vibeloom-implementation.md` §16 (Brownfield) — cut entirely.
- `vibeloom-implementation.md` §17 (UX/mockup) — cut entirely.
- `vibeloom-implementation.md` — renumbered §18 Acceptance → §16, §19 Templates → §17 (with §19.1/§19.2/§19.3 → §17.1/§17.2/§17.3), §20 See also → §18.
- `vibeloom-implementation.md` line 1307 — self-ref §19.3 → §17.3.
- `build-engine.md` — replace_all §19.3 → §17.3, §18 → §16.
- `build-skill.md` — replace_all §19.3 → §17.3, §19 templates inventory → §17 templates inventory, §18 → §16.

**downstream-impact:** all §-references in build-engine.md and build-skill.md swept; Implementation now has 18 sections (was 20) with no orphan stubs.

### CANON-FIND-008 [LOW / D] — Verification ladder direction-of-climb framing
**Decision:** Defer-as-resolved.
**Rationale:** Substantive issue (cost-direction error) was fixed by 003. Remaining "inconsistency" is purely presentation — methodology table top-down vs manifesto Rung 1→3 bottom-up. Both docs explicitly state "promote upward, heuristic → mechanical → structural" — no real ambiguity. Adding a clarifier would cost more cognitive overhead than it saves.

**downstream-impact:** none.

### CANON-FIND-009 [LOW / E] — SKILL.md authoritative sources omits manifesto
**Decision:** Accept.
**Applied:** `vibeloom-templates.md` skill/SKILL.md — added third bullet for `codæ-manifesto.html` (WHY) after methodology and implementation. Explicitly noted: "Paradigm context; not loaded for runtime decisions, but referenced when explaining the system or onboarding new contributors."

**downstream-impact:** templates re-extraction.

### CANON-FIND-010 [HIGH / B] — Contract Graph terminology unification (surfaced during walk)
**Decision:** Accept.
**Rationale:** User raised mid-walk that "derivation DAG" should be unified to one term. Audit showed: 18 uses of "contract graph", 5 uses of "derivation graph", 2 uses of "Derivation DAG", 1 use of "derivation DAG" lowercase, 1 use of "Context Graph" (broken citation pointing at non-existent methodology section).
**Applied:**
- `vibeloom-methodology.md` §8 — rewrote heading + opening to establish **"Contract Graph" as the canonical proper-noun entity name** with the stable definition: "The Contract Graph contains the relationships between all entities defined in the contract. The term is stable; the implementation evolves." Inline notes that v0.3 implements it as a derivation DAG.
- `vibeloom-methodology.md` §1 line 18 — "the derivation graph" → "the Contract Graph".
- `vibeloom-methodology.md` §4 line 96 — "approved derivation graph" → "approved Contract Graph".
- `vibeloom-methodology.md` §8.2 — "approved graph remains acyclic" → "approved Contract Graph remains acyclic".
- `vibeloom-implementation.md` §4 — "derivation DAG validation" → "Contract Graph validation (DAG invariants)".
- `vibeloom-templates.md` line 691 — "Derivation DAG" → "Contract Graph (§8)".
- `vibeloom-templates.md` line 806 — fixed broken citation "Derivation DAG (methodology ## Context Graph)" → "Contract Graph (methodology §8)".
- `vibeloom-templates.md` line 3292 — "derivation graph" → "Contract Graph".
- `vibeloom-templates.md` line 3525 — same.
- `vibeloom-templates.md` line 3642 — same.
- `vibeloom-templates.md` line 3939 — straggler caught in re-walk: "loading the full context graph" → "loading the full Contract Graph".

**downstream-impact:** 29 total "Contract Graph" references across canon (was 18); zero broken "Context Graph" references; vocabulary consistent across manifesto/methodology/implementation/templates.

### CANON-FIND-011 [HIGH / B] — Universal-trace + comprehensive prefix derivation rules (surfaced during walk)
**Decision:** Accept (b) — comprehensive (11 prefixes + universal-trace rule).
**Rationale:** User started with UX-prefix question (VIEW/INT/UXC/MOCK had no derivation rules in §5.1 Notes); discussion surfaced that the same gap exists for 7 other prefixes (DEF, MS, TERM, EXT, TB, SNFR, CONT). User articulated principle: "intent should broadly cover everything; all entities derive from intent (transitively)." Twin roots (CAP + CST) preserved — CST often expresses orthogonal stack/aspect choices that affect all CAPs and none.
**Applied:**
- `vibeloom-methodology.md` §8.2 — added bold sentence: "**Every other item derives, directly or transitively, from at least one root.**" Makes universal-trace rule explicit.
- `vibeloom-implementation.md` §5.1 prefix registry — explicit `Derives from X` rules added to Notes column for 11 prefixes:
  - `DEF`: derives from `CAP`/`CST` (normalized from intent)
  - `MS`: derives from `STORY` (and optionally `OBJ`)
  - `TERM`: derives from `CAP` (or `STORY`)
  - `VIEW`: derives from `CAP` and/or `STORY`/`FLOW`. May cite `MOCK` as evidence.
  - `INT`: derives from `VIEW` (structural) and `STORY`/`ACC` (semantic basis)
  - `UXC`: derives from `CST` and/or `DEF`
  - `MOCK`: derives from `CAP` and/or `CST`. May be cited by `VIEW`/`INT`/`UXC`/`STORY`/`ACC` as evidence (`evidence_for`)
  - `EXT`: derives from `CAP` and/or `FR`
  - `TB`: derives from `CST`, `SNFR`, or `NFR`
  - `SNFR`: derives from `NFR` or `CST`
  - `CONT`: derives from `FR`/`STORY`/`CAP`

**downstream-impact:** §5.1 registry now has explicit derivation rules for every non-root prefix; §8.2 carries the universal-trace principle. Skill task templates may need `derives_from` validation pass on next build (the engine should verify that every non-CAP-non-CST item declares `derives_from` per §5.1 rules).

---

## 3. Cross-cutting re-walk results (Step 5)

After the 11 findings landed, re-walk surfaced **4 cascade cleanups** that were applied as part of Step 5 (not separate findings):

- **Cascade A** — `README.md` line 32: §19 Templates → §17 Templates (cascade from 006/007 renumber).
- **Cascade B** — `build-engine.md` line 20: "derivation DAG" → "Contract Graph" (cascade from 010).
- **Cascade C** — `vibeloom-comparison.html` line 761: "first-class derivation graph" → "first-class Contract Graph" (cascade from 010).
- **Cascade D** — `build-engine.md` §16 mapping table: dropped stale "Lines" column and "(impl lines 1210–1228)" prose intro. Line numbers shift with every edit; §-numbers and item names are durable.

After cascades, sanity grep confirms:
- Zero stale `§18` / `§19` / `§20` references in canon, build prompts, or README.
- Zero "Context Graph" misuse (all uses are correct: roadmap CGKG-B's future implementation shape, OR the methodology line "v0.3 Contract Graph is essentially a derivation DAG" — which intentionally explains the v0.3 implementation).
- 29 "Contract Graph" canonical references across canon (vs ~18 pre-walk).
- All 11 §5.1 prefixes now carry explicit derivation rules in Notes.

## 4. Downstream-propagation list

Files that need attention after this canon review:

| File | Why |
|---|---|
| `templates/` (extracted tree) | Re-run `extract-templates.py` to materialize updated `vibeloom-templates.md` (touched by 001, 004, 009, 010). |
| `roadmap.md` | New entry A4 added (cognitive-surface instrumentation). |
| `vibeloom-comparison.html` | "Contract Graph" rename took (Cascade C). Site will pick this up automatically on next build/serve. |
| `README.md` | §17 Templates citation updated (Cascade A). |
| `build-engine.md` and `build-skill.md` | Cross-refs swept: §16 acceptance, §17 templates, §17.3 inventory, "Contract Graph" rename. Run `build-engine.md` next time per its updated §16 mapping table. |
| `vibeloom-implementation.md` §16 acceptance checklist | New acceptance item likely needed: "Engine validates `derives_from` per §5.1 derivation rules for every non-root item" (cascade from 011). **Flag for next implementation iteration.** |

Site pages (`v03/site/public/*.html`) **NOT** swept in this pass (out of scope per the prompt; review-site.md handles them). Likely follow-ups for `review-site.md`:
- Codae page may surface manifesto §7 verification ladder (no change needed, manifesto unchanged).
- Methodology page may surface §8 Contract Graph naming (rename took in canon; site needs check).
- Methodology page may surface §10 Cognitive surface (changed from metric to stub; site needs check).
- Implementation page may surface §16/§17 (new section content).
- Methodology page may surface §5.1 prefix derivation rules (new content).

## 5. Deferred items (for next review pass)

- **CANON-FIND-008** — verification-ladder direction-of-climb framing. Deferred-as-resolved by 003. If a future reader is confused by the methodology-table-top-down vs manifesto-Rung-1-to-3 bottom-up presentation, surface again with a 1-line clarifier in manifesto §7.

## 6. Reference commit SHA

To be captured at session end (commit + push pending).

Working tree state at report time:
- 5 canon-tier files modified: `codæ-manifesto.html` (none — no manifesto edits this pass), `vibeloom-methodology.md`, `vibeloom-implementation.md`, `vibeloom-templates.md`, plus `roadmap.md`.
- 3 derived files modified: `README.md`, `build-engine.md`, `build-skill.md`.
- 1 derived file modified: `vibeloom-comparison.html`.
- 3 new artifacts at repo root: `canon-fact-map.md`, `canon-review-packet.md`, `canon-review-report.md`.
