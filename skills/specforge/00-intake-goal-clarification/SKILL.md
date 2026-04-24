---
name: specforge-00-intake-goal-clarification
description: |
  SpecForge Phase 1 — Intake. Clarifies application purpose, target users,
  success criteria, and boundaries before any specification work begins.
user-invocable: true
allowed-tools:
  - task
  - ask_user_question
  - read_file
  - grep
---

# SpecForge: Intake & Goal Clarification

**Role:** `specforge-overseer` — Phase 1

## Mission

Establish crystal-clear intent before touching any specification work. This skill prevents garbage-in-garbage-out by forcing ambiguity resolution up front.

## When to Use

- Starting a new SpecForge run
- User provides vague intent ("build me an app", "make a system")
- Existing docs contradict stated goals
- Scope boundaries are undefined

## Questions to Ask (only what is needed)

```
1. What is the application supposed to accomplish?
2. Who uses it? (roles, personas, user classes)
3. What does success look like? (measurable outcomes)
4. Is this greenfield, existing work, or mixed?
5. What parts are fixed vs open to design?
6. What must NOT happen? (anti-goals, constraints)
```

## Instructions

1. **Read Any Provided Material**: Review user notes, README, issues, partial specs — but treat them as *input*, not truth.
2. **Ask Targeted Questions**: Use `ask_user_question` for each ambiguity. One question at a time.
3. **Document Responses**: Write `INTENT_LEDGER.md` with sections:
   ```
   PURPOSE:
   TARGET_USERS:
   SUCCESS_CRITERIA:
   APPLICATION_BOUNDARIES:
   FIXED_DECISIONS:
   OPEN_DECISIONS:
   ANTI_GOALS:
   ```
4. **Gate**: Do NOT proceed to Phase 2 if PURPOSE, TARGET_USERS, or SUCCESS_CRITERIA are undefined.

## Output

`INTENT_LEDGER.md` — the canonical source of user intent.

**Intent is normative. Everything else follows.**
