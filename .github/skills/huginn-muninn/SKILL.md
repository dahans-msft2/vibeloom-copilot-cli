---
name: huginn-muninn
description: "Use alongside karpathy-guidelines when doing coding, debugging, planning, reviews, QA, tool use, or multi-step agent work that should declare expected observations, track prediction error, calibrate confidence, and turn verification into durable learning. Huginn and Muninn represent thought and memory. Keywords: prediction ledger, expectation ledger, prediction trace, prediction error, confidence calibration, active inference, epistemic hygiene."
argument-hint: "Describe the task, expected result, verification check, and any uncertainty."
---

# Huginn And Muninn

## Purpose

Use this skill to augment disciplined coding workflows with explicit prediction tracking. It turns assumptions, success criteria, and verification checks into a compact ledger of expected observations, actual observations, prediction errors, and belief updates.

Huginn and Muninn are used here as a mnemonic: thought should fly ahead to predict, memory should return with what actually happened.

This skill is a companion to `karpathy-guidelines`:

- `karpathy-guidelines` keeps work simple, scoped, assumption-aware, and verifiable.
- `huginn-muninn` makes the agent state what it expects to observe, compare that with reality, and preserve the learning when expectations fail.

The core loop is:

```text
state -> prediction -> action -> observation -> prediction error -> confidence update -> next action
```

## When To Use

Use this skill for tasks where prediction quality matters:

- Debugging failures, flaky tests, regressions, or unclear behavior.
- Making non-trivial code changes that require verification.
- Reviewing code where assumptions, risks, or missing tests matter.
- Running QA scenarios, reproduction steps, migrations, deployments, or tool workflows.
- Choosing between multiple plans, models, tools, or implementation paths.
- Any task where the agent might otherwise overfit a plausible pattern and skip reality checks.

Do not use the full ledger for tiny, obvious tasks. For trivial work, use the lightweight checkpoint format.

## Relationship To Karpathy Guidelines

When `karpathy-guidelines` is also active, apply this mapping:

| Karpathy Guideline | Huginn And Muninn Addition |
| --- | --- |
| State assumptions | Record them as current priors and uncertainty sources. |
| Simplicity first | Prefer the smallest action that can reduce uncertainty. |
| Surgical changes | Keep blast radius small so prediction errors are attributable. |
| Goal-driven execution | Convert success criteria into expected observations. |
| Loop until verified | Compare actual observations to predictions and update confidence. |

The ledger should not add bureaucracy. It should sharpen the existing verification loop.

## Procedure

### 1. Establish State

Before acting, summarize only the task-relevant state:

- User goal.
- Known facts.
- Assumptions and uncertainty.
- Current confidence.
- Risk or blast radius.

Keep this short. If the state is too large, compress it to the minimum needed to make the next prediction testable.

### 2. Send Huginn Ahead

Before each meaningful action, predict what should happen if the current model is right:

- Planned action.
- Expected observation.
- Confidence from 0.00 to 1.00.
- What result would falsify or weaken the current belief.
- What result would increase confidence.

A good prediction is specific enough to be wrong.

Weak prediction:

```text
Tests should pass.
```

Strong prediction:

```text
The new invalid-input test should fail before the validation change and pass afterward; no unrelated serializer tests should change.
```

### 3. Act Surgically

Take the smallest action that can resolve the uncertainty or advance the task:

- Read the exact code or docs needed.
- Run the narrowest useful check first.
- Make the smallest viable edit.
- Avoid speculative refactors.

### 4. Let Muninn Return

Record what actually happened:

- Test output, diagnostics, runtime behavior, review finding, or tool result.
- Whether the expected observation appeared.
- Any unexpected side effects.
- Any absence of expected evidence.

### 5. Classify Prediction Error

Classify mismatches between prediction and observation:

- `none`: prediction matched observation.
- `minor`: harmless mismatch or wording/detail difference.
- `scope`: affected area was broader or narrower than expected.
- `model`: the causal explanation was wrong.
- `evidence`: the evidence was weaker, missing, stale, or contradicted.
- `execution`: command, tool, environment, or dependency behaved unexpectedly.
- `safety`: privacy, security, data-loss, permission, or user-impact assumption failed.

### 6. Update Confidence And Next Action

After observation, update:

- Confidence in the current explanation.
- Whether to proceed, retry, narrow scope, broaden search, ask the user, or stop.
- Any learning worth preserving for the current task or future tasks.

Do not treat every surprise as important. Weight surprise by relevance, risk, and repeatability.

## Lightweight Checkpoint Format

Use this for small tasks or fast inner loops:

```text
Huginn: [expected observation] (confidence: 0.xx)
Muninn: [actual result]
Update: [proceed/retry/change belief/ask/stop]
```

## Full Ledger Format

Use this for non-trivial debugging, QA, risky changes, or multi-step workflows:

```json
{
  "state": {
    "goal": "",
    "known_facts": [],
    "assumptions": [],
    "uncertainty": [],
    "blast_radius": "low|medium|high"
  },
  "prediction": {
    "planned_action": "",
    "expected_observation": "",
    "confidence": 0.0,
    "would_weaken_belief": "",
    "would_strengthen_belief": ""
  },
  "observation": {
    "actual_result": "",
    "matched": [],
    "unexpected": [],
    "missing_expected_evidence": []
  },
  "prediction_error": {
    "severity": "none|minor|medium|high",
    "category": "none|scope|model|evidence|execution|safety",
    "summary": ""
  },
  "update": {
    "new_confidence": 0.0,
    "belief_change": "",
    "next_action": "proceed|retry|narrow|broaden|ask|stop",
    "learning": ""
  }
}
```

## Review Mode

When reviewing code or plans, use the ledger to ask:

- What does this change assume?
- What observation would prove the assumption wrong?
- Are success criteria observable and specific?
- Is confidence higher than the available evidence supports?
- Are surprising results being ignored, over-weighted, or explained away?
- Did verification check the actual risk, or only a nearby proxy?

Findings should focus on mismatches between claims, evidence, and expected behavior.

## Planning Mode

When choosing between approaches, compare plans by expected information gain:

- Prefer actions that cheaply reduce the most uncertainty.
- Prefer reversible actions when confidence is low.
- Prefer narrow probes before broad rewrites.
- Escalate to broader exploration only after narrow predictions fail.

A plan is ready when each step has an expected observation and a verification check.

## Memory And Learning

Only preserve learning when it is likely to help future work:

- A repeated wrong assumption.
- A surprising dependency or hidden coupling.
- A tool/environment behavior that affected the task.
- A safety or privacy constraint that changed the plan.
- A useful calibration rule, such as "this test passing does not prove this privacy behavior."

Do not store raw secrets, private tenant data, user-sensitive outputs, or bulky logs.

## Anti-Patterns

Avoid these failure modes:

- Writing vague predictions that cannot be falsified.
- Treating a plausible explanation as verified before observation.
- Adding ledger ceremony to trivial one-step tasks.
- Updating confidence without explaining what evidence changed it.
- Ignoring low-confidence assumptions because the code change seems easy.
- Overreacting to irrelevant surprises.
- Recording everything instead of the few signals that changed the agent's belief.

## Completion Criteria

A task using this skill is complete when:

- Key assumptions were surfaced.
- Important actions had expected observations.
- Verification results were compared to those expectations.
- Any meaningful prediction error changed the plan, confidence, or memory.
- The final answer states what was verified and what residual uncertainty remains.
