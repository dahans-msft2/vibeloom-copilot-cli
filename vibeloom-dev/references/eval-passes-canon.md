# Reference: eval-passes-canon

Adversarial review passes for `eval canon` (and individual canon targets: intent, manifesto, methodology, implementation).

Adapted from v03's `review-canon.md` with the intent layer added.

## Goal

Make the canon **precise, concise, internally consistent, and operationally dependable** enough that downstream site/skill/engine work can trust it. NOT a general polish pass.

## Authority model

Use ownership-by-concern, not tier-precedence:

| Concern | Canonical owner | Other docs may do this |
|---|---|---|
| Why the paradigm exists | Manifesto | Reference the thesis without adding mechanics |
| What the user wants from this version (CAPs, CSTs, Vision) | Intent | Cite intent items without redefining |
| Concepts, terms, modes, operations, status semantics | Methodology | Cite methodology and avoid redefining |
| Runtime behavior, schemas, IDs, caches, validation, dispatch | Implementation | Cite implementation and avoid motivation |
| Concrete templates, task prompts, SKILL.md, reference docs | Templates | Materialize methodology + implementation only |

When ownership conflicts, surface the conflict. **Do not silently make one document match another.**

## Source map (build first)

For each canon file, extract:
- Heading outline.
- Major definitions and their canonical owner.
- Major schemas, ID rules, trace families, status categories, operation semantics.
- Repeated claims or repeated definitions across documents.
- Downstream surfaces likely affected by changes (skill, site, engine, helper prompts).

Map is audit evidence, not a new artifact. Keep concise.

## Attack passes (run all)

### A. Intent ↔ manifesto cross-consistency

- Every CAP-#### in intent has a paradigm expression in manifesto. (e.g., intent CAP "support cross-agent reviews" implies manifesto has something about multi-agent collaboration as a principle.)
- Every CST-#### in intent has a manifesto basis (e.g., intent CST "user approval at every gate" implies manifesto has something about human-in-the-loop).
- Every principle in manifesto surfaces as an intent CAP or CST, OR is explicitly marked manifesto-only philosophy. (Missing = drift; agent should flag and let user pick which to amend.)
- intent and manifesto don't CONTRADICT each other on any concept.

### B. Authority and separation (intra-canon)

- Methodology contains implementation details, file layout, runtime grammar, or schema tables.
- Implementation explains motivation instead of runtime behavior.
- Manifesto relies on low-level implementation mechanics to make the thesis.
- Templates define concepts that methodology should own.
- One fact appears in multiple tiers without a clear canonical owner.

### C. Internal consistency (intra-canon)

- Manifesto promises something methodology or implementation does not deliver.
- Methodology and implementation disagree on modes, operation names, status categories, trace families, graph semantics, approval semantics, or scope semantics.
- Implementation examples contradict their own schemas.
- Template inventory or task names in implementation do not match `vibeloom-templates.md`.
- Forward references and section citations do not resolve.

### D. Concision and load-bearing value

- A paragraph, table, example, or section can be removed without breaking a downstream consumer.
- The same concept is explained repeatedly within one document.
- A proof point, market claim, or example belongs in the site or evidence appendix, not durable canon.
- A detailed example obscures the rule it is supposed to clarify.

### E. Operational adequacy

- Runtime rules are too vague for an agent or engine to implement.
- Schema examples omit required fields, include noncanonical fields, or use inconsistent IDs.
- Operation pseudocode has hidden side effects or misses required validation.
- Acceptance criteria are mixed with stale project status.

### F. Known failure probes (per-version specifics)

For v04+ canon specifically, check:
- Decision trace identity: event ID vs rendered decision-record ID.
- Component to bounded-context cardinality.
- `root` as graph root vs repo/allocation scope.
- Vibe mode: whether it writes graph/cache/status artifacts.
- Task-template inventory names vs extracted template names.
- Task-template versioning promises vs actual templates.
- Stale acceptance checklists or build-status claims inside canon.
- Dated evidence and competitor claims embedded in durable canon.
- (Version-specific probes accumulate here over time.)

## Finding quality bar

Every finding includes:

- `id`: `CANON-001`, `INTENT-001`, `MANIF-001`, `METH-001`, or `IMPL-001` (use the layer-specific prefix when the finding is layer-local; use `CANON-###` when cross-layer).
- `severity`: Critical / High / Medium / Low.
- `location`: exact file and section; line numbers when practical.
- `issue`: what is wrong.
- `why it matters`: downstream consequence for readers, agents, site, skill, engine.
- `proposed fixes`: 1-3 options, each with the trade-off. Default 1; more only when there's genuine fix ambiguity.
- `recommended fix`: one option + rationale.
- `verification`: how to prove the fix worked.
- `downstream impact`: site, skill, templates, engine, helper prompts, or none.

**Reject vague findings.** "Tighten wording" is not a finding unless it cites exact wording and a proposed replacement direction.

## Priority order

Walk findings in this order:

1. Identity/schema contradictions that can break generated artifacts or trace replay.
2. Authority-boundary violations (cause future drift).
3. Cross-layer alignment issues (intent ↔ manifesto, methodology ↔ implementation).
4. Stale or false claims.
5. Concision cuts that reduce repeated or non-load-bearing text.
6. Local prose polish.

Group duplicates into one finding with all affected locations.

## Anti-patterns

- General commentary without concrete fix options.
- Treating lower-tier materialization (templates) as conceptually canonical.
- Turning methodology into implementation detail.
- Rewriting across many sections under one vague finding.
- Doing downstream propagation during canon eval (eval is read-only).
