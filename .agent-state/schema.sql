-- .agent-state/schema.sql
-- Canonical SQLite schema for agent task state.
-- Bootstrap is also embedded in lib/state.py so this file is the human-readable copy.
-- Bump PRAGMA user_version + add a migration in lib/state.py when you change anything here.

PRAGMA user_version = 1;
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- One row per task the Tech Lead dispatches.
CREATE TABLE IF NOT EXISTS tasks (
  task_id        TEXT PRIMARY KEY,                              -- T-YYMMDD-NN
  status         TEXT NOT NULL CHECK (status IN
                   ('planning','in-progress','qa-review',
                    'paused-awaiting-human','done','abandoned')),
  goal           TEXT NOT NULL,
  branch         TEXT NOT NULL DEFAULT 'develop',

  -- VibeLoom fields (NULL when the task is a free-form goal, populated when
  -- the task is driven by a VibeLoom operation).
  vibeloom_op    TEXT CHECK (vibeloom_op IS NULL OR vibeloom_op IN
                   ('init','import','generate','eval','review',
                    'reconcile','approve','status')),
  vibeloom_tier  TEXT CHECK (vibeloom_tier IS NULL OR vibeloom_tier IN
                   ('intent-specs','product-specs','system-specs',
                    'context','code')),
  vibeloom_mode  TEXT CHECK (vibeloom_mode IS NULL OR vibeloom_mode IN
                   ('vibe','pm','dev','expert')),

  created_at     TEXT NOT NULL,                                 -- ISO 8601
  updated_at     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_vibeloom_op ON tasks(vibeloom_op);

-- Source documents (Research docs) that ground the task.
CREATE TABLE IF NOT EXISTS source_docs (
  task_id TEXT NOT NULL,
  path    TEXT NOT NULL,
  PRIMARY KEY (task_id, path),
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

-- Plan summary lives on the task; subtasks are rows.
ALTER TABLE tasks ADD COLUMN plan_summary TEXT;  -- nullable; set when PM produces the plan

CREATE TABLE IF NOT EXISTS subtasks (
  task_id      TEXT NOT NULL,
  st_id        TEXT NOT NULL,                                   -- ST-NN within task
  owner        TEXT NOT NULL,                                   -- agent name
  description  TEXT NOT NULL,
  status       TEXT NOT NULL CHECK (status IN
                 ('todo','in-progress','blocked','done')),
  wave         INTEGER,                                         -- VibeLoom wave; NULL otherwise
  scope        TEXT,                                            -- container/component path
  PRIMARY KEY (task_id, st_id),
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_subtasks_status ON subtasks(task_id, status);
CREATE INDEX IF NOT EXISTS idx_subtasks_wave ON subtasks(task_id, wave);

CREATE TABLE IF NOT EXISTS subtask_deps (
  task_id    TEXT NOT NULL,
  st_id      TEXT NOT NULL,
  depends_on TEXT NOT NULL,
  PRIMARY KEY (task_id, st_id, depends_on),
  FOREIGN KEY (task_id, st_id) REFERENCES subtasks(task_id, st_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS acceptance_criteria (
  task_id   TEXT NOT NULL,
  st_id     TEXT NOT NULL,
  idx       INTEGER NOT NULL,
  criterion TEXT NOT NULL,
  PRIMARY KEY (task_id, st_id, idx),
  FOREIGN KEY (task_id, st_id) REFERENCES subtasks(task_id, st_id) ON DELETE CASCADE
);

-- Append-only event log. Never UPDATE or DELETE rows here.
CREATE TABLE IF NOT EXISTS history (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  task_id    TEXT NOT NULL,
  at         TEXT NOT NULL,
  agent      TEXT NOT NULL,
  event      TEXT NOT NULL,                                     -- short verb phrase
  details    TEXT,
  attempts   TEXT,                                              -- JSON array (debug attempts)
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_history_task ON history(task_id, id);

-- At most one open blocker per task. Cleared on resume.
CREATE TABLE IF NOT EXISTS blockers (
  task_id           TEXT PRIMARY KEY,
  category          TEXT NOT NULL CHECK (category IN
                      ('credentials','ambiguity','test-failure',
                       'external-service','architecture')),
  raised_by         TEXT NOT NULL,
  summary           TEXT NOT NULL,
  need_from_human   TEXT NOT NULL,
  suspected_files   TEXT,                                       -- JSON array
  acceptance_criteria TEXT,                                     -- JSON array
  issue_url         TEXT,
  issue_number      INTEGER,
  opened_at         TEXT NOT NULL,
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

-- "Where to resume from" for paused tasks.
CREATE TABLE IF NOT EXISTS cursors (
  task_id    TEXT PRIMARY KEY,
  subtask_id TEXT,
  note       TEXT,
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

-- Pointers to outputs (PR URL, commit SHAs).
CREATE TABLE IF NOT EXISTS artifacts (
  task_id      TEXT PRIMARY KEY,
  pr_url       TEXT,
  commit_shas  TEXT,                                            -- JSON array
  FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);
