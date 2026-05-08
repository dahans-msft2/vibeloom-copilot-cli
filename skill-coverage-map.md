# Skill coverage map

Externalized Step 1 verify for `review-skill.md`. Three coverage tables: command → task template, task template → impl §15 operation, artifact template → impl §6 frontmatter shape.

## Table 1 — command → task template (SKILL.md routing)

| Command | Routing entry | Task template | Status |
|---|---|---|---|
| `/vibeloom init` | `tasks/init.md` | `tasks/init.md` | ✓ |
| `/vibeloom import` | `tasks/import.md` | `tasks/import.md` | ✓ |
| `/vibeloom generate intent-specs` | `tasks/generate-intent-specs.md` | `tasks/generate-intent-specs.md` | ✓ |
| `/vibeloom generate product-specs` | `tasks/generate-product-specs.md` | `tasks/generate-product-specs.md` | ✓ |
| `/vibeloom generate product-specs --from ux` | `tasks/generate-product-specs-from-ux.md` | `tasks/generate-product-specs-from-ux.md` | ✓ |
| `/vibeloom generate ux-specs` | `tasks/generate-ux-specs.md` | `tasks/generate-ux-specs.md` | ✓ |
| `/vibeloom generate system-specs` | `tasks/generate-system-specs.md` | `tasks/generate-system-specs.md` | ✓ |
| `/vibeloom generate context` | `tasks/generate-context.md` | `tasks/generate-context.md` | ✓ |
| `/vibeloom generate code-component` | `tasks/generate-code-component.md` | `tasks/generate-code-component.md` | ✓ |
| `/vibeloom eval [target]` | `tasks/eval.md` | `tasks/eval.md` | ✓ |
| `/vibeloom review <target>` | `tasks/review.md` | `tasks/review.md` | ✓ |
| `/vibeloom reconcile <target>` | `tasks/reconcile.md` | `tasks/reconcile.md` | ✓ |
| `/vibeloom approve <approval-unit>` | `tasks/approve.md` | `tasks/approve.md` | ✓ |
| `/vibeloom status` | `tasks/status.md` | `tasks/status.md` | ✓ |

**14 task templates exist; coverage map has zero empty cells.** Status command coverage: ✓ complete.

## Table 2 — task template → impl §15 operation

Per the prompt: "Every task template must reference its source operation in `vibeloom-implementation.md` §15."

| Task template | "Operation:" header | Explicit §15.X cite |
|---|---|---|
| `tasks/init.md` | `Operation: init` (→ §15.7) | NO |
| `tasks/import.md` | `Operation: import` (→ §15.8) | NO |
| `tasks/generate-intent-specs.md` | `Operation: generate` (→ §15.1) | NO |
| `tasks/generate-product-specs.md` | `Operation: generate` (→ §15.1) | NO (but cites §5.1 in Validation) |
| `tasks/generate-product-specs-from-ux.md` | `Operation: generate` (→ §15.1) | NO |
| `tasks/generate-ux-specs.md` | `Operation: generate` (→ §15.1) | NO |
| `tasks/generate-system-specs.md` | `Operation: generate` (→ §15.1) | NO |
| `tasks/generate-context.md` | `Operation: generate` (→ §15.1) | NO |
| `tasks/generate-code-component.md` | `Operation: generate` (→ §15.1) | NO |
| `tasks/eval.md` | `Operation: eval` (→ §15.2) | NO (cites §14 in Postconditions, §14.3 in Steps) |
| `tasks/review.md` | `Operation: review` (→ §15.3) | NO |
| `tasks/reconcile.md` | `Operation: reconcile` (→ §15.4) | NO (cites §13.2 in Steps) |
| `tasks/approve.md` | `Operation: approve` (→ §15.5) | NO |
| `tasks/status.md` | `Operation: status` (→ §15.6) | NO (cites methodology §9) |

