# Build the v0.3 vibeloom skill bundle

A prompt for Claude Code (or any equivalent agentic coding tool). The agent extracts templates, validates the skill manifest, smoke-tests against fresh repos in two modes, and packages the deployable bundle.

This prompt names **what** must happen, not how. Bundle layout, manifest format choices, packaging strategy, smoke-test orchestration — those are the agent's call. The agent should consult `vibeloom-implementation.md`, `vibeloom-methodology.md`, and the templates source as the authoritative inputs.

This prompt assumes [`build-engine.md`](build-engine.md) has already been run and the engine passes its acceptance checklist. If not, run that first.

This prompt is itself codæ-shaped — Inputs, Preconditions, Steps, Output, Postconditions, Constraints, Invariants, Validation, Failure modes — for the same reason as the engine build: the construction of vibeloom should follow vibeloom's own discipline.

---

## Purpose

Assemble the v0.3 vibeloom skill bundle from canonical sources: the engine (built by `build-engine.md`), the templates (extracted from `vibeloom-templates.md`), and the skill manifest. Verify the bundle works end-to-end in `vibe` and `pm` modes on smoke-test repos. Produce a deployable skill package that Claude Code or Codex can load.

## Inputs

- **`v03/engine/`** — built by `build-engine.md`, all engine tests passing, §18 engine-related acceptance items checked off.
- **`v03/vibeloom-templates.md`** — canonical source for all 41 templates (skill manifest, subagent prompt, skill references, task templates, artifact templates, decision-trace template, validation-registry template, README).
- **`v03/extract-templates.py`** — the deterministic extractor with `--check` drift mode.
- **`v03/vibeloom-implementation.md`** — for §18 acceptance checklist and §19 templates inventory + per-family contracts.
- **`v03/vibeloom-methodology.md`** — for smoke-test workflow expectations (§16).

## Preconditions

- `v03/engine/` exists; engine tests pass; engine-related items in impl §18 are checked off.
- All input files present.
- Python 3.10+ and `git` available.
- A working Claude Code installation (or equivalent) is available locally for the load test.
- No partial `templates/` from a prior failed run; if one exists, regenerate from source first.

## Steps

1. **Extract templates and verify round-trip.** Use `extract-templates.py` in default mode then `--check` mode. Drift must be zero. If extraction reports fewer than 41 templates, the source is corrupt — stop and fix at the source.

2. **Validate the skill manifest** at `templates/skill/SKILL.md`. Confirm:
   - Frontmatter is well-formed YAML and complete per the SKILL.md template's contract (per impl §19.3 and `vibeloom-templates.md`).
   - Body sections are present and ordered as the template requires (when-to-use, authoritative sources, runtime references, templates, engine, substrate, command routing, failure recovery, getting started, guardrails, response shape).
   - Every `references/<file>.md` mentioned is present in `templates/skill/references/`.

   If anything is missing, fix at the source (`vibeloom-templates.md`), re-extract, retry. **Never hand-edit the extracted `templates/` tree.**

3. **Verify task-template family contract.** Every template under `templates/tasks/` must have the canonical 10 sections in order: Purpose / Inputs / Preconditions / Steps / Output / Postconditions / Constraints / Invariants / Validation / Failure modes (per impl §12.1 and §19.3). A template with any other shape is a contract violation — fix at the source.

4. **Verify artifact-template frontmatter shapes.** For every contract artifact template (intent-specs, product-specs, ux-specs, system-specs), the frontmatter must carry the v0.3 fields including `approval_unit`. For the system-specs templates, the layer-aware fields per impl §6.3 / §6.4. Context artifact templates must not carry `status` or `approval_unit`. Per impl §6 and §19.3.

5. **Verify ID prefix registry consistency.** The prefix registry in `templates/skill/references/artifacts.md` must match `vibeloom-implementation.md` §5.1. If they disagree, the implementation doc wins; the skill reference is a bug.

6. **Smoke-test in `vibe` mode end-to-end.** Drive the skill (or simulate the skill's behavior using the engine + templates + the corresponding task templates) through a complete vibe-mode session on a fresh scratch repo under `/tmp`. At minimum, the scenario covers:

   - `init --mode vibe`: layout per impl §2.2 is materialized; intent / defaults / system / per-assistant configs at root; `.vibeloom/traces/` initialized; **no** `.vibeloom/cache/` (vibe is genuinely minimal — methodology §5.1).
   - `eval intent-specs`: clean state, no blocking findings.
   - `approve intent-specs`: an approval trace appears; lifecycle flips to approved.
   - Direct edit on an approved artifact: `detect-edits` flags it; `status` reflects the drift.

   The smoke test passes when every command emits well-formed JSON, exit codes match the documented semantics, and the documented post-conditions hold.

7. **Smoke-test in `pm` mode end-to-end** on a separate scratch repo. Drive the fuller flow per methodology §16 (new-project workflow): `init --mode pm` → review and approve `intent-specs` → generate `product-specs` (with auto-eval) → review/approve product-specs → generate `system-specs` → run `affected` after a hypothetical CAP-level change → run `dispatch` and confirm a well-formed plan → run `status`. Verify:

   - The full layout per impl §2.1 is materialized, including `.vibeloom/cache/`.
   - The graph cache is built; affected-set walks return correct downstream items.
   - Wave assembly per impl §13.2 produces plans with correct ownership and dependency topology.
   - Status classifies items into the six categories per impl §10.

   Failures at any step trace back to engine, template, or spec. Fix at the source; do not hand-patch the smoke-test repo to mask bugs.

8. **Package the bundle.** The skill bundle is a self-contained, reproducible directory containing the skill manifest, subagent prompt, references, task templates, artifact templates, and the engine. Generate a release manifest recording:

   - name, version, build date (UTC ISO-8601), source commit SHA
   - file inventory with sha256 hashes for every file in the bundle
   - engine runtime requirements (Python 3.10+, zero deps)
   - templates count and source
   - smoke-test results (vibe + pm)

   Produce a release tarball and a checksum file alongside it. Hashes are computed after the bundle is assembled, before the tarball is created.

9. **Generate release notes** capturing what's in the release, smoke-test results, the §18 acceptance checklist (with each box's state), the source commit SHA, and the bundle artifacts (tarball name + sha256).

