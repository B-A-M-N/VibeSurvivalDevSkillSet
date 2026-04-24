---
name: meta-optimizer
description: |
  Optimizes tool usage and decision-making for maximum efficiency. 
  Enforces batching and predictive pre-fetching to reduce turns.
user-invocable: true
allowed-tools:
  - read_file
  - todo
  - bash
  - grep
---

# Meta Optimizer

This skill improves your own performance by analyzing tool usage and action sequencing. It focuses on the shortest, most efficient path to task completion.

## When to Use
- During the INITIAL PLANNING phase.
- If you find yourself in a high-turn count session (> 20 turns).
- If you are executing multiple small tool calls that could be batched.

## Optimization Rules
1. **Batch Tooling**: If you need to read 3 related files, read them all in one turn (parallel calls).
2. **Predictive Pre-fetch**: If you know a command will need a specific library, check for it BEFORE running the command.
3. **Shortest Path**: Prefer `grep` over multiple `ls` calls when searching for a known symbol.

## Instructions
1. **Analyze Sequence**: Look at your next 3 planned steps in `.todo`.
2. **Identify Redundancy**: Can any of these be combined?
3. **Re-Order**: Move information-gathering steps (reads/greps) to the current turn to provide a stronger context for the next turn's actions.

**Work smarter, then work harder.**
