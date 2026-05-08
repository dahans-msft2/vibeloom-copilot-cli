# Site review packet

Externalized Step 2 verify for `review-site.md`. Findings surfaced from cross-walk in `site-claim-map.md`, walked against the Review checklist in `review-site.md`.

**Total: 5 findings** (3 HIGH-A canon cascades, 1 MEDIUM-D cross-page hygiene, 1 NOTE about deferred marketing-punch deep dive). Estimated walk-time at ~2 min/finding: **~10 minutes**.

| Severity | Category | Count |
|---|---|---|
| HIGH | A — Canon misalignment | 3 |
| MEDIUM | D — Cross-page hygiene | 1 |
| NOTE | (deferred deep dive) | 1 |

## Up-front observations

- **No Category A canon-misalignments beyond the Contract Graph cascade** — the recent canon-review work largely didn't touch surface-level claims (no §10 metric on site; no §16/§17 section references; no §5.1 derivation-rule details surfaced).
- **Nav consistency: PERFECT.** Every page links to the same 6 destinations (codae, contact, get-started, implementation, index, methodology). 404 and codæ-manifesto are intentionally not in nav.
- **CTA routing: PERFECT.** Every "Get started" CTA points at `get-started.html`. No stale `index.html#start` references remain.
- **Brand consistency at the structural level: STRONG.** Same nav, footer, color/font system across all 8 pages.

## Marketing-punch deep dive — DEFERRED

A full Category B (marketing punch) pass would require reading each page top-to-bottom for: headline pull, hero copy strength, narrative arc cohesion, hedge-word density, comparison table cell concreteness. That's a heavy session in itself (~2 hours). This first review-site pass focuses on cascades + structural hygiene; deeper marketing review is a separate pass.

If you want a marketing-punch pass in this session, I can run it after these 4 findings. Otherwise, recommend deferring to a dedicated session.

---

## SITE-FIND-001 [HIGH / A — Canon misalignment]

**Single direct cascade from CANON-FIND-010 (Contract Graph rename) — site still uses "derivation graph" once.**

**Location:** `v03/site/public/methodology.html` line 205.

**Current text:**
```
<p>Two co-informing tiers. Either can lead depending on mode (<code>pm</code> or <code>ux</code>). The approved derivation graph remains acyclic.</p>
```

**Why it's a finding:** Canon §8.2 (after CANON-FIND-010) now reads "the approved Contract Graph remains acyclic." Site is one rename behind.

**Proposed fix:**

`old_string`: `<p>Two co-informing tiers. Either can lead depending on mode (<code>pm</code> or <code>ux</code>). The approved derivation graph remains acyclic.</p>`

`new_string`: `<p>Two co-informing tiers. Either can lead depending on mode (<code>pm</code> or <code>ux</code>). The approved Contract Graph remains acyclic.</p>`

**Affected pages:** methodology.html only.

---

## SITE-FIND-002 [HIGH / A — Canon misalignment]

**Methodology page uses "contract graph" lowercase in TOC, h2, table, and body prose where canon §8 now establishes "Contract Graph" as the proper noun.**

**Location:** `v03/site/public/methodology.html` lines 139, 245, 247, 369, 412 (5 occurrences).

**Current state — five lowercase usages:**
- Line 139 (TOC): `<li><a href="#graph">Contract graph</a></li>` — actually starts with capital "Contract"; let me verify
- Line 245 (h2): `<h2 id="graph">The contract graph</h2>` — lowercase
- Line 247 (body): `<p>v0.3 ships the contract graph as a <strong>knowledge graph</strong>...`
- Line 369 (table): `<td>Contract graph + reconciliation</td>` — title-case "Contract graph"; needs verification
- Line 412 (body): `<p>...the contract stack with ux-specs as peer to product-specs; modes...; the contract graph; drift detection...</p>`

Per canon §8 (after CANON-FIND-010): "The **Contract Graph** is the parsed, queryable model..." — proper noun convention established.

**Why it's a finding:** Canon-derived site page should use the canonical proper-noun term consistently when referring to **the** Contract Graph entity. Lowercase "contract graph" reads as a generic term; capitalized "Contract Graph" reads as the named entity. Site drift from canon convention.

**Proposed fix:** Replace "contract graph" → "Contract Graph" where the reference is to the entity (proper noun); leave alone where it's a generic compound noun. Five locations to walk individually:

1. Line 139 TOC: confirm it's already "Contract graph" (just capital C); make it "Contract Graph" (both capitals).
2. Line 245 h2: "The contract graph" → "The Contract Graph".
3. Line 247 body: "the contract graph as a knowledge graph" → "the Contract Graph as a knowledge graph".
4. Line 369 table cell: "Contract graph + reconciliation" → "Contract Graph + reconciliation".
5. Line 412 body: "the contract stack ...; the contract graph; drift detection..." → "the contract stack ...; the Contract Graph; drift detection..."

**Affected pages:** methodology.html only.

---

## SITE-FIND-003 [HIGH / A — Canon misalignment]

**Implementation page uses "contract graph" lowercase in meta, TOC, and body prose.**

**Location:** `v03/site/public/implementation.html` lines 8, 132, 146.

