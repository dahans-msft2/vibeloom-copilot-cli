# Example: multi-component reconciliation

A search system has three components: `web` (UI), `search-api` (query orchestration), `indexer` (content indexing). The PM wants to add a "search by tag" capability. The change touches all three components — and the existing search behavior on `web` differs subtly from what a clean regenerate would produce. This is the kind of conflict that requires `reconcile`, not `generate`.

## 1. Intent change

PM edits `intent.md` to add `CAP-0007: search by tag in addition to text`. Approves intent-specs.

```text
$ vibeloom approve intent-specs
✓ Approved.
ℹ Affected downstream:
  product-specs:  3 items stale, 2 uncovered
  system-specs:   3 components stale (web, search-api, indexer)
  code:           14 files in 3 components

→ Next: vibeloom generate product-specs
```

Product-specs and system-specs regenerate cleanly from the new intent. The new `FR-0023: search by tag` and `STORY-0034: filter results by tag` flow downstream. The `IF-0042` interface on `search-api` gets a new parameter; the `indexer` component grows a tag-index field; the `web` component gets a new tag-filter UI element.

## 2. The conflict

When the user runs `generate code`, the engine reports a problem:

```text
$ vibeloom generate code
ℹ Wave 1 (independent):
  ✓ search-api regenerated (4 files, validation passed)
  ✓ indexer regenerated (3 files, validation passed)
  ! web blocked: drifted from contract before this change
ℹ Web component has accumulated 3 manual edits over the last
  6 weeks that contract does not capture. Regenerating would
  overwrite them.
→ Next: vibeloom reconcile web
```

The two infrastructure components (`search-api`, `indexer`) regenerated cleanly because nobody had been hand-editing them. The `web` component, where humans live every day, had drifted: someone had tweaked the search-results UX behavior in ways the contract didn't reflect.

## 3. Reconciliation

```text
$ vibeloom reconcile web
```

Vibeloom presents three drift cases as a packet:

```yaml
packet_type: reconciliation
packet_id: RECON-0007
target: code
scope: component:web/search
drift_cases:
  - drift_id: DRIFT-0001
    summary: "Search results show inline tag chips; contract says text-only list."
    evidence: "web/src/search/Results.tsx:42-67"
    directions:
      - preserve_contract_regenerate_code
        # would remove the tag chips on regen
      - amend_contract_to_preserve_downstream_behavior
        # would add a UXC entry: "results display tag chips inline"
      - user_defined
    recommended: amend_contract_to_preserve_downstream_behavior

  - drift_id: DRIFT-0002
    summary: "Empty-results state has custom illustration; contract has no UXC for this."
    evidence: "web/src/search/EmptyState.tsx:1-33"
    directions:
      - preserve_contract_regenerate_code
      - amend_contract_to_preserve_downstream_behavior
      - user_defined
    recommended: amend_contract_to_preserve_downstream_behavior

  - drift_id: DRIFT-0003
    summary: "Search debounces input by 250ms; contract says no debounce."
    evidence: "web/src/search/SearchBox.tsx:18"
    directions:
      - preserve_contract_regenerate_code
      - amend_contract_to_preserve_downstream_behavior
      - user_defined
    recommended: amend_contract_to_preserve_downstream_behavior
```

The PM reviews each case interactively. They choose:

- DRIFT-0001 (tag chips): **amend contract** — the tag chips are a feature the team wants to keep; add `UXC-0019` to capture it.
- DRIFT-0002 (empty illustration): **amend contract** — also a deliberate choice; add `UXC-0020` and `MOCK-0009` referencing the illustration source.
- DRIFT-0003 (debounce): **preserve contract** — the debounce was a quick fix nobody approved; remove it on regen.

Each choice generates a contract amendment (for the first two) or a code patch (for the third). The amendments go through the normal review/approve cycle.

## 4. Final regeneration

```text
$ vibeloom approve ux-specs
✓ ux-specs approved (UXC-0019, UXC-0020 added).

$ vibeloom generate code --scope web
✓ web regenerated.
✓ Tag chips preserved (per UXC-0019).
✓ Empty illustration preserved (per UXC-0020 + MOCK-0009).
✓ Debounce removed (per DRIFT-0003 direction).
✓ New tag-filter UI added (per FR-0023).
✓ All three components synchronized to new intent.
```

Code-sync traces capture the new state. Reconciliation traces (`RECON-0007`) record why each direction was chosen — durable provenance for "why does web have tag chips when no spec mentions them?" six months from now.

## What this example illustrates

- **Multi-component regen rarely lands clean** — at least one component will have accumulated drift, and that's where reconciliation earns its keep.
- **Reconciliation is interactive and bounded.** Each drift case is presented separately with directions; the user chooses; the action is taken; nothing else changes.
- **Both directions are valid.** Sometimes the contract is right and the code is wrong (DRIFT-0003, the unauthorized debounce). Sometimes the code is right and the contract is incomplete (DRIFT-0001, DRIFT-0002 — real product behavior the contract had failed to capture).
- **Preserving downstream behavior amends the contract.** The contract grows to match reality; the contract is not a museum.
- **Reconciliation traces are durable provenance.** Why specific divergences exist becomes a queryable graph property, not tribal knowledge.
