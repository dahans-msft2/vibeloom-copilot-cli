# VibeLoom Implementation

This document is the concrete runtime specification for implementing the VibeLoom methodology in Codex and Claude. It defines the exact artifact mapping, generated app file structure, skill behavior, context-loading rules, and code-generation defaults.

If [vibeloom-methodology.md](/Users/ilya.baimetov/Projects/vibeloom/v02/vibeloom-methodology.md) answers "what VibeLoom means," this document answers "how the skill realizes it."

---

## What This Document Is

This document owns concrete implementation truth for the VibeLoom runtime and skill layer.

It defines:

- exact artifact names and file roles
- generated app filesystem layout
- lifecycle and metadata fields
- exact runtime operations
- context-loading rules for skill execution
- how scoped agent guidance is generated
- how templates are used
- code-generation defaults

It does **not** redefine methodology meaning. It implements it.

---

## Relationship To Methodology

The two primary documents have different authority:

- [vibeloom-methodology.md](/Users/ilya.baimetov/Projects/vibeloom/v02/vibeloom-methodology.md) owns conceptual methodology truth
- [vibeloom-implementation.md](/Users/ilya.baimetov/Projects/vibeloom/v02/vibeloom-implementation.md) owns concrete runtime and skill behavior

Precedence:

1. methodology owns meaning
2. implementation owns the concrete realization and concrete defaults
3. `templates/` own generation shape only
4. `SKILL.md`, if present, owns orchestration entrypoint behavior for a packaged skill

V1 does **not** include a `references/` layer. The runtime loads targeted sections from this implementation document directly.

---

## Shared Codex/Claude Skill-Runtime Model

VibeLoom uses one shared implementation model for Codex and Claude.

The common behavior is:

- one shared methodology
- one shared concrete runtime specification
- one shared artifact model
- one shared generation and review lifecycle
- one shared generated app layout

Codex and Claude may differ in:

- entrypoint packaging
- prompt wrapper shape
- tool integration details

They do **not** differ in the meaning of artifacts, lifecycle rules, generation order, or contract semantics.

If packaged as a skill:

- `SKILL.md` is the orchestration entrypoint
- it routes the assistant to the correct sections of this implementation doc
- it loads templates strictly on demand

This document remains the concrete source of truth even when `SKILL.md` exists.

---

## Concrete Artifact Mapping

The conceptual layers from methodology map to these concrete artifacts in a governed application:

| Conceptual layer | Concrete artifact | Scope | Role |
| --- | --- | --- | --- |
| Constitutional defaults | `defaults.md` | repo | Minimal constitution: foundations, repo defaults, binding rules, technology baseline, agent defaults, codegen defaults, quality defaults |
| Intent | `intent.md` | repo | Product purpose, rationale, non-normalized user intent |
| Requirements | `prd.md` | repo | Functional requirements and NFRs |
| Workflow/story layer | `usm.md` | repo | Story and workflow structure, acceptance framing |
| Domain layer | `dm.md` | repo | Bounded contexts, aggregates, invariants, ubiquitous language |
| System layer | `system.md` | repo | System context and external relationships |
| Deployment/runtime layer | `containers.md` | repo | Container topology, communication paths, hosting/runtime choices |
| Container contract | `/<container>/container.md` | container | Local runtime boundary and authoritative component inventory |
| Component contract | `/<container>/<component>/component.md` | component | Full contract for one owned technical boundary |
| Derived execution guidance | `AGENTS.md` | root / container / component | Scoped working brief derived from canonical truth |

Root canonical artifacts are:

- `defaults.md`
- `intent.md`
- `prd.md`
- `usm.md`
- `dm.md`
- `system.md`
- `containers.md`

There is **no canonical root `components.md`**.

---

## Generated App Filesystem

The canonical generated-app layout is:

```text
/
  defaults.md
  intent.md
  prd.md
  usm.md
  dm.md
  system.md
  containers.md
  AGENTS.md

  <container>/
    container.md
    AGENTS.md
    <component>/
      component.md
      AGENTS.md
      ...
```

Rules:

- containers live at repo root
- every first-class component has its own directory
- bounded context is not a path level; it lives in metadata and inventory
- a first-class component must be listed in its container's `container.md`
- each listed component must map to a directory containing `component.md`
- directories without `component.md` are not canonical components by default

This shape is optimized for:

- human readability
- shallow path depth
- swarm-friendly ownership boundaries
- predictable context loading for agents

---

## Exact Runtime Operations

The runtime exposes these logical operations:

