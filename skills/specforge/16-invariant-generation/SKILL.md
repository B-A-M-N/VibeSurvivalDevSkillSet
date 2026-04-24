---
name: specforge-16-invariant-generation
description: |
  SpecForge — Invariant Generation. Defines system-wide invariants
  that must hold true across all operations and state transitions.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# SpecForge: Invariant Generation

**Role:** `spec-architect` — PART 12

## Mission

Define invariants — statements that must ALWAYS be true, regardless of what the system is doing. These are the hardest enforcement surfaces in the spec.

## When to Use

- Building PART 12 — Invariants
- After data models, state machines, and API contracts are defined
- When you need enforcement surfaces for testing

## Invariant Template

```
INVARIANT: [INV-NNN]
STATEMENT: [must always be true, regardless of system state]

SCOPE:
  all_states: true | false
  states: [list of states where this applies, if not all]
  operations: [list of operations that must preserve this]

EXAMPLES_THAT_VIOLATE:
  - [concrete example 1]
  - [concrete example 2]

ENFORCEMENT_POINT:
  - [where checked: API middleware | state transition | DB constraint | business logic]

VIOLATION_RESPONSE:
  action: [reject | rollback | log_and_continue | alert]
  error_code: [if reject]

TESTABLE_BY:
  - [scenario ID that exercises this]
  - [kill test that breaks this]
```

## Instructions

1. **Read All Sections**: Data models, state machines, API contracts, error handling.
2. **Extract Invariants**: For each model/flow, ask "What must ALWAYS be true?"
3. **Examples**: Every invariant has at least one violation example.
4. **Enforcement**: Where is this checked? DB constraint? API middleware? Business logic?
5. **Testability**: Which scenario will exercise this? Which kill test will break it?
6. **Write Output**: PART 12 section for `MASTER_SPEC.md`.

## Examples of Good Invariants

```
INVARIANT: INV-001
STATEMENT: A user can only modify resources they own or have been granted access to.
```

```
INVARIANT: INV-002
STATEMENT: The sum of allocated budget across all active projects never exceeds the total available budget.
```

## Output

PART 12 section content for `MASTER_SPEC.md`.

**Invariants are the skeleton of testability. Define them or invite drift.**
