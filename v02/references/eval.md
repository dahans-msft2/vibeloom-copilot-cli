# Semantic Eval Reference

Load on demand during `eval`, `review`, `reconcile`, and `approve` when the target needs semantic validation on top of the engine's structural checks.

This file covers the **semantic drift** detector — one of three drift forms defined in [`vibeloom-methodology.md`](../vibeloom-methodology.md) ## Generation ### Drift. The other two forms are handled deterministically by the engine: structural drift via the staleness computation and lifecycle drift via direct-edit detection (see [`vibeloom-implementation.md`](../vibeloom-implementation.md) ## Metadata Format ### Direct Edit Detection / ### Staleness). This file defines what the agent checks on top of that.

Per [`vibeloom-methodology.md`](../vibeloom-methodology.md) ## Generation ### Eval, structural findings are blocking; semantic findings either escalate to the user (`breaking`) or surface as advisory. Both contribute to the combined finding list returned by `eval`.

**These checks describe WHAT to validate, not HOW.** Reason with whatever approach works best for the current model; emit findings in the schema below. Do not invent procedural steps, rubrics, or scoring systems.

---

## Finding Schema

Every semantic finding is a JSON object with these fields:

| Field | Type | Notes |
|---|---|---|
| `severity` | `breaking` \| `advisory` | See Severity Classification below |
| `dimension` | enum | `faithful-representation`, `naming-consistency`, `implicit-dependencies`, `capability-gap`, `other` |
| `upstream_id` | string \| null | The upstream item the downstream was checked against; null if not tied to a single upstream |
| `downstream_id` | string | The item or artifact being evaluated |
| `message` | string | One-sentence finding. Quote the specific divergent phrasing when possible. |
| `suggested_fix` | string \| null | Optional concrete edit direction; null when not obvious |

If no findings for a check, return an empty list. Do not invent severities, dimensions, or fields.

---

## Severity Classification

- **`breaking`** — the finding alters the meaning of an approved upstream item (narrowing, widening, reversing) or represents a capability entirely unaddressed. Breaking findings block delegated auto-advance in `pm` / `dev` modes and escalate to explicit user review (methodology ## Generation ### Approval And Auto-Advance).
- **`advisory`** — worth surfacing, but does not reliably indicate a spec defect. Naming drift, suggested implicit edges, and partial capability coverage are typically advisory.

When in doubt, classify as `breaking`. False advisories cost a review cycle; false-negative breaking findings let meaning drift past an approval gate.

---

## Dimensions

### Faithful Representation

**What:** For a downstream item and each item it declares in `derives_from`, judge whether the downstream faithfully represents the upstream's meaning.

**Faithful** means the downstream neither narrows, widens, reverses, nor contradicts the upstream. Adding detail or refinement consistent with the upstream is not a violation — that is what downstream tiers are for. Changing the scope, direction, or claim is.

**Breaking signals:**
- Downstream narrows upstream scope (e.g., upstream says "all users," downstream applies to "premium users only")
- Downstream widens upstream scope beyond what's stated
- Downstream reverses or negates upstream meaning
- Component interfaces (`IF-####`): contract, error behavior, or effects differ from the approved version
- Invariants (`INV-####`): rule weakened or strengthened compared to the approved version

**Advisory signals:**
- Downstream picks one plausible reading of an ambiguous upstream; another reading is equally plausible
- Downstream omits a detail that could be a deliberate refinement or a gap (when ambiguity is genuine)

If the downstream faithfully represents the upstream, emit no finding.

### Naming Consistency

**What:** Given the domain model's `TERM-####` items and a downstream artifact, judge whether the artifact's terminology aligns with the ubiquitous language.

**Consistent** means concepts defined by `TERM-####` are referred to using the same word or phrase throughout. Introducing a new word for a defined concept is a drift. Using a defined term with a different meaning than its `TERM` entry is a drift.

**Breaking** when the drift introduces genuine semantic confusion — the same word used for two different concepts in the same artifact, or a defined term used with a contrary meaning. **Advisory** for simple naming inconsistencies that don't obscure meaning.

If terminology aligns with the domain model, emit no finding.

### Implicit Dependencies

**What:** For a downstream item and its declared `derives_from`, judge whether there are upstream items the downstream's meaning depends on but that are not in `derives_from`.

**Candidate upstreams** are items of allowed upstream prefixes for the downstream's type per the Derivation DAG (methodology ## Context Graph). Do not propose edges to disallowed types.

**Depends on** means the downstream's description, constraints, or behavior would change if the candidate were removed or modified. A passing mention is not a dependency; a load-bearing reference is.

Emit one `advisory` finding per missing edge. Do not classify as `breaking` — whether to add the edge is a user decision, not an approval gate.

If no implicit dependencies are detected, emit no finding.

### Capability Gaps

**What:** Given all `CAP-####` and `CST-####` items from `intent` and the full downstream stack, judge whether each capability and hard constraint is substantively addressed somewhere downstream.

**Addressed** means at least one downstream artifact carries meaning that implements or enables the capability — not just a `derives_from` edge pointing at it. The engine's structural coverage check already ensures at least one edge exists; this check asks whether the meaning is actually carried.

**Breaking** for capabilities or hard constraints entirely unaddressed. **Advisory** when partially addressed, or addressed at an unexpectedly shallow level for the current mode.

If all capabilities and constraints are substantively addressed, emit no finding.

### Other Drift

The four dimensions above are not exhaustive. When you observe a semantic issue that clearly matters for approval but fits none of them, emit a finding with `dimension: other` and a message that identifies the nature of the drift. Prefer a named dimension when one fits; reserve `other` for genuine novelty.

---

## Application Notes

- Apply every dimension relevant to the target scope. `faithful-representation` and `implicit-dependencies` are per-item; `naming-consistency` and `capability-gap` are per-artifact or per-stack.
- Return the full finding list. Filtering to "most important" findings is the orchestrator's call, not the check's.
- Semantic eval is target-bounded — validate the target against its approved upstream basis; do not inspect downstream artifacts.
