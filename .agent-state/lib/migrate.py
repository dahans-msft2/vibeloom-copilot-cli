"""
.agent-state/lib/migrate.py — one-shot JSON -> SQLite migrator.

Scans .agent-state/T-*.json (legacy per-task files), inserts them into state.db,
and moves the originals to .agent-state/archive/. Idempotent: re-runs skip tasks
that already exist in the DB.

Usage:
    py .agent-state/lib/migrate.py            # dry run, show plan
    py .agent-state/lib/migrate.py --apply    # actually migrate + archive
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state  # noqa: E402

ROOT = state.ROOT
ARCHIVE = ROOT / "archive"


def _iter_legacy_files() -> list[Path]:
    return sorted(p for p in ROOT.glob("T-*.json") if p.is_file())


def _migrate_one(conn, path: Path, *, apply: bool) -> str:
    raw = json.loads(path.read_text())
    task_id = raw["taskId"]
    existing = conn.execute("SELECT 1 FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
    if existing:
        return f"skip   {task_id}  (already in DB)"
    if not apply:
        return f"would  {task_id}  ({raw.get('status', '?')})"

    state.create_task(
        conn,
        task_id=task_id,
        goal=raw["goal"],
        branch=raw.get("branch", "develop"),
        source_docs=raw.get("sourceDocs", []),
    )
    state.set_task_status(conn, task_id, raw["status"])
    plan = raw.get("plan") or {}
    if plan.get("summary"):
        state.set_plan_summary(conn, task_id, plan["summary"])
    for sub in plan.get("subtasks", []):
        state.add_subtask(
            conn,
            task_id=task_id,
            st_id=sub["id"],
            owner=sub["owner"],
            description=sub["description"],
            acceptance=sub.get("acceptanceCriteria", []),
            depends_on=sub.get("dependsOn", []),
        )
        if sub.get("status") and sub["status"] != "todo":
            state.set_subtask_status(conn, task_id, sub["id"], sub["status"])
    for h in raw.get("history", []):
        conn.execute(
            "INSERT INTO history (task_id, at, agent, event, details, attempts) VALUES (?, ?, ?, ?, ?, ?)",
            (
                task_id, h["at"], h["agent"], h["event"],
                h.get("details"),
                json.dumps(h["attempts"]) if h.get("attempts") else None,
            ),
        )
    if raw.get("blocker"):
        b = raw["blocker"]
        state.set_blocker(
            conn,
            task_id,
            category=b["category"],
            raised_by=b["raisedBy"],
            summary=b["summary"],
            need_from_human=b["needFromHuman"],
            suspected_files=b.get("suspectedFiles"),
            acceptance_criteria=b.get("acceptanceCriteria"),
            issue_url=b.get("issueUrl"),
            issue_number=b.get("issueNumber"),
        )
        state.set_task_status(conn, task_id, raw["status"])
    if raw.get("cursor"):
        c = raw["cursor"]
        state.set_cursor(conn, task_id, c.get("subtaskId"), c.get("note"))
    if raw.get("artifacts"):
        a = raw["artifacts"]
        state.set_artifacts(conn, task_id, pr_url=a.get("prUrl"), commit_shas=a.get("commitShas"))

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(ARCHIVE / path.name))
    return f"OK     {task_id}  -> archive/{path.name}"


def main() -> int:
    p = argparse.ArgumentParser(description="Migrate legacy .agent-state/T-*.json into state.db.")
    p.add_argument("--apply", action="store_true", help="actually migrate (default: dry run)")
    args = p.parse_args()

    files = _iter_legacy_files()
    if not files:
        print("no legacy T-*.json files in .agent-state/")
        return 0

    conn = state.connect()
    try:
        for f in files:
            print(_migrate_one(conn, f, apply=args.apply))
    finally:
        conn.close()

    if not args.apply:
        print(f"\nDry run. Re-run with --apply to migrate {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
