# VibeLoom Engine

Deterministic substrate for VibeLoom v2. The engine parses contract and context artifacts, builds the context graph, computes affected sets and staleness, runs structural eval, and emits status snapshots. The VibeLoom skill invokes the engine for all deterministic work; the engine does not make semantic judgments.

Authoritative specification: [`vibeloom-implementation.md`](../vibeloom-implementation.md). This package implements the engine responsibilities defined there.

## Install

**Zero-install.** Python 3.10+ is the only requirement — no pip install, no dependencies. The engine is pure Python.

The skill invokes the engine via `python -m`:

```bash
PYTHONPATH=/path/to/v02/engine python3 -m vibeloom_engine --version
# vibeloom-engine 0.2.0
```

If you want the `vibeloom-engine` command on your `PATH` for direct use (optional), install it:

```bash
cd v02/engine
pip install -e .
```

## CLI

The engine exposes a small CLI. All commands default `--repo` to the current working directory.

```bash
# (If installed — otherwise prefix each with `PYTHONPATH=.../v02/engine python3 -m vibeloom_engine ...`)

# Parse all artifacts in a repo and print the parsed inventory as JSON
vibeloom-engine parse --repo /path/to/repo

# Build or rebuild the context graph cache (.vibeloom/state/context-graph.json)
vibeloom-engine graph --repo /path/to/repo [--rebuild]

# Run structural eval on a target
vibeloom-engine eval --repo /path/to/repo --target <intent-specs|product-specs|system-specs|context|code>

# Compute the affected set from one or more changed item IDs
vibeloom-engine affected --repo /path/to/repo --ids FR-0001 STORY-0003

# Detect stale artifacts (approved-basis mismatch)
vibeloom-engine staleness --repo /path/to/repo

# Emit a status snapshot as JSON (and persist to .vibeloom/state/status.json)
vibeloom-engine status --repo /path/to/repo [--scope <scope-filter>]

# Detect direct edits on approved contract artifacts (mtime fast-path, per-item hash confirmation)
vibeloom-engine detect-edits --repo /path/to/repo
```

## Responsibilities (what this engine does)

From `vibeloom-implementation.md`:

- parsing artifacts and frontmatter
- assigning and validating stable IDs
- validating artifact schemas and required fields
- building and querying the context graph
- computing affected sets and staleness

The engine does **not** decide product meaning, semantic intent, or approval outcomes. Template materialization is skill-invoked subagent work. Status reports are skill-composed views that query the engine.

## Package layout

```
vibeloom_engine/
  __init__.py
  __main__.py     # python -m vibeloom_engine
  cli.py          # CLI entrypoint
  ids.py          # Short-ID prefix families and ID validation
  models.py       # Artifact, Item, Edge, Graph dataclasses
  io_.py          # Filesystem walker, artifact discovery, mtime
  parser.py       # Frontmatter + body parser (tables, ledger records)
  schema.py       # Per-artifact-type schema validation
  graph.py        # Context graph builder and queries
  indexes.py      # Dispatch-support indexes
  affected.py     # Forward-walk affected-set computation
  staleness.py    # Approved-basis mismatch detection
  eval_.py        # Structural eval checks
  status.py       # Status report composer
  cache.py        # JSON persistence to .vibeloom/state/
```

## Testing

`pytest` is the only dev dependency. Install it directly, or use a venv:

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
```

Smoke tests use small fixture repos under `tests/fixtures/`.

## Versioning

The engine is versioned independently of the methodology and implementation docs. The current engine targets the v2 stabilized methodology + implementation committed on `main`.
