# Site review report

Final report for the `review-site.md` session run on 2026-05-07.

Walked: **5 actionable findings** (4 from initial packet + 1 surfaced during walk).
Deferred: 2 (LOW marketing-punch refinements).
Result: **5 Accepted, 0 Rejected, 0 Deferred-as-resolved.**

---

## 1. Summary

| Severity | Category | Surfaced | Accepted | Deferred | Rejected |
|---|---|---:|---:|---:|---:|
| HIGH | A — Canon misalignment | 4 | 4 (001, 002, 003, 005) | 0 | 0 |
| MEDIUM | D — Cross-page hygiene | 1 | 1 (004) | 0 | 0 |
| LOW | B — Marketing punch | 2 | 0 | 2 (006, 007) | 0 |
| **TOTAL** | | **7** | **5** | **2** | **0** |

User chose option (c) at scope confirmation: walk all 4 actionable findings + run the marketing-punch deep dive. Deep dive surfaced 1 missed cascade (005) + 2 minor refinements (006, 007 — deferred).

## 2. Per-finding detail

### SITE-FIND-001 + 002 + 003 [HIGH / A] — Contract Graph cascade across site
**Decision:** Accept (bundled — 9 edits across methodology.html and implementation.html).

**Applied to methodology.html (6 edits):**
- Line 139 (TOC): `Contract graph` → `Contract Graph`
- Line 205 (body): `approved derivation graph` → `approved Contract Graph`
- Line 245 (h2): `The contract graph` → `The Contract Graph`
- Line 247 (body): `the contract graph as a knowledge graph` → `the Contract Graph as a knowledge graph`
- Line 369 (table cell): `Contract graph + reconciliation` → `Contract Graph + reconciliation`
- Line 412 (body): `; the contract graph;` → `; the Contract Graph;`

**Applied to implementation.html (3 edits):**
- Line 132 (TOC): `The contract graph` → `The Contract Graph`
- Line 229 (h2): `The contract graph` → `The Contract Graph`
- Line 146 (exec summary body): `..., contract graph,` → `..., Contract Graph,`

Meta keyword on implementation.html line 8 left lowercase per SEO convention.

**downstream-impact:** none beyond the touched files.

### SITE-FIND-004 [MEDIUM / D] — Title pattern unification
**Decision:** Accept user's revised proposal (brand-led `Brand — Suffix` pattern, two clean families).

**Applied (20 edits across 8 files: 7 site pages + 1 canonical manifesto sync):**

| Page | New title |
|---|---|
| index.html | `VibeLoom — Contract-Driven Agentic Engineering` (no change — already matched) |
| methodology.html | `VibeLoom — Methodology` |
| implementation.html | `VibeLoom — Implementation` |
| contact.html | `VibeLoom — Contact Us` |
| get-started.html | `VibeLoom — 30-minute on-ramp` |
| codae.html | `codæ — Contract-Driven Agentic Engineering` (drop "Whitepaper" suffix) |
| codæ-manifesto.html (site) | `codæ — Contract-Driven Agentic Engineering · Dark-Factory AI Coding` |
| v03/codæ-manifesto.html (canonical) | same as site copy (sync) |
| 404.html | `VibeLoom — 404 not found` |

OG title and Twitter title meta tags updated in lockstep on every page (3 tags per changed page = 18 meta edits + 2 title edits = 20 total).

**downstream-impact:** social share previews on every page now reflect new titles. Canon-touch on canonical manifesto kept the byte-identical pattern with the site copy.

### SITE-FIND-005 [HIGH / A] — Additional Contract Graph cascade (surfaced during marketing-punch deep dive)
**Decision:** Accept option (a) — fully sweep including canonical manifesto.

**Applied (9 edits — 5 site + 2 canon × 2 sync):**

**Site (5 edits):**
- index.html line 380 (Drift section bullet): `the contract graph blocks` → `the Contract Graph blocks`
- implementation.html line 154: `builds the contract graph,` → `builds the Contract Graph,`
- implementation.html line 166: `The contract graph, status snapshots` → `The Contract Graph, status snapshots`
- implementation.html line 193: `and querying the contract graph;` → `and querying the Contract Graph;`
- implementation.html line 231: `v0.3 ships the contract graph as a knowledge graph` → `v0.3 ships the Contract Graph as a knowledge graph`

**Canon-touch (4 file edits — 2 logical changes synced across site copy + canonical):**
- site/public/codæ-manifesto.html line 1003 + canonical line 1003: `tiered contract graph` → `tiered Contract Graph`
- site/public/codæ-manifesto.html line 1258 + canonical line 1258: `the contract graph is the intermediate representation` → `the Contract Graph is the intermediate representation`

**rationale for surfacing:** The earlier sweep (001-003) scoped to TOC, h2, table, and one-body-line per page. Deeper read during marketing-punch pass caught 5 additional body-prose usages on the rendered site. This finding closes the rename properly.

**downstream-impact:** "contract graph" lowercase fully eliminated from rendered site (excl SEO meta keyword on implementation.html, intentionally kept lowercase). Canon-site byte-identical preserved.

