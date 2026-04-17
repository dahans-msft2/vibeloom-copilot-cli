"""VibeLoom Engine CLI.

Exposes the engine's deterministic operations to the skill (or a user) via a
small argparse-driven CLI. All commands accept --repo (default: cwd) and emit
JSON or human-readable output.

Subcommands:
  parse           — discover + parse all artifacts; print as JSON
  graph           — build + persist the graph cache
  eval            — run structural eval on a target; print findings
  affected        — compute the affected set from changed item IDs
  staleness       — detect stale artifacts
  status          — emit a status snapshot and persist
  detect-edits    — detect direct edits on approved contract artifacts
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vibeloom_engine import __version__
from vibeloom_engine.affected import compute_affected_set
from vibeloom_engine.cache import load_graph, save_graph, save_status
from vibeloom_engine.eval_ import eval_graph, eval_target
from vibeloom_engine.graph import build_graph
from vibeloom_engine.indexes import build_indexes
from vibeloom_engine.parser import parse_repo_path
from vibeloom_engine.schema import Finding
from vibeloom_engine.staleness import compute_stale, detect_direct_edits
from vibeloom_engine.status import compute_status


def _findings_to_dicts(findings: list[Finding]) -> list[dict]:
    return [
        {
            "severity": f.severity,
            "artifact_id": f.artifact_id,
            "check": f.check,
            "message": f.message,
        }
        for f in findings
    ]


def _resolve_repo(args: argparse.Namespace) -> Path:
    return Path(args.repo).resolve()


def _cmd_parse(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    payload = [a.to_dict() for a in artifacts]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_graph(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    prior = load_graph(repo)
    graph = build_graph(artifacts, prior=prior)
    indexes = build_indexes(graph)
    path = save_graph(graph, repo)
    payload = {
        "saved": str(path.relative_to(repo)),
        "artifacts": len(graph.artifacts),
        "items": len(graph.items),
        "edges": len(graph.edges),
        "indexes": {
            "interface_providers": len(indexes.interface_provider),
            "dependency_targets": len(indexes.dependency_target),
            "write_scopes": len(indexes.write_scope),
            "context_scopes": len(indexes.context_relevance),
            "scope_summaries": len(indexes.scope_summary),
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_eval(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    prior = load_graph(repo)
    graph = build_graph(artifacts, prior=prior)
    if args.target:
        findings = eval_target(graph, artifacts, args.target)
    else:
        findings = eval_graph(graph, artifacts)
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    payload = {
        "target": args.target or "(all)",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "findings": _findings_to_dicts(findings),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    # Exit non-zero if any errors were found.
    return 1 if errors else 0


def _cmd_affected(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    prior = load_graph(repo)
    graph = build_graph(artifacts, prior=prior)
    affected = compute_affected_set(graph, args.ids)
    print(json.dumps(affected.to_dict(), indent=2, sort_keys=True))
    return 0


def _cmd_staleness(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    prior = load_graph(repo)
    graph = build_graph(artifacts, prior=prior)
    stale = compute_stale(graph)
    payload = [
        {
            "artifact_id": s.artifact_id,
            "reason": s.reason,
            "triggering_item_id": s.triggering_item_id,
        }
        for s in stale
    ]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_status(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    prior = load_graph(repo)
    graph = build_graph(artifacts, prior=prior)
    report = compute_status(graph, artifacts, repo)
    data = report.to_dict()
    save_status(data, repo)
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


def _cmd_detect_edits(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    prior = load_graph(repo)
    graph = build_graph(artifacts, prior=prior)
    edited = detect_direct_edits(graph)
    payload = [
        {
            "artifact_id": e.artifact_id,
            "path": e.path,
            "last_approved_mtime": e.last_approved_mtime,
            "current_mtime": e.current_mtime,
            "added_items": e.added_items,
            "removed_items": e.removed_items,
            "modified_items": e.modified_items,
        }
        for e in edited
    ]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="vibeloom-engine",
        description="VibeLoom v2 engine: parsing, graph, affected-set, staleness, eval, status.",
    )
    p.add_argument("--version", action="version", version=f"vibeloom-engine {__version__}")
    p.add_argument("--repo", default=".", help="Repo root (default: cwd)")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("parse", help="Parse all artifacts in the repo; emit JSON.")

    graph = sub.add_parser("graph", help="Build + persist the graph cache.")
    graph.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild even if the cache exists (current v0.1: always rebuilds).",
    )

    ev = sub.add_parser("eval", help="Run structural eval on a target or the whole graph.")
    ev.add_argument(
        "--target",
        choices=["intent-specs", "product-specs", "system-specs", "context", "code"],
        help="Limit eval to a target tier/layer. Omit to eval the whole graph.",
    )

    aff = sub.add_parser("affected", help="Compute the affected set from changed item IDs.")
    aff.add_argument("--ids", nargs="+", required=True, help="Changed item IDs (e.g., FR-0001 STORY-0003).")

    sub.add_parser("staleness", help="Detect stale artifacts (approved-basis mismatch).")
    sub.add_parser("status", help="Emit a status snapshot; persist to .vibeloom/state/status.json.")
    sub.add_parser(
        "detect-edits",
        help="Detect direct edits on approved contract artifacts (mtime fast-path, per-item hash confirmation).",
    )

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    dispatch = {
        "parse": _cmd_parse,
        "graph": _cmd_graph,
        "eval": _cmd_eval,
        "affected": _cmd_affected,
        "staleness": _cmd_staleness,
        "status": _cmd_status,
        "detect-edits": _cmd_detect_edits,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
