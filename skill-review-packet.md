# Skill review packet

Externalized Step 2 verify for `review-skill.md`. Findings surfaced from cross-walk in `skill-coverage-map.md`, walked against the Review checklist in `review-skill.md`.

**Total: 4 findings + 1 deferred-to-test-skill** (1 HIGH-A canon cascade, 1 MEDIUM-B coverage gap, 1 MEDIUM-C marginal completeness, 1 LOW-D consistency, 1 NOTE for behavioral test scenarios). Estimated walk-time at ~3 min/finding: **~15 minutes**.

| Severity | Category | Count |
|---|---|---|
| HIGH | A — Coverage gaps (canon cascade) | 1 |
| MEDIUM | B — Spec misalignment | 1 |
| MEDIUM | C — Template completeness | 1 |
| LOW | D — Inter-template consistency | 1 |
| NOTE | F — Test scenarios (deferred) | 1 |

## Up-front observations — what's strong

- **Command coverage: PERFECT.** All 8 operations from methodology §12 have task templates; 6 generation variants exist for the per-target generate splits. No commands without templates.
- **Codæ 10-section completeness: PERFECT.** All 14 task templates have all 10 sections (Purpose / Inputs / Preconditions / Steps / Output / Postconditions / Constraints / Invariants / Validation / Failure modes).
- **Vocabulary consistency: STRONG.** "approval unit" used 14 times, no "approval scope" drift. "subagent" used 62 times, no hyphen variants.
- **Mode coverage: STRONG.** Every task template handles vibe + full modes appropriately; ux-mode has a dedicated `generate-product-specs-from-ux.md` variant.
- **Artifact templates align with impl §6** by spot-check (intent.md, prd.md, usm.md, dm.md, ux.md, system.md, container.md, component.md all carry the v0.3 frontmatter shape including `approval_unit` and `layer` where applicable).

---

## SKILL-FIND-001 [HIGH / A — Canon misalignment cascade]

**Contract Graph cascade in skill bundle (CANON-FIND-010).**

**Locations — 9 lowercase "contract graph" usages in `vibeloom-templates.md`:**

| Line | Block | Current text |
|---|---|---|
| 189 | skill/SKILL.md authoritative-sources | `entities, tiers, modes, operations, approval model, contract graph, status taxonomy, ...` |
| 259 | skill/SKILL.md Substrate description | `regenerable state (contract graph, status). Safe to delete; engine rebuilds.` |
| 294 | skill/SKILL.md Guardrails | `the methodology's DAG. The valid set is in the methodology's DAG.` |
| 364 | skill/subagent-prompt.md | `The full contract graph (you have your slice; that's enough).` |
| 1500 | tasks/approve.md | `Refresh contract graph cache.` |
| 1507 | tasks/approve.md | `Contract graph cache refreshed.` |
| 1573 | tasks/eval.md Step 1 | `Build/refresh contract graph via engine \`parse + graph\`.` |
| 1766 | tasks/generate-context.md (or similar) | `Contract graph updated.` |
| 1943 | tasks/generate-product-specs-from-ux.md (or similar) | `Contract graph updated.` |

**Why it's a finding:** Per CANON-FIND-010, "Contract Graph" is the canonical proper-noun entity name. These skill-template references to **the** Contract Graph (the entity) should be capitalized. (Bare "DAG" referring to the structural property stays lowercase per the same finding.)

**Proposed fix:** 9 string replacements:
- 8 of: `contract graph` → `Contract Graph` (lines 189, 259, 364, 1500, 1507, 1573, 1766, 1943)
- 1 of (line 294): `the methodology's DAG. The valid set is in the methodology's DAG.` → `the methodology's Contract Graph (§5.1 derivation rules + §8 graph). The valid set is in the methodology.`

**Affected pages:** vibeloom-templates.md (single canonical file). Templates extraction will re-materialize.

---

## SKILL-FIND-002 [MEDIUM / B — Spec misalignment / coverage gap]

**`derives_from` validation per §5.1 is inconsistent across generation tasks and absent at gate-point tasks.**

**Cascade source:** CANON-FIND-011 added §5.1 derivation rules + §8.2 universal-trace rule. The new §16 acceptance item I just added says "Engine validates `derives_from` per §5.1 derivation rules and §8.2 universal-trace rule." Skill task templates should know to expect this validation at structural-eval time.

**Current state per generation task:**

| Task | derives_from coverage |
|---|---|
| `tasks/generate-intent-specs.md` | ✓ Correctly notes intent is root, no derives_from required |
| `tasks/generate-product-specs.md` | ✓ Has explicit §5.1 reference + Validation check |
| `tasks/generate-product-specs-from-ux.md` | ✓ Multi-source derives_from check (intent + ux + mockup) |
| `tasks/generate-ux-specs.md` | Partial — checks derives_from but doesn't cite §5.1 |
| **`tasks/generate-system-specs.md`** | **MISSING — no derives_from / derivation references at all** |
| `tasks/generate-context.md` | Implicit (relies on engine `eval --target context`) — OK |
| `tasks/generate-code-component.md` | N/A — code doesn't have IDed items with derives_from |

**Current state at gate-point tasks (approve / eval / review):**

