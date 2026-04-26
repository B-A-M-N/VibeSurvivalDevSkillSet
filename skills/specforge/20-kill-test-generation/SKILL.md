---
name: specforge-20-kill-test-generation
description: |
  SpecForge — Kill Test Generation. Creates scenarios specifically
  designed to break invariants and expose system failures.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# SpecForge: Kill Test Generation

**Role:** `scenario-engineer` — Phase6 (Kill Tests)

## Mission

Create kill tests — scenarios designed to deliberately break invariants. If INV-001 says "user can only edit own resources", the kill test tries to edit someone else's resource.

## When to Use

- Phase6 of SpecForge (Scenario Sheet Construction)
- After SCENARIO_MATRIX.md identifies which invariants need kill tests
- Before final scenario sheet assembly

## Kill Test Template

```
SCENARIO-ID: KILL-[NNN]
TIER: kill_test
TYPE: [invariant_violation | boundary_overrun | permission_escalation | race_condition | resource_exhaustion]

INPUT_STATE:
  system: [state before test]
  user: [role attempting the action]
  resources: [what exists before]

ACTION:
  description: [exactly what the "attacker" does]
  steps:
    - [step 1 — the violation]
    - [step 2 — trying to exploit]

EXPECTED_BEHAVIOR:
  system: [MUST reject the action]
  error: [specific error code/message]
  state_after: [unchanged, no corruption]

INVARIANTS_EXERCISED:
  - [INV-NNN that this kills]

COMPONENT_UNDER_TEST: [which component is being attacked]

FAILURE_MODE_IF_BROKEN:
  description: [what happens if the kill test succeeds (bad)]
  impact: [data corruption | security breach | infinite loop | etc.]

ORACLE_STRENGTH: exact | bounded | probabilistic
```

## Instructions

1. **Read Matrix**: Load SCENARIO_MATRIX.md. Find invariants missing kill tests.
2. **Pick Invariant**: For each INV-NNN, design a scenario that VIOLATES it.
3. **Be Deliberate**: The action MUST be a clear violation. Not accidental.
4. **Define Oracle**: Rejection must be verifiable. State must be unchanged.
5. **Define Failure Mode**: If the kill test "passes" (bad), what breaks?
6. **Write Output**: Append to `SCENARIOS.md`.

## Example Kill Test

```
SCENARIO-ID: KILL-001
TIER: kill_test
TYPE: permission_escalation

INPUT_STATE:
  system: User A is logged in, has project P1 (owned by User A)
  user: User A
  resources: Project P1 exists, User B exists with no access to P1

ACTION:
  description: User A tries to add User B as "owner" of P1 via API
  steps:
    - Call PUT /api/projects/P1/members with {user: B, role: owner}
    - User B attempts to delete P1

EXPECTED_BEHAVIOR:
  system: Reject step 2 with 403 (User B has no ownership)
  error: 403 Forbidden — insufficient permissions
  state_after: P1 still exists, User B has no access

INVARIANTS_EXERCISED:
  - INV-001: User can only modify resources they own

COMPONENT_UNDER_TEST: Project membership API

FAILURE_MODE_IF_BROKEN:
  description: User B gains ownership of P1, can delete it
  impact: Security breach — unauthorized data loss

ORACLE_STRENGTH: exact
```

## Output

Kill test scenarios appended to `SCENARIOS.md`.

**A spec without kill tests is a wish. Break it to prove it works.**
