<!--
VibeLoom task template: import
Operation: import
Invoked by: SKILL.md when user runs `/vibeloom import --mode <mode>`
-->

# Task: import

## Purpose

Bootstrap from existing code. Produce candidate contract artifacts in `draft` with confidence scores and evidence pointers; user reviews top-down before approving.

## Inputs

- `--mode`: required. Target mode for the imported project.
- Existing repo: filesystem under `./` containing source code, tests, configs, mockups, decision docs (any combination).
- Optional `--scan-paths`: limit scan to specified paths.
- Optional `--exclude-paths`: paths to exclude (defaults: `node_modules`, `.git`, `dist`, `build`, common build dirs).

## Preconditions

- Working directory is writable.
- `./intent.md` does NOT exist (or `--force` set with explicit confirmation).
- Existing code surface large enough to make import worthwhile (heuristic: under ~500 LOC, recommend prompt-only generation instead).

## Steps

1. Codebase scan: enumerate languages, frameworks, dependencies, test files, config files.
2. Aggregate evidence: per-language entry points, declared interfaces, dependency graph, observed deployment hints (Dockerfile, package.json scripts, CI configs).
3. Per-tier candidate inference (in order):
   a. **intent-specs**: infer capabilities (CAP) from observable user-facing functionality, constraints (CST) from configs and dependencies. Tech stack inferred from frameworks → populates Tech Stack section in `defaults.md`.
   b. **product-specs**: infer FRs from API endpoints + user flows; STORYs from observed user journeys; BCs from cohesive code modules.
   c. **ux-specs** (if presentation code present): infer VIEWs from page/route definitions, INTs from event handlers, UXCs from i18n + accessibility configs.
   d. **system-specs**: infer CONT from deployment topology, CMP from cohesive code modules, IF from public API surfaces, DEP from import graph, BEH from test descriptions, `layer` from heuristic (presentation = frontend bundle / static; application = API/server; domain = service workload; infrastructure = IaC).
4. Confidence scoring per candidate (high / medium / low) based on evidence quality (multiple corroborating signals = high; single weak signal = low).
5. Evidence linking: each draft item carries `derives_from` plus a free-form `evidence` field pointing at source paths.
6. Draft writing in batches: intent → product → ux → system. Each batch is its own `generate` invocation under the hood.
7. Emit one `import` trace per invocation summarizing aggregate counts and confidence distribution; per-candidate evidence lives in the draft artifacts' frontmatter.
8. Run structural eval; surface coverage gaps (uncovered upstream items, dangling references) as findings.
9. Surface review packets to the user, top-down (intent first).

## Output

- Draft artifacts at every tier in scope for the target mode (status: `draft`).
- Trace entry in `.vibeloom/traces/imports.jsonl` with aggregate evidence summary.
- `.vibeloom/cache/contract-graph.json` initialized with candidate items + edges.
- Per-tier review packets with confidence indicators.

## Constraints

- Imported items are NOT trusted until reviewed and approved by the user.
- Confidence scoring is an honest metric: agent must NOT inflate confidence to bias approval.
- Evidence pointers MUST cite real source paths (no fabricated references).
- Per-tier order respected: don't surface ux-specs review before intent-specs, etc.
- Layer inference is heuristic; user must confirm `layer` field on each container during review.

## Validation

- Structural eval after each batch (must pass before next batch generates).
- No mechanical runners invoked (existing code already exists; no new code generated yet).
- Heuristic semantic eval per batch surfaces concerns about inference quality (e.g. "FR-0019 has no clear acceptance criterion in observed code").

## Failure modes

- No discoverable code: surface guidance to use `init` instead.
- Mixed-language codebase exceeding agent context: scan in chunks; surface a "scan-only-this-subtree" suggestion.
- Conflicting evidence (e.g. both REST and GraphQL endpoints): emit ambiguity finding; user picks during review.
- Missing test coverage: import proceeds but FRs lacking ACC are flagged as low-confidence.
