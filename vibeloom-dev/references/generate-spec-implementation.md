# Spec: generate implementation

Target-specific procedure for `vibeloom-dev generate implementation`. Loaded on demand by `tasks/generate.md`.

Full rewrite of `vNN/canon/vibeloom-implementation.md` AND `vNN/canon/vibeloom-templates.md` from current methodology. Treats implementation + templates as one unit. Assumes upstream (methodology) is consistent.

## Purpose

- Produce the runtime/implementation specs and the materialization templates from methodology.
- Two files; one logical layer. Both rewritten together because they're tightly coupled: templates materialize what implementation specifies.

## Inputs

- `--version <vNN>` (optional, default = latest mutable).
- Upstream: `vNN/canon/vibeloom-methodology.md`.

## Preconditions

- methodology.md exists and is consistent with intent + manifesto (user's responsibility; not enforced).
- The user has committed or stashed any recent edits.

## Steps

1. **Load methodology.** Read in full. Build a mental model of: concepts, operations, modes, status taxonomy, approval gates, verification ladder, trace classification.

2. **Load current implementation + templates** for baseline context. Read outlines to understand existing structure conventions.

3. **Plan implementation.** Implementation owns HOW (runtime model, schemas, IDs, dispatch, validation, layer-aware constraints, frontmatter shapes, trace I/O schemas, operation pseudocode). Map every methodology concept/operation/mode to its runtime expression. Plan section structure.

4. **Author implementation.md.** Full rewrite. Sections typically include: Repo layout, Frontmatter shape, ID schema, Cache vs traces, Contract Graph, Runtime loop, Dispatch plan + wave assembly, Subagent task header, Trace schemas (per family), Layer-aware constraints, Operation pseudocode (per operation), Late-fetch policy, Validation gates.

5. **Plan templates.** Templates materialize implementation. They include:
   - SKILL.md (the skill manifest)
   - subagent-prompt.md (the subagent body template)
   - references/ (load-on-demand docs: operations, modes, runtime, artifacts, eval, troubleshooting)
   - tasks/ (one per operation: init, import, generate-*, eval, review, reconcile, approve, status)
   - artifacts/ (one per artifact type, organized by spec layer: intent-specs, product-specs, ux-specs, system-specs, context, plus decision-trace.md, validation-registry.md)

6. **Author templates.md.** Full rewrite. Each template is a fenced block tagged with its destination path. **Fence convention: four backticks** (so inner three-backtick code blocks don't close the outer fence prematurely). Destination paths are relative to `vNN/skill/` per file-layout.md §6.3:
   - `template:SKILL.md` (not `template:skill/SKILL.md`)
   - `template:subagent-prompt.md`
   - `template:references/X.md`
   - `template:tasks/X.md`
   - `template:artifacts/X/Y.md`

7. **Cross-validate** implementation ↔ templates:
   - Every operation named in implementation has a `tasks/<operation>.md` template.
   - Every artifact type in implementation has an `artifacts/<tier>/<type>.md` template.
   - Every reference doc in implementation has a `references/<name>.md` template.
   - Template paths use the canonical mapping (per step 6).

8. **Print summary.**
   - implementation.md: word/line count changes, sections added/removed/restructured, schemas added/modified.
   - templates.md: count of template blocks, list of added/removed/modified templates by destination path.
   - Suggested next: `git diff vNN/canon/vibeloom-implementation.md vNN/canon/vibeloom-templates.md` then `vibeloom-dev reconcile implementation`.

## Output

- Updated `vNN/canon/vibeloom-implementation.md` (full rewrite, in place).
- Updated `vNN/canon/vibeloom-templates.md` (full rewrite, in place).
- A printed summary.

## Postconditions

- implementation.md reflects current methodology.
- templates.md materializes what implementation specifies (every operation/artifact has a template; every template traces to an implementation concept).
- Fence-tag paths in templates.md are in the canonical (new-layout) form.
- No upstream artifact (methodology, manifesto, intent) is modified.
- No skill bundle artifact (`vNN/skill/**`) is modified by this task. Use `generate skill` next to materialize templates into the skill bundle.

## Constraints

- **Full rewrite of both files.** Don't try to incrementally update templates.md to match a slightly-changed implementation.md; just rewrite both.
- **Authority discipline.** implementation owns HOW. It must not contain methodology rationale or marketing language. Templates must not redefine concepts (those belong to methodology).
- **Fence integrity.** Every template fenced block opens with exactly four backticks immediately followed by `template:<path>` and closes with a line of exactly four backticks. The extractor (`vibeloom-dev/scripts/extract-templates.py`) depends on this exactly.
- **Path canonicalization.** All fence-tag paths use new-layout conventions (no `template:skill/...` prefix).
- **No invented schemas.** Schemas in implementation must derive from methodology's concepts; don't introduce entity types, ID prefixes, or trace families that methodology hasn't named.

## Invariants

- After this task: `python3 vibeloom-dev/scripts/extract-templates.py --source vNN/canon/vibeloom-templates.md --dest /tmp/probe-extract/` succeeds end-to-end (extractor parses every fence cleanly and materializes them, with no malformed blocks). Note: a successful run + a subsequent `--check` against the same `--dest` would also succeed and prove zero drift.
- Template inventory matches implementation's operation/artifact lists.

## Failure modes

- **methodology.md missing.** Halt.
- **methodology has concepts without operational expression.** Methodology defines but doesn't operationalize. Warn and proceed; implementation will list those concepts as "TBD" sections rather than invent specifics.
- **Template fence-tag uses old prefix.** Should be impossible after step 6 if the author followed canonical paths. Validation gate in step 8 will catch.
- **Existing implementation has hand-edits that don't trace to methodology.** Drops them; surfaces in summary as "Sections X, Y had no upstream basis — dropped. If load-bearing, amend methodology first."
- **Existing templates have customizations** (manually-tuned task prompts that deviate from what implementation would naturally produce). Drops them; user sees in `git diff` and `reconcile`.

## Validation gates

- After step 4: implementation.md is valid markdown.
- After step 6: templates.md is valid markdown.
- After step 6: run `python3 vibeloom-dev/scripts/extract-templates.py --source vNN/canon/vibeloom-templates.md --dest /tmp/probe-extract/` end-to-end — must succeed (this exercises the extractor as a parse validator; success means every fenced block is well-formed and writeable).
- Every template destination path in templates.md is one of: `SKILL.md`, `subagent-prompt.md`, `references/<name>.md`, `tasks/<name>.md`, `artifacts/<tier>/<name>.md`.
- Every operation listed in implementation's "operations" section has a corresponding `template:tasks/<op>.md` fence in templates.md.
- Every artifact tier in implementation has at least one `template:artifacts/<tier>/...` fence in templates.md.
