"""VibeLoom engine CLI.

Each subcommand emits a command-specific JSON payload on stdout (no unified
envelope). Exit codes:
  0 — clean (advisories OK)
  1 — blocking findings (e.g. structural-rule violation)
  2 — engine error (invalid input, internal exception, malformed trace)

Subcommands (filled in as stages ship):
  parse           — discover + parse all artifacts
  graph           — build the graph; print summary
  eval            — structural eval (Stage 2)
  affected        — compute affected set (Stage 4)
  staleness       — compute staleness (Stage 4)
  detect-edits    — direct-edit detection (Stage 4)
  dispatch        — emit a dispatch plan (Stage 5)
  status          — six-category classification (Stage 6)
  decisions       — render per-record markdown (Stage 6)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vibeloom_engine import __version__


def _resolve_repo(args: argparse.Namespace) -> Path:
    return Path(args.repo).resolve()


def _emit(payload) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True))
    sys.stdout.write("\n")
    sys.stdout.flush()


def _err(payload) -> None:
    sys.stderr.write(json.dumps(payload, indent=2, sort_keys=True))
    sys.stderr.write("\n")
    sys.stderr.flush()


# ---------------------------------------------------------------------------
# parse / graph (Stage 1)
# ---------------------------------------------------------------------------


def _cmd_parse(args: argparse.Namespace) -> int:
    from vibeloom_engine.parser import parse_repo_path
    from vibeloom_engine.schema import validate_repo

    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    findings = validate_repo(artifacts)
    blocking = [f for f in findings if f.severity == "blocking"]
    payload = {
        "repo": str(repo),
        "artifact_count": len(artifacts),
        "artifacts": [a.to_dict() for a in artifacts],
        "schema_findings": [f.to_dict() for f in findings],
    }
    _emit(payload)
    return 1 if blocking else 0


def _cmd_graph(args: argparse.Namespace) -> int:
    from vibeloom_engine.cache import save_graph
    from vibeloom_engine.graph import build_graph, find_cycles
    from vibeloom_engine.parser import parse_repo_path

    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    graph = build_graph(artifacts)
    if args.save:
        save_graph(graph, repo)
    cycles = find_cycles(graph)
    payload = {
        "repo": str(repo),
        "artifact_count": len(graph.artifacts),
        "item_count": len(graph.items),
        "edge_count": len(graph.edges),
        "cycles": cycles,
        "saved": args.save,
    }
    _emit(payload)
    return 1 if cycles else 0


# ---------------------------------------------------------------------------
# eval (Stage 2)
# ---------------------------------------------------------------------------


def _cmd_eval(args: argparse.Namespace) -> int:
    from vibeloom_engine.eval_ import structural_eval
    from vibeloom_engine.graph import build_graph
    from vibeloom_engine.parser import parse_repo_path

    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    graph = build_graph(artifacts)
    findings = structural_eval(graph, artifacts, target=args.target)
    blocking = [f for f in findings if f.severity == "blocking"]
    advisory = [f for f in findings if f.severity == "advisory"]
    payload = {
        "target": args.target or "(all)",
        "blocking_count": len(blocking),
        "advisory_count": len(advisory),
        "findings": [f.to_dict() for f in findings],
        "errors": [],
    }
    _emit(payload)
    return 1 if blocking else 0


# ---------------------------------------------------------------------------
# affected / staleness / detect-edits (Stage 4)
# ---------------------------------------------------------------------------


def _cmd_affected(args: argparse.Namespace) -> int:
    from vibeloom_engine.affected import compute_affected_set
    from vibeloom_engine.graph import build_graph
    from vibeloom_engine.parser import parse_repo_path

    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    graph = build_graph(artifacts)
    affected = compute_affected_set(graph, args.ids)
    _emit(affected.to_dict())
    return 0


def _cmd_staleness(args: argparse.Namespace) -> int:
    from vibeloom_engine.graph import build_graph
    from vibeloom_engine.parser import parse_repo_path
    from vibeloom_engine.staleness import compute_staleness

    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    graph = build_graph(artifacts)
    stale = compute_staleness(repo, graph, artifacts)
    _emit({"stale": stale})
    return 0


def _cmd_detect_edits(args: argparse.Namespace) -> int:
    from vibeloom_engine.graph import build_graph
    from vibeloom_engine.parser import parse_repo_path
    from vibeloom_engine.staleness import detect_direct_edits

    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    graph = build_graph(artifacts)
    edits = detect_direct_edits(repo, graph, artifacts)
    _emit({"direct_edits": edits})
    return 0


# ---------------------------------------------------------------------------
# dispatch (Stage 5)
# ---------------------------------------------------------------------------


def _cmd_dispatch(args: argparse.Namespace) -> int:
    from vibeloom_engine.affected import compute_affected_set
    from vibeloom_engine.dispatch import dispatch_plan
    from vibeloom_engine.graph import build_graph
    from vibeloom_engine.parser import parse_repo_path

    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    graph = build_graph(artifacts)
    affected = compute_affected_set(graph, args.ids or [])
    plan = dispatch_plan(graph, affected, max_wave_size=args.max_wave_size)
    _emit(plan)
    return 0


# ---------------------------------------------------------------------------
# status (Stage 6)
# ---------------------------------------------------------------------------


def _cmd_status(args: argparse.Namespace) -> int:
    from vibeloom_engine.cache import save_status
    from vibeloom_engine.graph import build_graph
    from vibeloom_engine.parser import parse_repo_path
    from vibeloom_engine.status import compute_status

    repo = _resolve_repo(args)
    artifacts = parse_repo_path(repo)
    graph = build_graph(artifacts)
    report = compute_status(repo, graph, artifacts)
    save_status(report, repo)
    _emit(report)
    return 0


def _cmd_decisions_render(args: argparse.Namespace) -> int:
    from vibeloom_engine.decisions import render_decisions

    repo = _resolve_repo(args)
    rendered = render_decisions(repo)
    _emit({"rendered_files": rendered})
    return 0


# ---------------------------------------------------------------------------
# arg parsing
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="vibeloom-engine",
        description=(
            "VibeLoom v0.3 deterministic engine. Parsing, schema, graph, "
            "traces, dispatch, status. JSON on stdout; exit 0/1/2 per docs."
        ),
    )
    p.add_argument("--version", action="version", version=f"vibeloom-engine {__version__}")
    p.add_argument("--repo", default=".", help="Repo root (default: cwd)")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("parse", help="Parse all artifacts; emit JSON inventory + schema findings.")

    g = sub.add_parser("graph", help="Build the contract graph; emit summary.")
    g.add_argument("--save", action="store_true", help="Persist to .vibeloom/cache/contract-graph.json")

    ev = sub.add_parser("eval", help="Structural eval (decidable rung).")
    ev.add_argument(
        "--target",
        choices=["intent-specs", "product-specs", "ux-specs", "system-specs", "context"],
        default=None,
        help="Limit to a tier; omit for all.",
    )

    aff = sub.add_parser("affected", help="Compute affected set from changed item IDs.")
    aff.add_argument("--ids", nargs="+", required=True, help="Changed item IDs.")

    sub.add_parser("staleness", help="Compute staleness vs latest approval traces.")
    sub.add_parser("detect-edits", help="Detect direct edits on approved contract artifacts.")

    disp = sub.add_parser("dispatch", help="Emit a dispatch plan for the affected set.")
    disp.add_argument("--ids", nargs="+", default=None, help="Seed item IDs (else use whole repo affected set).")
    disp.add_argument("--max-wave-size", type=int, default=5, help="Concurrency cap per wave.")

    sub.add_parser("status", help="Six-category status classification + report.")

    dec = sub.add_parser("decisions", help="Decision-trace operations.")
    dec_sub = dec.add_subparsers(dest="dec_command", required=True)
    dec_sub.add_parser("render", help="Render per-record markdown from decisions.jsonl (idempotent).")

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        # argparse uses SystemExit(2) for errors — that matches our engine-error code.
        return int(e.code) if e.code is not None else 2

    dispatch_table = {
        "parse": _cmd_parse,
        "graph": _cmd_graph,
        "eval": _cmd_eval,
        "affected": _cmd_affected,
        "staleness": _cmd_staleness,
        "detect-edits": _cmd_detect_edits,
        "dispatch": _cmd_dispatch,
        "status": _cmd_status,
    }
    try:
        if args.command == "decisions":
            if args.dec_command == "render":
                return _cmd_decisions_render(args)
            _err({"error": f"unknown decisions subcommand: {args.dec_command}"})
            return 2
        return dispatch_table[args.command](args)
    except (FileNotFoundError, NotADirectoryError) as e:
        _err({"error": "file_not_found", "detail": str(e)})
        return 2
    except ValueError as e:
        _err({"error": "value_error", "detail": str(e)})
        return 2
    except RuntimeError as e:
        _err({"error": "runtime_error", "detail": str(e)})
        return 2
    # Unexpected exceptions propagate — that's a real engine bug, surface it
    # rather than swallowing into "engine error".


if __name__ == "__main__":
    sys.exit(main())
