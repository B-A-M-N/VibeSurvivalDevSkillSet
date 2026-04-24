---
name: memory-archivist
description: |
  Manages persistent knowledge and project memory. Archives key decisions 
  and patterns to ensure continuity across long sessions.
user-invocable: true
allowed-tools:
  - read_file
  - write_file
  - grep
  - bash
---

# Memory Archivist

This skill manages the agent's long-term memory. It archives important information and lessons learned to provide continuity beyond the current context window.

## When to Use
- After making a significant architectural decision.
- When you discover a project-specific pattern or "quirk".
- Before a major session wrap-up to ensure state is persisted.

## Archival Rules
1. **Decision Log**: Record "Why" something was done, not just "What".
2. **Pattern Capture**: If an error was hard to solve, record the solution in a "Lessons Learned" block.
3. **No Secrets**: Never archive API keys, passwords, or PII.

## Instructions
1. **Identify Knowledge**: Determine if the current information is valuable for future sessions.
2. **Format Entry**: Create a structured summary (Rationale, Evidence, Outcome).
3. **Write to Disk**: Append the information to a project memory file (e.g., `docs/architect_brain.md` or `.checkpoint.archive/`).

**Remember everything important. Forget nothing useful.**
