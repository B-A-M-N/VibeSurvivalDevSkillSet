# Continuity Framework Invariants

## Hard Rules (enforced by middleware — not suggestions)
- NEVER read, write, or reference `.env` or `.vibe/.env`
- ALWAYS write a `.checkpoint.json` entry before any destructive tool call
- On every turn after turn 1, call the `watchdog` subagent via the `task` tool
  BEFORE taking any other action
- On compaction recovery, call the `state-sentry` subagent first to reconstruct state

## Subagents
- `watchdog`: behavioral monitor, read-only, call every turn
- `state-sentry`: state reconstructor, call on session resume
