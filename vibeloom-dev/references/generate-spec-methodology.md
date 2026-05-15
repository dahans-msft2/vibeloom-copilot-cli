# Spec: generate methodology

Target-specific procedure for `vibeloom-dev generate methodology`. Loaded on demand by `tasks/generate.md`.

Full rewrite of `vNN/canon/vibeloom-methodology.md` from current intent + manifesto. Assumes upstream is consistent (does NOT auto-invoke eval).

## Purpose

- Produce a methodology document that reflects current intent (capabilities, constraints) and current manifesto (paradigm, principles).
- Single canonical output: one file. Written in place. Git is the safety net.

## Inputs

- `--version <vNN>` (optional, default = latest mutable).
- Upstream files: `vNN/intent.md`, `vNN/canon/codæ-manifesto.html`.

## Preconditions

- `vNN/intent.md` and `vNN/canon/codæ-manifesto.html` exist.
- The user has committed (or stashed) any recent edits so `reconcile` has a stable baseline. (The skill doesn't enforce this; it's a discipline note.)
- The user has run `eval canon` recently OR is confident that intent ↔ manifesto are consistent. (Not enforced; vibe-mode.)

## Steps

1. **Load upstream.**
   - Read `vNN/intent.md` in full: Intent prose, Vision, Capabilities (CAP-####), Constraints (CST-####), Out of scope, Open assumptions.
   - Read `vNN/canon/codæ-manifesto.html` in full: paradigm exposition, principles, illustrative claims.

2. **Load current methodology** (if exists) for context. This is the baseline we're rewriting. Read its outline to understand existing structure conventions. We may diverge if intent changed materially.

3. **Plan the methodology shape.**
   - Layered structure (typical): Concepts → Operations → Modes → Status taxonomy → Approval model → Verification ladder → Trace classification → Governance semantics.
   - For each Capability (CAP) in intent: identify which methodology section(s) it manifests in. CAPs should not appear verbatim, but they should each have a methodological expression.
   - For each Constraint (CST) in intent: identify how methodology encodes it (as a rule, an invariant, a gate, etc.).
   - For each principle in manifesto: identify how methodology operationalizes it (or marks it as manifesto-only philosophy).

4. **Author the methodology.** Full rewrite. Write to `vNN/canon/vibeloom-methodology.md`.

   **Default section skeleton** (use this shape unless intent fundamentally changes the structure of vibeloom; deviations should be justified in the summary):

   1. **Overview** — one-paragraph elevator pitch; cite intent's Vision.
   2. **Concepts and entities** — the named things vibeloom traffics in (artifacts, items, IDs, layers, tiers, contracts, traces, decision-records).
   3. **Tiered contract** — the canonical chain (intent-specs → product-specs ⇄ ux-specs → system-specs → context → code), derivation rules, what each tier owns.
   4. **Modes** — vibe, pm, dev, ux, expert. Per-mode user ownership, delegation, contract-stack depth, public surface.
   5. **Operations** — the verbs (init, import, generate, eval, review, reconcile, approve, status). Per-operation purpose, preconditions, postconditions.
   6. **Approval model** — gates per tier per mode; the auto-advance rule.
   7. **Status taxonomy** — current, stale, uncovered, dangling, drifted, obsolete (or whatever set intent calls for).
   8. **Verification ladder** — decidable / mechanical / heuristic; what gets checked at each rung.
   9. **Trace classification** — trace families (approval, generation, eval, code-sync, decision, import) and decision-trace record types (IDR, PDR, UDR, ADR, general).
   10. **Governance semantics** — what users approve vs what's regenerated; layer-aware constraints; vibe-to-full upgrade.
   11. **Glossary** (optional) — terse definitions of the named entities for quick reference.

   For each Capability (CAP) and Constraint (CST) in intent: identify which section(s) it manifests in, and ensure the resulting prose expresses it (without verbatim CAP-#### references in body prose — IDs are intent-internal). For each principle in manifesto: identify which section operationalizes it (or mark it as manifesto-only).

5. **Authority discipline.** Methodology owns WHAT (concepts, operations, modes, status semantics). It should NOT contain runtime implementation details (those belong in implementation), schema tables (implementation), file paths (implementation or file-layout.md), or marketing language (site). If you're tempted to write any of those, stop and reconsider.

6. **Cross-link** sections that depend on each other, using anchor links within the file.

7. **Preserve frozen ID schemes** if they exist. If intent's CAPs are CAP-0001 through CAP-0015, methodology may reference those IDs but does not renumber them.

8. **Print summary.**
   - Word/line counts before/after.
   - Sections added, removed, restructured.
   - Notable intent items (CAPs/CSTs) that drove the changes.
   - Suggested next: `git diff vNN/canon/vibeloom-methodology.md` then `vibeloom-dev reconcile methodology` to interactively walk the changes.

## Output

- Updated `vNN/canon/vibeloom-methodology.md` (full rewrite, in place).
- A printed summary.

## Postconditions

- methodology.md reflects current intent + manifesto.
- methodology.md does NOT contain implementation details, file paths, or schemas (those belong to implementation.md or file-layout.md).
- methodology.md does NOT reference any intent CAP-### or CST-### that doesn't exist in intent.md.
- No downstream artifact (implementation, templates, skill, site) is modified by this task. Those need their own `generate <target>` invocations.

## Constraints

- **Full rewrite, not incremental.** generate produces a fresh methodology from current upstream. It does not try to preserve hand-edits made directly to methodology since the last generate; those edits should have either been (a) propagated upstream into intent/manifesto first, or (b) accepted as drift that this regeneration will overwrite.
- **No eval invocation.** Trust the user that intent ↔ manifesto are consistent. If they aren't, the output will reflect that inconsistency — that's the user's signal to run eval next.
- **Authority discipline** (see step 5). Do not bleed implementation into methodology.
- **Don't touch any other file.** Single output: `vibeloom-methodology.md`.

## Invariants

- methodology.md is the WHAT layer. Every section either defines a concept, names an operation, specifies a mode, or sets a governance rule. No runtime mechanics.
- Manifesto is HTML, methodology is Markdown. Don't transcribe manifesto HTML structure into methodology.

## Failure modes

- **intent.md or manifesto.html missing.** Halt with the missing path.
- **intent.md has no CAPs.** Warn: "intent has no Capabilities section — methodology will be skeletal. Run `init` to refactor intent, or hand-author CAPs first."
- **The current methodology has hand-edits that look load-bearing** (e.g., a section that doesn't trace to any intent CAP). The rewrite will drop them. The user will see this in `git diff` and in `reconcile methodology`. Surface a warning in the summary: "Section X in prior methodology had no upstream basis — dropped. If load-bearing, amend intent first."

## Validation gates

- After step 4: methodology.md is valid markdown.
- After step 4: every CAP-### / CST-### reference in methodology.md exists in intent.md (no dangling references).
- After step 4: no implementation-layer content has leaked in. Check: does any section describe file paths, JSON schemas, Python class names, or trace JSON shapes? If yes, fix in step 5.
- Summary's line counts and section diff match the actual diff.
