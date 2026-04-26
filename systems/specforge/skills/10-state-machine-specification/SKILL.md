---
name: specforge-10-state-machine-specification
description: |
  SpecForge — State Machine Specification. Defines all state machines
  with states, transitions, guards, and side effects.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# SpecForge: State Machine Specification

**Role:** `spec-architect` — PART 5

## Mission

Define every state machine in the system. States, transitions, guards, side effects, and what happens on invalid transitions. No "magic" state changes.

## When to Use

- Building PART 5 — State Machines
- After execution flows are defined
- When entities have lifecycle states (pending → active → archived)

## State Machine Template

```
STATE_MACHINE: [EntityName]
CURRENT_STATE_FIELD: [field that stores current state]

STATES:
  - name: [state_name]
    description: [what this means]
    is_terminal: true | false

TRANSITIONS:
  - from: [state_a]
    to: [state_b]
    trigger: [event or condition]
    guard: [precondition that must be true]
    side_effects:
      - [action 1]
      - [action 2]
    invalid_transition_response: [error | ignore | force]

INITIAL_STATE: [starting state]
TERMINAL_STATES: [states where entity rests]

INVARIANTS:
  - [invariant that must hold for this state machine]
```

## Instructions

1. **Read Models + Flows**: Identify entities with lifecycle states from PART 4 and PART 3.
2. **Define States**: Every state must have a meaning and terminality flag.
3. **Map Transitions**: From → To with trigger, guard, and side effects.
4. **Handle Invalid**: What happens if code tries `pending → archived` directly? Define it.
5. **Set Invariants**: What must be true in each state?
6. **Write Output**: PART 5 section for `MASTER_SPEC.md`.

## Output

PART 5 section content for `MASTER_SPEC.md`.

**States without transitions are just labels. Define the machine.**
