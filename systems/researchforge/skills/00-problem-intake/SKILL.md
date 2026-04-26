---
name: researchforge-00-problem-intake
description: |
  ResearchForge Phase1 — Problem Intake. Clarifies the real problem,
  success criteria, and scope before any research begins.
user-invocable: true
allowed-tools:
  - Agent
  - AskUserQuestion
  - Read
  - Grep
  - Bash
---

# ResearchForge: Problem Intake

**Role:** `research-overseer` + `problem-framer` — Phase1

## Mission

Turn a messy task or bug report into a researchable problem. No research begins until the problem frame is coherent.

## When to Use

- Starting a new ResearchForge run
- User provides vague issue ("it's slow", "something's wrong")
- Multiple possible interpretations exist
- Failure mode is ambiguous

## Output Template

```
PROBLEM_FRAME.md
===============

OBSERVED_ISSUE:
  [what is happening that shouldn't, or what isn't happening that should]

DESIRED_OUTCOME:
  [what should happen instead, specifically]

KNOWN_CONSTRAINTS:
  - [constraint 1: environment, version, resource limit]
  - [constraint 2]

UNKNOWNS:
  - [what we don't know yet]
  - [what we're guessing at]

SUSPECTED_CAUSES:
  - [suspected cause 1, with confidence low/medium/high]
  - [suspected cause 2]

AFFECTED_COMPONENTS:
  - [component or system that seems affected]

SUCCESS_CRITERIA:
  - [measurable condition 1 that means "solved"]
  - [measurable condition 2]

NON_GOALS:
  - [what we are explicitly NOT trying to solve]
```

## Instructions

1. **Read User Input**: Understand the issue as described.
2. **Ask Clarifying Questions**: Use `ask_user_question` for:
   - Goal unclear?
   - Success criteria undefined?
   - Failure mode ambiguous?
   - Environment details missing?
3. **Gather Context**: Read logs, error traces, configs if available.
4. **Frame the Problem**: Write `PROBLEM_FRAME.md` with all sections filled.
5. **Gate**: Do NOT proceed to evidence collection if SUCCESS_CRITERIA or OBSERVED_ISSUE are undefined.

## Output

`PROBLEM_FRAME.md` — the researchable problem statement.

**Problem first. Evidence second. Hypotheses third. Recommendations last.**
