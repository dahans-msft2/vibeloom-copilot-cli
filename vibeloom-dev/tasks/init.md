# Task: init

Initialize a new vibeloom version directory. Layout-aware: reads the source version's actual file structure, reads the destination's intended structure (from `/file-layout.md`), and migrates files into the new locations. Then interactively interviews the user to refactor or seed `intent.md`.

## Purpose

- Bring up a new `vNN/` directory (e.g., v05 from v04) ready for further work.
- Handle both same-layout copies (v04 → v05) and layout migrations (v03 → v04, where v03 uses the legacy layout) with one code path.
- Refactor the user's existing intent into a clean version-specific `intent.md`, or interview from scratch if no intent exists.

## Inputs

- `--from <vNN>` (optional) — source version. Default: the latest existing version directory under repo root.
- `--version <vNN>` (optional) — destination version. Default: source version number + 1 (e.g., from v04 → v05).
- `--from-scratch` (optional, boolean) — skip the copy step; create an empty skeleton; interview from a blank slate.
- The repo root `/file-layout.md` — the canonical destination shape.

## Preconditions

- The repo root contains `/file-layout.md`.
- The destination version directory does NOT already exist (refuse without `--force`; `--force` is intentionally undocumented).
- The source version directory exists (unless `--from-scratch`).
- Working tree may have unrelated dirty files. Capture `git status --short` before starting; do not revert unrelated changes.

## Steps

1. **Resolve versions.**
   - Source: `--from` if provided; else `ls -d v*` and pick highest-numbered.
   - Destination: `--version` if provided; else source + 1 (with appropriate zero-padding: v04 → v05, v09 → v10, v99 → v100).
   - If destination already exists, halt: "v05/ already exists. Use --force to overwrite (will destroy contents) or pick a different version."

2. **Read source layout.**
   - Walk source `vNN/`. Record every file path, its size, and whether it's text or binary.
   - For legacy-layout sources (v01-v03), note which files map to new locations (e.g., `v03/codæ-manifesto.html` → `v04/canon/codæ-manifesto.html`, `v03/templates/` flattened to `v04/skill/`).

3. **Read destination layout from `/file-layout.md`.**
   - Parse §6 (per-version layout) to get the canonical destination shape.
   - Build a path-mapping table: for each source file, where it goes in destination (or "drop" if it has no equivalent — e.g., adversarial-*-report.md files are gone from the new layout; reports/ goes to repo root, not into vNN/).

4. **Show the user the migration plan.**
   - Print: source files count, destination files count, per-file mapping summary, files dropped (with reasons).
   - Ask: "Proceed? (y/n)". On no: exit without writes.

5. **Execute the copy.**
   - For each source file with a destination mapping: copy (or transform — see §6) into destination.
   - For text files in canon/skill/site/examples that reference the source version number in path strings or frontmatter, bump the version reference. Examples: `v03/skill/SKILL.md` references → `v05/skill/SKILL.md` references; "v03" in body text → "v05" where it referred to "this version" (not where it referred to "a prior version's behavior").

6. **Transform the fenced-block path tags inside `vNN/canon/vibeloom-templates.md`** if migrating FROM a legacy layout (v03 or earlier):
   - `template:skill/SKILL.md` → `template:SKILL.md`
   - `template:skill/subagent-prompt.md` → `template:subagent-prompt.md`
   - `template:skill/references/X.md` → `template:references/X.md`
   - `template:tasks/X.md` → unchanged
   - `template:artifacts/X.md` → unchanged
   - (See `/file-layout.md §6.3` for the canonical mapping.)

7. **Seed or refactor `intent.md`.**
   - If source had `intent.md` (i.e., not migrating from legacy v01-v03), it has been copied. Read it.
   - If source had no `intent.md`, create blank.
   - Interview the user (interactive Q&A) to elicit:
     - **Intent** — one-paragraph statement of purpose for this version.
     - **Vision** — 2-5 sentence success state.
     - **Context and motivation** — what changed since the prior version that motivates this version.
     - **Capabilities** — list of CAP-#### items (observable changes this version delivers).
     - **Constraints** — list of CST-#### items (hard requirements).
     - **Out of scope** — what this version explicitly does NOT do.
     - **Open assumptions and risks** — optional.
   - Mirror vibeloom's own intent template shape (see `vNN/skill/artifacts/intent-specs/intent.md` in the source for reference).
   - Write the refactored `intent.md` to `vNN/intent.md` (NOT under canon/ — `intent.md` lives at version root per file-layout.md §6).

8. **Print a summary.**
   - Files created: count.
   - Files dropped: count + list.
   - Intent.md: created or refactored.
   - Suggested next: `vibeloom-dev eval canon --version vNN` to check the migrated canon for drift, OR `vibeloom-dev generate methodology --version vNN` to start refreshing downstream.

## Output

- The new `vNN/` directory tree on disk.
- `vNN/intent.md` populated from the interview.
- A printed summary of the operation.

## Postconditions

- Destination `vNN/` matches the structure defined in `/file-layout.md §6`.
- All version references in the destination point to the new version (not the source).
- No source file is modified (this is a copy, not a move — the source version stays intact, especially important for frozen v01-v03).
- No file is committed (the user reviews `git status` and commits themselves).

## Constraints

- Propose only — never auto-apply destructive changes. The migration plan in step 4 requires explicit user confirmation.
- Never modify source version files. Even for legacy v01-v03 migrations: copy out, don't move.
- Never invent intent. The interview elicits the user's intent; if the user says "skip this section" the section is omitted (don't fill it in from your own model).
- Don't generate downstream artifacts (methodology, implementation, skill, site). `init` only sets up the directory and intent. Downstream artifacts come from `generate <target>`.

## Invariants

- After step 8 succeeds, the destination is in a consistent "draft" state: directory exists, intent.md exists, canon docs are copied from source (possibly with version bumps), but downstream artifacts are still source-derived (not yet regenerated for the new version's intent).
- The source version directory is byte-for-byte unchanged.

## Failure modes

- **Destination exists.** Halt at step 1.
- **Source not found.** Halt at step 1 with the list of existing versions and ask the user which to use.
- **Legacy-layout file with no destination mapping.** Surface as "DROP" in the migration plan with reason; user confirms in step 4.
- **`vibeloom-templates.md` fenced-block transform produces malformed output** (e.g., a tag pattern not covered by step 6). Surface the specific tag, ask the user to clarify, do not proceed.
- **Interview interrupted.** Save partial intent.md as `vNN/intent.md.partial` and tell the user to resume manually or re-run init.
- **User says "abort" mid-interview.** Leave whatever was written; do not roll back.

## Validation gates

- After step 5: `find vNN/ -type f | wc -l` matches the count printed in step 4.
- After step 6: every fenced-block path tag in `vNN/canon/vibeloom-templates.md` is in the canonical form (`template:SKILL.md`, `template:references/...`, `template:tasks/...`, `template:artifacts/...`). No remaining `template:skill/...` tags.
- After step 7: `vNN/intent.md` parses as valid markdown with the expected sections (Intent, Vision, Context and motivation, Capabilities, Constraints).
- `git status --short` after run shows only additions under `vNN/` (no unrelated modifications).