| Operation | Direction | Behavior |
| --- | --- | --- |
| `init` | top-down | Bootstrap a governed repo, create missing root artifacts, and produce first drafts from user input |
| `vibeloom` | top-down | Main orchestrator for natural-language change requests |
| `generate` | top-down | Produce one artifact or one scoped artifact set from upstream truth |
| `review` | up + lateral | Critique a selected scope and optionally apply bounded fixes |
| `eval` | up | Run structural and semantic checks over the selected scope |
| `fix` | top-down | Propagate approved upstream changes to stale downstream artifacts |
| `approve` | gate | Move canonical drafts to approved, record provenance, increment version |
| `status` | read-only | Show lifecycle state, stale dependencies, and coverage gaps |
| `import` | bottom-up | Reconstruct candidate contracts from an unmanaged or drifted codebase |

### Generation Order

The default top-down generation order is:

1. `intent.md`
2. `defaults.md`
3. `prd.md`
4. `usm.md`
5. `dm.md`
6. `system.md`
7. `containers.md`
8. affected `container.md` files
9. affected `component.md` files
10. derived `AGENTS.md` files
11. code

`defaults.md` becomes the authoritative home for normalized global constraints after intent capture. `intent.md` retains product purpose, rationale, and non-normalized nuance.

### Profiles

Profiles control workflow rigor, not artifact scope.

| Profile | Classification | Approval behavior | Typical use |
| --- | --- | --- | --- |
| `lite` | Hidden internal classifier for safe scoping and escalation | One approval pause after the canonical spec stack for the current run is generated; code still waits for approved specs | Smaller or lower-risk projects |
| `full` | Explicit visible classifier | Tiered approval gates before proceeding downward | Larger, longer-lived, or parallelized systems |

`lite` may generate multiple spec tiers in one orchestrated run from upstream drafts created earlier in that same run.

### Review Modes

`review` exposes one logical operation with selectable behavior:

- advisory review
- bounded remediation
- custom-instruction review

Review may:

- surface contradictions and missing links
- propose upstream or lateral corrections
- apply bounded fixes within the allowed scope

Review may **not** silently rewrite semantically meaningful upstream truth.

### Eval Tiers

| Tier | Type | Purpose | Blocking |
| --- | --- | --- | --- |
| 1 | Structural | Validate frontmatter, IDs, lifecycle rules, dependency declarations, path/spec consistency, and reference integrity | Yes |
| 2 | Semantic | Analyze requirement coverage, boundary sanity, componentization fit, contradiction with upstream truth, and context sufficiency | No |
| 3 | Behavioral | Produce on-demand Gherkin scenarios from approved contracts for later implementation | No |

Tier 3 outputs are non-canonical.

---

## Context Loading And AGENTS Generation

Agents have finite attention. The runtime therefore uses deterministic loading rules.

### Loading Priorities

Always load:

- `defaults.md`

Usually load for generation, review, and repo-wide architectural work:

- `intent.md`

For technical work, load scope-first:

1. start from the target `component.md` when one component is being changed
2. start from `container.md` when local container structure or local inventory is the question
3. use `container.md` to discover components; do not infer canonical components from arbitrary folders
4. load only the relevant `dm.md`, `usm.md`, or `prd.md` slices needed to understand touched semantics
5. load `containers.md` or `system.md` slices when runtime boundaries, external interfaces, or NFR boundaries matter

If an agent is unsure whether a change stays within one component, one bounded context, or one container, it must escalate scope upward rather than under-scope the context.

### `AGENTS.md` Generation

`AGENTS.md` is derived, regenerable, non-canonical execution guidance.

Generated governed applications may produce it at:

- repo root
- container level
- component level

Derivation model:

- root `AGENTS.md` is derived from root canonical artifacts
- container `AGENTS.md` is derived from root truth plus local `container.md`
- component `AGENTS.md` is derived from root truth plus local `container.md` and `component.md`

`AGENTS.md` answers:

- what this scope owns
- what to load first
- what not to touch
- which checks or commands are common here
- which local caveats matter during execution

It helps execution, but it never substitutes for canonical truth.

---

## Templates And Generation Inputs

`templates/` is the generation-shape layer.

Rules:

- templates are loaded strictly on demand
- templates define structure, sections, and expected metadata shape
- templates do not define independent methodology truth
- users may customize templates, but resulting artifacts must still conform to methodology and implementation rules

Templates are especially useful for:

- root contract generation
- container contract generation
- component contract generation
- behavioral scenario generation

The runtime should prefer templates when producing new artifacts and may use them as interview scaffolds when eliciting missing information.

---

## Code Generation Defaults

