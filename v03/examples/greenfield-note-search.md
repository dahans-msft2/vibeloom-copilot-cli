# Example: greenfield note-search app

A solo developer wants a personal note-taking app with full-text search, tags, and offline support. This example shows VibeLoom in `vibe` mode and the upgrade trigger when the app outgrows it.

## 1. Initial intent

```text
$ vibeloom init --mode vibe
✓ Created intent.md (draft)
→ Next: edit intent.md, then `vibeloom approve intent-specs`
```

The user opens `intent.md` and writes:

> A personal note-taking app. Notes are plain text with optional tags. The app must work offline and search by text or tag in under 200ms for 10,000 notes.

Vibeloom extracts:

```text
CAP-0001  create / edit / delete notes
CAP-0002  tag notes
CAP-0003  search notes by text or tag
CST-0001  must work offline
CST-0002  search must complete in under 200ms for 10,000 notes
```

User approves. Approval trace is written.

## 2. First conflict

User asks vibeloom to generate the system. The model proposes a cloud-backed Elasticsearch index for the search component. Vibeloom catches the conflict in `eval`:

```text
$ vibeloom eval system
! Finding (blocking): SEARCH component proposes cloud-backed index;
  conflicts with CST-0001 (must work offline).
```

This is the kind of conflict that proves the methodology: a passable-looking generation that quietly violates an upstream constraint. Catching it at eval rather than in production is the point.

User runs `review system`:

```yaml
packet_type: review
target: system
basis: [CAP-0003, CST-0001, CST-0002]
findings:
  blocking:
    - finding_id: FIND-0001
      summary: "SEARCH proposes cloud-backed index; violates CST-0001 (offline)."
      proposed_fix: "Use local SQLite FTS5 with BM25 ranking; sized for 10k rows."
recommendation: apply_proposed_fix
```

User accepts the fix. Re-eval passes.

## 3. Code generation

```text
$ vibeloom approve system
✓ system approved · approval trace SYNC-0003

$ vibeloom generate code
✓ Generated 14 files across NOTES and SEARCH components
✓ Code-sync trace SYNC-0007 emitted
✓ Validation: typecheck=pass, unit=pass, contract-conformance=pass
```

Code-sync trace records that `web/src/search/index.ts` realizes `BEH-0006` (text-or-tag search) on `CMP-0003` (search component), with file hashes and validation results.

## 4. Upgrade trigger

Three months later, the project has grown: 4 contributors, 12 components, an embedding-based semantic search proposed alongside the original text search. Vibeloom flags:

```text
$ vibeloom status
ℹ Vibe limits exceeded:
  - 12 components (vibe recommends ≤ 5)
  - 4 contributors (vibe recommends 1-2)
  - 3 reconciliations in last 30 days
→ Consider: vibeloom init --upgrade --mode pm
```

User upgrades. Migration trace records that compact intent + flat system became full intent-specs + product-specs + ux-specs + system-specs. Existing code is import-analyzed; most of it is recognized; a few drifted spots are flagged for reconciliation.

## What this example illustrates

- **Vibe is genuinely minimal** — no graph cache, no code-sync trace folder, no formal status until generated.
- **Conflict is the test, not clean cascade** — the value of the contract shows up when the agent's generation contradicts an upstream constraint.
- **Upgrade is a feature** — when vibe outgrows itself, vibeloom recommends migration and the migration is a traceable operation, not a tool reset.
