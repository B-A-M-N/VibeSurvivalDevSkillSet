---
name: specforge-18-conflict-resolution-layer
description: |
  SpecForge — Conflict Resolution Layer. Defines how competing rules,
  permissions, and state transitions are resolved when they conflict.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# SpecForge: Conflict Resolution Layer

**Role:** `spec-architect` — PART 14

## Mission

Define what happens when rules conflict. If Role A CAN and Role B CANNOT on the same resource — who wins? If two state transitions are both valid — which fires? This is the tie-breaker layer.

## When to Use

- Building PART 14 — Conflict Resolution
- After authority boundaries and state machines are defined
- When overlapping permissions or competing rules exist

## Conflict Template

```
CONFLICT_TYPE: [permission | state_transition | data_validation | priority]

SCENARIO: [describe the conflicting situation]

COMPETING_RULES:
  - rule: [rule A]
    source: [which part of spec]
    priority: [number, lower = higher priority]

  - rule: [rule B]
    source: [which part of spec]
    priority: [number]

RESOLUTION_STRATEGY:
  type: [most_specific_wins | highest_priority_wins | deny_by_default | allow_by_default | admin_override]

  most_specific_wins: [how specificity is determined]
  highest_priority_wins: [which priority value wins]
  deny_by_default: [default when no rule matches]
  allow_by_default: [default when no rule matches - use with caution]
  admin_override: [conditions under which admin can override]

EXAMPLE:
  given: [concrete conflicting situation]
  resolved: [which rule wins and why]
```

## Instructions

1. **Read Authority Boundaries**: Find overlapping permissions (Role A vs Role B on same resource).
2. **Read State Machines**: Find competing transitions from the same state.
3. **Read Invariants**: Find any that contradict each other.
4. **Define Resolution**: For each conflict type, define the tie-breaker.
5. **Priority Scheme**: If using priority, define the numbering (1 = highest or lowest?).
6. **Write Output**: PART 14 section for `MASTER_SPEC.md`.

## Common Conflict Scenarios

| Scenario | Resolution |
|----------|------------|
| Role A CAN, Role B CANNOT on same resource | Most specific role wins |
| Two transitions valid from same state | Highest priority transition wins |
| Data passes validation A but fails B | Fail closed (reject) |
| Invariant A says allow, Invariant B says deny | Deny wins (fail safe) |

## Output

PART 14 section content for `MASTER_SPEC.md`.

**Conflicts without resolution are bugs waiting to happen. Decide who wins.**
