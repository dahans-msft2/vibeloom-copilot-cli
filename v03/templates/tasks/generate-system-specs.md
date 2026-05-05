<!--
VibeLoom task template: generate-system-specs
Operation: generate
Invoked by: SKILL.md when user runs `/vibeloom generate system-specs` or as part of a top-down generation cascade after product-specs (and ux-specs if present) are approved
-->

# Task: generate-system-specs

## Purpose

Generate or repair `system-specs` (system.md + containers.md + per-container container.md + per-component component.md) from approved product-specs (and ux-specs if present), with layer-aware container synthesis.

## Inputs

- `target_tier`: `system-specs` (fixed)
- `mode`: pm / dev / ux / expert (any full mode)
- `affected_ids`: optional. Item IDs that triggered the regeneration.
- Approved upstream: intent.md, defaults.md (Tech Stack section is critical here), prd.md, usm.md, dm.md, ux.md (if approved).
- Previous approval trace for system-specs (if exists).

## Preconditions

- intent-specs, product-specs are `approved`.
- ux-specs is `approved` (if mode is pm / dev / expert with ux-specs in scope).
- Defaults Tech Stack section has at least the Domain stack populated (decomposition: monolith vs multi-service).
- Working directory contains placeholder system.md and containers.md.

## Steps

1. Load approved upstream items via engine `parse + graph`.
2. Read defaults Tech Stack to determine:
   - Presentation stack → presentation container(s) shape and deployment target.
   - Application stack → application container(s) shape.
   - Domain stack → number of domain containers (monolith = 1; multi-service = 1 per BC).
   - Infrastructure stack → infrastructure container shape.
3. Generate `system.md`:
   - EXT-#### derives from FR, NFR, CAP (external actors and systems).
   - TB-#### derives from NFR (trust boundaries).
   - SNFR-#### derives from NFR, CST, DEF (system-wide non-functional requirements).
4. Generate `containers.md`:
   - CONT-#### entries per layer:
     - One presentation container (e.g. "web-app") unless micro-frontends explicit.
     - One or more application containers (one per UI surface served, e.g. "web-api", "mobile-api", "admin-api").
     - Domain containers per the decomposition choice (monolith → one container hosting all BCs; multi-service → one container per BC).
     - One infrastructure container ("infra") declaring consumed platform services.
   - Each CONT carries its `layer` field.
   - Inter-container communication paths recorded as structured content.
5. Generate per-container `<container>/container.md` files:
   - Required `layer` field in frontmatter.
   - Deployment target section filled per layer + platform choice from defaults.
   - Resident bounded contexts (DOMAIN ONLY).
   - Component inventory.
   - Local dependency edges.
   - Cross-layer interactions (prose; structural in v0.4 per roadmap).
6. Generate per-component `<container>/<component>/component.md` files:
   - `bounded_context` field populated for domain components; null for others.
   - IF-#### per provided interface (derives from FR, STORY, ACC).
   - DEP-#### per consumed dependency.
   - BEH-#### per local behavior contract (derives from STORY, ACC, INV).
   - NOTE-#### per local concern.
7. Run engine `parse + eval --target system-specs` for structural checks (including layer-aware constraints: hosted_bounded_contexts non-empty only for domain layer).
8. Run heuristic semantic eval (faithful representation, naming consistency, implicit dependencies, capability gaps, target-platform mismatch — flags if Tech Stack and inferred container layer don't agree).
9. Emit a `generation` trace recording basis_ids, output_artifact_ids (system, containers, all per-container + per-component files), output_item_ids.

## Output

- system.md, containers.md updated (status: draft).
- Per-container container.md and per-component component.md files created/updated.
- New trace entry in .vibeloom/traces/generations.jsonl.
- Contract graph updated.
- Findings.

## Constraints

- Every CONT carries `layer`. Every CMP inherits its container's layer.
- Bounded contexts ONLY in domain-layer containers. Structural eval enforces.
- Domain decomposition follows defaults (monolith: all BCs in one container; multi-service: one per BC). Conflicts surface as semantic finding.
- Deployment target on each container.md must be consistent with infrastructure stack in defaults.
- Don't fabricate components without traceable basis — every CMP derives from at least its container plus (for domain) at least one BC.

## Validation

- Structural eval must pass: layer-aware constraints, ID validity, reference integrity, DAG validity, ownership rules, context sufficiency.
- Mechanical runners not invoked at the system-specs tier (no code yet).
- Semantic eval surfaces target-platform mismatches and capability gaps.

## Failure modes

- Missing approved upstream: abort, surface "approve product-specs (and ux-specs if applicable) first."
- Defaults Tech Stack incomplete (e.g. no domain decomposition choice): surface advisory; ask user to fill Tech Stack before generating system-specs.
- Bounded context too large to fit in one component: surface decomposition advisory; user splits BC during review.
- Inferred deployment target conflicts with declared platform: surface as semantic finding.