Concrete code-generation behavior belongs here, not in the conceptual methodology.

The default code-generation rules are:

1. For behavior changes, prefer test-first delivery: write or update unit, component, contract, or scenario tests before implementation when practical.
2. Use the smallest test scope that can prove the behavior: unit tests inside one component first, broader workflow tests only when the change crosses explicit boundaries.
3. Implement from the owned component boundary inward. Do not widen scope unless an explicit interface or contract change requires it.
4. Keep domain logic inside the owning component and keep infrastructure-specific logic behind adapters.
5. If behavior is semantically unclear, generate or refine scenarios first rather than inventing behavior in code.

These defaults are concrete runtime behavior, not abstract methodology.

---

## Metadata, Lifecycle, And Approval Provenance

### Lifecycle States

Canonical artifacts use these lifecycle states:

- `draft`
- `approved`
- `stale`
- `superseded`

There is no separate `auto-approved` lifecycle state.

### Approval Provenance

Delegated approval is represented through provenance metadata:

```text
approval_mode: human | delegated
```

Delegated approval still results in `approved`. It records how approval happened without changing lifecycle semantics.

### Minimum Metadata

All canonical artifacts should carry at minimum:

- `status`
- `version`
- `dependencies`

`component.md` frontmatter must include at minimum:

- `status`
- `version`
- `dependencies`
- `approval_mode`
- `bounded_context`
- `container`
- `owned_paths`
- `owned_interfaces`
- `trace_to`

`container.md` must contain at minimum:

- container purpose and runtime boundary
- resident bounded contexts
- authoritative component inventory for that container
- component-to-folder mapping
- one-line responsibility per component
- grouped component inventory by bounded context
- local inter-component interfaces or dependency summary
- local NFR or operational constraints

### `defaults.md` Structure

`defaults.md` contains these sections:

1. `Repo Defaults`
2. `Foundations`
3. `Repo-Wide Rules`
4. `Technology Baseline`
5. `Agent Defaults`
6. `Code Generation Defaults`
7. `Quality Defaults`
8. `Toolbox Note`

The binding structural rules in `defaults.md` are:

1. The component is the primary unit of ownership, safe change, and agent work allocation.
2. Every component belongs to exactly one bounded context.
3. A bounded context must not span multiple containers.
4. Components from the same bounded context must be co-located in the same container.
5. A container may host multiple bounded contexts, but each component has exactly one container home.
6. Cross-component interaction must occur through explicit owned interfaces.
7. External systems and infrastructure must be isolated behind adapter boundaries rather than leaking into core component logic.
8. Component naming and contracts must follow the bounded context's ubiquitous language.
9. Canonical technical work must be scoped through `container.md` and `component.md`, not inferred from code alone.
10. Dependency and trace metadata must be explicit enough to support stale detection and impact analysis.

The quality defaults in `defaults.md` are:

1. Changes to a component should include or update test or scenario coverage appropriate to that component's risk.
2. Retryable handlers, jobs, and integrations should be idempotent by default.
3. Mutating component boundaries should emit sufficient logging or audit signals when the domain requires accountability.
4. Security, authorization, and NFR constraints captured upstream are binding on downstream design and code.

The toolbox note may mention optional tactics such as adapters, selective CQRS, SOLID heuristics, and familiar design-pattern catalogs, but they do not outrank explicit VibeLoom rules.

---

## Validation And Consistency Checks

An implementation is acceptable only if all of these hold:

- `vibeloom-methodology.md` contains no concrete generated-app filesystem tree
- `vibeloom-methodology.md` contains no exact filenames such as `defaults.md`, `container.md`, `component.md`, or `AGENTS.md`
- `vibeloom-methodology.md` still clearly explains constitutional defaults vs derived guidance as concepts
- this implementation doc contains the full concrete artifact mapping with no need to consult methodology for filenames or runtime behavior
- the implementation clearly defines one shared Codex/Claude runtime model
- the implementation contains concrete code-generation defaults
- there is no `references/` dependency in v1
- there is no duplicated ownership of truth between methodology and implementation
- `container.md` is clearly the authoritative component inventory for its container
- a reader can answer "what does VibeLoom mean?" from methodology and "how does the skill implement it?" from implementation

---

## Future Optimization Notes

V1 deliberately omits `references/`.

If later measurement shows that direct section loading from this document is too expensive in latency, too large for reliable context use, or repeatedly loads the same operational slices, a derived `references/` layer may be added later as a runtime optimization.

If it returns, it should be:

- derived, not hand-authored
- disposable, not canonical
- subordinate to this implementation document
