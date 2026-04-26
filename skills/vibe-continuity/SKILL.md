---
name: vibe-continuity
description: |
trigger: for ongoing continuity checks
  Restores agent state after context compaction or session resume. 
  Invokes State Sentry subagent to verify file artifacts and rebuild mental model.
user-invocable: true
allowed-tools:
  - Agent
  - Read
  - TaskCreate
  - Bash
  - Grep
---

# Vibe Continuity

This skill provides automatic state restoration following context compaction events. It ensures long-horizon tasks maintain continuity by delegating state verification to the State Sentry subagent.

## When to Use
- Immediately after a "Compaction successful" message.
- At the start of a new session if a `.checkpoint.json` exists.
- If you suspect "Mode Drift" or context loss.

## Instructions
1. Invoke the State Sentry subagent via the `task` tool.
2. Provide the task: "Verify current project state. Read .checkpoint.json, verify file artifacts, and return next immediate action."
3. Consume the subagent's report and update your internal state.
4. Resume execution from the verified `next_step`.

**Focus on the Checkpoint. Trust the Sentry. Maintain the Vibe.**
