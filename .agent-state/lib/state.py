"""
.agent-state/lib/state.py — SQLite helper for the agent team.

Single file. Stdlib only (sqlite3, json, argparse, pathlib, datetime).
All agents read and write task state through these functions.
No ORM, no migrations framework — KISS.

Bootstrap: import state then call state.connect() — it auto-creates the DB
and schema if missing. WAL mode is enabled for concurrent writes.

CLI mode for quick inspection:
    py -m lib.state list                         # list all tasks
    py -m lib.state list --status in-progress
    py -m lib.state show T-260516-01             # full task as JSON
    py -m lib.state export T-260516-01           # write audit/<task>.json
    py -m lib.state next-id                      # mint next T-YYMMDD-NN
    py -m lib.state schema                       # print embedded DDL
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "state.db"
AUDIT_DIR = ROOT / "audit"
SCHEMA_FILE = ROOT / "schema.sql"

SCHEMA_VERSION = 1

_DDL = """
CREATE TABLE IF NOT EXISTS tasks (
  task_id TEXT PRIMARY KEY,
  status TEXT NOT NULL,
  goal TEXT NOT NULL,
  branch TEXT NOT NULL DEFAULT 'develop',
  vibeloom_op TEXT,
  vibeloom_tier TEXT,
  vibeloom_mode TEXT,
  plan_summary TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_vibeloom_op ON tasks(vibeloom_op);

CREATE TABLE IF NOT EXISTS source_docs (
  task_id TEXT NOT NULL,
  path TEXT NOT NULL,
  PRIMARY KEY (task_id, path),
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS subtasks (
  task_id TEXT NOT NULL,
  st_id TEXT NOT NULL,
  owner TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL,
  wave INTEGER,
  scope TEXT,
  PRIMARY KEY (task_id, st_id),
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_subtasks_status ON subtasks(task_id, status);
CREATE INDEX IF NOT EXISTS idx_subtasks_wave ON subtasks(task_id, wave);

CREATE TABLE IF NOT EXISTS subtask_deps (
  task_id TEXT NOT NULL,
  st_id TEXT NOT NULL,
  depends_on TEXT NOT NULL,
  PRIMARY KEY (task_id, st_id, depends_on),
  FOREIGN KEY (task_id, st_id) REFERENCES subtasks(task_id, st_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS acceptance_criteria (
  task_id TEXT NOT NULL,
  st_id TEXT NOT NULL,
  idx INTEGER NOT NULL,
  criterion TEXT NOT NULL,
  PRIMARY KEY (task_id, st_id, idx),
  FOREIGN KEY (task_id, st_id) REFERENCES subtasks(task_id, st_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task_id TEXT NOT NULL,
  at TEXT NOT NULL,
  agent TEXT NOT NULL,
  event TEXT NOT NULL,
  details TEXT,
  attempts TEXT,
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_history_task ON history(task_id, id);

CREATE TABLE IF NOT EXISTS blockers (
  task_id TEXT PRIMARY KEY,
  category TEXT NOT NULL,
  raised_by TEXT NOT NULL,
  summary TEXT NOT NULL,
  need_from_human TEXT NOT NULL,
  suspected_files TEXT,
  acceptance_criteria TEXT,
  issue_url TEXT,
  issue_number INTEGER,
  opened_at TEXT NOT NULL,
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cursors (
  task_id TEXT PRIMARY KEY,
  subtask_id TEXT,
  note TEXT,
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS artifacts (
  task_id TEXT PRIMARY KEY,
  pr_url TEXT,
  commit_shas TEXT,
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    current = conn.execute("PRAGMA user_version").fetchone()[0]
    if current == 0:
        conn.executescript(_DDL)
        conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
    elif current != SCHEMA_VERSION:
        raise RuntimeError(
            f"state.db user_version={current} but code expects {SCHEMA_VERSION}. "
            f"Add a migration to lib/state.py."
        )
    return conn


def mint_task_id(conn: sqlite3.Connection) -> str:
    today = datetime.now(timezone.utc).strftime("%y%m%d")
    prefix = f"T-{today}-"
    row = conn.execute(
        "SELECT task_id FROM tasks WHERE task_id LIKE ? ORDER BY task_id DESC LIMIT 1",
        (prefix + "%",),
    ).fetchone()
    next_n = int(row["task_id"].rsplit("-", 1)[1]) + 1 if row else 1
    return f"{prefix}{next_n:02d}"


def create_task(
    conn: sqlite3.Connection,
    task_id: str,
    goal: str,
    *,
    branch: str = "develop",
    source_docs: Iterable[str] = (),
    vibeloom_op: str | None = None,
    vibeloom_tier: str | None = None,
    vibeloom_mode: str | None = None,
) -> None:
    now = _now()
    conn.execute(
        """INSERT INTO tasks
           (task_id, status, goal, branch, vibeloom_op, vibeloom_tier, vibeloom_mode, created_at, updated_at)
           VALUES (?, 'planning', ?, ?, ?, ?, ?, ?, ?)""",
        (task_id, goal, branch, vibeloom_op, vibeloom_tier, vibeloom_mode, now, now),
    )
    for p in source_docs:
        conn.execute(
            "INSERT OR IGNORE INTO source_docs (task_id, path) VALUES (?, ?)",
            (task_id, p),
        )
    append_history(conn, task_id, agent="tech-lead", event="created task", details=goal[:200])


def set_task_status(conn: sqlite3.Connection, task_id: str, status: str) -> None:
    conn.execute(
        "UPDATE tasks SET status = ?, updated_at = ? WHERE task_id = ?",
        (status, _now(), task_id),
    )


def set_plan_summary(conn: sqlite3.Connection, task_id: str, summary: str) -> None:
    conn.execute(
        "UPDATE tasks SET plan_summary = ?, updated_at = ? WHERE task_id = ?",
        (summary, _now(), task_id),
    )


def add_subtask(
    conn: sqlite3.Connection,
    task_id: str,
    st_id: str,
    owner: str,
    description: str,
    acceptance: Iterable[str] = (),
    depends_on: Iterable[str] = (),
    wave: int | None = None,
    scope: str | None = None,
) -> None:
    conn.execute(
        """INSERT INTO subtasks (task_id, st_id, owner, description, status, wave, scope)
           VALUES (?, ?, ?, ?, 'todo', ?, ?)""",
        (task_id, st_id, owner, description, wave, scope),
    )
    for i, c in enumerate(acceptance):
        conn.execute(
            "INSERT INTO acceptance_criteria (task_id, st_id, idx, criterion) VALUES (?, ?, ?, ?)",
            (task_id, st_id, i, c),
        )
    for d in depends_on:
        conn.execute(
            "INSERT INTO subtask_deps (task_id, st_id, depends_on) VALUES (?, ?, ?)",
            (task_id, st_id, d),
        )


def set_subtask_status(conn: sqlite3.Connection, task_id: str, st_id: str, status: str) -> None:
    conn.execute(
        "UPDATE subtasks SET status = ? WHERE task_id = ? AND st_id = ?",
        (status, task_id, st_id),
    )
    conn.execute("UPDATE tasks SET updated_at = ? WHERE task_id = ?", (_now(), task_id))


def ready_subtasks(conn: sqlite3.Connection, task_id: str, wave: int | None = None) -> list[dict[str, Any]]:
    sql = (
        "SELECT s.* FROM subtasks s "
        "WHERE s.task_id = ? AND s.status = 'todo' "
        "AND NOT EXISTS ("
        "  SELECT 1 FROM subtask_deps d "
        "  JOIN subtasks dep ON dep.task_id = d.task_id AND dep.st_id = d.depends_on "
        "  WHERE d.task_id = s.task_id AND d.st_id = s.st_id AND dep.status != 'done'"
        ")"
    )
    params: list[Any] = [task_id]
    if wave is not None:
        sql += " AND s.wave = ?"
        params.append(wave)
    return [dict(r) for r in conn.execute(sql, params)]


def append_history(
    conn: sqlite3.Connection,
    task_id: str,
    *,
    agent: str,
    event: str,
    details: str | None = None,
    attempts: list[dict[str, Any]] | None = None,
) -> None:
    conn.execute(
        "INSERT INTO history (task_id, at, agent, event, details, attempts) VALUES (?, ?, ?, ?, ?, ?)",
        (task_id, _now(), agent, event, details, json.dumps(attempts) if attempts else None),
    )
    conn.execute("UPDATE tasks SET updated_at = ? WHERE task_id = ?", (_now(), task_id))


def set_blocker(
    conn: sqlite3.Connection,
    task_id: str,
    *,
    category: str,
    raised_by: str,
    summary: str,
    need_from_human: str,
    suspected_files: list[str] | None = None,
    acceptance_criteria: list[str] | None = None,
    issue_url: str | None = None,
    issue_number: int | None = None,
) -> None:
    conn.execute(
        """INSERT OR REPLACE INTO blockers
           (task_id, category, raised_by, summary, need_from_human,
            suspected_files, acceptance_criteria, issue_url, issue_number, opened_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            task_id, category, raised_by, summary, need_from_human,
            json.dumps(suspected_files) if suspected_files else None,
            json.dumps(acceptance_criteria) if acceptance_criteria else None,
            issue_url, issue_number, _now(),
        ),
    )
    set_task_status(conn, task_id, "paused-awaiting-human")


def clear_blocker(conn: sqlite3.Connection, task_id: str) -> None:
    conn.execute("DELETE FROM blockers WHERE task_id = ?", (task_id,))


def set_cursor(conn: sqlite3.Connection, task_id: str, subtask_id: str | None, note: str | None) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO cursors (task_id, subtask_id, note) VALUES (?, ?, ?)",
        (task_id, subtask_id, note),
    )


def set_artifacts(
    conn: sqlite3.Connection, task_id: str,
    *, pr_url: str | None = None, commit_shas: list[str] | None = None,
) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO artifacts (task_id, pr_url, commit_shas) VALUES (?, ?, ?)",
        (task_id, pr_url, json.dumps(commit_shas) if commit_shas else None),
    )


def get_task(conn: sqlite3.Connection, task_id: str) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
    if row is None:
        return None
    task = dict(row)
    task["source_docs"] = [r["path"] for r in conn.execute(
        "SELECT path FROM source_docs WHERE task_id = ? ORDER BY path", (task_id,)
    )]
    subtasks = []
    for s in conn.execute(
        "SELECT * FROM subtasks WHERE task_id = ? ORDER BY st_id", (task_id,)
    ):
        sd = dict(s)
        sd["acceptance_criteria"] = [r["criterion"] for r in conn.execute(
            "SELECT criterion FROM acceptance_criteria WHERE task_id = ? AND st_id = ? ORDER BY idx",
            (task_id, sd["st_id"]),
        )]
        sd["depends_on"] = [r["depends_on"] for r in conn.execute(
            "SELECT depends_on FROM subtask_deps WHERE task_id = ? AND st_id = ?",
            (task_id, sd["st_id"]),
        )]
        subtasks.append(sd)
    task["subtasks"] = subtasks
    task["history"] = [dict(r) for r in conn.execute(
        "SELECT at, agent, event, details, attempts FROM history WHERE task_id = ? ORDER BY id",
        (task_id,),
    )]
    for r in task["history"]:
        if r.get("attempts"):
            r["attempts"] = json.loads(r["attempts"])
    blocker = conn.execute("SELECT * FROM blockers WHERE task_id = ?", (task_id,)).fetchone()
    task["blocker"] = dict(blocker) if blocker else None
    if task["blocker"]:
        for k in ("suspected_files", "acceptance_criteria"):
            if task["blocker"].get(k):
                task["blocker"][k] = json.loads(task["blocker"][k])
    cursor = conn.execute("SELECT * FROM cursors WHERE task_id = ?", (task_id,)).fetchone()
    task["cursor"] = dict(cursor) if cursor else None
    artifacts = conn.execute("SELECT * FROM artifacts WHERE task_id = ?", (task_id,)).fetchone()
    task["artifacts"] = dict(artifacts) if artifacts else None
    if task["artifacts"] and task["artifacts"].get("commit_shas"):
        task["artifacts"]["commit_shas"] = json.loads(task["artifacts"]["commit_shas"])
    return task


def list_tasks(conn: sqlite3.Connection, *, status: str | None = None) -> list[dict[str, Any]]:
    if status:
        rows = conn.execute(
            "SELECT task_id, status, goal, vibeloom_op, vibeloom_tier, updated_at "
            "FROM tasks WHERE status = ? ORDER BY updated_at DESC", (status,),
        )
    else:
        rows = conn.execute(
            "SELECT task_id, status, goal, vibeloom_op, vibeloom_tier, updated_at "
            "FROM tasks ORDER BY updated_at DESC"
        )
    return [dict(r) for r in rows]


def export_task(conn: sqlite3.Connection, task_id: str, out_dir: Path | None = None) -> Path:
    task = get_task(conn, task_id)
    if task is None:
        raise KeyError(task_id)
    out = (out_dir or AUDIT_DIR) / f"{task_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(task, indent=2, ensure_ascii=False))
    return out


def _cli(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="agent-state", description="SQLite state helper for the agent team.")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="list tasks")
    pl.add_argument("--status")

    ps = sub.add_parser("show", help="dump one task as JSON")
    ps.add_argument("task_id")

    pe = sub.add_parser("export", help="export task to audit/<task-id>.json")
    pe.add_argument("task_id")

    sub.add_parser("next-id", help="mint next T-YYMMDD-NN for today")
    sub.add_parser("schema", help="print embedded DDL")

    args = p.parse_args(argv)

    if args.cmd == "schema":
        print(_DDL.strip())
        return 0

    conn = connect()
    try:
        if args.cmd == "list":
            for t in list_tasks(conn, status=args.status):
                print(f"{t['task_id']:>16}  {t['status']:<22}  "
                      f"{(t['vibeloom_op'] or '-'):<10}  "
                      f"{(t['vibeloom_tier'] or '-'):<15}  "
                      f"{t['updated_at']}  {t['goal'][:60]}")
        elif args.cmd == "show":
            task = get_task(conn, args.task_id)
            if task is None:
                print(f"no such task: {args.task_id}", file=sys.stderr)
                return 1
            print(json.dumps(task, indent=2, ensure_ascii=False))
        elif args.cmd == "export":
            out = export_task(conn, args.task_id)
            print(str(out))
        elif args.cmd == "next-id":
            print(mint_task_id(conn))
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
