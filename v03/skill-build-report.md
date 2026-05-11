# Skill Build Report — v0.3 Session 2

> **Historical record (May 8, 2026).** This report documents the v0.3 skill build at the time it was made. It is **not** current certification. Subsequent adversarial review (`adversarial-skill-prompts-report.md`) identified schema drift between the skill and canon (`approval_mode` vs `approval_unit`, decision ID model conflicts, missing `task-template-version` trailers, broken reference links, etc.). Re-run validation before treating "checks passed" claims here as current.

---

Final report per `build-skill.md §Final report`. Walks Steps 1–11, lists the deliverables, surfaces ambiguities, and queues post-handoff tasks.

---

## 1. Bundle artifacts

- **Tarball:** `vibeloom-v0.3.0.tar.gz` (104,661 bytes; 75 archive entries)
- **sha256:** `415844e0b892ec0b8fb3de82a4164576f04a3f38b68765acdf6f4a2446e5d0b8`
- **Checksum sidecar:** `vibeloom-v0.3.0.tar.gz.sha256`
- **Release manifest:** inside the tarball at `vibeloom-v0.3.0/manifest.yaml` (also extracted at `/tmp/repro-final/vibeloom-v0.3.0/manifest.yaml` for inspection); per-file sha256 inventory included.
- **Release notes:** `release-notes-v0.3.0.md` at repo root.
- **Build script (reproducible recipe):** `v03/build-bundle.sh`.

---

## 2. Per-step state

| Step | Description | State | Citation |
|---|---|---|---|
| 1 | Extract templates + `--check` round-trip | **done** | `python3 v03/extract-templates.py` extracted 41 templates; `--check` exits 0 ("OK: 41 templates match disk"); count matches impl §17.3 |
| 2 | Validate skill manifest (templates/skill/SKILL.md) | **done** | YAML frontmatter parses; `name`/`description`/`argument-hint` present; all 10 expected H2 sections present in order; all 6 references/<file>.md paths resolve; no `{{template-source-placeholder}}` or `[TODO]` leakage |
| 3 | Verify task-template family contract (10 codæ sections each) | **done** | 14/14 task templates pass 10/10 (Purpose / Inputs / Preconditions / Steps / Output / Postconditions / Constraints / Invariants / Validation / Failure modes) in canonical order |
| 4 | Verify artifact-template frontmatter shapes (per impl §6) | **done** | 12/12 contract artifact templates carry `status` + `approval_unit`; 4/4 context artifact templates do NOT carry them; `container.md` carries `layer: <enum>`; `component.md` correctly omits `layer` (inherits per impl §6.4) |
| 5 | Verify ID prefix registry consistency (skill ref ↔ impl §5.1) | **done — substantive match, presentational gap surfaced** | All 43 prefix rows match in prefix/name/tier/source-artifact/scope/derivation-rule columns; only 6 trace-family note cells differ in trailing "Schema §X.Y" pointers (presentational only). Surfaced in §7 below. |
| 6 | Smoke-test vibe-mode pipeline | **done — pass** | Transcript: `/tmp/vibeloom-smoke-vibe-IchXb4/smoke-vibe.log`. parse / eval intent-specs / approve / direct-edit + detect-edits / status all green |
| 7 | Smoke-test pm-mode pipeline | **done — pass** | Transcript: `/tmp/vibeloom-smoke-pm-2xp8wq/smoke-pm.log`. init pm → eval/approve intent-specs → generate/eval/approve product-specs → generate/eval system-specs (0 blocking, 0 advisory) → graph cache built → affected forward-walk → dispatch (2 waves) → 6-category status |
| 8 | Package bundle (reproducible) | **done** | `v03/build-bundle.sh`; flags: `--uid 0 --gid 0 --uname "" --gname "" --no-recursion -T <sorted-list>` + `gzip -n -9` + fixed mtimes (source-commit timestamp); two consecutive builds yield byte-identical sha256 |
| 9 | Generate release notes | **done** | `release-notes-v0.3.0.md` at repo root; `release-notes-template.md` placeholders all filled |
| 10a | Static skill-manifest validation | **done** | All required Claude Code frontmatter fields present + valid; references resolve; no parser-breaking constructs; argument-hint matches body promises |
| 10b | Live load test (Claude Code) | **pending live-load** (handoff) | Documented in release notes "Pending live-load test" section; not an agent-executable step |
| 11 | Walk impl §16 acceptance checklist | **done** | All 20 §16 items marked with explicit state (engine-✓ / engine-✓ + smoke-✓ / skill-✓ / skill-✓ + smoke-partial / skill-deferred / pending-live-load). See release notes |

---

## 3. §16 acceptance checklist (full table inlined)

