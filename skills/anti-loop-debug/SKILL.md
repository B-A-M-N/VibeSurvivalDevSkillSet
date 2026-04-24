---
name: anti-loop-debug
description: |
  Analyzes repeating failure patterns and provides a way out of loops.
  Use this when you've hit the retry limit or are oscillating between actions.
user-invocable: true
allowed-tools:
  - read_file
  - todo
  - bash
  - grep
---

# Anti-Loop Debug

This skill provides a structured way to break out of execution loops and repeating failures.

## When to Use
- After 3 consecutive failed attempts on the same target.
- If you are stuck in an "A -> B -> A" oscillation.
- If an error message repeats 2+ times.

## Instructions
1. **Analyze Failure**: Review `failed_paths[]` in `.checkpoint.json` and recent tool output to identify the root cause (e.g., Permissions, Missing Dependency).
2. **Commit to Third Path**: Propose a recovery strategy that is fundamentally different from the previous two failed attempts.
3. **Blacklist Failure**: Update `.checkpoint.json` with `do_not_retry: true` for the failed paths.
4. **Pivot**: Set the new `next_step` to the new approach and execute.

**Insanity is doing the same thing twice. Break the loop.**