| Task | derives_from check |
|---|---|
| `tasks/approve.md` | **Doesn't explicitly enforce derives_from per §5.1** at approval time |
| `tasks/eval.md` | **Doesn't cite §5.1 derivation rules** in structural checks (relies on engine knowing) |
| `tasks/review.md` | **Doesn't surface derives_from violations** as a finding category |

**Why it's a finding:** Engine validates per the new §16 acceptance, but skill task templates don't tell users this validation is enforced. When a user runs `/vibeloom approve product-specs` and the engine rejects on a §5.1 derivation violation, the user has no template-level expectation of that check. Documentation gap.

**Proposed fix:** Three small edits:

1. **`tasks/generate-system-specs.md` Validation section** — add bullet:
   `- Every IDed item cites at least one approved upstream item in derives_from per implementation §5.1 derivation rules.`

2. **`tasks/generate-ux-specs.md` Validation section** — append `(per implementation §5.1 derivation rules)` to existing derives_from bullet.

3. **`tasks/eval.md` Steps Decidable tier OR Failure modes** — add reference: "Structural checks include §5.1 derivation rule validation — every non-root item must cite valid upstream basis transitively reaching CAP/CST."

(approve.md and review.md don't need separate edits — they can rely on eval.md's coverage since eval is part of approval/review preconditions.)

**Affected pages:** vibeloom-templates.md (3 task-template Validation sections). Templates re-extraction.

---

## SKILL-FIND-003 [MEDIUM / C — Template completeness]

**Task templates implicitly identify their source operation via the HTML comment `Operation: X` header, but don't cite the canonical §15.X explicitly.**

**Current state:** All 14 task templates have an HTML comment header like:
```
<!--
VibeLoom task template: approve
Operation: approve
Invoked by: SKILL.md when user runs `/vibeloom approve <approval-unit>`
-->
```

The `Operation: approve` line maps by name to impl §15.5. An agent reading the template can find the source by operation name + §15.X lookup.

**Why it's borderline a finding:** The review-skill.md prompt says "Every task template must reference its source operation in `vibeloom-implementation.md` §15." Two readings:
- **Strict:** explicit `§15.X` citation required → finding (none have it)
- **Pragmatic:** `Operation: X` line + §15 lookup is sufficient → coverage met

**Proposed fix — three options:**

- **(a) Defer / mark as coverage-met-by-convention.** The `Operation: X` line is sufficient; adding explicit §15.X citations is bureaucratic.
- **(b) Add a one-line `Source: implementation §15.X` to every task template's HTML comment header.** 14 small edits, traceability win.
- **(c) Add §15.X cite to Purpose section.** Each task's Purpose para gains `(implementation §15.X)`. More visible than HTML comment.

I lean **(a)** — the existing convention is enough; explicit citation is bureaucratic.

**Affected pages:** vibeloom-templates.md (only if (b) or (c)).

---

## SKILL-FIND-004 [LOW / D — Inter-template consistency]

**Artifact templates use "(per DAG)" — could tighten to "(per Contract Graph §8 + §5.1)" for consistency with CANON-FIND-010 + CANON-FIND-011.**

**Current state:** Multiple artifact templates have headings like:
```
Derivation rules (per DAG):
```

(In artifact templates for prd.md, usm.md, dm.md, container.md, component.md, etc.)

**Why it's a finding:** Per CANON-FIND-010, "Contract Graph" is the canonical entity name. Bare "DAG" is acceptable for the structural property (the graph IS a DAG), but in this context the rules being cited are derivation-edge rules from §5.1 — those live in the Contract Graph (§8 + §5.1). The phrase "(per DAG)" reads as "per the DAG structure," which is technically right but loses the §-precision.

**Proposed fix:** Replace `Derivation rules (per DAG):` → `Derivation rules (per Contract Graph §5.1 derivation rules):` in all 6 artifact-template instances.

OR: tighter — `Derivation rules (per §5.1):` — even less verbose.

**Affected pages:** vibeloom-templates.md (6 instances across artifact templates).

I lean the tighter form.

---

## SKILL-FIND-005 [NOTE / F] — Test scenarios (deferred to test-skill once engine ships)

Per the review-skill.md prompt's design, behavioral testing of the skill on a scratch repo is deferred to a future `test-skill.md` prompt that requires a working engine (engine v0.4+).

Test scenarios that will eventually need coverage when test-skill exists:
- vibe-init in empty dir + intent.md edit + approve + generate cycle
- pm-init + generate product-specs (with §5.1 derives_from validation expected)
- ux-init + drop mockups + generate-product-specs-from-ux (peer-review surface)
- approve on already-approved item (lifecycle check)
- generate with no approved upstream (should fail at §5.1 universal-trace check)
- import on existing codebase + brownfield draft generation
- reconcile on detected drift (preserve-contract / amend-contract / user-defined paths)
- vibe → pm upgrade migration

Surfaced here as informational.

---

## Combined application notes

- **SKILL-FIND-001** (Contract Graph cascade) — straightforward 9-string replacement batch.
- **SKILL-FIND-002** (derives_from coverage) — 3 small Validation-section edits.
- **SKILL-FIND-003** (§15 reference) — defer or pick (b)/(c); my lean is defer.
- **SKILL-FIND-004** (DAG → Contract Graph in artifacts) — 6 replacements; pure consistency polish.
- **SKILL-FIND-005** — informational, no action.

If all applied: ~18-19 small edits across `vibeloom-templates.md`. Net likely +0 to +5 lines (substitutions + small additions).
