# VibeLoom Engine

Deterministic substrate for VibeLoom v2. The engine parses contract and context artifacts, builds the context graph, computes affected sets and staleness, runs structural eval, and emits status snapshots. The VibeLoom skill invokes the engine for all deterministic work; the engine does not make semantic judgments.

Authoritative specification: [`vibeloom-implementation.md`](../vibeloom-implementation.md). This package implements the engine responsibilities defined there.

## Install

```bash
cd v02/engine
pip install -e .
```

Python 3.10+ required. The only runtime dependency is `pyyaml`.

## CLI

The engine exposes a small CLI. All commands are read-only except when an explicit writable target is given.

```bash
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

# Detect direct edits on approved contract artifacts (filesystem mtime comparison)
vibeloom-engine detect-edits --repo /path/to/repo
```

All commands default `--repo` to the current working directory.

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

```bash
pip install -e '.[dev]'
pytest
```

Smoke tests use small fixture repos under `tests/fixtures/`.

## Versioning

The engine is versioned independently of the methodology and implementation docs. v0.1 targets the stabilized methodology + implementation committed on `main`.
