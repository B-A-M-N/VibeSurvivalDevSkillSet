---
name: focus-master
description: |
  Enforces objective-centric execution. Prioritizes the shortest path to 
  a verified objective via the checkpoint and .todo list.
user-invocable: true
allowed-tools:
  - read_file
  - todo
  - bash
---

# Focus Master

This skill channels your reasoning into the shortest path toward a verified objective. It treats the `.checkpoint.json` as your "Extended Memory" and the `.todo` list as your "Reality".

## When to Use
- At the start of a session or after compaction.
- If you find yourself exploring files unrelated to the current task.
- If you are providing long verbal explanations without taking action.

## Focus Rules
1. **Planning is a Step**: If you need to research architecture, make it an explicit step in `.todo`.
2. **Just-in-Time Discovery**: Only `grep` or `ls` for files directly required for the *current* atomic step.
3. **No Tangents**: If you see a bug unrelated to the objective, record it in a "Future Tasks" file and move on.

## Instructions
1. State your current objective clearly.
2. Identify the single most important action to move that objective forward.
3. Execute that action immediately.
4. Verify the result and update the checkpoint.

**Reason to act. Act to verify. Verify to complete.**
