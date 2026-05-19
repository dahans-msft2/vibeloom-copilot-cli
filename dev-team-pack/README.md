# dev-team-pack

A portable AI development team for any project. Install it into a target repository and your full autonomous team (Tech Lead, Project Manager, Backend/Frontend/Infrastructure Engineers, QA, Documentation) shows up in VS Code Copilot Chat.

The team lives here in `vibeloom-copilot-cli`. Target projects get a copy installed into them. `vibeloom-copilot-cli` is never modified when you're working on other projects.

---

## What gets installed

```
<target-project>/
├── .github/
│   ├── agents/                  ← 8 .agent.md files (tech-lead, pm, engineers, qa, docs)
│   ├── skills/
│   │   ├── huginn-muninn/       ← prediction ledger skill
│   │   ├── karpathy-guidelines/ ← coding discipline skill
│   │   └── vibeloom/            ← contract governance skill (activates when .vibeloom/ exists)
│   └── ISSUE_TEMPLATE/
│       └── agent-blocker.md     ← structured blocker issue template
├── docs/
│   ├── agent-principles.md      ← universal agent rules (all agents read this)
│   └── escalation-protocol.md   ← BlockerReport shape + 3-attempt rule
└── .agent-state/
    ├── lib/
    │   ├── state.py             ← SQLite helper (CRUD + CLI)
    │   └── migrate.py           ← legacy JSON → SQLite migrator
    ├── schema.sql               ← canonical DDL (human-readable)
    ├── README.md                ← state-DB lifecycle docs
    ├── .gitignore               ← excludes state.db, keeps audit/
    ├── VERSION                  ← install metadata (source, commit, date)
    └── audit/                   ← committed JSON snapshots of completed tasks
```

The `state.db` file is created on first use (by `py -m lib.state next-id` or any `state.connect()` call). It is gitignored by default — the `audit/` directory holds committed snapshots.

---

## Install

Run from the `vibeloom-copilot-cli` root:

```powershell
# Windows
.\dev-team-pack\install.ps1 -Target C:\GitHub-Repos\your-project

# macOS / Linux
bash dev-team-pack/install.sh --target ~/GitHub-Repos/your-project
```

The installer:
1. Validates the target is a git repo and is not `vibeloom-copilot-cli` itself.
2. Creates required directories in the target.
3. Copies team files (agents, skills, docs, state-lib).
4. Writes `.agent-state/VERSION` with source path, commit SHA, and timestamp.
5. Adds `.gitignore` rules in the target if missing.
6. Prints next steps.

**Upgrade** (re-run to pick up changes from vibeloom-copilot-cli):

```powershell
.\dev-team-pack\install.ps1 -Target C:\GitHub-Repos\your-project -Update
```

This overwrites team files in the target. Your `state.db` and `audit/` are preserved.

---

## First use in a target project

1. Open the target project folder in VS Code.
2. In Copilot Chat, type: `@tech-lead <your goal>`  
   Or: `@tech-lead resume` (if continuing a paused task).
3. The Tech Lead reads `docs/agent-principles.md`, `docs/escalation-protocol.md`, and the state DB, then coordinates the team.

---

## Keeping the team current

When you update agents, skills, or state-lib in `vibeloom-copilot-cli`, re-run the installer with `-Update` on each target project. The installer shows a diff summary of what changed.

---

## VibeLoom (optional)

The `vibeloom/` skill is installed in every target. It activates automatically when the Tech Lead detects a `.vibeloom/` directory with approved contract specs. For projects without VibeLoom governance, it sits dormant and costs nothing.

To add VibeLoom governance to a project: `@tech-lead vibeloom init --mode pm`

---

## State DB

The team tracks work in a single SQLite file per target project. It is **project-local** — clone the target repo on another machine and the team picks up from the `audit/` snapshots.

```powershell
# From target project root:
$env:PYTHONPATH = ".agent-state"
py -m lib.state list                         # all tasks
py -m lib.state list --status in-progress
py -m lib.state show T-260519-01
py -m lib.state export T-260519-01           # write audit/<task>.json (commit this)
py -m lib.state next-id                      # mint next task id
```

---

## Repo layout

```
vibeloom-copilot-cli/
├── dev-team-pack/               ← you are here
│   ├── install.ps1
│   ├── install.sh
│   └── README.md
├── .github/
│   ├── agents/                  ← canonical agent source
│   ├── skills/                  ← canonical skills source
│   └── ISSUE_TEMPLATE/
├── docs/                        ← canonical docs source
├── .agent-state/                ← vibeloom-copilot-cli's own team state
├── v02/                         ← VibeLoom runnable substrate
└── v03/                         ← VibeLoom v0.3 spec (read-only)
```
