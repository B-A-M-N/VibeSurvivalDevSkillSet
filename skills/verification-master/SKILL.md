---
name: verification-master
description: |
trigger: during verification phases
  Enforces evidence-based engineering. Ensures every state change 
  (write/run/delete) is verified via tool output (ls, grep, cat).
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Grep
  - TaskCreate
---

# Verification Master

This skill ensures technical accuracy by requiring concrete evidence for every claim or action. An action is not complete until its result is observed and compared against the expected outcome.

## When to Use
- After any file modification (`write_file`, `replace`).
- After running a shell command that is expected to change state.
- If a subagent (Watchdog) flags "Optimistic Completion" drift.

## Verification Rules
1. **No Assumed Success**: Never state a task is "Done" until you have tool output (exit code 0, file content) proving it.
2. **Delta Check**: When modifying code, read the file AFTER the change to verify the "Delta" matches your intent.
3. **Ghost Errors**: If a command fails, you MUST read the full stderr to diagnose the failure before proposing a retry.

## Instructions
1. Execute your planned state-changing tool call.
2. Observe the output.
3. Call a secondary "Verification Tool" (e.g., `ls -la` for creation, `cat` for modification).
4. State: "VERIFIED: [Outcome] matches [Expected Outcome]."

**Evidence is the only ground truth.**
