---
name: verification-enforcer
description: |
trigger: after fixes are applied
  Strictly enforces verification-based completion. Prevents "Optimistic 
  Completion" by requiring tool-based proof for every step.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Grep
  - TaskCreate
---

# Verification Enforcer

This skill prevents "Phantom Progress" by requiring that every step in the `.todo` list be verified with a tool call before it is marked as completed.

## When to Use
- Before marking any step "Done" in the checkpoint.
- If you find yourself assuming a command worked without checking the output.
- If a subagent (Watchdog) flags "Optimistic Completion" drift.

## The Three Gates
1. **Execution Gate**: Was the tool call actually made (not just discussed)?
2. **Proof Gate**: Did you call a secondary tool (e.g., `ls`, `cat`) to observe the side-effect?
3. **Match Gate**: Does the observed proof match the `expected_outcome` defined in the checkpoint?

## Instructions
1. **Perform Action**: Execute the primary tool (e.g., `write_file`).
2. **Gather Proof**: Execute a verification tool (e.g., `grep` for the new content).
3. **Validate**: If proof matches, mark as completed. If not, record the failure and pivot.

**Issuing a command is NOT completion. VERIFICATION is completion.**
