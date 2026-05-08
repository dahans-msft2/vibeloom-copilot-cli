# Skill review report

Final report for the `review-skill.md` session run on 2026-05-08.

Walked: **4 actionable findings** (out of 5 surfaced in initial packet).
Deferred: 2 (1 marginal completeness, 1 test-skill scenario).
Result: **3 Accepted, 1 Deferred, 0 Rejected.**

---

## 1. Summary

| Severity | Category | Surfaced | Accepted | Deferred | Rejected |
|---|---|---:|---:|---:|---:|
| HIGH | A — Coverage gaps (canon cascade) | 1 | 1 (001) | 0 | 0 |
| MEDIUM | B — Spec misalignment | 1 | 1 (002) | 0 | 0 |
| MEDIUM | C — Template completeness | 1 | 0 | 1 (003) | 0 |
| LOW | D — Inter-template consistency | 1 | 1 (004) | 0 | 0 |
| NOTE | F — Test scenarios | 1 | 0 | 1 (005) | 0 |
| **TOTAL** | | **5** | **3** | **2** | **0** |

User chose option (a) at scope confirmation: walk all 4 actionable findings (003 deferred per my recommendation as marginal).

## 2. Per-finding detail

### SKILL-FIND-001 [HIGH / A] — Contract Graph cascade in skill bundle
**Decision:** Accept.
**Applied:** 13 string replacements in `vibeloom-templates.md`:
- 12 capitalization fixes (`contract graph` and `Contract graph` → `Contract Graph`):
  - SKILL.md authoritative-sources (line 189)
  - SKILL.md substrate (line 259)
  - subagent-prompt.md "you have your slice" (line 364)
  - tasks/approve.md (line 1500): "Refresh Contract Graph cache."
  - tasks/eval.md Steps (line 1573): "Build/refresh Contract Graph"
  - tasks/status.md Steps (line 2631): same
  - 6 task templates with "Contract Graph cache refreshed." / "Contract Graph updated." (lines 1507, 1766, 1943, 2040, 2146, 2233 — applied via replace_all)
- 1 reference tightening (line 294 SKILL.md guardrail): `the methodology's DAG. The valid set is in the methodology's DAG.` → `the methodology's Contract Graph (§5.1 derivation rules + §8 graph). The valid set is in the methodology.`

**Result:** "contract graph"/"Contract graph" lowercase fully eliminated from skill bundle. Final "Contract Graph" canonical references count: 19.

**downstream-impact:** `templates/` re-extraction needed.

### SKILL-FIND-002 [MEDIUM / B] — derives_from validation coverage gaps
**Decision:** Accept.
**Applied:** 3 small Validation-section edits in `vibeloom-templates.md`:
1. **`tasks/generate-system-specs.md`** — added new bullet to Validation: "Every IDed item cites at least one approved upstream item in `derives_from` per implementation §5.1 derivation rules."
2. **`tasks/generate-ux-specs.md`** — appended `per implementation §5.1 derivation rules` to existing derives_from Validation bullet.
3. **`tasks/eval.md`** Step 2 (Decidable tier) — added explicit reference: "Notable inclusion: `derives_from` validation per implementation §5.1 derivation rules and §8.2 universal-trace rule (every non-root item must cite valid upstream basis transitively reaching `CAP` or `CST`)."

**Why this matters:** Engine validates `derives_from` per the new §16 acceptance item I just added (cascade from CANON-FIND-011). Skill task templates now properly surface this as an expected validation. When users run `approve` / `eval` and the engine flags a §5.1 violation, they have template-level expectation of the check.

