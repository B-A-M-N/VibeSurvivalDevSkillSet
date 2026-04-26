---
name: researchforge-05-hypothesis-disconfirmation
description: |
  ResearchForge — Hypothesis Disconfirmation. Actively tests
  hypotheses by seeking evidence that proves them wrong.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# ResearchForge: Hypothesis Disconfirmation

**Role:** `contradiction-hunter` — Phase3 (testing)

## Mission

Actively try to prove hypotheses WRONG. Run tests, check sources, look for counterexamples. A hypothesis that can't be falsified is useless.

## When to Use

- Phase3 of ResearchForge (after hypotheses are generated)
- When you have hypotheses that need testing
- Before settling on a "most likely" explanation

## Disconfirmation Template

```
DISCONFIRMATION_REPORT.md
=======================

HYPOTHESIS: H-NNN
STATEMENT: [hypothesis being tested]

DISCONFIRMATION_TESTS:
  - test: [specific action or check to prove this false]
    expected_if_false: [what we'd see if hypothesis is wrong]
    observed: [what we actually saw]
    outcome: CONFIRMED | DISCONFIRMED | INCONCLUSIVE
    confidence_change: [increased | decreased | unchanged]

  - test: [another test]
    ...

EVIDENCE_FOR:
  - [new evidence supporting hypothesis]

EVIDENCE_AGAINST:
  - [new evidence contradicting hypothesis]

UPDATED_CONFIDENCE: high | medium | low
  reasoning: [why it changed]

DISCONFIRMED_BY: [which test proved it wrong, if applicable]
```

## Instructions

1. **Read Hypotheses**: Load HYPOTHESIS_MATRIX.md.
2. **Run Disconfirmation Tests**: For each hypothesis, execute the `TEST_NEEDED` items from HYPOTHESIS_MATRIX.
3. **Seek Counterexamples**: Look for evidence that contradicts the hypothesis.
4. **Update Confidence**: If tests fail to disconfirm, confidence may increase. If disconfirmed, mark as false.
5. **Document**: Write `DISCONFIRMATION_REPORT.md`.
6. **Drop False Hypotheses**: Remove any that were conclusively disconfirmed.

## Output

`DISCONFIRMATION_REPORT.md` — updated hypothesis confidence levels.

**A hypothesis that survives disconfirmation is worth considering. The rest — discard.**
