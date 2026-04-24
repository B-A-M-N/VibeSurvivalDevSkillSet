---
name: pattern-prediction
description: |
  Predicts failure points in the current plan by analyzing the .todo list 
  for compound language and vague outcomes.
user-invocable: true
allowed-tools:
  - read_file
  - bash
  - grep
  - todo
---

# Pattern Prediction

This skill analyzes your current `next_step` and `.todo` list to proactively identify potential behavioral failures before they result in tool errors.

## When to Use
- During the PLANNING phase of a new task.
- Before a high-risk refactor involving multiple files.
- If you have recently hit a "Strict Retry Limit".

## Instructions
1. **Analyze Language**: Inspect the `.todo` list for compound language (and, also, while) or vague outcomes (e.g., "fix bug").
2. **Verify Constraints**: Check if proposed actions conflict with `invariants[]` in `.checkpoint.json`.
3. **Predict Risk**: Identify which "BEHAVIORAL FIREWALL" pattern is most likely to trigger.
4. **Mitigate**: Return a PREDICTION block: "RISK: [Pattern]. MITIGATION: [Specific Action to simplify step]."

**Preventing drift is easier than recovering from it.**
