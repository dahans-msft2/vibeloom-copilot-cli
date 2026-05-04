# Example: UX-led design (`ux` mode)

A designer hands the team eight Figma mockups for a redesigned checkout flow before the PM has written any requirements. In a traditional pipeline, the designer's work would sit in Figma until requirements caught up. In codæ, the mockups are first-class evidence and can drive product-spec generation. This example uses `ux` mode (methodology §5.3), which makes the designer the primary contract author with the PM as peer reviewer.

## 0. Bootstrap in ux mode

```text
$ vibeloom init --mode ux
✓ Created intent.md (draft) and ux-specs/ folder
✓ ux-specs/mockups/ ready for designer-supplied snapshots
→ Designer: drop mockups in ux-specs/mockups/, then `vibeloom review intent-specs`
```

## 1. Mockup ingestion

```text
$ vibeloom mockup add ux-specs/mockups/*.png \
    --source figma://team/checkout-redesign-v2
✓ Created 8 MOCK records: MOCK-0001..MOCK-0008
ℹ Each mockup is now evidence; no contract truth yet.
```

Each `MOCK-####` record carries the snapshot, the Figma link, and notes (extracted from the file or added by the user):

```yaml
id: MOCK-0003
source: figma://team/checkout-redesign-v2/empty-cart
snapshot: ux-specs/mockups/03-empty-cart.png
notes: |
  Shows empty-cart state. Includes:
  - friendly empty-state copy
  - disabled checkout CTA
  - sign-in prompt for returning users
  - link to "browse products"
evidence_for: []
```

`evidence_for` is empty initially — the link to IDed items happens when those items get generated.

## 2. Product-specs derived from UX

In `ux` mode, the designer writes ux-specs first; product-specs are generated *from* approved intent + ux evidence via the `generate-product-specs-from-ux` task variant.

```text
$ vibeloom approve ux-specs
✓ ux-specs approved (UXC-0001..UXC-0014, VIEW-0001..VIEW-0008, INT-0001..INT-0017).

$ vibeloom generate product-specs --from ux
ℹ Running task template: generate-product-specs-from-ux v0.3.1
✓ Drafted prd.md (objectives, requirements derived from ux evidence)
✓ Drafted usm.md (epics, flows, stories — flow shapes inferred from VIEW + INT)
✓ Drafted dm.md (terms, bounded contexts, invariants — entities inferred from mockup labels + states)
✓ Backlinked MOCK-0001..MOCK-0008 to derived items.
→ Next: PM peer review via `vibeloom review product-specs`
```

The agent extracts implicit obligations from the mockups. For `MOCK-0003`:

```yaml
extracted_from: MOCK-0003
proposed_items:
  - kind: STORY
    label: "Returning user with empty cart can sign in to restore last cart"
  - kind: VIEW
    label: "Empty cart state with sign-in prompt"
  - kind: ACC
    label: "Given empty cart and recognized user, when viewing cart, sign-in prompt is shown"
  - kind: UXC
    label: "Empty-state copy is friendly and action-oriented (no error tone)"
  - kind: INT
    label: "Sign-in CTA opens modal without leaving cart context"
```

Some of these are clearly product (the sign-in-restores-last-cart story is a real product decision); others are clearly UX (the friendly tone constraint). The co-synthesis splits them into `prd.md`/`usm.md` and `ux.md` while preserving the link to `MOCK-0003`.

## 3. PM peer review of generated product-specs

The PM is now the peer reviewer of an artifact the designer effectively authored (through mockups). The review packet shows ux-evidence backing for each derived requirement — so the PM can ask "is this what we actually want?" with the visual context attached.

```yaml
packet_type: review
target: product-specs
basis: approved intent-specs + approved ux-specs + 8 MOCK records
findings:
  blocking: []
  advisory:
    - finding_id: FIND-0011
      summary: "Sign-in restores last cart — implies persistent cart storage.
                No upstream capability for persistent carts. Add CAP, or remove story."
    - finding_id: FIND-0012
      summary: "MOCK-0006 (payment-failed state) implies retry-with-different-method;
                no acceptance criterion captures this. Recommend new ACC."
mockup_coverage:
  fully_extracted: [MOCK-0001, MOCK-0002, MOCK-0004, MOCK-0005, MOCK-0007, MOCK-0008]
  partial: [MOCK-0003 (sign-in prompt under-specified), MOCK-0006 (retry under-specified)]
recommendation: address_advisory_then_approve
```

The PM reviews. The first finding is a real product decision (do we want persistent carts? yes), so they add `CAP-0009` for persistent carts and accept the story. The second finding gets a new `ACC-0024`. They approve the result.

## 4. System and code follow

System-specs derive from the approved product + UX truth. The checkout container ends up with a `cart-persistence` component that didn't exist before, traced back to the sign-in flow that came from `MOCK-0003`.

Code generation produces the components. Code-sync traces back to the `VIEW`, `INT`, `STORY`, `ACC`, and `UXC` items, which themselves trace back to the mockups.

## What this example illustrates

- **`ux` mode makes the designer the primary author.** Same artifacts, different primary author. The PM becomes a peer reviewer of designer-driven product-specs rather than the originator.
- **Mockups are evidence, not normative truth.** The designer's intent shapes generation; the IDed items are what get approved.
- **Mockup-derived items get traceable lineage.** Six months later, a developer asking "why does the empty-cart state have this sign-in prompt?" can trace it back to `MOCK-0003` and the original Figma link.
- **The agent's interpretation is reviewable.** The "fully extracted" / "partial" distinction in the packet lets the PM see where the agent might have missed something visible in a mockup.
- **The mirror works both ways.** A team can switch between `pm` and `ux` modes per project — design-led products get `ux`, product-led products get `pm`, the contract stack and agents are the same.
