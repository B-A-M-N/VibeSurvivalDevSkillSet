---
name: specforge-17-hard-gate-definition
description: |
  SpecForge — Hard Gate Definition. Defines non-negotiable conditions
  that block deployment, release, or execution if violated.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# SpecForge: Hard Gate Definition

**Role:** `spec-architect` — PART 13

## Mission

Define hard gates — conditions that MUST be true or the system refuses to deploy, release, or execute. These are the ultimate enforcement points.

## When to Use

- Building PART 13 — Hard Gates
- After invariants and error handling are defined
- When there are deployment/release blockers

## Hard Gate Template

```
HARD_GATE: [HG-NNN]
NAME: [human-readable name]

CONDITION: [exact boolean expression that must be true]

CHECKED_AT:
  - [deployment time | runtime start | every N minutes | per request]

CHECK_METHOD:
  - [automated test | health endpoint | invariant check | manual sign-off]

BLOCKS:
  - [deployment | feature release | user action | API request]

VIOLATION_RESPONSE:
  action: [abort deployment | return 503 | disable feature | panic]
  message: [what is shown/logged]
  alert: [who is notified]

EXCEPTIONS:
  - [none | emergency override with sign-off from X]

RECOVERY:
  - [how to resolve the violation]
```

## Instructions

1. **Read Invariants**: Any invariant that is MUST-NOT-BREAK becomes a hard gate.
2. **Read Error Handling**: Critical errors (500s, security violations) may be gates.
3. **Define Condition**: Boolean expression. No "mostly true" — binary pass/fail.
4. **Define Check Timing**: When is this checked? Deployment? Runtime? Per request?
5. **Define Blocker**: What does a violation block?
6. **Define Recovery**: How do you fix a violation?
7. **Write Output**: PART 13 section for `MASTER_SPEC.md`.

## Examples

```
HARD_GATE: HG-001
NAME: Database migration consistency
CONDITION: All pending migrations are applied and schema version matches expected
CHECKED_AT: deployment time
BLOCKS: deployment
VIOLATION_RESPONSE: abort deployment, alert DevOps
```

```
HARD_GATE: HG-002
NAME: Authentication service availability
CONDITION: auth service health endpoint returns 200
CHECKED_AT: runtime start, every 60 seconds
BLOCKS: user actions (login, API requests)
VIOLATION_RESPONSE: return 503, show maintenance page
```

## Output

PART 13 section content for `MASTER_SPEC.md`.

**Gates that are fuzzy are not gates. Binary pass/fail or it's not a hard gate.**
