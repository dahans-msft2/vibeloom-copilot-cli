# VibeLoom Introspection Prompt

Use this prompt for periodic full-repository audits of VibeLoom. The purpose is to inspect the current workspace for consistency, coherency, minimality, and runtime context efficiency, then produce a grouped remediation plan and, if later requested, execute fixes one approved step at a time.

This file is an audit prompt, not methodology canon. When this prompt summarizes repository rules for checker convenience, the canonical source of truth remains:
- `docs/vibeloom-methodology.md` for methodology and dependency contract
- `SKILL.md` for runtime orchestration and help-topic routing

## Operating Mode

- Inspect the actual current workspace on every run. Do not rely on memory, stale summaries, or assumptions from earlier audits.
- Ground yourself in canonical inputs first before judging lower layers.
- Use direct repo inspection.
- During the audit phase, do not edit files.
- If the operator later asks for remediation, keep every fix approval-gated and bounded to one approved step at a time.

## Canon And Dependency Contract

Treat these as authoritative audit inputs:
- `docs/vibeloom-methodology.md` owns the methodology prose and dependency contract
- `SKILL.md` owns runtime bootstrap, cross-layer orchestration, and exact `help` topic routing
- `references/` owns routine runtime authority
- `templates/` owns generation inputs
- the sibling `../site/` workspace is derivative public documentation and marketing

Audit-facing summary of folder roles:
- `docs/` = canonical prose methodology and help material
- `references/` = distilled runtime execution layer
- `templates/` = artifact-generation input layer
- `SKILL.md` = runtime entrypoint and cross-layer orchestrator
- sibling public site workspace = derivative public-facing layer

Allowed dependency edges:
- `docs/ -> docs/`
- `references/ -> references/`
- `references/ -> templates/`
- `templates/ -> templates/`
- `SKILL.md -> docs/`
- `SKILL.md -> references/`
- `SKILL.md -> templates/`

Disallowed dependency edges:
- `docs/ -> references/`
- `docs/ -> templates/`
- `references/ -> docs/`
- `templates/ -> docs/`
- `templates/ -> references/`

Help routing rule:
- `help` is the only command family allowed to load explanatory material outside `references/`
- `references/` may escalate only by help topic name such as `help methodology` or `help evals`
- exact `help` topic routing belongs to `SKILL.md`
- `references/` must not contain direct `docs/*` paths, even for help
- `commands` help may route to `references/`
- `templates` help may route to `templates/`

Layering rules:
- `docs/` may mention templates only by semantic name such as `intent template` or `technical spec template`
- `references/` may duplicate methodology information from `docs/`, but only in a distilled and structured runtime form
- `references/` may refer directly to `templates/` because template loading is part of runtime execution
- `templates/` must not define independent methodology truth
- `SKILL.md` may know the full repository disposition, but it should stay pointer-oriented and should not duplicate large runtime rule bodies already owned by `references/`

Duplication rules:
- duplication across `docs/` and `references/` is allowed when the layering is clear and the runtime form is materially more structured or smaller
- overlap between `references/` and `templates/` is allowed when generation and runtime loading both require the same concept
- duplication within the same folder should be treated as a likely drift risk unless the local layering clearly justifies it
- public-site repetition is acceptable by default; only contradictions matter

If this audit-facing summary conflicts with the canonical wording in `docs/vibeloom-methodology.md` or the operational routing in `SKILL.md`, the canon wins. Call out the conflict explicitly.

## Core Repository Constraints

Use these as hard audit constraints:
- `intent.md` is intentionally loose prose and is exempt from mandatory stable item IDs, though optional structured capability IDs may appear
- `docs/` are canonical prose methodology and help material, not routine runtime authority
- only `references/` is routine runtime authority for the skill
- `templates/` are generation inputs only
- the sibling public site workspace is public documentation and marketing, not runtime authority, but it must not contradict the canon
- `SKILL.md` is the runtime entrypoint and orchestrator, but detailed runtime rules should not be duplicated there if they already exist in `references/`
- the canonical abstract command model is `<action> <target> <context>` wherever the general syntax is described
- docs in `docs/` can reference each other but not docs in other folders
- docs in `references/` can reference each other as well as docs in `templates/`, but not docs in other folders
- docs in `templates/` can reference each other but not docs in other folders
- only `SKILL.md` may contain exact cross-folder `help` routing into `docs/`
- `references/` run-time instructions and `templates/` spec templates are generated from `docs/` prose, so duplication across those layers should be reported but not automatically marked for fixing
- between documents in the same folder there should be no unnecessary duplication

