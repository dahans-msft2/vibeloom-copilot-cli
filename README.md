# VibeLoom

**Contract-driven governance for long-lived AI-coded projects.** VibeLoom generates a tiered stack of specifications (`intent-specs` → `product-specs` → `system-specs` → `context` → `code`), keeps every tier aligned with the approved tier above, and detects drift structurally, lifecycle-wise, and semantically as the project evolves. The user keeps approval authority at configurable gates; subagents do the scoped work in parallel waves.

🌐 Website: [**vibeloom.ai**](https://vibeloom.ai) · Methodology: [vibeloom.ai/methodology](https://vibeloom.ai/methodology) · Implementation: [vibeloom.ai/implementation](https://vibeloom.ai/implementation)

## What's in this repo

| Path | Status | Purpose |
| --- | --- | --- |
| [`v02/`](v02/) | **Active** | Current VibeLoom methodology, skill, artifact templates, and the deterministic `vibeloom-engine` Python substrate |
| [`v01/`](v01/) | Archived | Earlier skill-only package; kept runnable but no longer the active methodology |
| [`site/`](site/) | Active | Public website source for `vibeloom.ai` (Cloudflare Workers static assets) |

Everything new lives in `v02/`:

- **[v02/SKILL.md](v02/SKILL.md)** — the skill file Claude Code and Codex load (operation routing, guardrails, response shape)
- **[v02/vibeloom-methodology.md](v02/vibeloom-methodology.md)** — authoritative WHY (tiers, modes, operations, approval model, drift, eval framework)
- **[v02/vibeloom-implementation.md](v02/vibeloom-implementation.md)** — authoritative HOW (artifact layout, metadata, stable IDs, subagent dispatch, graph cache, snapshot lifecycle)
- **[v02/references/](v02/references/)** — load-on-demand skill guides (operations, modes, runtime, artifacts, eval prompts, troubleshooting)
- **[v02/assets/](v02/assets/)** — 17 artifact templates (intent, defaults, prd, usm, dm, system, containers, container, component, pdr, adr, bdd, configs)
- **[v02/engine/](v02/engine/)** — deterministic Python engine (`vibeloom-engine` 0.2.0): parser, graph, hash-based drift detection, structural eval

## Quick start

```bash
# Clone — no install, no dependencies
git clone https://github.com/ilya-baimetov/vibeloom
cd vibeloom

# Verify the engine runs (Python 3.10+ is the only requirement)
PYTHONPATH=v02/engine python3 -m vibeloom_engine --version
# vibeloom-engine 0.2.0

# Open a project directory in Claude Code or Codex
# The v02/ skill is loaded automatically; run:
/vibeloom init --mode pm     # or vibe | dev | expert
```

The engine is pure Python — no `pip install` needed. The skill invokes it via `python -m` using the path to `v02/engine`.

See [`v02/README.md`](v02/README.md) for a deeper walkthrough and [vibeloom.ai/implementation](https://vibeloom.ai/implementation) for how the skill + engine fit together.

## What's new in v2

- **Five-tier contract stack** — `intent-specs` → `product-specs` → `system-specs` → `context` → `code`, with typed `derives_from` edges forming a DAG between stable short IDs
- **Four modes** — `vibe` (single user gate), `pm` (product-focused), `dev` (dev-focused), `expert` (full gates, nothing delegated)
- **Eight operations** — `init`, `import`, `generate`, `eval`, `review`, `reconcile`, `approve`, `status`
- **Deterministic engine** — `vibeloom-engine` handles parsing, graph construction, 9 structural eval checks, and hash-based drift detection; agent handles semantic judgment
- **Three-form drift model** — structural (upstream changed), lifecycle (approved artifact directly edited), semantic (meaning shifted); each with its own detection mechanism
- **Approved-state snapshots** — per-artifact mtime + per-item SHA-256 canonical hashes, captured at approval and preserved across rebuilds; enables precise direct-edit detection and node-level staleness

## Deployment

The public site at `vibeloom.ai` is deployed via Cloudflare Workers' GitHub integration. Pushes to `main` that touch `site/` are deployed automatically — no CI workflow is required.

## License

MIT.