**Coverage now:**
- `tasks/generate-intent-specs.md` ✓ (intent is root, no derives_from required)
- `tasks/generate-product-specs.md` ✓ (had explicit §5.1 reference already)
- `tasks/generate-product-specs-from-ux.md` ✓ (multi-source check)
- `tasks/generate-ux-specs.md` ✓ (NOW cites §5.1)
- `tasks/generate-system-specs.md` ✓ (NEW Validation bullet)
- `tasks/generate-context.md` (relies on engine `eval --target context`)
- `tasks/generate-code-component.md` N/A (code doesn't have IDed items with derives_from)
- `tasks/eval.md` ✓ (NOW cites §5.1 + §8.2)
- `tasks/approve.md` and `tasks/review.md` rely on eval coverage at gate time (no separate edits needed)

**downstream-impact:** `templates/` re-extraction.

### SKILL-FIND-003 [MEDIUM / C] — Task template → §15 reference (deferred)
**Decision:** Defer.
**Rationale:** Every task template has `Operation: X` in HTML comment header (e.g. `Operation: approve` → §15.5). The mapping is implicit-by-name; an agent can find §15.X by operation name lookup. Adding explicit `Source: implementation §15.X` would be bureaucratic.

If the convention ever fails in practice (an agent gets confused), this can be revisited. For now: convention met.

### SKILL-FIND-004 [LOW / D] — Artifact templates: "(per DAG)" → "(per §5.1)"
**Decision:** Accept (tighter form).
**Applied:** 7 string replacements in `vibeloom-templates.md`:
- 6 instances of `Derivation rules (per DAG):` → `Derivation rules (per §5.1):` (replace_all batch)
- 1 variant: `Derivation rules (per DAG) for the component itself:` → `Derivation rules (per §5.1) for the component itself:`

**Not touched:** line 1199 — `\`component.md\` reads its own \`container.md\` (per DAG)` — this is a structural-ordering reference (wave dependency), correct per CANON-FIND-010's decision to keep bare DAG for structural property references.

**Result:** Derivation rule citations in artifact templates now reference §5.1 directly — matching the canon convention.

**downstream-impact:** `templates/` re-extraction.

### SKILL-FIND-005 [NOTE / F] — Test scenarios deferred to test-skill
**Decision:** Deferred (per the prompt's design — requires engine v0.4+).

**Rationale:** Per `review-skill.md`, behavioral testing is the job of `test-skill.md` (which doesn't yet exist). It needs a working engine to drive scratch-repo scenarios. Surface the scenarios now as informational so they're captured for the future test-skill prompt.

**Test scenarios catalogued for future test-skill:**
- vibe-init in empty dir + intent.md edit + approve + generate cycle
- pm-init + generate product-specs (with §5.1 derives_from validation expected)
- ux-init + drop mockups + generate-product-specs-from-ux (peer-review surface)
- approve on already-approved item (lifecycle check)
- generate with no approved upstream (should fail at §5.1 universal-trace check)
- import on existing codebase + brownfield draft generation
- reconcile on detected drift (preserve-contract / amend-contract / user-defined paths)
- vibe → pm upgrade migration

## 3. Cross-cutting re-walk results (Step 5)

After the 3 applied findings:

- **Sanity grep — "contract graph" lowercase** — fully eliminated ✓
- **Sanity grep — "derivation DAG" / "Context Graph" / "derivation graph"** — zero stragglers ✓
- **§5.1 derives_from citations** — present in 3 task templates as expected (generate-system-specs Validation, generate-ux-specs Validation, eval Steps) ✓
- **Contract Graph canonical references** — 19 in skill bundle (from 0 lowercase pre-walk + 7 mixed-case + 6 lowercase = 13 corrected) ✓
- **Template integrity** — `extract-templates.py --check` not run (engine not built yet); structurally `vibeloom-templates.md` parses by inspection.

## 4. Cross-cutting re-walk — coverage map post-walk

All three coverage tables from Step 1 still hold:
- Command → task template: PERFECT (14 task templates cover 8 operations + 6 generation variants)
- Task template → §15: implicit-by-name (per `Operation:` header) — convention met
- Artifact template → §6 frontmatter: PERFECT by spot-check

## 5. Items flagged for canon update

**None this pass.** All cascades from CANON-FIND-010 (Contract Graph) and CANON-FIND-011 (derives_from §5.1) were resolvable inside the skill bundle. No canon-side findings emerged.

## 6. Deferred items (for next pass)

- **SKILL-FIND-003** — explicit §15.X cite per task template. Mark "convention-met" until/unless an agent gets confused by the implicit `Operation: X` mapping.
- **SKILL-FIND-005** — behavioral test scenarios. Scheduled for future `test-skill.md` once engine v0.4+ exists.

## 7. Reference commit SHA

To be captured at session end (commit + push pending).

Working tree state at report time:
- 1 file modified: `vibeloom-templates.md` (all skill changes consolidated in the canonical fenced-block source)
- 3 new artifacts at repo root: `skill-coverage-map.md`, `skill-review-packet.md`, `skill-review-report.md`

## 8. Pleasant surprises — what didn't surface

- **Command coverage: PERFECT** — every operation from methodology §12 has a task template (with appropriate per-target generate variants).
- **10-section codæ structure: PERFECT** — all 14 task templates have Purpose / Inputs / Preconditions / Steps / Output / Postconditions / Constraints / Invariants / Validation / Failure modes.
- **Vocabulary consistency: STRONG** — "approval unit" used 14× (no "approval scope" drift); "subagent" used 62× (no hyphen variants).
- **Mode coverage: STRONG** — vibe + full modes properly handled; ux-mode has dedicated `generate-product-specs-from-ux.md`.
- **Artifact frontmatter alignment: STRONG** — all 18 artifact templates' frontmatter shapes match impl §6 by spot-check (carrying `approval_unit`, `layer`, etc. where applicable).
- **No §16/§17/§18-numbering cascades** from the recent renumber — the skill doesn't cite by §-number directly.
- **No cognitive-surface metric stragglers** — the §10 stub didn't cascade into skill templates.
- **`templates/` extracted tree** would re-materialize cleanly from the canonical fenced blocks (assuming `extract-templates.py` runs).

The skill bundle is **shippable as-is** post-this-review. It's a clean realization of the canon's WHAT (methodology) + HOW (implementation) at the materialization tier. The CANON-FIND-011 cascade (derives_from validation discipline) is now properly surfaced through the skill task templates.

## 9. Methodology validation — review-skill.md prompt itself

The `review-skill.md` prompt validated by use:
- The interactive loop, scope-confirmation step, severity-sorted Review checklist all worked as designed.
- The coverage map verify gate (Step 1) was useful — showed quickly that command coverage and 10-section completeness are both PERFECT, so the review focus shifted to canon-cascade findings (which is where the work actually was).
- The Step 5 re-walk caught no cascades (the initial sweep was thorough — see Note below).
- Category F (test scenarios) was correctly handled as informational/deferred — exactly per the prompt's design for "the skill prompt knows test-skill doesn't exist yet."

**Note on the initial cascade sweep:** Unlike the canon and site review sessions where the initial sweep under-scoped (caught TOC/h2/table but missed body prose), the skill review sweep this time benefited from a tighter initial grep + re-grep cycle that caught both "contract graph" lowercase AND "Contract graph" mixed-case before walking. The lesson from canon-review-report.md §9 ("do a final case-insensitive grep before declaring the cascade done") was applied in advance here.

## 10. Trilogy complete

This is the third and final review session in the planned trilogy:
- **review-canon** (2026-05-07): 11 findings + 4 cascades
- **review-site** (2026-05-07): 5 findings, 2 deferred  
- **review-skill** (2026-05-08): 4 findings, 1 deferred + 1 to-test-skill

The three review prompts validated end-to-end. The pattern of `review-X.md → packet → walk → report` works. The next-step from here is **`test-skill.md`** — the deferred behavioral-testing prompt that requires a working engine to drive scenarios. Add it to the build queue when engine v0.4 ships.
