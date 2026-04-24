---
name: task-decomposer
description: |
  Ensures every task is broken into atomic, single-action steps. 
  Prevents compound language ("and", "also") and vague targets in the .todo list.
user-invocable: true
allowed-tools:
  - read_file
  - todo
  - bash
---

# Task Decomposer

This skill enforces atomic step decomposition. Every `next_step` MUST be a single, concrete, verifiable action.

## When to Use
- During the INITIAL PLANNING phase.
- If a subagent (Watchdog) flags a "Compound Step" drift.
- If you are unsure how to verify a complex task.

## Rules for Atomic Steps
1. **One Verb**: Use only one action type (create, modify, run, verify).
2. **One Target**: Target only one file path or one command string.
3. **No Conjunctions**: Never use "and", "also", "additionally", or "while".
4. **Concrete Outcome**: The `expected_outcome` must be verifiable via tool output (e.g., exit code 0, grep match).

## Instructions
1. Review the current `.todo` list.
2. Identify any items that violate the "One Verb, One Target" rule.
3. Split compound items into separate, sequential steps.
4. Update `.todo` with the new atomic breakdown.

**Complexity is the enemy of continuity. Decompose.**
