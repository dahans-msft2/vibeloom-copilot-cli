# Getting started with vibeloom

This is the 30-minute on-ramp. If you're new to vibeloom (or to codæ), read this once, then point your agent at the repo and try it.

## Prerequisites

- **Python 3.10+** — the only system dependency.
- **Your favorite agent** — Claude Code or Codex are both supported (they pick up vibeloom as a Skill).
- Optional: a project to try this on. A throwaway prototype works for the vibe-mode walkthrough; an existing real codebase works for the brownfield import path (see [examples/brownfield-import.md](examples/brownfield-import.md)).

## Install

```bash
git clone https://github.com/ilya-baimetov/vibeloom.git
```

Then point your agent at the cloned directory as a Skill source. In Claude Code:

```text
> add vibeloom as a Skill source from /path/to/vibeloom/v03
```

Codex setup is the same shape — point its Skill loader at the same directory. No `pip install`, no runtime dependencies beyond Python.

## First 5 minutes — bootstrap a vibe project

In an empty directory (or a folder you want to seed):

```text
> /vibeloom init --mode vibe "a personal note-taking app with full-text search and tags"
```

vibeloom creates `intent.md`, `system.md` (compact), and `AGENTS.md`. It writes the one-line description into `intent.md` and asks you to expand. Open `intent.md` and add capabilities and constraints in plain English — that's the only real work this step requires.

```text
> /vibeloom approve intent-specs
```

This writes the first approval trace and unlocks downstream generation.

## Next 10 minutes — generate

```text
> /vibeloom generate
```

In vibe mode this auto-advances through the compact stack and into code. Expect output that looks roughly like:

```text
✓ generated system.md (compact: 3 components, 2 interfaces)
✓ generated AGENTS.md
✓ generated code (14 files across 3 components in 2 dispatch waves)
✓ all validation runners passed
ℹ status: current; 0 stale, 0 drifted, 0 uncovered
```

Look at what got generated. Ignore the engine's status report for a second — just open the files and skim them. The whole point of vibe mode is that a small system stays comprehensible.

## Next 10 minutes — read, ship, iterate

If the generated code looks roughly right:

```text
> /vibeloom status
```

Read the report. If it says `current` everywhere, you can ship. Run the code, see if it does what you wanted.

If you want to change something:

- **Change the intent** — edit `intent.md`, `approve` it again, `generate` again. The engine regenerates affected scopes.
- **Edit the code by hand** — ok, but on the next `status` you'll see `drifted` for whichever files you touched. Use `reconcile code` to either bring the code back in line with the contract or amend the contract to match what you wrote. Don't ignore drift.

## When vibe outgrows itself — upgrade

After a few weeks of iteration, vibeloom may surface:

```text
ℹ Vibe limits exceeded:
  - 12 components (vibe recommends ≤ 5)
  - 3 contributors (vibe recommends 1-2)
  - 4 reconciliations in last 30 days
→ Consider: vibeloom init --upgrade --mode <pm|dev|ux|expert>
```

This is the upgrade prompt. Pick a mode based on who's leading discovery on your team:

- **`pm`** — product-led. PM owns intent + product specs. Best for product-driven teams.
- **`dev`** — tech-led. Dev owns intent + system specs. Best for architecture-first work.
- **`ux`** — design-led. Designer owns intent + UX specs; PM is peer reviewer of generated product specs. Best for design-heavy products. See [examples/ux-led-design.md](examples/ux-led-design.md).
- **`expert`** — all approval gates explicit. Best for regulated systems or co-owned design.

Upgrade is one-way and produces an explicit migration trace. The compact stack expands into the full graph; existing code is import-analyzed against the freshly generated full contract. Plan ~1 hour for the first review pass after upgrade.

## I have an existing codebase — what then?

Use brownfield import:

```text
> /vibeloom import --mode <mode>
```

vibeloom scans the existing code, infers a candidate contract with confidence scores per item, and writes it as `draft`. You review top-down (intent → product → system) and approve. Existing code is then code-synced or reconciled against the approved contract. Plan a half-day to a day for the first import + review cycle on a 50K-LOC project. See [examples/brownfield-import.md](examples/brownfield-import.md) for a worked walkthrough.

## Where to next

- Read the [codæ manifesto](codæ-manifesto.html) for the case ("why does this exist?").
- Read [vibeloom — methodology](vibeloom-methodology.md) for the model (contract stack, modes, operations, status categories).
- Read [vibeloom — implementation](vibeloom-implementation.md) for the engine (skill + engine + validation runners; trace schemas; dispatch + parallel semantics).
- Browse [examples/](examples/) for greenfield, brownfield, UX-led, multi-component reconciliation, and parallel-dispatch scenarios.
- Read [vibeloom — comparison](vibeloom-comparison.html) if you want to know how this differs from Kiro, Spec Kit, BMAD.
- Skim the [roadmap](roadmap.md) for what's coming in v04 (dry-run, contract REPL, contract debugger, contract pattern library, DDD context maps, compliance mode, trace-derived learning).

## When NOT to use vibeloom

If your project is a throwaway prototype, a single-file utility, a weekend demo, or a hackathon submission — prompt-only generation is faster. The contract overhead pays back when the system has to survive past one development cycle and matters to more than one person. See manifesto §6 for the underlying argument.
