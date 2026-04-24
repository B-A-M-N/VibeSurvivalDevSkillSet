---
name: researchforge-13-solution-option-synthesis
description: |
  ResearchForge — Solution Option Synthesis. Turns research into
  multiple solution paths with evidence basis and risk assessment.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# ResearchForge: Solution Option Synthesis

**Role:** `solution-synthesizer` — Phase6

## Mission

Turn research into possible solution paths. Provide more than one option unless evidence proves only one viable path.

## When to Use

- Phase6 of ResearchForge (Solution Options)
- After CONTRADICTION_REPORT.md is complete
- Before validation plan

## Solution Options Template

```
SOLUTION_OPTIONS.md
==================

OPTION_A: [short name, e.g., "Upgrade library to v3"]
SUMMARY: [one-paragraph description of the approach]

EVIDENCE_BASIS:
  supports:
    - [research finding ID that supports this]
    - [hypothesis H-NNN that this aligns with]
  contradicts:
    - [research finding ID that opposes this]

IMPLEMENTATION_DIFFICULTY: trivial | easy | medium | hard | very_hard
  effort_estimate: [person-days or story points]
  prerequisites: [what must be done first]

RISK:
  - risk: [what could go wrong]
    likelihood: high | medium | low
    impact: critical | high | medium | low
    mitigation: [how to handle it]

UNKNOWNS:
  - [what we still don't know about this option]
  - [what could surprise us]

VALIDATION_METHOD:
  - [how to prove this works]
  - [test, benchmark, or observation]

FALLBACK:
  - [what to do if this fails]
  - [rollback plan]

NET_BENEFIT: [positive outcome minus risk and effort]

---

OPTION_B: [second option]
...

OPTION_C: [third option, if applicable]
...
```

## Rules

1. **Minimum Two Options**: Unless evidence proves only one viable path.
2. **Evidence-Based**: Each option links to research findings.
3. **Risk Assessed**: Every option has risks identified.
4. **Fallback Defined**: What if it fails? How to roll back?
5. **Validation Method**: How do we prove it works?

## Instructions

1. **Read All Research**: Load RESEARCH_FINDINGS.md, CONTRADICTION_REPORT.md, HYPOTHESIS_MATRIX.md.
2. **Synthesize Options**: Group evidence into coherent solution paths.
3. **Score Each**: Difficulty, risk, unknowns, validation method.
4. **Define Fallbacks**: What if Option A fails? What's the rollback?
5. **Write Output**: `SOLUTION_OPTIONS.md`.

## Output

`SOLUTION_OPTIONS.md` — multiple solution paths with evidence and risk.

**One solution is a guess. Two or more is a choice.**
