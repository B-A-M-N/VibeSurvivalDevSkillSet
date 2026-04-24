---
name: researchforge-04-hypothesis-generation
description: |
  ResearchForge — Hypothesis Generation. Creates possible explanations
  from evidence, with disconfirmation criteria for each.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# ResearchForge: Hypothesis Generation

**Role:** `hypothesis-builder` — Phase3

## Mission

Create possible explanations for the problem from the evidence. Every hypothesis MUST include disconfirmation criteria — how to prove it wrong.

## When to Use

- Phase3 of ResearchForge (Generate Hypotheses)
- After EVIDENCE_LEDGER.md and SOURCE_QUALITY_REPORT.md are complete
- Before targeted research

## Hypothesis Template

```
HYPOTHESIS_MATRIX.md
====================

HYPOTHESIS: [H-NNN]
STATEMENT: [possible explanation for the observed issue]

SUPPORTING_EVIDENCE:
  - [evidence ID or claim that supports this]
  - [another supporting evidence]

CONTRADICTING_EVIDENCE:
  - [evidence that conflicts with this hypothesis]
  - [gaps that weaken this hypothesis]

MISSING_EVIDENCE:
  - [what we need to know to strengthen this]
  - [what would confirm this hypothesis]

TEST_NEEDED:
  - [specific test or observation that would prove this false]
  - [another disconfirmation test]

RISK_IF_WRONG:
  - [what happens if we act on this but it's wrong]

CONFIDENCE: high | medium | low
  reasoning: [why this confidence level]

SYMPTOMS_EXPLAINED:
  - [observed issue 1 that this explains]
  - [observed issue 2 that this explains]
```

## Rules

1. **Disconfirmation Required**: Every hypothesis MUST have a `TEST_NEEDED` section. No "unfalsifiable" hypotheses.
2. **Multiple Hypotheses**: Generate at least 2-3 competing explanations. Don't fall in love with the first one.
3. **Evidence-Based**: Each hypothesis links to supporting AND contradicting evidence.
4. **Confidence**: Must be justified with reasoning. No "medium" by default.

## Instructions

1. **Read Evidence**: Load EVIDENCE_LEDGER.md and SOURCE_QUALITY_REPORT.md.
2. **Generate Hypotheses**: For each possible cause, write a H-NNN block.
3. **Include Disconfirmation**: For each, define how to prove it false.
4. **Assign Confidence**: Based on evidence strength, not gut feel.
5. **Write Output**: `HYPOTHESIS_MATRIX.md`.

## Output

`HYPOTHESIS_MATRIX.md` — the competing explanations with disconfirmation criteria.

**A hypothesis without disconfirmation is speculation. Falsify or discard.**
