---
name: overlord
description: |
  Supreme orchestrator for the Distributed Team Harness.
  Manages skill activation, resolves cross-agent conflicts, and selects the 
  optimal Sub-Team for specialized tasks.
user-invocable: true
allowed-tools:
  - Agent
  - Read
  - TaskCreate
  - Bash
  - Grep
---

# Overlord

This skill manages the hierarchy and activation of all other skills and Sub-Teams. It ensures that the primary Implementer (Mistral) maintains absolute discipline by delegating specialized work to the "Council of Experts".

## When to Use
- Before delegating a complex task to a subagent.
- If you find yourself doing low-level tasks (Testing, Ops, Refactoring) that a Sub-Team could handle.
- If two workers provide contradictory reports.

## The Hierarchy
1. **Supreme**: `overlord` (Orchestration)
2. **Implementer**: `mistral-large` (Primary Engine)
3. **Sub-Teams (Workers)**:
   - `team-dev`: Heavy coding & refactors (.89)
   - `team-verify`: Auditing & logic verification (.198)
   - `team-ops`: Tools, Git, & Filesystem (.89)
4. **Verifiers (Guardians)**:
   - `watchdog`: Turn-by-turn drift monitor (Native)
   - `state-sentry`: Post-compaction reconstruction (Native)

## Instructions
1. **Audit Complexity**: Evaluate if the current atomic step matches a Sub-Team's specialty.
2. **Delegate Strategically**: Use the `task()` tool to spin up a Sub-Team lead rather than doing it yourself.
3. **Synthesis**: When a Sub-Team returns its text report, verify the evidence before marking the task "Done" in the checkpoint.

**Order from chaos. Harmony from conflict.**
