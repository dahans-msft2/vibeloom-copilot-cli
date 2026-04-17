<!--
VibeLoom template: defaults
Tier: intent-specs (all modes)
Purpose: minimal repo-wide constitution — binding global rules, technology baseline, quality guardrails.
Entities: `default` items carried as CST-#### (derives from `constraint` in intent per DAG).
Rules: only always-on, globally binding constraints. Downstream tiers treat `defaults` as binding.

Generator guidance:
- Keep this short. Defaults are the narrow set of rules every downstream tier must respect.
- Each default derives from exactly one `constraint` in intent — every CST-#### row here must have a derives_from pointing at an intent CST-####.
- Do not duplicate the prose of the source constraint. State the binding rule crisply.
- If a rule is optional, situational, or tactical, it belongs in intent or in a config artifact, not in defaults.
- A default becomes universally binding once derived; downstream entities may reference it without requiring an additional typed edge.
-->

---
artifact_id: defaults
artifact_type: defaults
tier: intent-specs
scope_kind: root
scope_id: root
status: draft
timestamp: "<ISO-8601 timestamp>"
derives_from: []
---

# Defaults

Repo-wide constitution. Binding globally and always.

## Rules

<!-- Each rule is a `default` item. It derives from a `constraint` in intent. -->

| id | rule | derives_from | notes |
|---|---|---|---|
| CST-0001 | | | |

## Technology baseline

<!-- Language, runtime, framework, and platform choices that are globally binding. Each still carries a CST-#### id and a derives_from link. -->

| id | rule | derives_from | notes |
|---|---|---|---|

## Quality guardrails

<!-- Testing, invariant enforcement, reconciliation discipline. Each still carries a CST-#### id and a derives_from link. -->

| id | rule | derives_from | notes |
|---|---|---|---|
