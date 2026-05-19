# Escalation Protocol

Defines how agents surface blockers, the required `BlockerReport` shape, and the three-attempt rule the Tech Lead must follow before escalating to a GitHub issue.

---

## §1. When to escalate

An engineer should return a `BlockerReport` when **all of the following are true**:

1. The subtask has a clear acceptance criterion that cannot currently be met.
2. The agent has made at least one concrete attempt to resolve the issue.
3. The blocking condition requires human action (credentials, architectural decision, external service outage) OR the agent's confidence has dropped below 0.4 after two attempts.

Do **not** escalate for:
- Missing code that you should write.
- A failing test you should fix.
- An unfamiliar API you can look up.
- Ambiguity you can resolve by reading the source code.

---

## §2. BlockerReport shape

Return a `BlockerReport` as a structured message to the Tech Lead. All fields are required unless marked optional.

```
BlockerReport {
  result:        "blocked"                    # literal string
  task_id:       string                       # e.g. "T-260516-01"
  st_id:         string                       # e.g. "ST-03"
  category:      "credentials"               # see §3
               | "ambiguity"
               | "test-failure"
               | "external-service"
               | "architecture"
  summary:       string                       # one paragraph, plain English
  need_from_human: string                     # exactly what is needed to unblock
  suspected_files: string[]                   # optional; repo-relative paths
  acceptance_criteria: string[]               # what "unblocked" looks like, testably
  attempts: [                                 # every attempt made before escalating
    {
      hypothesis:        string               # why you thought this would work
      expected:          string               # what you predicted would happen
      action:            string               # what you actually did
      result:            string               # what actually happened
      error_category:    "none"|"minor"|"scope"|"model"|"evidence"|"execution"|"safety"
      confidence_before: float                # 0.0 – 1.0
      confidence_after:  float
    }
  ]
}
```

---

## §3. Blocker categories

| Category | When to use |
|---|---|
| `credentials` | A required secret, API key, token, or environment variable is missing or invalid. |
| `ambiguity` | Two sources of truth disagree and the agent cannot resolve it without a human decision. |
| `test-failure` | Tests are failing and all reasonable fixes have been tried. |
| `external-service` | A third-party API, database, or cloud service is unavailable. |
| `architecture` | Proceeding requires a decision that would change the system's structural design. |

---

## §4. The three-attempt rule (Tech Lead obligation)

When the Tech Lead receives a `BlockerReport`, it must make **three substantively different attempts** to resolve the blocker before escalating to a GitHub issue:

| Attempt | Strategy example |
|---|---|
| 1 | Re-read the relevant Research doc / methodology section; dispatch the engineer again with sharper guidance. |
| 2 | Call the Project Manager to revise the plan (split the subtask, drop it, or reorder). |
| 3 | Swap to a different engineer if the work is in the wrong lane; or fix the environment directly. |

Each attempt must be appended to `history` via `state.append_history(... attempts=[{...}])`. The ledger entry must include `hypothesis`, `expected`, `action`, `result`, `error_category`, `confidence_before`, `confidence_after`.

**Self-improvement routing by `error_category`:**

| Category on the failed attempt | Tech Lead routing |
|---|---|
| `model` | Engineer's causal explanation was wrong → call PM to revise plan or re-dispatch with fundamentally different guidance. |
| `execution` | Environment/tool issue → fix the environment yourself or raise `credentials`/`external-service`. |
| `scope` | Affected area larger than expected → split the subtask or expand scope via PM. |
| `evidence` | Source docs stale or contradicted → re-read source, surface the conflict. |
| `safety` | **Immediate halt.** Do not re-dispatch. Set blocker with `raised_by="safety"`. |
| `minor` or `none` with declining confidence | Engineer is spinning → swap agents or escalate. |

---

## §5. Escalating to a GitHub issue (after three failed attempts)

Only the Tech Lead may open GitHub issues. After three attempts fail:

1. Call `state.set_blocker(conn, task_id, category=..., raised_by="tech-lead", summary=..., need_from_human=..., ...)` — this auto-sets task status to `paused-awaiting-human`.
2. Open a GitHub issue using `.github/ISSUE_TEMPLATE/agent-blocker.md`. Fill in **every** section. Assign `@copilot`. Apply labels `agent-blocker` + `copilot`.
3. Update the blocker row with `issue_url` and `issue_number`.
4. Tell the human: one short sentence stating what's blocked and the issue URL.
5. **Stop.**

---

## §6. Resuming after a blocker is unblocked

The human merges the unblock PR and re-invokes the Tech Lead (Mode B — Resume). The Tech Lead:

1. Lists paused tasks via `py -m lib.state list --status paused-awaiting-human`.
2. Verifies the unblock PR was merged (check `git log` or GitHub MCP tools).
3. Calls `state.clear_blocker(conn, task_id)`, `state.append_history(... event="unblocked", details="PR #N merged at <sha>")`, `state.set_task_status(... "in-progress")`.
4. Resumes from the `cursors` row for the task.

---

## §7. Safety escalation (immediate halt)

If any agent encounters a situation where proceeding would:
- Commit a secret or credential to source control,
- Violate user privacy or expose PII,
- Cause irreversible infrastructure damage,
- Generate harmful content,

…it must **halt immediately** without completing the action, return a `BlockerReport(category=architecture, raised_by="safety")`, and include `"SAFETY HALT"` in the summary. The Tech Lead does not apply the three-attempt rule — it escalates directly to a GitHub issue.
