---
name: specforge-12-ui-behavior-specification
description: |
  SpecForge — UI Behavior Specification. Defines interface behavior,
  user interactions, feedback, and state-driven UI changes.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# SpecForge: UI Behavior Specification

**Role:** `spec-architect` — PART 8

## Mission

Define UI behavior as a contract. What the user sees, what they can do, how the system responds, and how state drives the interface. No "intuitive" or "responsive" — be exact.

## When to Use

- Building PART 8 — UI / UX Behavioral Rules
- After state machines and API contracts are defined
- When the system has a user interface (web, mobile, CLI, etc.)

## UI Element Template

```
UI_ELEMENT: [component or page name]
PURPOSE: [what this enables for the user]

VISIBLE_WHEN:
  - state: [system state or user role]
  - condition: [additional condition]

INTERACTIONS:
  - action: [click | type | drag | submit | etc.]
    target: [element]
    precondition: [must be true]
    effect:
      - [immediate feedback]
      - [state change]
      - [API call or navigation]
    error_feedback: [what user sees on failure]

STATE_DRIVEN_BEHAVIOR:
  - when: [state X]
    then: [UI shows Y, disables Z, enables W]

VALIDATION_FEEDBACK:
  - field: [input name]
    invalid_when: [condition]
    message: [exact text shown]
    location: [where message appears]

ACCESSIBILITY_REQUIREMENTS:
  - [aria labels, keyboard nav, screen reader considerations]
```

## Instructions

1. **Read State Machines**: UI is driven by state — map each state to UI appearance.
2. **Define Elements**: Each component/page gets its own block. No "header changes based on X" — define each variant.
3. **Interaction Paths**: For each action, define precondition → effect → error feedback.
4. **Validation**: Every input field has validation rules and exact error messages.
5. **Write Output**: PART 8 section for `MASTER_SPEC.md`.

## Output

PART 8 section content for `MASTER_SPEC.md`.

**"User-friendly" is not a spec. Define what they see and touch.**
