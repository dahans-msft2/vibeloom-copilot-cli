# Profile Selection Guide

VibeLoom offers two profiles that determine the level of structure and the artifacts required.

## Lite Profile

**The default for most projects.** Single-module, streamlined artifact stack.

### Use Lite when ALL of these are true:

- [ ] The domain model has **≤ ~15 entities**
- [ ] All entities belong to **one cohesive domain** (no natural boundaries between subdomains)
- [ ] The expected codebase is **≤ ~50 files**
- [ ] **One developer or agent** will work on it at a time
- [ ] No **independently deployable components** needed

### What's different in Lite:

| Aspect | Lite behavior |
|--------|-------------|
| USM | Inlined as a section in prd.md (not a separate file) |
| Modules | None — the whole app is one unit |
| Module specs | Not generated |
| Interface contracts | Not needed |
| AGENTS.md | Single root file |
| Approval gates | 2: intent → product specs batch → tech specs |

### Lite file structure:
```
project/
├── intent.md
├── prd.md          # includes USM section
├── dm.md
├── spec.md
├── AGENTS.md
├── src/
├── tests/
└── .vibeloom/state.md
```

---

## Full Profile

**For complex systems with natural domain boundaries.** Multiple modules with explicit interface contracts.

### Use Full when ANY of these are true:

- [ ] The domain model has **natural bounded context boundaries** (e.g., "billing" vs "scheduling" vs "inventory")
- [ ] **Multiple agents or developers** will work in parallel
- [ ] The codebase will exceed **~50 files or ~10K LOC**
- [ ] **Independent deployment** of subsystems is needed
- [ ] Different parts of the system have **different tech stacks**

### What's different in Full:

| Aspect | Full behavior |
|--------|-------------|
| USM | Separate usm.md file with full epic structure |
| Modules | Per bounded context, each in its own directory |
| Module specs | Each module has its own spec.md and AGENTS.md |
| Interface contracts | Required: exports, imports, shared types, dependency DAG |
| AGENTS.md | Root + per-module |
| Approval gates | 3: intent → product specs batch → root spec + module specs |

### Full file structure:
```
project/
├── intent.md
├── prd.md
├── usm.md
├── dm.md
├── spec.md
├── AGENTS.md
├── modules/
│   ├── mod-{name}/
│   │   ├── spec.md
│   │   ├── AGENTS.md
│   │   ├── src/
│   │   └── tests/
│   └── shared/types/
└── .vibeloom/state.md
```

---

## How the Agent Selects a Profile

After product specs (prd + dm) are approved, the Agent analyzes dm.md:

1. **Count bounded contexts.** If dm.md defines multiple BCs → **Full**.
2. **Count entities.** If >15 entities even in a single BC → likely **Full** (suggests hidden complexity).
3. **Check for natural boundaries.** If entities cluster into groups with few cross-group relationships → **Full**.
4. **Check parallelism need.** If the user mentioned parallel development or multiple agents → **Full**.
5. **Default to Lite** if none of the above triggers.

The Agent proposes the profile with its reasoning. **The human always has the final say** — they can override in either direction.

---

## Upgrading from Lite to Full

If a project grows beyond Lite's scope:

1. Extract the USM section from prd.md into a separate usm.md
2. Identify bounded context boundaries in dm.md
3. Add module decomposition to spec.md
4. Create module directories with per-module spec.md and AGENTS.md
5. Define interface contracts between modules
6. Run `/vibeloom eval` to verify everything is consistent

This is a manual process (guided by the Agent) because it involves architectural decisions.

---

## Downgrading from Full to Lite

Rarely needed, but possible:

1. Merge module specs back into root spec.md
2. Merge usm.md back into prd.md as a section
3. Remove module directories (move code to root src/)
4. Remove interface contracts from spec.md
5. Update `.vibeloom/state.md` profile to `lite`
