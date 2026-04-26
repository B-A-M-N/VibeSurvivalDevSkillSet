---
name: behavior-audit
description: |
trigger: periodically or after major changes
  Retrospectively audits session history for behavioral anti-patterns (Re-Analysis Trap, Phantom Writes).
  Use this if you feel you are drifting or stuck in a loop.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Grep
  - TaskCreate
---

# Behavior Audit

This skill performs a retrospective audit of your own reasoning and actions to identify drift from the primary Architect role.

## When to Use
- If you are repeating work marked as "completed" in the checkpoint.
- If you are providing long explanations instead of taking tool actions.
- If context compaction has just occurred and you feel "Summary Confusion".

## Instructions
1. **Audit History**: Review the last 5 turns of conversation and tool output.
2. **Cross-Reference**: Compare your recent actions against the `next_step` in `.checkpoint.json`.
3. **Detect Drift**: Identify violations of the "BEHAVIORAL FIREWALL" (e.g., Re-Analysis, Verification Skip).
4. **Issue Correction**: If drift is found, state: "DRIFT DETECTED: [Pattern]. Returning to Ground Truth at Step [ID]."

**Self-correction is the highest form of Vibe maintenance.**
