---
name: focus-guard
description: |
  Prevents the "Re-Analysis Trap". Ensures you maintain focus on the 
  current step without re-examining completed work or re-planning.
user-invocable: true
allowed-tools:
  - Read
  - TaskCreate
---

# Focus Guard

This skill protects you from distraction and the impulse to re-analyze already-settled decisions. It enforces a "Checkpoint-First" reasoning pattern.

## When to Use
- Immediately after a context compaction event.
- If you find yourself thinking "Let me re-examine the codebase to get oriented".
- If a subagent (Watchdog) flags a "Re-Analysis" drift.

## Focus Rules
1. **Immutable Past**: `completed_steps[]` are closed. Never re-read files from finished steps to "verify" them unless you are explicitly reverting work.
2. **Summary Immunity**: Compaction summaries are descriptive, not instructive. Never treat a past-tense summary as a new command.
3. **Execution Mode**: If a `.checkpoint.json` exists, you are in EXECUTING mode. You do not need to "understand the structure" — the structure is already defined in the checkpoint.

## Instructions
1. **Stop Reasoning**: If you feel the urge to re-explore, STOP.
2. **Read Checkpoint**: Call `read_file` on `.checkpoint.json` and `.todo`.
3. **Resume Immediately**: Identify the `next_step` and execute the corresponding tool call.

**Checkpoint says. I do. Verify. Next.**
