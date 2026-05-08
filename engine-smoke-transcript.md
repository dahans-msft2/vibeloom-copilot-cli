# Engine smoke test transcript

Run date: 2026-05-08T08:39:17Z  
Engine: v03/engine  
Smoke repo: /tmp/vibeloom-engine-smoke

This transcript exercises every CLI verb end-to-end on a minimal scratch
repo, demonstrating the parse → graph → eval → approve → status →
detect-edits → reconcile-style cycle. Each block records the command,
its JSON stdout, and the exit code (0 clean, 1 blocking, 2 engine error).

## Phase 1 — parse / graph / eval (clean)

### parse

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke parse
{
  "artifact_count": 2,
  "artifacts": [
    {
      "approval_unit": "intent-specs",
      "artifact_id": "intent",
      "artifact_type": "intent",
      "derives_from": [],
      "extras": {},
      "items": [
        {
          "artifact_id": "intent",
          "derives_from": [],
          "description": "Track personal expenses by category.",
          "extra": {},
          "item_id": "CAP-0001",
          "scope": {
            "kind": "root",
            "scope_id": "root"
          },
          "section": "Capabilities",
          "tier": "intent-specs"
        },
        {
          "artifact_id": "intent",
          "derives_from": [],
          "description": "Export expenses as CSV.",
          "extra": {},
          "item_id": "CAP-0002",
          "scope": {
            "kind": "root",
            "scope_id": "root"
          },
          "section": "Capabilities",
          "tier": "intent-specs"
        },
        {
          "artifact_id": "intent",
          "derives_from": [],
          "description": "Must work offline.",
          "extra": {},
          "item_id": "CST-0001",
          "scope": {
            "kind": "root",
            "scope_id": "root"
          },
          "section": "Constraints",
          "tier": "intent-specs"
        }
      ],
      "layer": null,
      "mtime": 1778229530.7763042,
      "path": "intent.md",
      "scope": {
        "kind": "root",
        "scope_id": "root"
      },
      "status": "draft",
      "tier": "intent-specs",
      "timestamp": "2026-05-08T00:00:00Z"
    },
    {
      "approval_unit": "product-specs",
      "artifact_id": "prd",
      "artifact_type": "prd",
      "derives_from": [
        "CAP-0001",
        "CAP-0002",
        "CST-0001"
      ],
      "extras": {},
      "items": [
        {
          "artifact_id": "prd",
          "derives_from": [
            "CAP-0001"
          ],
          "description": "User can add an expense.",
          "extra": {},
          "item_id": "FR-0001",
          "scope": {
            "kind": "root",
            "scope_id": "root"
          },
          "section": "Functional requirements",
          "tier": "product-specs"
        },
        {
          "artifact_id": "prd",
          "derives_from": [
            "CAP-0002"
          ],
          "description": "User can export expenses as CSV.",
          "extra": {},
          "item_id": "FR-0002",
          "scope": {
            "kind": "root",
            "scope_id": "root"
          },
          "section": "Functional requirements",
          "tier": "product-specs"
        }
      ],
      "layer": null,
      "mtime": 1778229530.7799296,
      "path": "prd.md",
      "scope": {
        "kind": "root",
        "scope_id": "root"
      },
      "status": "draft",
      "tier": "product-specs",
      "timestamp": "2026-05-08T00:00:00Z"
    }
  ],
  "repo": "/private/tmp/vibeloom-engine-smoke",
  "schema_findings": []
}
exit=0
```

### graph

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke graph
{
  "artifact_count": 2,
  "cycles": [],
  "edge_count": 2,
  "item_count": 5,
  "repo": "/private/tmp/vibeloom-engine-smoke",
  "saved": false
}
exit=0
```

### eval

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke eval
{
  "advisory_count": 3,
  "blocking_count": 0,
  "errors": [],
  "findings": [
    {
      "artifact_id": "intent",
      "check": "coverage",
      "finding_id": "FIND-0001",
      "item_id": "CST-0001",
      "message": "orphan: CST-0001 has no downstream item that derives_from it",
      "severity": "advisory"
    },
    {
      "artifact_id": "prd",
      "check": "coverage",
      "finding_id": "FIND-0002",
      "item_id": "FR-0001",
      "message": "orphan: FR-0001 has no downstream item that derives_from it",
      "severity": "advisory"
    },
    {
      "artifact_id": "prd",
      "check": "coverage",
      "finding_id": "FIND-0003",
      "item_id": "FR-0002",
      "message": "orphan: FR-0002 has no downstream item that derives_from it",
      "severity": "advisory"
    }
  ],
  "target": "(all)"
}
exit=0
```

## Phase 2 — write approval trace, recompute status

We mark the prd as approved (so the artifact's lifecycle == approved),
then write an approval trace covering its current item hashes via the
engine API. Subsequent `status` should report items as `current`.

### status (after approval)

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke status
{
  "affected_artifacts": [],
  "category_counts": {
    "current": 5,
    "dangling": 0,
    "drifted": 0,
    "obsolete": 0,
    "stale": 0,
    "uncovered": 0
  },
  "current_mode": "pm-or-dev",
  "items": {
    "CAP-0001": {
      "status": "current"
    },
    "CAP-0002": {
      "status": "current"
    },
    "CST-0001": {
      "status": "current"
    },
    "FR-0001": {
      "status": "current"
    },
    "FR-0002": {
      "status": "current"
    }
  },
  "lifecycle": {
    "intent": "approved",
    "prd": "approved"
  },
  "recommended_next": "status (no action needed)",
  "uncovered_artifacts": []
}
exit=0
```

