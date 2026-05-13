# vibeloom — file layout

This document defines the canonical file layout of the `vibeloom` repository. It is the reference the `vibeloom-dev` skill operates against.

**Status of versions.**
- `v01/`, `v02/`, `v03/` are **frozen** in a legacy layout. They are not described here.
- From **v04 onward**, every version directory conforms to the structure defined in §6.

---

## 1. Repo root

```
vibeloom/
├── README.md                          # project intro
├── roadmap.md                         # cross-version roadmap
├── file-layout.md                     # this spec
├── .gitignore
├── .git/  .github/  .claude/  .wrangler/
│
├── site/                              # production site (Cloudflare-deployed; §3)
├── vibeloom-dev/                      # dev skill (§4; design deferred)
├── reports/                           # gitignored, ephemeral build/review outputs (§5)
├── pitch-deck/                        # gitignored, version-agnostic marketing material
│
├── v01/  v02/  v03/                   # FROZEN — legacy layout, do not touch
└── v04/  v05/  ...                    # new layout per §6
```

---

## 2. Versioning model

At any moment:
- **One version is "current production"** — the site at `vibeloom.ai` serves its `site/public/`. This is indicated **only** by the target of the root `site/public/` symlink. There is no separate marker file.
- **Older shipped versions** are frozen and read-only.
- **One or more future in-progress versions** may exist as full or partial directories. They are not served until their `public/` becomes the symlink target.

Cutting over production from vNN to vNN+1:

```bash
ln -sfn ../vNN+1/site/public site/public
```

---

## 3. `site/` — production deployment

```
site/
├── wrangler.jsonc                     # name: "vibeloom"
├── README.md
├── og-image-source.html               # source for OG image generation
├── scripts/
│   └── render-og-image.cjs            # version-agnostic OG generator
└── public/                            # SYMLINK → ../vNN/site/public/ of current production
```

- A **single** Cloudflare project (`name: "vibeloom"`) deploys from this directory.
- No per-version Cloudflare project. Local preview of unflipped versions is via `npx http-server vNN/site/public`.
- Version-agnostic infrastructure (the OG generator, the source HTML it consumes, the wrangler config) lives here, not inside any `vNN/`.

**Symlink risk.** Cloudflare's project root is `site/`; a `site/public/` symlink resolves to a path outside that root. If Wrangler rejects this in production, the mitigation is to move `wrangler.jsonc` to the repo root, set Cloudflare project root to repo root, and point `assets.directory` at `./vNN/site/public` directly (no symlink; one-line edit on version bump). This must be verified with a test deploy.

---

## 4. `vibeloom-dev/` — the dev skill (design deferred)

Design is **deferred** to a forthcoming intent-spec. The following constraints are known:

**Owned content.**
- The build/review prompts that today live at `v03/`: `build-engine.md`, `build-skill.md`, `review-canon.md`, `review-site.md`, `review-skill.md`. These are **version-aware** — one prompt, version passed as argument.
- The template extractor `extract-templates.py` (unpacks `canon/vibeloom-templates.md` into individual files inside `skill/` to lighten context load).
- Version-specific validators that today live at `v03/site/scripts/` (e.g., `check_consistency.py`, `check_site.py`).

**Behavioral constraints.**
- vibeloom-dev **reviews and proposes only.** It writes reports and discussion artifacts. It does **not** edit canon/skill/site/examples files without explicit user approval.
- Cross-agent reviews: each adversarial review is a multi-agent pass. Both Claude and Codex run the same prompt and write to deterministic per-agent files; a consensus file is produced at the end. The skill auto-detects which agent is running. Cap at 3 rounds, then user manually reviews.

---

## 5. `reports/` — build/review outputs

```
reports/                                 # gitignored, ephemeral, overwrite-on-rerun
└── vNN/
    ├── review-canon/
    │   ├── claude.md                    # Claude's findings
    │   ├── codex.md                     # Codex's findings
    │   └── consensus.md                 # reconciled list, ACCEPT/REJECT/DEFER per finding
    ├── review-site/    (same shape)
    ├── review-skill/   (same shape)
    ├── build-engine/   (same shape)
    └── build-skill/    (same shape)
```

- All of `reports/` is gitignored.
- Reports are **ephemeral** — deleted after fixes are applied. The audit trail of fixes lives in git history of the artifacts themselves.
- Reruns **overwrite** the previous file for that (version, target, agent).

---

## 6. `vNN/` — per-version layout (v04 onward)

