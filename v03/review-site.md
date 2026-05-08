# Review the site

A prompt for Claude Code (or any equivalent agentic coding tool). Reads the marketing-surface artifacts and runs an interactive review loop with the user — surfacing findings, proposing bounded fixes, applying or deferring per user direction.

This prompt is itself codæ-shaped and reuses the interactive loop from [`tasks/review.md`](vibeloom-templates.md). The criteria the agent surfaces against live in **§ Review checklist** below — that's the human-editable surface.

**Time budget.** Half-day; ~1–3 min per finding (marketing prose iterates faster than canon).

---

## Purpose

Audit the marketing-surface artifacts — every page under `v03/site/public/` and the standalone `v03/vibeloom-comparison.html` — against the **Review checklist** below. Apply changes in place via the interactive loop. Produce a re-render checklist plus any items flagged for canon update.

## Inputs

| Surface | Files | Role |
|---|---|---|
| Site pages | `v03/site/public/*.html` (index, codae, methodology, implementation, get-started, contact, 404) | Public marketing + onboarding surface |
| Styling | `v03/site/public/styles.css` | Shared visual system |
| Standalone marketing | `v03/vibeloom-comparison.html` | Comparison vs spec-driven tools |
| Source of truth (read-only) | `v03/codæ-manifesto.html`, `v03/vibeloom-methodology.md`, `v03/vibeloom-implementation.md` | What the site faithfully represents |

The canon is **read-only** during this review. Site contradictions are site bugs (Category A). Canon issues belong in [`review-canon.md`](review-canon.md).

## Preconditions

- All site files exist; working tree is clean (recommend a checkpoint commit).
- A local server is running (e.g. `python3 -m http.server 8126` from `v03/site/public/`) so the agent can fetch live-rendered pages and screenshot via Chrome MCP for visual checks.
- The user is committing time for an interactive session.

## Architecture sketch — narrative arc

```text
index.html       → claim, evidence, hero CTA
codae.html       → WHY: makes the philosophical case
methodology.html → WHAT: paradigm contents (practitioners)
implementation.html → HOW: engine internals (builders)
get-started.html → HOW DO I START
contact.html     → HOW DO I GET HELP
```

The arc must pull a visitor from "I don't know what this is" → "I see why it matters" → "I'm trying it."

## Steps

1. **Read each site page top-to-bottom + skim the canon.** (a) Site only — note headlines, claims, CTAs, structural anomalies. (b) Canon — refresh on what the site is supposed to represent. (c) Cross-walk — for every load-bearing claim on the site, locate the canon basis.
   **Verify:** write `site-claim-map.md` at repo root listing every load-bearing claim and the canon section that backs it.

2. **Build the site review packet.** Walk every item in the **Review checklist** below. For each surfaced finding: location (file + section + element), current text/attribute (verbatim quote), why it's a finding, proposed bounded fix (concrete diff), affected pages if the fix cascades.
   **Verify:** `site-review-packet.md` at repo root.

3. **Surface the packet to the user as a summary first** — counts by severity, total findings, estimated walk-time. Confirm scope.

4. **Walk findings in priority order.** For each:
   - Quote location + current text/attribute.
   - Explain why.
   - Propose the fix.
   - User picks: **Accept** / **Edit** / **Defer** / **Reject**.
   - On Accept / Edit: apply, log, move on.
   - On Defer / Reject: log + rationale, move on.
   - After every batch (default: one per page-section, OR every 5 fixes): take a fresh screenshot of the affected page (Chrome MCP), visually re-verify, surface any new visual finding immediately.

5. **After all findings: re-render every page at desktop (1280×800) AND mobile (414×900).** Confirm no horizontal overflow, no broken layouts, all CTAs route correctly. Re-walk the Review checklist on the full site.

6. **Produce `site-review-report.md`** per § Final report.

## Review checklist

**This is the human-editable surface — adjust bullets as project priorities shift.** The agent surfaces a finding for any item that fails on inspection.

### A — Canon misalignment (HIGH)

