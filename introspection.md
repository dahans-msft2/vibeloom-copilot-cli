Analyze this entire VibeLoom repository as a full consistency/coherency/minimality audit.

Do not make changes yet. Inspect the actual workspace thoroughly and produce a repo-grounded report based on what is really in the repository, not on assumptions.

Audit goals:
- redundancy / duplication: identify rules, concepts, command definitions, authority statements, runtime instructions, or methodological constraints repeated across files in ways that increase maintenance cost, drift risk, or runtime/context-window overhead
- coherency / correctness: identify contradictions, stale wording, outdated paths, inconsistent syntax, mismatched templates, broken authority boundaries, or artifacts that no longer agree with the canon
- verbosity / size: identify wording, sections, structures, or entire files that could be shortened, consolidated, moved, or removed without losing necessary meaning

Architectural constraints you must use during the audit:
- `intent.md` is intentionally loose prose and is exempt from mandatory stable item IDs, though optional structured capability IDs may appear
- only `references/` is routine runtime authority for the skill
- `templates/` are generation inputs only
- `docs/` are canonical prose methodology / help material, not routine runtime authority
- `site/` is public documentation / marketing, not runtime authority, but it must not contradict the canon
- `SKILL.md` is the runtime entrypoint and orchestrator, but detailed runtime rules should not be duplicated there if they already exist in `references/`
- the canonical abstract command model is `<action> <target> <context>` wherever the general syntax is described

What to inspect carefully:
- `SKILL.md`
- all files in `references/`
- root canonical artifacts: `constitution.md`, `intent.md`, `prd.md`, `usm.md`, `dm.md`, `spec.md`
- all files in `templates/`
- relevant files in `docs/`
- relevant files in `site/`
- metadata such as `agents/openai.yaml`
- package-map / authority-model docs such as `README.md`

Method:
- inspect the repo directly; do not rely on memory
- use fast repo search and targeted file inspection
- distinguish clearly between:
  - actual contradictions / bugs
  - acceptable duplication due to layering
  - optional cleanup opportunities
- treat repeated normative definitions as suspect unless the layering clearly justifies them
- pay special attention to:
  - command surface consistency
  - authority boundaries between `SKILL.md`, `references/`, `docs/`, `templates/`, `site/`, and metadata
  - runtime leakage outside `references/`
  - stale public-site claims
  - template/canon mismatches
  - deadweight artifacts
  - places where a shorter formulation would reduce maintenance burden without losing clarity

Review standard:
- if runtime guidance exists outside `references/`, call it out unless it is clearly help-only or an explicit escalation path
- if `site/` says something broader, simpler, or different than the canon, classify it explicitly as either acceptable simplification or an actual contradiction
- if two files define the same normative rule, assume that is a problem unless the layering clearly justifies it
- if a rule is runtime-operational, prefer it to exist in exactly one authoritative place inside `references/`, with higher-level files only pointing to it
- if a general syntax definition appears anywhere and does not use `<action> <target> <context>`, call it out
- if a file exists but serves no current runtime, canonical-doc, template, or honest public-site purpose, call it out as possible deadweight
- if wording cites brittle exact counts where no count is operationally necessary, call that out as maintainability deadweight

Output requirements:
1. Findings first, ordered by severity.
2. Every finding must include:
   - severity
   - why it matters
   - exact file references
3. Then provide separate sections:
   - `Redundancy / Deadweight`
   - `Already Coherent / Leave Alone`
   - `Open Questions / Judgment Calls`
4. Be strict, concrete, and evidence-based.
5. Do not modify files.
6. Do not drift into generic advice; keep the report tied to the actual repository.
