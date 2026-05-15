# Task: generate

Generate (or update) a downstream artifact from current upstream. Dispatcher across the four valid targets (`methodology`, `implementation`, `skill`, `site`); the target-specific procedure lives in `references/generate-spec-<target>.md`.

## Purpose

- One entry point for every generate operation.
- Per-target procedure (which upstream to read, what to write, what conventions to enforce) loaded on demand from the matching spec reference.
- Assumes upstream is consistent. Does NOT auto-invoke eval.

## Inputs

- `<target>` (required) — one of: `methodology`, `implementation`, `skill`, `site`.
- `--version <vNN>` (optional, default = latest mutable).

## Preconditions

- `<target>` is one of the valid generate targets above. (`intent` and `manifesto` are hand-authored — refuse with explanation.)
- The relevant spec reference exists: `references/generate-spec-<target>.md`.
- Version `vNN` exists and is mutable (not frozen, not current production).

## Steps

1. **Validate target.**
   - If target is `intent` or `manifesto`: halt. "Those are hand-authored, not generated. See `references/targets.md`."
   - If target is not one of the four valid targets: halt with the valid list.

2. **Load the target-specific spec.** Read `references/generate-spec-<target>.md`.

3. **Execute the spec's procedure end-to-end.** Each spec is self-contained: it lists its specific inputs (which upstream files), preconditions, steps, output, postconditions, constraints, invariants, failure modes, and validation gates. Follow them in order.

4. **Print summary.** Per the spec's summary requirements: what was generated/updated, what changed, what to do next.

## Output

Per the loaded spec. Typically: updated file(s) in `vNN/<canon|site|skill>/...`, plus a printed summary.

## Postconditions

- The target artifact reflects current upstream.
- No upstream artifact is modified.
- No artifact outside the target's scope is modified.
- The user knows what to inspect (`git diff`) and what to do next (typically `reconcile <target>`).

## Constraints (common across all targets)

- **Full rewrite, not incremental.** generate produces the target fresh from current upstream. Hand-edits made directly to the target since the last generate are overwritten — those edits should have been propagated upstream first.
- **No eval invocation.** Trusts the user that upstream is consistent.
- **Authority discipline** per layer (see `references/layering.md`). Each spec restates the relevant authority rules for its target.
- **Write in place.** Git is the safety net. User commits (or stashes) before generate so `reconcile` has a stable baseline.

## Invariants

- After successful generate, the target file(s) parse / lint / extract cleanly per the spec's validation gates.
- Frozen versions are never written to.

## Failure modes

- **Invalid target.** Halt at step 1.
- **Spec reference missing.** Halt at step 2 with the missing path; the skill is incomplete.
- **Upstream files missing.** Halt per the spec's failure modes (each spec lists which upstream it needs).
- **Validation gate fails after writing.** The spec's failure-modes section instructs how to handle (e.g., rollback, surface error, ask user).

## Validation gates

Per the loaded spec. Common gates:
- The generated file(s) parse as valid markdown / HTML / Python / JSON per the target type.
- `git status --short` shows changes only in the target's expected location.

## Related

- `references/generate-spec-methodology.md` — methodology procedure
- `references/generate-spec-implementation.md` — implementation + templates procedure
- `references/generate-spec-skill.md` — skill bundle extraction + optional engine regen
- `references/generate-spec-site.md` — site HTML pages, styling preservation
- `references/layering.md` — the dependency chain that defines what's upstream of what
- `references/targets.md` — what each target is and which commands accept it
