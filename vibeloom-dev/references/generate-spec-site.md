# Spec: generate site

Target-specific procedure for `vibeloom-dev generate site`. Loaded on demand by `tasks/generate.md`.

Produce/update `vNN/site/public/**` HTML files from current methodology + implementation (and manifesto for marketing-y framing). Site is marketing register — full HTML, may be abbreviated relative to canon, must not contradict canon.

## Purpose

- Generate the public marketing site for this vibeloom version.
- Site reflects the canon's substance in promotional / accessible form. It is NOT a 1:1 transcription of canon.
- Inputs are full canon (intent + manifesto + methodology + implementation+templates); the site is downstream of all of them.

## Inputs

- `--version <vNN>` (optional, default = latest mutable).
- Upstream: `vNN/canon/codæ-manifesto.html`, `vNN/canon/vibeloom-methodology.md`, `vNN/canon/vibeloom-implementation.md` (templates only consulted, not transcribed).
- Optional source helper: `vNN/site/comparison-source.html` (long-form comparison; used to generate abbreviated comparison snippets across pages).
- The existing `vNN/site/public/**` (provides styling, layout patterns, navigation conventions to preserve).

## Preconditions

- canon docs exist.
- `vNN/site/public/` exists (may be empty for a brand-new version; usually contains prior pages and styles.css).
- The user has committed or stashed any recent site edits.

## Steps

1. **Load upstream.**
   - Read intent.md, manifesto (full HTML), methodology.md, implementation.md (outline + key sections).
   - Read existing `vNN/site/public/` page list. Identify: index.html, methodology.html, implementation.html, contact.html, the manifesto copy at codæ-manifesto.html, styles.css, sitemap.xml, robots.txt, llms.txt, plus any other pages.
   - Read `comparison-source.html` if present.

2. **Plan page set.**
   - For a vibeloom site, the typical page set is: `/` (overview), `/methodology`, `/implementation`, `/codæ-manifesto`, `/contact`, plus `robots.txt`, `sitemap.xml`, `llms.txt`. Adjust based on what exists.
   - For each page, decide its purpose, audience, length, and what it transcribes vs summarizes vs links out.
   - Plan navigation: every page links to every other page (small site).

3. **Preserve styling.**
   - Read `vNN/site/public/styles.css` — this defines the visual language. Do NOT regenerate styles.css unless the user explicitly asks. Pages must use existing classes/elements.
   - Read one existing page (e.g., index.html) to understand layout patterns: header, nav, main content structure, footer, OG meta tags. New pages should match these patterns.

4. **Generate / update each page.**
   - For each page in the plan:
     - Determine content: derived from which canon source, what level of detail (full / abbreviated / linked).
     - Author the HTML. Use existing layout patterns + existing CSS classes. Inline only what's unique to the page.
     - Keep title, meta description, OG tags consistent with the page's purpose.
     - If the page is the manifesto, copy `vNN/canon/codæ-manifesto.html` literally to `vNN/site/public/codæ-manifesto.html` (manifesto is hand-authored design-heavy HTML; site just serves it).
   - Write each updated page in place.

5. **Update `sitemap.xml`** and `robots.txt` to reflect the current page set. Update `llms.txt` (if present — the AI-discovery file) with a current summary.

6. **Validation.**
   - All inter-page links resolve (no 404s within the site).
   - All canon references in pages are accurate (e.g., a methodology page that lists modes lists the EXACT modes from methodology.md, no extras, no omissions).
   - Frontend-only sanity: open `vNN/site/public/index.html` locally and confirm it loads (no missing CSS/img references).

7. **Print summary.**
   - Pages added/modified/unchanged.
   - Notable canon items reflected (or notable items omitted by design as too detailed for marketing).
   - Suggested next: `npx http-server vNN/site/public -p 8124` to preview locally, then `vibeloom-dev reconcile site` to walk changes interactively, then `vibeloom-dev eval site` after to check canon alignment.

## Output

- Updated `vNN/site/public/**` HTML files.
- Updated `sitemap.xml`, possibly `robots.txt`, `llms.txt`.
- A printed summary.

## Postconditions

- Every page in the plan exists in `vNN/site/public/` and serves correctly.
- Every page is consistent with canon (does not contradict).
- styles.css is unchanged (unless the user explicitly requested style updates).
- canon files are unchanged.
- The manifesto file at `vNN/site/public/codæ-manifesto.html` is byte-identical to `vNN/canon/codæ-manifesto.html`.

## Constraints

- **Marketing register.** Pages may simplify, abbreviate, use friendlier language. They MUST NOT contradict canon. If methodology says "modes are vibe/pm/dev/ux/expert", the site can't say "modes are casual/professional".
- **No new visual design.** Reuse existing styles.css and existing layout patterns. If a new style is genuinely needed, surface to the user and ask before generating.
- **Manifesto is byte-copied.** Don't regenerate manifesto HTML; copy from canon.
- **No JavaScript dependencies.** The site is static HTML + CSS. No build step beyond authoring + serving.
- **No external assets.** All images, fonts, etc. live in `vNN/site/public/` (or are loaded from canonical CDNs already in use, like Google Fonts if the site uses them).
- **OG image source lives at root site/, not in vNN/site/.** Don't generate or modify the OG image generator; only consume what root site/ provides.

## Invariants

- Every page renders in a modern browser without JavaScript errors.
- Every internal link resolves to an actual file under `vNN/site/public/`.
- No page references a CSS class that styles.css doesn't define.

## Failure modes

- **Existing styles.css doesn't cover a needed component** (e.g., a new "feature card" layout for a new section). Surface to the user: "Need new CSS for X. Add to styles.css now or use existing pattern Y as fallback?". Don't silently add new CSS.
- **A canon concept is too detailed to surface on site.** Decide: omit (note in summary), abbreviate, or link to canon. Default: abbreviate with a "see methodology for details" link.
- **The site has accumulated cruft** (pages that no longer correspond to any canon section). Surface to user: "Page X has no canon basis — keep, archive, or delete?". Don't unilaterally delete.

## Validation gates

- After step 4: every page is valid HTML5 (lints clean).
- After step 5: sitemap.xml lists every page in `vNN/site/public/` and no extra URLs.
- After step 6: `grep -E "href=\"[^\"#]" vNN/site/public/*.html` — every href resolves to an existing file (or is an absolute external URL).
- After step 6: `grep -E "class=\"[^\"]+\"" vNN/site/public/*.html | extract class names | check against styles.css selectors` — every class is defined.
- The manifesto file in site/public/ matches canon/codæ-manifesto.html exactly (use `diff` to check).
