# `.agent-state/` — Resumable Task State (SQLite)

Every task the **Tech Lead** dispatches is one row in a single SQLite database, `state.db`. Subtasks, history, blockers, cursors, and artifacts are related rows in the same DB.

```
.agent-state/
  state.db              ← single source of truth (gitignored)
  schema.sql            ← canonical DDL (committed; human-readable)
  audit/                ← committed JSON snapshots of completed tasks
    T-260513-01.json
    ...
  lib/
    state.py            ← Python stdlib SQLite helper (CRUD + CLI)
    migrate.py          ← one-shot JSON → SQLite migrator
  archive/              ← legacy per-task JSON files post-migration (gitignored)
```

## Why a database, not files

The original schema kept one JSON file per task. Every history append rewrote the whole file — slow, race-prone, no concurrent-write safety, no cross-task queries. A single SQLite DB gives us:

- **Atomic, concurrent-safe writes** (WAL mode) — parallel subagents can append history without stomping on each other.
- **Queryable state** — "show me all paused tasks", "which subtasks are blocked", "what's the next wave of ready subtasks for this task".
- **One file** instead of N — fewer merge conflicts, easier to grep.
- **Append-only history is cheap** — one `INSERT` per event, not a whole-file rewrite.

The audit trail still lives in git: every completed task is exported to `audit/<task-id>.json` and committed. The live DB itself is gitignored.

## Task ID format

```
T-YYMMDD-NN
  │ │     └─ zero-padded sequence within the day (01, 02, …)
  │ └─ date the task was created (UTC)
  └─ literal "T-"
```

Mint with `py -m lib.state next-id` (called from `.agent-state/`).

## Lifecycle

1. **Tech Lead** calls `state.create_task(...)` with `status="planning"` when a new goal arrives.
2. **Project Manager** writes `plan_summary` and inserts `subtasks` (+ `acceptance_criteria`, `subtask_deps`). Tech Lead sets `status="in-progress"`.
3. Each engineer / QA / Docs run appends rows to `history` and updates the relevant `subtasks.status`. They never touch other tasks' rows.
4. On a blocker, the raising agent calls `state.set_blocker(...)` — that automatically sets `status="paused-awaiting-human"`.
5. On resume, Tech Lead calls `state.clear_blocker(task_id)`, sets `status="in-progress"`, and continues from the `cursors` row.
6. On completion, QA sets `status="done"`. Tech Lead then runs `py -m lib.state export <task-id>` to commit a JSON snapshot under `audit/`.

## Statuses

| Status | Meaning |
| --- | --- |
| `planning` | Tech Lead has the goal; PM hasn't produced a plan yet. |
| `in-progress` | An engineer or QA is actively working. |
| `qa-review` | Engineering is done; QA is verifying. |
| `paused-awaiting-human` | Blocker escalated to a GitHub issue; waiting for the human to merge the unblock PR. |
| `done` | QA approved, PR opened to `main`, ready for human merge. Snapshot exported to `audit/`. |
| `abandoned` | Human cancelled the task. Snapshot exported to `audit/` for the record. |

## VibeLoom-specific fields

When a task is driven by a VibeLoom operation (not a free-form goal), the `tasks` row also carries:

- `vibeloom_op` — `init`, `import`, `generate`, `eval`, `review`, `reconcile`, `approve`, `status`
- `vibeloom_tier` — `intent-specs`, `product-specs`, `system-specs`, `context`, `code`
- `vibeloom_mode` — `vibe`, `pm`, `dev`, `expert`

And each `subtasks` row carries:

- `wave` — integer wave number from the VibeLoom dispatch plan
- `scope` — container/component path (e.g., `system-specs/containers/api/`)

These let the Tech Lead query "the next ready wave" with one SQL statement and dispatch it as one parallel `task` call.

## What every agent must do

- **Read** the task row + its subtasks + cursor before doing anything (call `state.get_task(conn, task_id)`).
- **Update** state after every meaningful step (subtask complete, attempt failed, blocker raised). Use the helper functions in `state.py` — do not write raw SQL from agent code.
- **Never DELETE or UPDATE `history` rows.** Append only.
- Subagents (engineers, QA, Docs) operate on **one subtask at a time**. The Tech Lead is the only writer of `subtasks.status` transitions other than the owning agent.

## CLI cheat sheet

From the `.agent-state/` directory (or pass `PYTHONPATH=.agent-state`):

```powershell
py -m lib.state list                         # all tasks
py -m lib.state list --status in-progress    # filter by status
py -m lib.state show T-260516-01             # full task as JSON
py -m lib.state export T-260516-01           # write audit/<task>.json
py -m lib.state next-id                      # mint next task id
py -m lib.state schema                       # print embedded DDL
py lib/migrate.py                            # dry-run JSON → SQLite migration
py lib/migrate.py --apply                    # actually migrate
```

## Migration from the JSON-file model

If you're carrying a `.agent-state/T-*.json` file from the previous schema:

```powershell
cd .agent-state
py lib/migrate.py            # show what would happen
py lib/migrate.py --apply    # migrate + move originals to archive/
```

Migration is idempotent: re-runs skip task ids that are already in the DB.

## Pruning

Tasks older than 90 days with `status` `done` or `abandoned` can be pruned from `state.db` once their `audit/<task-id>.json` snapshot is committed — the git history is the long-term record. Tech Lead handles pruning on demand; agents never prune autonomously.