## Phase 3 — modify approved prd in-place; detect-edits + status reclassify

We modify FR-0001's description directly in prd.md. `detect-edits`
should surface this as a direct edit; `status` should reclassify
FR-0001 to `drifted`.

### detect-edits

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke detect-edits
{
  "direct_edits": [
    {
      "added_items": [],
      "approval_trace_id": "APPROVAL-20260508-001",
      "artifact_id": "prd",
      "modified_items": [
        "FR-0001"
      ],
      "path": "prd.md",
      "removed_items": []
    }
  ]
}
exit=0
```

### status (after direct edit)

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke status
{
  "affected_artifacts": [
    "prd"
  ],
  "category_counts": {
    "current": 4,
    "dangling": 0,
    "drifted": 1,
    "obsolete": 0,
    "stale": 0,
    "uncovered": 0
  },
  "current_mode": "pm-or-dev",
  "items": {
    "CAP-0001": {
      "status": "current"
    },
    "CAP-0002": {
      "status": "current"
    },
    "CST-0001": {
      "status": "current"
    },
    "FR-0001": {
      "reason": "direct_edit",
      "status": "drifted"
    },
    "FR-0002": {
      "status": "current"
    }
  },
  "lifecycle": {
    "intent": "approved",
    "prd": "approved"
  },
  "recommended_next": "reconcile (resolve drift)",
  "uncovered_artifacts": []
}
exit=0
```

## Phase 4 — affected + dispatch after CAP-level change

A change to CAP-0001 propagates to FR-0001 (which derives from it).
`affected` returns the closure; `dispatch` emits a wave-assembly plan.

### affected (CAP-0001)

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke affected --ids CAP-0001
{
  "affected_artifacts": [
    "intent",
    "prd"
  ],
  "affected_items": [
    "CAP-0001",
    "FR-0001"
  ],
  "seed_ids": [
    "CAP-0001"
  ]
}
exit=0
```

### dispatch (CAP-0001)

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke dispatch --ids CAP-0001
{
  "affected_set": [
    "CAP-0001",
    "FR-0001"
  ],
  "max_wave_size": 5,
  "plan_id": "PLAN-20260508-001",
  "waves": [
    {
      "dependencies": [],
      "scopes": [
        {
          "allowed_read_paths": [
            "intent.md",
            "defaults.md"
          ],
          "derives_from_scopes": [],
          "is_eval": false,
          "is_reconciliation": false,
          "kind": "product-specs",
          "owned_paths": [
            "prd.md",
            "usm.md",
            "dm.md"
          ],
          "scope_id": "product-specs",
          "task_template_id": "generate-product-specs"
        }
      ],
      "wave_id": "W1"
    }
  ]
}
exit=0
```

## Phase 5 — decision-trace markdown rendering

Append a decision trace, render to markdown. Verify (a) byte-identical
re-render after delete, (b) user-edit body preservation across re-render.

### decisions render (fresh)

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke decisions render
{
  "rendered_files": [
    "decisions/adr/DEC-20260508-001-csv-export-strategy.md"
  ]
}
exit=0
```


**Generated file:** `decisions/adr/DEC-20260508-001-csv-export-strategy.md`  
**SHA-256 (initial):** `6419b834f3538b9244443dc8b22dd2e66525e8600ebb52c321299c578f501942`

### decisions render (after delete)

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke decisions render
{
  "rendered_files": [
    "decisions/adr/DEC-20260508-001-csv-export-strategy.md"
  ]
}
exit=0
```


**SHA-256 (regenerated):** `6419b834f3538b9244443dc8b22dd2e66525e8600ebb52c321299c578f501942`  
**Idempotency:** byte-identical regenerate from JSONL.

### decisions render (after user edit)

```
$ python3 -m vibeloom_engine --repo /tmp/vibeloom-engine-smoke decisions render
{
  "rendered_files": [
    "decisions/adr/DEC-20260508-001-csv-export-strategy.md"
  ]
}
exit=0
```


**Body preservation check:**
```
---
trace_id: DEC-20260508-001
kind: decision
record_type: ADR
timestamp: "2026-05-08T15:00:00Z"
author: ilya@vibeloom.ai
topic: csv-export-strategy
load_bearing: true
affects: [FR-0002]
---
# My custom title

My hand-edited notes.
```

User-edited body preserved across re-render. 

## Phase 6 — execute_plan callback semantics

A small Python harness invokes `execute_plan` with a stub callback to
verify the orchestrator-callback contract per §13.3 (deterministic
`scope_id` ordering; failed peers do not block).

### execute_plan (callback harness)

```
$ python3 -c '... execute_plan ...'
{
  "plan_id": "PLAN-20260508-001",
  "callbacks": 1,
  "completed": [
    "product-specs"
  ],
  "failed": []
}
exit=0
```

## Smoke summary

All CLI commands returned the documented exit codes:
- exit 0 — clean state (advisories acceptable),
- exit 1 — blocking findings (none in this clean smoke; see test_eval for cycle examples),
- exit 2 — engine error (none).

All stdout payloads are valid JSON (verified by sequential JSON-decoding
in the recorded blocks).

End-to-end cycle reached the documented end state without manual
intervention. Generated artifacts left for inspection:
- /tmp/vibeloom-engine-smoke/.vibeloom/traces/approvals.jsonl
- /tmp/vibeloom-engine-smoke/.vibeloom/traces/decisions.jsonl
- /tmp/vibeloom-engine-smoke/decisions/adr/DEC-20260508-001-csv-export-strategy.md
- /tmp/vibeloom-engine-smoke/.vibeloom/cache/status.json