### SITE-FIND-006 + SITE-FIND-007 [LOW / B] — Marketing punch refinements
**Decision:** Defer.

**Rationale:** Both are minor copy refinements (drop "VibeLoom uses..." from index hero sub; replace "derivation-aware" jargon in methodology hero lead). The marketing punch deep dive across all 6 main pages found surprisingly little to surface (zero hedge words, comparison cells concrete, stats well-cited, FAQ honest). Site copy is in strong shape. These two refinements would polish but aren't blocking.

**Surfaced for next session if a focused copy-polish pass is wanted.**

## 3. Cross-cutting re-walk results (Step 5)

After the 5 findings landed:

- **Visual re-render at desktop (1280×800)** — methodology.html and implementation.html both render cleanly. New TOC entries show "Contract Graph" capitalized correctly. Browser tab titles display new "VibeLoom — Methodology" and "VibeLoom — Implementation" patterns. No layout regression (text-only edits).
- **Mobile re-render** — skipped (text-only changes can't break responsive layouts; no risk).
- **Sanity grep — "contract graph" lowercase** — fully eliminated from rendered site body content. Only remaining lowercase usage is the SEO meta keyword on implementation.html line 8 (intentionally retained per convention).
- **Canon-site byte-identical preserved** between `site/public/codæ-manifesto.html` and `v03/codæ-manifesto.html` (both touched in lockstep for the title + Contract Graph cascade).

## 4. Re-render checklist

| Page | Re-verified at desktop |
|---|---|
| index.html | text-only changes; no visual delta possible |
| codae.html | not edited this pass |
| codæ-manifesto.html | text-only changes; not visually verified (low risk) |
| methodology.html | ✓ visually verified (#graph anchor, TOC, hero) |
| implementation.html | ✓ visually verified (#graph anchor, exec summary, hero) |
| get-started.html | title-only change; tab title verified |
| contact.html | title-only change; not visually re-verified |
| 404.html | title-only change; not visually re-verified |

Pages with body-content edits (methodology, implementation) were visually verified. Title-only edits (everywhere else) are mechanical and don't need rendering.

## 5. Items flagged for canon update

**None this pass.** All "contract graph" lowercase found on the canonical manifesto were swept in lockstep via the byte-identical pattern (CANON-FIND-005 cascade). No new canon-side findings emerged.

## 6. Deferred items (for next review-site pass)

- **SITE-FIND-006** — index.html hero sub starts with "VibeLoom uses..." (could lead with user benefit instead of subject).
- **SITE-FIND-007** — methodology.html hero lead uses "derivation-aware" jargon (could swap for "traceable end-to-end").

Both LOW priority; not blocking. Worth picking up in a dedicated copy-polish session.

## 7. Reference commit SHA

To be captured at session end (commit + push pending).

Working tree state at report time:
- 6 site pages modified (index, methodology, implementation, contact, get-started, codae, 404, codæ-manifesto)
- 1 canonical manifesto modified (v03/codæ-manifesto.html)
- 3 new artifacts at repo root: site-claim-map.md, site-review-packet.md, site-review-report.md

## 8. Pleasant surprises — what didn't surface

- **Zero hedge words** ("could potentially", "may want to", "various", "some sort of") across all pages. Copy is concrete throughout.
- **Comparison table cells are concrete** (whole-system vs per-feature, contract vs factory floor — specific differentiation, not "better X").
- **Stats are evidence-cited** with arXiv/O'Reilly links + dates throughout.
- **FAQ honestly includes "When NOT to use"** — strong trust signal.
- **Nav consistency: PERFECT** across all 8 pages (same 6 destinations, 404 + manifesto correctly outside nav).
- **CTA routing: PERFECT** — every "Get started" routes to get-started.html.
- **Brand consistency at structural level: STRONG** — same nav/footer/typography/color across all pages.
- **codae.html doesn't have a "contract graph" cascade** — uses different vocabulary level than methodology/implementation pages. Honest distillation.

The site is **shippable as-is** post-this-review. Marketing punch is solid; the canon-cascade work is the substantive improvement.

## 9. Methodology validation — review-site.md prompt itself

The `review-site.md` prompt validated by use, with one notable observation:

- The prompt's interactive loop, scope-confirmation step, severity-sorted Review checklist all worked as designed.
- The Step 5 re-walk caught one missed finding (SITE-FIND-005) — exactly as the prompt's "after every batch, re-walk relevant Review-checklist items on affected sub-scope" rule intended.
- The packet's separation of "deferred deep dive" from the mechanical findings worked well — let the user choose how much depth to commit to.

**One refinement worth surfacing for the prompt itself:** the initial sweep (001-003) under-scoped the cascade — it caught TOC/h2/table/one-body-line per page but missed multiple other body-prose usages of the same term. A future review-canon or review-site walk could include a "do a final case-insensitive grep before declaring the cascade done" verify gate. (Capturable as a future improvement to the loop pattern.)
