# Reference: file-layout-pointer

The canonical repo file layout lives in **`/file-layout.md`** at the repo root. Do not duplicate that content here.

This file exists so other prompts can link to a single authoritative pointer without each prompt having to know the path.

## Key sections of /file-layout.md (in order)

- **§1** Repo root layout (what's at the top: site/, vibeloom-dev/, reports/, v01/, ..., README.md, roadmap.md, file-layout.md, .gitignore)
- **§2** Versioning model (which version is production, how cutover works)
- **§3** `site/` — production deployment (symlink-based; one Cloudflare project)
- **§4** `vibeloom-dev/` — the dev skill (i.e., this skill)
- **§5** `reports/` — flat, gitignored, ephemeral build/review outputs
- **§6** `vNN/` — per-version layout (canon/, site/, skill/, examples/, dist/, intent.md, getting-started.md)
  - §6.1 canon/
  - §6.2 site/
  - §6.3 skill/ (and the fenced-block path convention `template:<path>`)
  - §6.4 skill/engine/ (Python package; `vibeloom_engine/` subfolder is required)
  - §6.5 dist/ per version
  - §6.6 top-level loose docs in vNN/

## When to consult /file-layout.md

- `init`: to know the destination shape when migrating a version.
- `generate skill`: to know where extracted templates go (and to confirm fence-tag path conventions).
- `generate site`: to know what's at `vNN/site/` (public/, comparison-source.html).
- Any time a task needs to know "where does X live" — don't guess; consult.

## Frozen layout for v01-v03

v01/v02/v03 use a LEGACY layout (codæ-manifesto.html at vNN/ root, templates/ subfolder with skill/SKILL.md inside, etc.). They are FROZEN — don't modify them. dev-skill's `init` task handles the migration to the new layout when initializing v04 from v03.

## Update discipline

If dev-skill's understanding of the layout drifts from `/file-layout.md`, fix `/file-layout.md` (or fix the skill). Don't have two sources of truth. dev-skill is allowed to refer to `/file-layout.md` for any "where does X go" question.
