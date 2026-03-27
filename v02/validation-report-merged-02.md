# VibeLoom Validation Report — Merged Post-Fix Pass #2

## Source

This report merges findings from two independent validation passes (my own and an external AI's) conducted after the 13-fix round. Findings are consolidated, deduplicated, and amended with fix suggestions.

---

## Consolidated Findings

### F01 — Lite delegation scope is still ambiguous [P1]

**Source:** External AI (confirmed by my review)

**Problem:** The methodology says intent-specs are "always human-gated and never delegated" (line 344) but also says lite's approval unit is the "affected contract stack" (lines 278, 333, 394). Since "affected contract stack" conceptually starts from intent-specs, a reader can't tell whether lite delegates the *whole* stack or only product-specs + system-specs. The table cell for lite's "Delegated auto-advance by default" column says "affected contract stack" — which *includes* intent-specs — contradicting the "never delegated" rule.

The footnote on line 338 and the clarification on line 344 *intend* to resolve this, but the table itself still says "affected contract stack" in the delegation column, which is the contradiction.

**Refs:** methodology:57, 278, 333, 394; implementation:499, 531

**Severity:** P1 — A skill author will have to guess what "affected contract stack" means for delegation.

**Fix suggestion:** Replace the ambiguous "affected contract stack" phrasing in the delegation column. The precise semantics are:

- Lite's **approval unit** is still the affected contract stack (intent + product + system considered together).
- Lite's **delegated auto-advance** applies to product-specs and system-specs only — intent-specs are always human-gated.

Options:
1. **Change the delegation column** from "affected contract stack" to "product-specs + system-specs" in the mode table (methodology:333, implementation:499, SKILL:310). Then adjust the surrounding prose (methodology:278, 394; implementation:531) to say "lite delegates product-specs and system-specs by default" rather than "the affected contract stack."
2. **Keep "affected contract stack" in the approval-unit column** but change the delegation column and add a one-line qualifier: "Delegation applies to product-specs and system-specs; intent-specs are always human-gated."

**Recommended:** Option 1 — it eliminates the contradiction at the source rather than patching it with prose.

---

### F02 — Normal forward surface only comprehensible by cross-referencing both docs [P2]

**Source:** External AI (confirmed by my review)

**Problem:** The methodology presents a mode-specific "normal forward surface" (lines 62-66, 331) that lists commands per mode (e.g., `lite`: `generate code`). A reader of the methodology alone could think these are the *only* valid commands per mode. The implementation (line 514) clarifies that all `generate <target>` combinations are valid in every mode and that the forward surface is just "what the skill should suggest." But this clarification only exists in the implementation, not in the methodology.

**Refs:** methodology:62-66, 331, 348; implementation:514

**Severity:** P2 — Not a logical defect, but a comprehension barrier for anyone reading the methodology as a standalone document.

**Fix suggestion:** Add a one-line clarification to the methodology near the forward surface definition. Specifically, after the forward surface bullets (methodology:62-66), insert:

> All `generate <target>` combinations are valid in every mode. The normal forward surface lists the commands the skill should suggest after each stop, not the only valid commands.

This makes the methodology self-contained on this point without duplicating the full smart orchestration table.

---

### F03 — Ledger artifact-level `derives_from` semantics are underspecified [P2]

**Source:** External AI (confirmed by my review)

**Problem:** The implementation requires every context artifact to carry `derives_from` in frontmatter (line 182). The `pdr` and `adr` templates include `derives_from: []` in frontmatter. But unlike execution guidance or `bdd` (where artifact-level `derives_from` clearly points to the upstream contract items that triggered generation), ledgers are append-only collections of records where *each record* has its own per-record `derives_from` (e.g., `derives_from: [FR-0001, Q-0001]` on PDR-0001).

A skill author must decide: is artifact-level `derives_from` always empty, the union of all per-record `derives_from`, or something else?

**Refs:** implementation:171-182, 356; pdr.md:7, adr.md:7

**Severity:** P2 — The skill will work either way, but two implementations could make different choices, leading to inconsistent graph behavior.

**Fix suggestion:** Add a brief rule to the implementation's context artifact frontmatter section (near line 189) or to the item carriers section (near line 356):

> For ledger artifacts (`pdr`, `adr`): artifact-level `derives_from` in frontmatter is always empty (`[]`). Per-record `derives_from` inside each `PDR-####` / `ADR-####` section is the canonical derivation link. The engine builds graph edges from per-record `derives_from`, not from artifact-level frontmatter.

This is the cleanest option because:
- Ledgers are append-only — their artifact-level derivation basis never stabilizes.
- Per-record `derives_from` is already the meaningful granularity.
- Keeping artifact-level `derives_from: []` avoids a growing, hard-to-maintain union list.

---

### F04 — SKILL.md `generate intent-specs` table cell uses "regen" instead of "reshape" [Cosmetic]

**Source:** My review

**Problem:** SKILL:104 says "regen intent+defaults, stop" while methodology and implementation use "reshape intent, regenerate defaults." The table abbreviation loses the deliberate "reshape" semantics (user's intent is preserved, only structure is adjusted).

**Refs:** SKILL:104

**Severity:** Cosmetic — but since the SKILL.md is what the agent directly executes from, precision matters.

**Fix suggestion:** Change SKILL:104 from "regen intent+defaults, stop" to "reshape intent, regen defaults, stop".

---

## Assessment

### Dimension Ratings

| Dimension | Rating | Notes |
| --- | --- | --- |
| Consistency | Strong (one P1 remaining) | F01 is the only real cross-doc contradiction |
| Coherence | Strong | Contract/context/code model is solid |
| Logic | Strong | No logical gaps |
| Comprehensibility | Good | F02 is a speed-bump, not a defect |
| Ambiguity | Strong (one P2 remaining) | F01 creates actual interpretation ambiguity; F03 is an underspecification |
| Fidelity for skill | High (close to ready) | F01 and F03 would force a skill author to interpret; F02 and F04 are polish |

### Value Summary

**What VibeLoom does well:**
- Treats AI-assisted development as a governed system, not a chat transcript
- Clean separation of semantic truth (contract), execution truth (context), and executable result (code)
- Flexible governance via 4 modes with principled delegation and escalation
- Context graph as coherence engine (derivation + containment → 4 derived views)
- Operation symmetry (review:eval :: reconcile:generate) aids memorability
- Well-specified enough to build a working skill from

**Remaining risks:**
- High ceremony cost (mitigated by lite mode but still present)
- Agent capability is the single point of failure for validation (no executable engine in v1)
- Learning curve is steep (~700 lines of methodology + ~650 lines of implementation)
- Direct-edit detection and frontmatter discipline are operationally heavy

### Bottom Line

Three targeted fixes (F01-F03) plus one cosmetic tweak (F04) would close all remaining specification gaps. After those, the system is ready for skill implementation.