**Pattern:** every task template has `Operation: X` in its HTML comment header — this implicitly links to §15.X by operation name. None cite §15.X explicitly. Marginal coverage gap.

## Table 3 — artifact template → impl §6 frontmatter

| Artifact template | Tier | impl §6 reference shape | Match (spot-check) |
|---|---|---|---|
| `intent-specs/intent.md` | intent | §6.1 contract artifact | ✓ |
| `intent-specs/vibe-intent.md` | intent (compact) | §6.1 + §2.2 vibe layout | ✓ |
| `intent-specs/defaults.md` | intent | §6.1 contract artifact | ✓ |
| `product-specs/prd.md` | product | §6.1 contract artifact | ✓ |
| `product-specs/usm.md` | product | §6.1 contract artifact | ✓ |
| `product-specs/dm.md` | product | §6.1 contract artifact | ✓ |
| `ux-specs/ux.md` | ux | §6.1 contract artifact | ✓ |
| `system-specs/system.md` | system | §6.1 contract artifact | ✓ |
| `system-specs/containers.md` | system | §6.1 contract artifact | ✓ |
| `system-specs/container.md` | system | §6.3 container frontmatter (with `layer`) | ✓ |
| `system-specs/component.md` | system | §6.4 component frontmatter | ✓ |
| `system-specs/vibe-system.md` | system (compact) | §6.1 + §2.2 vibe layout | ✓ |
| `context/bdd.md` | context | §6.2 context artifact | ✓ |
| `context/{root,container,component}-config.md` | context | §6.2 context artifact | ✓ |
| `validation-registry.md` | validation registry | §7 | ✓ |
| `decision-trace.md` | trace render | §8.5 + §8.5.1 | ✓ |

**18 artifact templates; spot check passes.** Detailed per-field validation deferred — would require parsing each frontmatter and comparing to §6 schema field-by-field. That's engine work (CANON-FIND-011's new §16 acceptance item).

## Codæ 10-section completeness for task templates

| Section | Expected (14 task templates) | Found |
|---|---|---|
| Purpose | 14 | 14 ✓ |
| Inputs | 14 | 14 ✓ |
| Preconditions | 14 | 14 ✓ |
| Steps | 14 | 14 ✓ |
| Output | 14 | 14 ✓ |
| Postconditions | 14 | 14 ✓ |
| Constraints | 14 | 14+ ✓ (extra count from artifact templates) |
| Invariants | 14 | 14+ ✓ (extra count from artifact templates) |
| Validation | 14 | 14 ✓ |
| Failure modes | 14 | 14 ✓ |

**All 14 task templates have all 10 codæ sections.** No incomplete templates.

## Vocabulary consistency

| Term | Count | Drift |
|---|---|---|
| "approval unit" | 14 | none — no "approval scope" usages |
| "subagent" | 62 | none — no "sub-agent" or "sub agent" |
| "Contract Graph" (after CANON-FIND-010) | confirm in cascade scan |  |
| "contract graph" lowercase | **9 stragglers** | cascade from CANON-FIND-010 (see SKILL-FIND-001) |

## Cascade scan (from recent canon work)

| Cascade source | Site location |
|---|---|
| CANON-FIND-010 (Contract Graph rename) | 9 lowercase usages in skill templates (SKILL-FIND-001) |
| CANON-FIND-011 (universal-trace + §5.1 derivation rules) | derives_from validation gaps in some generation tasks + at gate points (SKILL-FIND-003) |
| CANON-FIND-005 (cognitive surface stub) | NONE (skill doesn't surface this) |
| CANON-FIND-006/007 (impl §16/§17 cuts + renumber) | NONE (skill doesn't cite by §-number) |

## Items NOT load-bearing for the canon (skill-original)

- Task template Steps procedures, subagent-prompt body, references/troubleshooting recovery procedures, CLI invocation patterns, exec summaries, response-shape conventions: skill-internal decisions, not derived from canon.
