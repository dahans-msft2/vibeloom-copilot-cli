# Spec: generate skill

Target-specific procedure for `vibeloom-dev generate skill`. Loaded on demand by `tasks/generate.md`.

Produce/update `vNN/skill/` from current `vNN/canon/vibeloom-implementation.md` + `vNN/canon/vibeloom-templates.md`. Mostly mechanical (run the template extractor); also regenerates the engine when implementation introduces a structural skill-bundle refactor.

## Purpose

- Materialize the skill bundle from canon.
- Two phases: (a) mechanical extraction of templates into the bundle file layout; (b) engine regeneration if implementation has changed in ways that warrant it.

## Inputs

- `--version <vNN>` (optional, default = latest mutable).
- Upstream: `vNN/canon/vibeloom-implementation.md`, `vNN/canon/vibeloom-templates.md`.

## Preconditions

- implementation.md and templates.md exist and are consistent (user's responsibility).
- `vibeloom-dev/scripts/extract-templates.py` exists and is executable.
- The user has committed or stashed any recent skill/ edits (so `reconcile skill` can show what changed).

## Steps

1. **Validate templates** before extracting. Run:
   ```bash
   python3 vibeloom-dev/scripts/extract-templates.py --check vNN/canon/vibeloom-templates.md
   ```
   This is a parse-only check. Must succeed before proceeding.

2. **Extract templates into `vNN/skill/`.**
   ```bash
   python3 vibeloom-dev/scripts/extract-templates.py vNN/canon/vibeloom-templates.md --dest vNN/skill/
   ```
   This produces:
   - `vNN/skill/SKILL.md`
   - `vNN/skill/subagent-prompt.md`
   - `vNN/skill/references/*.md`
   - `vNN/skill/tasks/*.md`
   - `vNN/skill/artifacts/<tier>/*.md`
   
   The extractor is deterministic: it parses fenced blocks tagged `template:<path>` and writes their bodies to `<dest>/<path>`, creating directories as needed.

3. **Assess engine regeneration need.**
   - Read `vNN/canon/vibeloom-implementation.md` sections that describe engine behavior (typically: Cache vs traces, Contract Graph, Runtime loop, Dispatch plan, Trace schemas, Operation pseudocode).
   - Compare to the current `vNN/skill/engine/vibeloom_engine/` modules.
   - If implementation has STRUCTURAL changes (new operations, new trace families, new schema fields, dispatch logic changes) that the engine doesn't reflect, the engine needs regeneration. Otherwise skip step 4.
   - Surface to the user: "Engine appears <up-to-date | stale>. Reason: <evidence>. Regenerate engine? (y/n)". If user says no, skip step 4. If yes or auto-detected as needed, proceed.

4. **Regenerate engine (only if step 3 deemed it necessary).**
   - For each engine module that needs changes, generate updated code. The engine is deterministic Python (no LLM at runtime); the regeneration is offline. Modules to consider: parser, registry, models (schemas), graph, dispatch, eval, staleness, cache, traces, validation_registry, status, affected, cli.
   - Write updates in place.
   - Keep tests in sync: any new operation needs a test in `vNN/skill/engine/tests/`.
   - Ensure the package still imports: `vibeloom_engine` must be importable from the `engine/` directory.

5. **Sanity checks.**
   - SKILL.md frontmatter parses (valid YAML between `---` markers).
   - Every routing entry in SKILL.md points to an existing `tasks/<file>.md`.
   - Every reference in SKILL.md's "Runtime references" points to an existing `references/<file>.md`.
   - Every artifact template path mentioned in SKILL.md exists in `artifacts/`.
   - If engine was regenerated: `python3 -m vibeloom_engine --help` (from `vNN/skill/engine/`) prints usage without error.

6. **Print summary.**
   - Templates extracted: count, list of new/modified/unchanged files.
   - Engine: untouched OR regenerated (with list of modified modules).
   - Validation gate results (pass/fail per gate).
   - Suggested next: `git diff vNN/skill/` then `vibeloom-dev reconcile skill`.

## Output

- `vNN/skill/**` updated in place (SKILL.md, subagent-prompt.md, references/, tasks/, artifacts/, optionally engine/).
- A printed summary.

## Postconditions

- skill/ matches what templates.md materializes (zero drift between source-of-truth canon and extracted skill).
- If engine was regenerated, it imports cleanly and tests run.
- No canon (implementation.md, templates.md, manifesto, methodology, intent) is modified.
- No site artifact is modified.

## Constraints

- **Extractor is deterministic.** No LLM judgment in step 2. If the extractor produces wrong output, the bug is in the extractor or in templates.md (malformed fence), not in the skill.
- **Engine regen is non-trivial.** Only do it when implementation clearly warrants. When in doubt, ask the user.
- **Engine package name is fixed.** `vibeloom_engine` (the importable module name = the folder name). Never rename.
- **Don't touch tests beyond what's necessary** to keep them passing for new operations.
- **No side effects on the running agent's environment.** Don't `pip install` anything. The engine is `python3 -m vibeloom_engine` only.

## Invariants

- After step 2: `extract-templates.py --check vNN/canon/vibeloom-templates.md` succeeds (no drift between source and extracted files).
- After step 5: SKILL.md is loadable by Claude/Codex skill loaders (frontmatter valid, no broken internal links).
- engine/ folder name = `vibeloom_engine` (the importable package name).

## Failure modes

- **Extractor `--check` fails.** Halt at step 1. The fence convention in templates.md is broken (missing 4-backtick close, wrong tag format, etc.). Surface the specific line and tag.
- **A fence-tag path is malformed** (e.g., uses old-layout `template:skill/SKILL.md` prefix). Halt at step 2 with the specific tag; the user must fix templates.md.
- **Engine regen breaks tests.** Halt. Show which tests failed; ask the user how to proceed. Options: rollback engine changes, accept failing tests temporarily, or iterate on the regen.
- **Engine regen would require restructuring** (e.g., implementation adds a whole new trace family that needs a new module). Surface the scope; ask user to confirm.

## Validation gates

- After step 2: `python3 vibeloom-dev/scripts/extract-templates.py --check vNN/canon/vibeloom-templates.md` exits 0.
- After step 2: `find vNN/skill -type f -name "*.md" | wc -l` matches the count of `template:` fenced blocks in templates.md.
- After step 4 (if engine regenerated): `python3 -m vibeloom_engine --help` succeeds.
- After step 5: SKILL.md's argument-hint frontmatter line parses as a single string.
- Summary's counts match actual file counts.
