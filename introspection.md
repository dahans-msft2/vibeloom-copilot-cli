Analyze this entire VibeLoom repository as a full consistency/coherency/minimality audit, then help fix it step-by-step with explicit approval gates.

Critical process rule:
- Even “safe automatic” fixes are approval-gated.
- The grouping below is only to reduce my cognitive load and help me review the work in sensible buckets.
- Do not modify files until I approve a specific step.

## Overall Goal

Audit the repository for:
- redundancy/duplication
- coherency/correctness
- verbosity/size/deadweight
- context window size/load (during execution)

Then produce a grouped remediation plan and execute it one approved step at a time.

## Architectural Constraints

Use these as hard audit constraints:
- `intent.md` is intentionally loose prose and is exempt from mandatory stable item IDs, though optional structured capability IDs may appear
- `docs/` are canonical prose methodology / help material, not routine runtime authority
- only `references/` is routine runtime authority for the skill
- `templates/` are generation inputs only
- `site/` is public documentation / marketing, not runtime authority, but it must not contradict the canon
- `SKILL.md` is the runtime entrypoint and orchestrator, but detailed runtime rules should not be duplicated there if they already exist in `references/`
- the canonical abstract command model is `<action> <target> <context>` wherever the general syntax is described
- docs in `docs/` can reference each other but not docs in other folders
- docs in `references/` can reference each other as well as docs in `templates/` but not docs in other folders
- docs in `templates/` can reference each other but not docs in other folders
- `references/` run-time instructions and `templates/` spec templates are generated based on `docs/` prose, so duplication across them should be reported but not marked for fixing because in most cases it’s intentional.
- however, between the documents in the same folder there should be no duplication
- `site/` will repeat/restate/summarize information from many other source, so don;t consider it a duplication. It just should not contradict the canon.

## What To Inspect

Inspect the actual workspace thoroughly:
- `SKILL.md`
- all files in `references/`
- root canonical artifacts: `constitution.md`, `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md`
- all files in `templates/`
- relevant files in `docs/`
- relevant files in `site/`
- metadata such as `agents/openai.yaml`
- package / authority docs such as `README.md`

Use direct repo inspection. Do not rely on memory or assumptions.

## Audit Goals

1. Redundancy / duplication
- identify rules, concepts, command definitions, authority statements, runtime instructions, or methodological constraints repeated across files in ways that increase maintenance cost, drift risk, or runtime/context-window overhead

2. Coherency / correctness
- identify contradictions, stale wording, outdated paths, inconsistent syntax, mismatched templates, broken authority boundaries, or artifacts that no longer agree with the canon

3. Verbosity / size
- identify wording, sections, structures, or entire files that could be shortened, consolidated, moved, or removed without losing necessary meaning

4. Context window size/load (during execution)
- identify oppporunities to reduce the size/load of the context window in run-time


## Review Standard

- if runtime guidance exists outside `references/`, call it out unless it is clearly help-only or an explicit escalation path
- if `site/` says something broader, simpler, or different than the canon, classify it explicitly as either acceptable simplification or an actual contradiction
- if two files define the same normative rule, assume that is a problem unless the layering clearly justifies it
- if a rule is runtime-operational, prefer it to exist in exactly one authoritative place inside `references/`, with higher-level files only pointing to it
- if a general syntax definition appears anywhere and does not use `<action> <target> <context>`, call it out
- if a file exists but serves no current runtime, canonical-doc, template, or honest public-site purpose, call it out as possible deadweight
- if wording cites brittle exact counts where no count is operationally necessary, call it out as maintainability deadweight

## Required Output: Phase 1 Audit Only

Do not edit files in Phase 1.

Produce:
1. Findings first, ordered by severity
2. Every finding must include:
- severity
- why it matters
- exact file references
3. Then provide:
- `Redundancy / Deadweight`
- `Already Coherent / Leave Alone`
- `Open Questions / Judgment Calls`

## Required Output: Phase 2 Grouped Fix Plan

After the audit, propose a remediation plan grouped into these buckets:

### Group A: Safe Mechanical Cleanup
Use only for low-judgment fixes where the canon is already settled.
Examples:
- stale path fixes
- stale command examples after a command surface is already settled
- duplicate wording removal where authority is already clear
- moving/deleting clearly unreferenced deadweight
- replacing outdated references with already-canonical terminology

### Group B: Local Consistency Fixes
Use for contained semantic fixes that affect a limited number of files but do not change core architecture.
Examples:
- aligning command tables and examples
- syncing templates with canon
- fixing local contradictions between two or a few artifacts
- resolving wording mismatches where the intended rule is already clear

### Group C: Canon / Runtime / Architecture Fixes
Use for anything that affects authority boundaries or the operating model.
Examples:
- changing what is runtime-authoritative
- changing command surface semantics
- changing lifecycle rules
- changing projection rules
- changing layering between `SKILL.md`, `references/`, `docs/`, `templates/`, and `site/`

### Group D: Public Site / Marketing Alignment
Use for public-site changes that align marketing material to the canon.
Examples:
- correcting public claims
- updating comparison language
- fixing public command tables
- removing misleading simplifications

If a fix could fit multiple buckets, choose the stricter bucket.

## Step Planning Rules

- break the remediation into small, reviewable steps
- each step must belong to one group
- each step must list:
  - short step name
  - why it belongs in that group
  - files it would touch
  - whether it fully resolves one finding or only part of one
- do not batch unrelated fixes together
- if two fixes are tightly coupled and safer together, say why
- after presenting the grouped plan, stop and wait for my approval of the first step

## Approval-Gated Execution Rules

After I approve a step:
- make only that step’s changes
- preserve unrelated existing changes
- do not silently widen scope
- if you discover the approved step requires a broader change than expected, stop and explain before proceeding

After applying an approved step, report:
- what changed
- files touched
- verification performed
- whether the targeted finding is now fully resolved or partially resolved
- what related issues remain
- the next proposed step, with its group label

Then stop and wait for approval again.

## Additional Guardrails

- do not drift into generic advice; keep everything tied to the actual repository
- do not treat acceptable layering repetition as a bug unless it clearly increases drift risk
- do not “fix” marketing tone just because it is marketing; only fix it if it becomes misleading relative to the canon
- do not remove files unless they are clearly deadweight or replaced by a more authoritative source
- do not make any file changes until after the audit and my explicit approval of a specific step