## Inspection Scope

Inspect the actual workspace thoroughly:
- `SKILL.md`
- all files in `references/`
- root canonical artifacts: `constitution.md`, `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md`
- all files in `templates/`
- relevant files in `docs/`
- relevant files in the sibling `../site/` workspace
- metadata such as `agents/openai.yaml`
- package and authority docs such as `README.md`

Use direct repo inspection. Do not rely on memory or assumptions.

## Audit Dimensions

1. Redundancy / duplication
- identify rules, concepts, command definitions, authority statements, runtime instructions, or methodological constraints repeated across files in ways that increase maintenance cost, drift risk, or runtime context load

2. Coherency / correctness
- identify contradictions, stale wording, outdated paths, inconsistent syntax, mismatched templates, broken authority boundaries, or artifacts that no longer agree with the canon

3. Verbosity / size / deadweight
- identify wording, sections, structures, or entire files that could be shortened, consolidated, moved, or removed without losing necessary meaning

4. Context window size / load during execution
- identify opportunities to reduce runtime load and avoid unnecessary reference or artifact loading

## Review Standard

- if runtime guidance exists outside `references/`, call it out unless it is clearly help-only material or an explicit orchestration rule owned by `SKILL.md`
- if the public site says something broader, simpler, or different than the canon, classify it explicitly as either acceptable simplification or an actual contradiction
- if two files define the same normative rule, assume that is a problem unless the layering clearly justifies it
- if a rule is runtime-operational, prefer it to exist in exactly one authoritative place inside `references/`, with higher-level files only pointing to it
- if a general syntax definition appears anywhere and does not use `<action> <target> <context>`, call it out
- if a file exists but serves no current runtime, canonical-doc, template, or honest public-site purpose, call it out as possible deadweight
- if wording cites brittle exact counts where no count is operationally necessary, call it out as maintainability deadweight
- distinguish, when possible:
  - new contradiction
  - longstanding accepted layering
  - acceptable simplification
  - intentional duplication
  - likely deadweight
- if recency or intent cannot be determined from the current repo, say so instead of guessing

## Audit Procedure

Before forming judgments:
1. read `docs/vibeloom-methodology.md`
2. read `SKILL.md`
3. inspect the relevant runtime, template, canonical, and public-site files directly
4. judge lower-layer files against canon rather than against memory

## Required Output: Phase 1 Audit

Do not edit files in Phase 1.

Produce:
1. Findings first, ordered by severity
2. Every finding must include:
- severity
- why it matters
- exact file references
- suggested resolution direction
- `Canon consulted` when the judgment depends on a specific authoritative source
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
- moving or deleting clearly unreferenced deadweight
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
- changing layering between `SKILL.md`, `references/`, `docs/`, `templates/`, and the sibling public site workspace

### Group D: Public Site / Marketing Alignment

Use for public-site changes that align public claims to the canon.

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
- after presenting the grouped plan, stop and wait for approval of the first step

## Approval-Gated Execution Rules

After a step is approved:
- make only that step's changes
- preserve unrelated existing changes
- do not silently widen scope
- if the approved step requires a broader change than expected, stop and explain before proceeding

After applying an approved step, report:
- what changed
- files touched
- verification performed
- whether the targeted finding is now fully resolved or partially resolved
- what related issues remain
- the next proposed step, with its group label

Then stop and wait for approval again.

## Periodic-Run Guardrails

- this prompt is for repeatable repository health checks, not one-off commentary
- inspect the full current workspace each run
- focus on maintenance cost, drift risk, and runtime context load
- do not drift into generic advice; keep everything tied to the actual repository
- do not treat acceptable layering repetition as a bug unless it clearly increases drift risk
- do not "fix" marketing tone just because it is marketing; only fix it if it becomes misleading relative to the canon
- do not remove files unless they are clearly deadweight or replaced by a more authoritative source
- if no fixes are requested, it is valid to stop after the audit and grouped remediation plan