10. **Load test in Claude Code.** Install the bundle into a clean Claude Code instance and confirm:
    - The skill registers (visible under `/skills`).
    - `/<vibeloom-command-prefix> init --mode vibe` (the skill's argument-hint surface) is recognized.
    - Loading the skill produces no warnings or schema errors.

    If the manifest fails to load, the SKILL.md frontmatter is malformed for Claude Code's expected schema. Fix at the source, re-extract, repackage, retry.

11. **Walk impl §18 acceptance checklist line by line.** Every box must check. Where a box covers an engine concern, defer to the engine's pre-validated state; templates concerns verify against the extracted tree; smoke-test concerns verify against the runs in §6 and §7. Document any unchecked items in the release notes as known limitations and explain why.

## Output

- A self-contained skill-bundle directory.
- A release tarball plus its sha256 checksum.
- Release notes summarizing what's in the bundle, smoke-test results, and the source commit SHA.
- The smoke-test repos under `/tmp` left intact for human inspection.

## Postconditions

- `extract-templates.py --check` exits 0 (round-trip clean).
- All 14 task templates pass the 10-section DbC contract.
- All contract artifact templates carry the v0.3 frontmatter shape.
- The ID prefix registry in `templates/skill/references/artifacts.md` matches impl §5.1.
- Smoke tests pass for both `vibe` and `pm` modes end-to-end.
- The bundle loads cleanly in Claude Code.
- Impl §18 acceptance checklist is fully satisfied (or unchecked items are documented in release notes).
- The bundle is reproducible: same source commit + same templates source + same engine source → byte-identical bundle (modulo timestamps in the manifest).

## Constraints

- Do not modify any canonical source (`vibeloom-templates.md`, `vibeloom-methodology.md`, `vibeloom-implementation.md`, `codæ-manifesto.html`) during this build. Outputs are the bundle and release notes only.
- Do not hand-edit anything under `templates/`. If something must change, change `vibeloom-templates.md` and re-extract.
- Do not introduce runtime dependencies the engine doesn't already have. Bundle stays Python-3.10+-only, zero `pip install` required at runtime.
- Do not skip a smoke-test step. If a step is broken, fix it at the source; do not document around it.

## Invariants

- The skill manifest is what Claude Code / Codex parses to register the skill. It must validate against the platform's expected schema; if the platform's schema drifts, the SKILL.md template in `vibeloom-templates.md` needs updating, not the bundle.
- The bundle is reproducible (same inputs → byte-identical output, modulo manifest timestamps).
- The bundle is self-contained: no file outside the bundle directory is required at runtime.
- Smoke-test repos live under `/tmp`, never inside the vibeloom repo or any project the user cares about.

## Validation

Before declaring the bundle ready to ship:

1. Round-trip clean (`extract-templates.py --check` exits 0).
2. Family contracts pass (10-section task templates; v0.3 contract-artifact frontmatter shape; non-numbered context-artifact frontmatter).
3. Smoke tests pass end-to-end in both `vibe` and `pm` modes.
4. Impl §18 acceptance checklist fully satisfied (paste it into release notes with each box's state).
5. Bundle integrity: manifest hashes match actual file contents; tarball extracts to a directory whose contents match the manifest.
6. Load test in Claude Code: skill registers and accepts its expected commands.
7. Reproducibility spot-check: rerun the entire build prompt on the same source commit; result should be byte-identical (modulo manifest timestamps).

## Failure modes

- **Drift reported by the extractor.** The source was edited but not re-extracted, or the extracted tree was hand-edited. Re-extract from source; never hand-edit the tree.
- **Skill manifest fails to load in Claude Code.** Either the SKILL.md template is malformed or the platform's schema changed. Identify which; fix the source.
- **Smoke test fails at a specific operation.** Trace to engine bug, template bug, or spec ambiguity. Fix at the source. Re-run from the failing step.
- **Acceptance checklist fails on a specific item.** Surface to the human. Some §18 items reflect design choices, not bugs; do not auto-fix.
- **Bundle integrity check fails.** Hash mismatch — regenerate the manifest after the bundle is final and before the tarball; fix the script ordering if needed.
- **Spec ambiguity.** Prefer the conservative interpretation, comment the choice, surface in your final summary.

## Anti-patterns to avoid

- Hand-editing the extracted `templates/` tree.
- Patching the smoke-test repo to mask a bug instead of fixing the source.
- Skipping the load test "because the file looks right" — Claude Code's parser is the only judge.
- Generating the manifest before the bundle is final.
- Bundling tests, scratch fixtures, or `__pycache__/`.
- `git push`-ing a release tag from inside the build prompt; tagging is a human decision after inspection.

## After this build

If everything passes:
- Tag the source commit, push the tag.
- Publish release notes to the marketing site.
- Optionally upload the tarball as a GitHub release asset.
- Announce.

If anything failed and you couldn't fix it cleanly: stop, surface the failure in your final summary, do not ship a release that didn't pass its own smoke tests.