**Current state:**
- Line 8 (meta keywords): `<meta name="keywords" content="vibeloom-engine, Claude Code skill, deterministic substrate, contract graph, approval traces, dispatch plan">`
- Line 132 (TOC): `<li><a href="#graph">The contract graph</a></li>`
- Line 146 (body): `<p>...This page covers boundaries, substrate, engine CLI, approval traces, contract graph, IDs and frontmatter, trace families, subagent dispatch, install + run, source layout.</p>`

**Why it's a finding:** Same as 002 — canon §8 established "Contract Graph" proper noun; implementation.html's reference to the entity should be consistent.

**Proposed fix:** Three locations to walk:
1. Meta keywords: arguably keep lowercase (SEO keywords are conventionally lowercase). DEFER decision per user.
2. TOC: "The contract graph" → "The Contract Graph".
3. Body prose: "...contract graph, IDs..." → "...Contract Graph, IDs...".

There's likely also a section heading near `id="graph"` — I'll need to check during the walk.

**Affected pages:** implementation.html only.

---

## SITE-FIND-004 [MEDIUM / D — Cross-page hygiene]

**Title patterns are inconsistent across pages — at least 3 distinct shapes.**

**Location:** all 8 site pages, the `<title>` tag.

**Current state — patterns:**

| Pattern | Page(s) |
|---|---|
| `X — Y · VibeLoom` | methodology, implementation, contact, 404 |
| `X — Y` (no VibeLoom suffix) | codae ("codæ — Contract-Driven Agentic Engineering · Whitepaper") |
| `X — Y · v0.3` (version suffix instead of brand) | get-started ("Get started — VibeLoom (30-minute on-ramp) · v0.3") |
| `VibeLoom — Y` (brand-led, no suffix) | index |
| `codæ — Y · Z` | codae and codæ-manifesto (both pages, slightly different Z) |

**Why it's a finding:** Title is the most-visible cross-page element (browser tab, search result, share preview). Inconsistent patterns confuse the SEO + UX. Pick one canonical pattern.

**Proposed fix — option (a), conservative: all pages adopt `X — Y · VibeLoom` shape, with codæ pages having Y as the differentiator:**

| Page | Proposed title |
|---|---|
| index.html | `VibeLoom — Contract-Driven Agentic Engineering` (current — keep as the brand-led landing) |
| codae.html | `codæ — Contract-Driven Agentic Engineering · VibeLoom` (drop "Whitepaper" suffix or move it inline) |
| codæ-manifesto.html | `codæ Whitepaper — Dark-Factory AI Coding · VibeLoom` |
| methodology.html | `Methodology — Contract-Driven Agentic Engineering · VibeLoom` (current) |
| implementation.html | `Implementation — Skill + Engine + Runtime · VibeLoom` (current) |
| get-started.html | `Get started — VibeLoom 30-minute on-ramp · VibeLoom` — wait, redundant. Or: `Get started — 30-minute on-ramp · VibeLoom` (drop the "VibeLoom" mid-title since it's in the suffix) |
| contact.html | `Contact Us — Make Coding Agents Useful Past the Demo · VibeLoom` (current) |
| 404.html | `404 — Not found · VibeLoom` (current) |

**Proposed fix — option (b), aggressive consolidation: rewrite all titles to `Page — Tagline · VibeLoom`:**

| Page | Proposed title |
|---|---|
| index.html | `VibeLoom — Contract-Driven Agentic Engineering for Long-Lived AI Codebases` |
| codae.html | `codæ — Contract-Driven Agentic Engineering · VibeLoom` |
| codæ-manifesto.html | `codæ Manifesto — Dark-Factory AI Coding · VibeLoom` |
| methodology.html | `Methodology — VibeLoom` |
| implementation.html | `Implementation — VibeLoom` |
| get-started.html | `Get started — VibeLoom` |
| contact.html | `Contact — VibeLoom` |
| 404.html | `404 — VibeLoom` |

I lean (a) — preserves SEO-valuable taglines while normalizing the suffix pattern.

**Affected pages:** all 8 site pages (title-tag-only edits — minimal risk).

---

## SITE-FIND-005 [NOTE / deferred] — Marketing punch deep dive

Not a single finding, but a flag. A full Category B (marketing punch) review of headline pull, hero copy, narrative arc, hedge-word density, and comparison-table cell concreteness across all 8 pages would be a separate ~2-hour session. **Recommend deferring to a dedicated review-site pass** focused on copy improvement.

If approved, scope of that pass would include:
- Per-page hero/sub copy critique
- Comparison section (in methodology.html) cell-by-cell concreteness check
- Hedge-word audit ("could potentially help teams that may want to…")
- Trust strip + hero meta concreteness
- Codae page case-making density vs distillation

This packet captures findings that are mechanical or hygiene-level. Deeper copy work is honest creative work — separate session.

---

## Combined application notes

- SITE-FIND-001 + 002 + 003 are all the Contract Graph cascade. They could be applied as one batch, OR walked individually for finer control.
- SITE-FIND-004 (title patterns) is independent. Walk separately.
- SITE-FIND-005 is informational; no decision needed beyond "approve the deferral" or "want it now in this session."
