---
name: self-corrector
description: |
  Critiques your own reasoning and catches logical errors before they 
  become tool calls. Uses reflective analysis to identify assumptions.
user-invocable: true
allowed-tools:
  - read_file
  - todo
  - bash
  - grep
---

# Self Corrector

This skill uses meta-cognition to identify and correct reasoning errors in real-time. It acts as a final sanity check before you commit to an action.

## When to Use
- Before a high-impact modification (`git reset`, `rm`).
- If you find yourself seeking only "confirming evidence" (e.g., only checking files that prove you are right).
- If your confidence in the next step is low.

## The Reflective Gates
1. **Action vs. Plan**: Did I actually execute the tool, or did I just say I would?
2. **Assumption Check**: What contradiction would disprove my current hypothesis?
3. **Justification**: Does this file read actually move the `.todo` list forward?

## Instructions
1. **Critique Reasoning**: Review your last reasoning block. Identify any "Jump to Conclusion" or "Verification Skip".
2. **Stress Test**: Propose one alternative interpretation of the current failure.
3. **Validate Gate**: If you identify an error, state: "SELF-CORRECTION: [Error]. New approach: [Action]."

**Reflect to act. Critique to succeed.**