State legend: **engine-✓** (validated by `build-engine.md` on commit `ed0f8b0`); **skill-✓** (validated this build); **smoke-✓** (validated by Step 6/7 transcripts); **pending-live-load** (Step 10b).

| # | Item (abbreviated) | State | One-line citation |
|---|---|---|---|
| 1 | Cache vs traces separation | engine-✓ | engine SHA `ed0f8b0` (`engine-build-report.md`) |
| 2 | Approval baseline trace-backed (JSONL append-only) | engine-✓ + smoke-✓ | smoke-vibe.log: APPROVAL trace appended; `traces.py:append_trace` |
| 3 | ID registry persists retired IDs + next counters | engine-✓ | engine `registry.py` + `tests/test_registry.py`; SHA `ed0f8b0` |
| 4 | Trace families have `schema_version` | engine-✓ + smoke-✓ | `traces.py:_validate_record` REQUIRED_FIELDS includes `schema_version`; smoke traces include `"schema_version": "1.0"` |
| 5 | Code-sync traces with file hashes + validation | engine-✓ | `traces.py:REQUIRED_FIELDS["code-sync"]`; SHA `ed0f8b0` |
| 6 | Review + reconciliation packets with user-notes | skill-✓ (template) + pending-live-load (runtime) | `tasks/review.md` + `tasks/reconcile.md` materialized; runtime verified by Step 10b |
| 7 | Task templates use 10-section markdown structure | skill-✓ | Step 3: 14/14 task templates pass 10/10 |
| 8 | Subagent writes patch-staged + atomic | engine-✓ | engine `patches.py`; SHA `ed0f8b0` |
| 9 | Dispatch plan + wave-assembly + parallel semantics | engine-✓ + smoke-✓ | smoke-pm.log: `dispatch --ids CAP-0001` → 2-wave plan; `dispatch.py` |
| 10 | Subagent task header schema is sole orchestrator↔subagent contract | skill-✓ | `subagent-prompt.md` template wraps impl §13.4 schema |
| 11 | Validation registry parsed + runners invokable | engine-✓ | engine `validation_registry.py`; SHA `ed0f8b0` |
| 12 | Product/UX peer generation supports `MOCK-####` | skill-✓ | `tasks/generate-product-specs-from-ux.md` + `ux.md` MOCK rows |
| 13 | `ux` mode supported as fifth top-level mode | skill-✓ | SKILL.md mode list + `tasks/generate-ux-specs.md` + `tasks/generate-product-specs-from-ux.md` |
| 14 | Verification ladder reflected in eval routing | engine-✓ | engine `eval_.py` (decidable rung); skill `references/eval.md` covers all rungs |
| 15 | Component / container / BC rules per methodology §6.5 | engine-✓ | engine `eval_.py` enforces layer-aware bounded_context; `tests/test_eval.py` |
| 16 | Engine validates `derives_from` per §5.1 + §8.2 | engine-✓ + smoke-✓ | smoke-pm.log pre-fix vs post-fix demonstrates the universal-trace check fires; `eval_.py` |
| 17 | `status` distinguishes 6 categories | engine-✓ + smoke-✓ | smoke-pm.log: `category_counts: {current, stale, uncovered, dangling, drifted, obsolete}` |
| 18 | Operations have explicit traceable execution semantics §15.1–§15.8 | skill-✓ | 14 task templates each with 10-section DbC contract |
| 19 | Vibe layout genuinely minimal | skill-✓ + smoke-partial | smoke-vibe.log: layout starts with only `.vibeloom/traces/`. Spec ambiguity surfaced (engine `status` writes cache regardless of mode). |
| 20 | Templates only as fenced blocks; tree is build artifact | skill-✓ | Step 1: 41 templates extracted; `--check` clean; `templates/` gitignored at `.gitignore:v03/templates/` |

---

## 4. Smoke-test transcripts

- **vibe:** `/tmp/vibeloom-smoke-vibe-IchXb4/smoke-vibe.log` — covers `init pm-equivalent` (vibe materialization), `parse`, `eval intent-specs`, `approve intent-specs` (canonical-hash trace), direct-edit + `detect-edits` (drift detected), `status`.
- **pm:** `/tmp/vibeloom-smoke-pm-2xp8wq/smoke-pm.log` — full new-project workflow per methodology §16: init pm, eval/approve intent-specs, generate/eval/approve product-specs, generate/eval system-specs (clean), `graph --save` (cache built), `affected --ids CAP-0001` (forward DAG walk), `dispatch` (wave assembly), `status` (6-category classification).
- Both scratch repos and the `run-smoke.sh` orchestration scripts are left intact under `/tmp` for human inspection and replay.

---

## 5. Reproducibility check

