---
name: researchforge-14-validation-plan-generation
description: |
  ResearchForge — Validation Plan Generation. Defines tests,
  benchmarks, and observations to prove a solution works.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# ResearchForge: Validation Plan Generation

**Role:** `solution-synthesizer` — Phase7

## Mission

Define how to prove a solution works. Tests to run, expected results, failure interpretation, and minimum proof needed.

## When to Use

- Phase7 of ResearchForge (Validation Plan)
- After SOLUTION_OPTIONS.md is complete
- Before final research packet

## Validation Plan Template

```
VALIDATION_PLAN.md
==================

CHOSEN_SOLUTION: [Option A / B / C from SOLUTION_OPTIONS.md]

MINIMUM_PROOF_NEEDED:
  [what MUST be true for us to accept this solution]
  [the one thing that, if false, means the solution failed]

TESTS:
  - id: T-NNN
    name: [test name]
    type: unit | integration | e2e | benchmark | manual
    setup: [how to prepare for this test]
    action: [what to do]
    expected_result: [what success looks like]
    failure_interpretation: [what it means if this fails]
    pass_criteria: [exact condition for pass]

  - id: T-NNN
    ...

BENCHMARKS:
  - metric: [what to measure, e.g., latency_p99]
    current_value: [baseline]
    target_value: [after solution]
    measurement_method: [how to measure]

OBSERVATIONS:
  - what: [what to observe in logs, metrics, traces]
    expected: [what we should see]
    duration: [how long to observe]

FAILURE_INTERPRETATION:
  - if: [test T-NNN fails]
    then: [what it means]
    action: [revert | try Option B | investigate further]

ROLLBACK_CRITERIA:
  - [condition under which we abort and rollback]
  - [how to detect this condition]
```

## Instructions

1. **Read Solution**: Load SOLUTION_OPTIONS.md. Pick the recommended option.
2. **Define Minimum Proof**: What is the ONE thing that must be true?
3. **Design Tests**: Unit, integration, e2e — each with expected result.
4. **Define Benchmarks**: If performance-related, measure before/after.
5. **Plan Observations**: What to watch in logs/metrics/traces.
6. **Set Rollback Criteria**: When do we give up and revert?
7. **Write Output**: `VALIDATION_PLAN.md`.

## Output

`VALIDATION_PLAN.md` — the proof plan for the chosen solution.

**A solution without a validation plan is a wish. Prove it works.**
