# Reference: eval-passes-site

Adversarial review passes for `eval site`.

Adapted from v03's `review-site.md`. Adjusted for the marketing-register expectation: the site does not need to cover every canon concept; it MUST NOT contradict canon.

## Goal

Check that `vNN/site/**` does not contradict canon, accurately represents the value proposition, and is technically functional (links resolve, OG metadata correct, sitemap accurate, accessible).

## Scope

The site bundle includes:
- `public/` — HTML pages (index, methodology, implementation, contact, codæ-manifesto copy, etc.), styles.css, images, robots.txt, sitemap.xml, llms.txt
- `comparison-source.html` — build input for abbreviated comparisons (not directly served)

## Source map (build first)

For the site, extract:
- Page list (every `*.html` in `public/`).
- Nav structure (cross-page links).
- For each page: title, meta description, OG tags, primary content sections.
- CSS class inventory (which classes styles.css defines).
- Robots.txt directives.
- Sitemap.xml URL list.
- llms.txt content if present.

## Attack passes

### A. Canon alignment (the BIG one for site)

- Every concept the site names (modes, operations, tiers, artifacts, status categories) matches canon. NO invented concepts; NO renamed concepts; NO dropped concepts that are still in canon and load-bearing.
- Every claim of behavior (e.g., "vibeloom auto-generates X") is true per implementation.
- Every code example matches the actual code / templates / engine behavior.
- The manifesto copy at `site/public/codæ-manifesto.html` is **byte-identical** to `canon/codæ-manifesto.html`.
- Cross-references to canon docs (links to methodology.html, implementation.html on the site) resolve correctly.

### B. Messaging quality

- Page titles and meta descriptions are accurate and distinct per page.
- Value propositions on landing pages match canon's actual capabilities.
- Comparison content (vs other methodologies/tools) is fair: claims about competitors are accurate; claims about vibeloom are supported by canon.
- No stale marketing claims (e.g., "now in beta" when the project is past beta).

### C. Public web integrity

- All inter-page links resolve (no 404s within the site).
- All outbound links resolve (no dead external links, or at least no obvious typos).
- All image / asset references resolve (CSS classes match defined ones; img src files exist).
- sitemap.xml lists every page in `public/` and no extra URLs.
- robots.txt is consistent with intent (allow/deny matches what the user wants indexed).
- llms.txt (AI-discovery file) is up-to-date and accurate.
- HTTPS-only references (no http:// for internal resources).

### D. UX / accessibility

- Every page has a `<title>`, meta description, OG title/description/image, and canonical URL.
- Heading hierarchy is reasonable (one h1, h2s nest under h1, etc.).
- Color contrast meets WCAG AA for body text.
- All images have alt text (or empty alt for decorative).
- Tab order is sensible; no `tabindex` weirdness.
- Mobile-responsive (test at common widths).

### E. Visual consistency

- All pages use the same nav, footer, header pattern.
- Page-level CSS doesn't override layout in unexpected ways.
- Typography is consistent (one body font, one heading font, etc.).
- Spacing/padding rhythm is consistent.

### F. Known failure probes

- Manifesto copy IS byte-identical to canon. (Diff site/public/codæ-manifesto.html vs canon/codæ-manifesto.html; expect zero output.)
- All `class="X"` in HTML — X is defined in styles.css.
- OG image is the current one (from root site/scripts/render-og-image.cjs output).
- The site doesn't claim version numbers stale (e.g., "v0.2 features" when v0.3 is out).
- Comparison page abbreviations are consistent with the long-form comparison-source.html.

## Finding quality bar

Same as eval-passes-canon.md. Per finding: id (`SITE-001`), severity, location, issue, why, fixes, recommended, verification, downstream.

## Priority order

1. Canon contradictions (the site says things canon doesn't support).
2. Broken HTML / dead internal links / missing OG metadata.
3. Outdated marketing claims.
4. Accessibility violations.
5. Visual inconsistencies.
6. Concision / polish.

## Anti-patterns

- Treating site as a 1:1 transcription of canon (it's NOT; marketing register is allowed to abbreviate).
- Flagging "site missing X" when X is a methodology detail too granular for marketing — that's acceptable abbreviation, not drift.
- Generating new visual designs unprompted — preserve existing styling.
- Editing canon based on site eval (canon is authoritative; if site contradicts, fix site).
