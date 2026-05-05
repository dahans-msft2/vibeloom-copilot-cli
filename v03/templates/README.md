# v03/templates/

Generation-ready templates for v0.3 VibeLoom. The methodology + implementation docs (in `v03/`) define WHAT VibeLoom is and HOW it's built; this directory provides the concrete templates an agent uses to *generate* a working VibeLoom project from those specs.

## Directory layout

```
v03/templates/
├── README.md                          (this file)
├── artifacts/                         per-artifact templates (the contract stack itself)
│   ├── intent-specs/
│   │   ├── intent.md                  full-mode intent
│   │   ├── vibe-intent.md             vibe-mode compact intent
│   │   └── defaults.md                repo-wide defaults + Tech Stack section per DDD layer
│   ├── product-specs/
│   │   ├── prd.md                     OBJ / KR / MET / FR / NFR
│   │   ├── usm.md                     EPIC / FLOW / STORY / ACC / MS
│   │   └── dm.md                      TERM / BC / AGG / ENT / VO / INV
│   ├── ux-specs/
│   │   └── ux.md                      VIEW / INT / UXC / MOCK
│   ├── system-specs/
│   │   ├── system.md                  EXT / TB / SNFR
│   │   ├── vibe-system.md             vibe compact system
│   │   ├── containers.md              CONT inventory
│   │   ├── container.md               per-container; layer field + deployment target
│   │   └── component.md               per-component; layer-aware bounded_context
│   ├── context/
│   │   ├── bdd.md                     SCN per Gherkin scenario
│   │   ├── decision-trace.md          single template for IDR / PDR / UDR / ADR / general
│   │   ├── root-config.md             AGENTS.md / CLAUDE.md at root
│   │   ├── container-config.md        per-container config
│   │   └── component-config.md        per-component config
│   └── validation-registry.md         project-level meta artifact
├── tasks/                             per-operation task templates (Inputs / Steps / Output / Constraints / Validation)
│   ├── init.md
│   ├── import.md
│   ├── generate-intent-specs.md
│   ├── generate-product-specs.md
│   ├── generate-product-specs-from-ux.md
│   ├── generate-ux-specs.md
│   ├── generate-system-specs.md
│   ├── generate-context.md
│   ├── generate-code-component.md     leaf subagent task
│   ├── eval.md
│   ├── review.md
│   ├── reconcile.md
│   ├── approve.md
│   └── status.md
└── skill/
    ├── SKILL.md                       the loaded-by-Claude-Code/Codex skill manifest
    ├── subagent-prompt.md             body shape wrapping the subagent task header
    └── references/
        ├── artifacts.md               artifact layout, frontmatter, ID schema, derivation rules
        ├── eval.md                    verification ladder + heuristic dimensions
        ├── modes.md                   per-mode behavior (vibe / pm / dev / ux / expert)
        ├── operations.md              per-operation quick reference
        ├── runtime.md                 dispatch plan / wave assembly / parallel semantics / subagent task header
        └── troubleshooting.md         failure modes + recovery
```

## How an agent uses these templates

1. **Skill loads `skill/SKILL.md`** automatically when Claude Code or Codex sees `/vibeloom` or `$vibeloom`. The skill orchestrates everything else.
2. **Skill loads relevant `skill/references/*.md`** on demand per operation (e.g. `runtime.md` for `generate`, `eval.md` for `eval`/`review`).
3. **Skill loads the relevant `tasks/*.md`** for the invoked operation (one task template per operation).
4. **Skill materializes `artifacts/*.md`** when generating new artifacts (one artifact template per file generated).
5. **Subagents receive `skill/subagent-prompt.md`** wrapped around their task header from the dispatch plan.

Authoritative sources (the methodology + implementation specs) live one level up at `../vibeloom-methodology.md` and `../vibeloom-implementation.md`. If a template here disagrees with those specs, the specs win.

## Worked example with real content

For an end-to-end demonstration that the templates produce real, usable artifacts, see [`../examples/greenfield-note-search.md`](../examples/greenfield-note-search.md). It walks through a full vibe-mode session and an upgrade to pm mode, with embedded `intent.md`, `defaults.md`, `system.md`, `container.md` content showing what the templates materialize into.

## Quality conventions enforced across templates

- No count words in headings or sentence-leading positions ("Three forms", "Five modes", etc.). Counts change; copy shouldn't bake them in.
- Layer-aware constraints in container.md (`layer` field) and component.md (`bounded_context` empty for non-domain components).
- Tech Stack section in `defaults.md` organized per DDD layer (presentation / application / domain / infrastructure).
- Decision traces classified by `record_type` (IDR / PDR / UDR / ADR / general); single template, materialized per record into `decisions/<record_type>/<RECORD>-<NNNN>-<slug>.md`.
- No `context/decisions/` folder — decisions live exclusively in the `decision` trace family with a `load_bearing` flag.
- All trace schemas designed for future graph promotion (see roadmap CGKG-B).

## Versioning

Templates follow the v0.3 spec exactly. When the methodology or implementation changes (in a v0.3.x or v0.4 release), templates here update in lockstep. The skill's `template_version` field on every dispatched task records which template version was used, for reproducibility.