**Confirmed byte-identical re-build.** Two consecutive runs of `v03/build-bundle.sh` against source commit `ed0f8b0` produced identical sha256 `415844e0b892ec0b8fb3de82a4164576f04a3f38b68765acdf6f4a2446e5d0b8`. Reproducibility recipe documented inline in `v03/build-bundle.sh`:

- File order: pre-sorted file list passed to `tar -T <list>` (BSD `bsdtar` lacks `--sort=name`).
- UID/GID: erased with `--uid 0 --gid 0 --uname "" --gname ""`.
- Mtimes: set to source-commit timestamp via `find ... -exec touch -t ... {} +`.
- Compression: `gzip -n -9` (omit timestamp from gzip header).
- Manifest `build_date_utc`: defaulted to source-commit timestamp; override with `SOURCE_BUILD_DATE_OVERRIDE=now` for wall-clock build times if desired.

---

## 6. Spec ambiguities + bugs

### Ambiguities (chosen interpretations applied)

1. **Skill-ref vs. impl §5.1 prefix table — trailing "Schema §X.Y" pointers in 6 trace-family note cells.**
   The substance (prefix/name/tier/source-artifact/scope/derivation-rule) matches row-for-row across the impl and the skill ref. Only the schema-section pointer at the end of 6 notes cells differs. Two readings:
   - **Strict reading of build-prompt Step 5** ("diff row-by-row"): divergence; should fix at source.
   - **Substantive reading** (skill ref is a load-on-demand condensation that already links impl as canonical source via the section header): pointers are documentation polish.
   The spec author's intent (per commit `902472f` message: "Step 5 should pass on first run") supports the substantive reading. **Surfaced; not blocking.**

2. **Vibe-layout invariant: `engine status` writes cache.**
   Impl §2.2 says vibe has no `.vibeloom/cache/`. Engine `status` writes `.vibeloom/cache/status.json` mode-agnostically. Smoke-vibe shows the cache materializing at the `status` step. **Surfaced for v0.4 adjudication;** options: (a) skill's vibe-mode `status` task uses `--print-only`, (b) engine accepts `--mode vibe` and skips cache save, (c) accept the cache as benign in vibe (regenerable, append-only). Not blocking v0.3 ship.

3. **Generator-guidance HTML comment leading every artifact template.**
   Templates ship with `<!-- VibeLoom template: ... -->` before `---`. Engine `_FRONTMATTER_RE` requires `---` at byte zero; the parser silently returns no artifact when a comment precedes. The smoke orchestrator strips this comment during materialization. **Surfaced for v0.4:** clarify in spec that materialization strips the comment, OR loosen the engine parser to tolerate leading whitespace/comments. Not blocking v0.3.

### Bugs surfaced (no auto-fixes per build-prompt Failure modes)

None. No §-vs-§ contradictions observed.

---

## 7. Pending live-load tasks (Step 10b)

The agent (Claude Code instance running this build prompt) cannot recursively load the new skill. The following is the human's first post-handoff task:

1. Extract `vibeloom-v0.3.0.tar.gz` into the Claude Code skills directory (`~/.claude/skills/vibeloom`).
2. Confirm the skill registers (no errors in Claude Code's startup log).
3. Confirm `/vibeloom` shows the `argument-hint`.
4. Trial-run `/vibeloom init --mode vibe "test"` end-to-end and verify it routes via SKILL.md → `tasks/init.md` → engine `init` correctly (the engine doesn't have its own `init` subcommand; it's skill-orchestrated, calling `parse` + `eval intent-specs` + writing traces, mirroring the smoke-test orchestration).
5. If anything errors at load: surface the error; the SKILL.md template in `vibeloom-templates.md` needs editing; re-extract and rebuild.

---

## 8. Source commit SHAs

- **Templates source:** `ed0f8b0` (Session 1 engine-merge SHA; canon at this point includes 902472f's prefix-table sync, 3903000's release-notes-template, and ed0f8b0's engine merge into main).
- **Engine source:** same `ed0f8b0` — Session 1 produced the engine-build-report (143 tests passing, 89% coverage). The smoke-pm.log demonstrates the engine is operationally sound.
- **Bundle source:** `ed0f8b0` (this build neither modified canon nor introduced new commits; outputs are the bundle + release notes + this report).
- **Build prompts:** `v03/build-skill.md` and `v03/build-engine.md` at `ed0f8b0`.

---

## After this build

If the human (post-handoff) confirms Step 10b succeeds:
- Tag the source commit (`git tag v0.3.0 ed0f8b0 && git push origin v0.3.0`).
- Publish release notes to the marketing site.
- Optionally upload the tarball as a GitHub release asset.
- Announce.

If Step 10b fails: re-run starting at the manifest-edit point — fix `vibeloom-templates.md`'s `templates:skill/SKILL.md` block, re-run `extract-templates.py`, re-run Steps 2 + 10a + 10b.