- Site claim with no canon basis (a feature mentioned that the methodology doesn't define).
- Site contradicts canon (e.g. methodology says "five modes," site says "four").
- Outdated stat, claim, or quote (an evidence stat from an older version of the manifesto).
- Manifesto excerpt on `codae.html` doesn't match the canonical `v03/codæ-manifesto.html` text.

### B — Marketing punch (MEDIUM-HIGH)

- Headline that doesn't pull (vague verbs, abstract nouns, missing the "so what").
- Hero copy that buries the lede.
- Hedge-padded claim ("could potentially help teams that may want to…").
- Concrete number / outcome buried in prose where it should be the headline.
- Section that summarizes the canon without adding marketing value (cut or compress).
- Comparison table cell that's vague where it could be concrete (e.g. "better drift handling" → "drift detection across whole-system contract; per-feature competitors detect only within feature scope").

### C — Brand consistency (MEDIUM)

- Typography drift (heading using wrong weight; code block using wrong font).
- Color drift (button using non-brand red; missing the signature `#e84057`).
- Spacing irregularity (inconsistent vertical rhythm between sections).
- Codæ wordmark inconsistent (the æ should always be in signature red).
- Voice drift (one page sounds like a brochure, another like a textbook — both should be confident, declarative, technical).

### D — Cross-page hygiene (MEDIUM)

- Nav entries differ across pages.
- Footer differs across pages.
- A CTA labeled "Get started" routing somewhere other than `get-started.html`.
- Stale link (e.g. a page still references `index.html#start` after the get-started page was added).
- Missing `aria-current="page"` or wrong `is-active` on the current page's nav entry.

### E — SEO / accessibility (LOW)

- Page missing unique title or meta description.
- OG tags missing or generic (same OG image across pages where page-specific would help).
- Image without alt text (or stale alt text after a content change).
- JSON-LD with stale `dateModified` or wrong `@type`.
- Skip link missing or pointing at wrong anchor.
- Heading hierarchy skips levels (h1 → h3, no h2).

### F — Mobile / responsive (LOW-MEDIUM)

- Horizontal overflow at 414px width.
- Comparison matrix that doesn't reflow on mobile.
- Hero text too large on mobile.
- Touch targets smaller than 44×44px.

## Output

- Edits applied in place across site files (per Accept / Edit decisions).
- `site-claim-map.md` — Step 1 verify.
- `site-review-packet.md` — Step 2 verify.
- `site-review-report.md` — final disposition + re-render checklist + items flagged for canon update.

## Postconditions

- Every checklist item walked; every finding resolved with rationale logged.
- Every page that was edited has been visually re-verified at desktop AND mobile widths.
- Cross-cutting re-walk after each batch surfaced no un-handled findings.

## Constraints

- **Agents propose; humans approve.** Never auto-apply a fix.
- **Canon is the source of truth.** Site contradictions are site bugs; don't edit the canon to make a site claim true. Flag for [`review-canon.md`](review-canon.md) instead.
- **Marketing punch ≠ marketing fluff.** Every word earns its place; the marketing surface gets to be *catchier* than the canon, not just shorter.
- **Brand consistency over personal preference.** Established brand (Inter sans, JetBrains Mono, Fraunces italic serif, signature red `#e84057`, codæ wordmark) is fixed.
- **No silent rewrites.**
- **Don't drift into canon edits.** If a finding requires canon change, flag in report; don't edit canon here.

## Invariants

- The narrative arc is preserved (claim → why → what → how → start → contact).
- Nav/footer are consistent across every page.
- The codæ wordmark renders correctly (æ in signature red) on every page where it appears.
- Every CTA routes to a real, non-404 destination.
- Skip link present on every page; nav keyboard-traversable.

## Validation (exit gates)

- Every Review-checklist item considered (or explicitly skipped, recorded in report).
- Every accepted/edited finding applied to site files in place.
- Every page edited visually re-verified at desktop + mobile.
- The final report produced.
- Reference commit SHA at session end.

## Failure modes

- **Site claim with no canon basis.** Two paths: (a) edit the site claim to match canon, or (b) flag for canon update via [`review-canon.md`](review-canon.md). User picks.
- **Brand drift on >3 pages.** Group as ONE finding with `affected pages: [...]`, not N findings.
- **User wants a major redesign.** Out of scope. Note in report; recommend a separate design pass.
- **Visual screenshot reveals a layout regression caused by an accepted CSS edit.** Surface immediately; ask user to reconsider; do not silently roll back.
- **Canon change cascades to many site claims.** Flag the cascade; schedule a follow-up review-site after the canon settles.

## Anti-patterns

- Auto-applying any fix.
- Proposing a redesign instead of bounded edits.
- Editing the canon to "make the site claim true."
- Inventing new visual elements when the right answer is reusing existing primitives.
- Skipping the visual re-verify after CSS-affecting edits.
- Suggesting "consider rephrasing" without the actual rephrasing.

## Final report

`site-review-report.md` at repo root:

1. **Summary table:** N findings; M applied, K modified, D deferred, R rejected; by Category × Severity.
2. **Per-finding detail.** ID (`SITE-FIND-001`…), location (file + section + element), severity, category, current quote, why, proposed fix, user decision, applied diff (if Edit), rationale (if Defer/Reject), `affected pages: [...]`.
3. **Cross-cutting re-walk results.**
4. **Re-render checklist:** which pages visually re-verified at desktop + mobile.
5. **Items flagged for canon update:** input for the next [`review-canon.md`](review-canon.md) session.
6. **Deferred items.**
7. **Reference commit SHA** at session end.

## Checkpointing

Commit after each batch — group by page or category (e.g. `site: codae.html — claim alignment`).

## After this review

- If findings flagged for canon update, schedule [`review-canon.md`](review-canon.md) before the next site pass.
- If no canon-side cascades, the site is shippable.
- A major brand shift discussed but deferred = a separate design pass, not a future review-site run.