```
v04/
├── getting-started.md                  # version-specific onboarding
├── (small handful of other loose docs as needed — design notes, ADRs, migration guides)
│
├── canon/                              # the normative documents for this version (§6.1)
│   ├── codæ-manifesto.html             # HTML-authored, no MD source
│   ├── vibeloom-methodology.md
│   ├── vibeloom-implementation.md
│   └── vibeloom-templates.md           # canonical source for all template fenced blocks
│
├── site/                               # the published site for this version (§6.2)
│   ├── comparison-source.html          # build INPUT, not directly served
│   └── public/                         # the deployable static site
│       ├── index.html
│       ├── methodology.html
│       ├── implementation.html
│       ├── codæ-manifesto.html
│       ├── styles.css
│       └── ...
│
├── skill/                              # the skill bundle (§6.3)
│   ├── SKILL.md                        # extracted from canon
│   ├── subagent-prompt.md              # extracted
│   ├── references/                     # extracted: runtime, modes, eval, artifacts, operations, troubleshooting
│   ├── tasks/                          # extracted: init, import, generate-*, eval, review, reconcile, status, approve
│   ├── artifacts/                      # extracted, grouped by spec layer:
│   │   ├── intent-specs/                 vibe-intent.md, intent.md, defaults.md
│   │   ├── product-specs/                prd.md, usm.md, dm.md
│   │   ├── system-specs/                 vibe-system.md, system.md, container.md, containers.md, component.md
│   │   ├── context/                      root-config.md, container-config.md, component-config.md, bdd.md
│   │   └── ux-specs/                     ux.md
│   └── engine/                         # hand-authored Python package (§6.4)
│       ├── pyproject.toml              # name = "vibeloom-engine"; CLI = vibeloom-engine
│       ├── vibeloom_engine/            # = the importable Python module (folder name MUST equal module name)
│       │   ├── __init__.py
│       │   └── parser.py, dispatch.py, registry.py, eval_.py, ...   (~20 modules)
│       └── tests/
│
├── examples/                           # use-case walkthroughs in markdown
│   ├── brownfield-import.md
│   ├── greenfield-bootstrap.md
│   └── ...
│
└── dist/                               # release artifacts for this version
    ├── vibeloom-vN.M.0.tar.gz
    └── vibeloom-vN.M.0.tar.gz.sha256
```

### 6.1 `canon/`

- Filenames keep the verbose `vibeloom-` prefix so a downloaded or emailed file is self-identifying.
- `codæ-manifesto.html` is HTML-authored, with no MD source. It is design-heavy and primarily for human consumption. The other three canon docs are equally or more for machine processing.
- These four files are the **single normative source** for a version. Everything in `skill/` (except `engine/`) is derived from them by the template extractor.

### 6.2 `site/`

- `vNN/site/` contains only what is specific to this version's site: `public/` (the deploy target) and any build-input source files (e.g., `comparison-source.html`).
- It does **not** contain a `wrangler.jsonc` or generator scripts. Those are version-agnostic and live in root `site/`.

### 6.3 `skill/`

- `skill/` is the deliverable Claude/Codex skill bundle for this version. It is loaded by pointing the agent's skill loader at `vNN/skill/`.
- Everything in `skill/` **except `engine/`** is extracted from `canon/vibeloom-templates.md` by `extract-templates.py` (owned by vibeloom-dev). The destination root of the extractor is `vNN/skill/`.
- The fenced-block path tags inside `vibeloom-templates.md` are relative to `skill/`:
  - `template:SKILL.md` → `skill/SKILL.md`
  - `template:subagent-prompt.md` → `skill/subagent-prompt.md`
  - `template:references/X.md` → `skill/references/X.md`
  - `template:tasks/X.md` → `skill/tasks/X.md`
  - `template:artifacts/X/Y.md` → `skill/artifacts/X/Y.md`

### 6.4 `skill/engine/`

- The engine lives inside the skill because it ships with the skill.
- It keeps its own `pyproject.toml`. It remains a standalone, installable Python package (`pip install -e vNN/skill/engine`).
- The `vibeloom_engine/` subfolder is **required** — Python requires the folder name to equal the importable module name. Flattening would force a generic name (`engine`) that collides on `sys.path`, or break every `from vibeloom_engine.X import Y` statement in the codebase.
- The engine is **hand-authored**. `build-engine.md` (in vibeloom-dev) is a regeneration prompt for drift recovery, not the day-to-day path.

### 6.5 `dist/`

- `vNN/dist/` holds release tarballs for this version. Gitignored.
- New releases write here, not to a root-level `dist/`.

### 6.6 Top-level loose docs in `vNN/`

- `getting-started.md` is always present (version-specific onboarding).
- Other loose docs (design notes, ADRs, migration-from-prev.md, etc.) sit at `vNN/` root as needed. There is no dedicated `notes/` or `docs/` subfolder. If the count grows beyond a handful for any version, revisit and introduce a folder.

---

## 7. `.gitignore`

```
# Ephemeral build/review outputs (vibeloom-dev)
/reports/

# Version-agnostic marketing material (not tracked in repo)
/pitch-deck/

# Per-version release artifacts (rebuildable from source)
/v*/dist/
```

---

## 8. Cloudflare configuration

- **One** Cloudflare project: `vibeloom`. Its project root is `site/`; its asset directory is `./public` (which is a symlink, see §3).
- No per-version Cloudflare projects.
- If Wrangler rejects out-of-root symlinked assets, apply the mitigation in §3.

---

## 9. Cross-references between layers

- The skill loader is pointed at `vNN/skill/`.
- The skill imports the engine via `from vibeloom_engine.X import Y` — this works because `skill/engine/` is a proper Python package.
- The site has no runtime dependency on canon or skill — it is a static export. Build inputs that *derive* from canon (e.g., `comparison-source.html`) are version-scoped under `vNN/site/`.
- vibeloom-dev operates on a version by reading `vNN/canon/`, `vNN/skill/`, `vNN/site/`, `vNN/examples/`, and writing to `reports/vNN/...`.
