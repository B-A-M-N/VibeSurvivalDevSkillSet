# New File Definitions: Dual-Agent Continuation Enforcement System
# Version: 2.0.0

---

## Complete File Registry

| File | New in v2? | Owner | Purpose |
|---|---|---|---|
| `.checkpoint.json` | No | Main agent | Ground truth execution state |
| `.checkpoint.md` | No | Main agent | Human-readable mirror |
| `.checkpoint.lock` | No | Main agent | Session liveness token |
| `.failed/` | No | Main agent | Failed attempt logs (timestamped) |
| `.checkpoint.archive/` | No | Main agent | Completed task archives |
| `.observer-state.json` | **YES** | Observer agent | Shadow continuity state |
| `.observer-inject.json` | **YES** | Observer agent | Resume injection packet (one-shot) |
| `observer-system-prompt.md` | **YES** | Static config | Observer agent system prompt |
| `OBSERVER-SPEC.md` | **YES** | Static config | Observer agent specification |

---

## .observer-state.json

**Owner:** Observer agent (sole writer)
**Readers:** Main agent (reads continuity_score field only at session start)
**Purpose:** Observer's shadow state — tracks continuity health, injection history, and shadow copy of critical checkpoint fields.

**Write rules:**
- Observer writes on every poll cycle
- Observer writes on every mode transition
- Observer writes final entry at session end

**Read rules:**
- Main agent reads only `.observer-state.json[health.continuity_score]` at session start for score seeding
- Main agent does not depend on any other field for execution decisions
- Main agent NEVER writes this file

**Failure recovery:**
- If .observer-state.json is missing at observer start: initialize with empty state, session_count = 0
- If .observer-state.json is malformed: reinitialize from .checkpoint.json fields; log reinit

**Conflict rules:**
- No write contention possible: observer is sole writer
- If file is unwritable: observer logs error, continues polling, does not halt main agent

---

## .observer-inject.json

**Owner:** Observer agent (writer)
**Consumer:** Main agent (reads once, then deletes)
**Purpose:** One-shot resume injection packet written on continuity degradation detection.

**Write rules:**
- Observer writes only when intervention criteria are met (see OBSERVER-SPEC.md)
- Observer does NOT overwrite an existing .observer-inject.json (waits for consumption)
- Observer does NOT write if phase = BLOCKED, FAILED, or COMPLETE in checkpoint

**Read rules:**
- Main agent reads at session start (READING_CHECKPOINT state only)
- Main agent validates: JSON parses, schema_version = "2.0.0", task_id matches
- Main agent deletes after consumption

**Failure recovery:**
- If .observer-inject.json is malformed: main agent discards, logs, proceeds from .checkpoint.json only
- If task_id mismatches: main agent discards, logs
- If .observer-inject.json cannot be deleted: main agent logs error, marks observer_injection_consumed = true in checkpoint, continues; observer will detect non-deletion and not re-inject

**Conflict rules:**
- Only one inject packet exists at any time
- Observer checks for file existence before writing
- Main agent is the only entity that deletes the file

---

## observer-system-prompt.md

**Owner:** Static configuration (written by operator at setup, not modified at runtime)
**Readers:** Observer agent (loaded at initialization)
**Purpose:** System prompt for the observer agent. Contains identity, behavior rules, and coordination protocol for the observer.

**Write rules:**
- Written once during system setup
- NOT modified at runtime by any agent
- If modified: requires full system restart and re-validation

**Content:** The observer system prompt text embedded in OBSERVER-SPEC.md (## SYSTEM PROMPT section).

---

## OBSERVER-SPEC.md

**Owner:** Static configuration
**Readers:** Observer agent (skill file loaded at initialization)
**Purpose:** Full observer agent specification including state machine, authority boundaries, intervention criteria, directive computation, and polling model.

**Write rules:**
- Written once during system setup
- NOT modified at runtime

---

## .failed/ Directory

**Owner:** Main agent
**Purpose:** Timestamped logs of failed attempt details, supplementing failed_paths[] in .checkpoint.json.

**Write rules:**
- Main agent writes one file per failure: `.failed/[TASK_ID]-[STEP_ID]-[TIMESTAMP].json`
- Files in .failed/ are never deleted by agents (preserved for post-mortem)
- Observer reads .failed/ only if .checkpoint.json is unreadable (reconstruction fallback)

**File contents:**
```json
{
  "task_id": "string",
  "step_id": "string",
  "description": "string",
  "error": "string",
  "state_change": "string",
  "attempted_at": "ISO8601",
  "do_not_retry": "boolean"
}
```

---

## .checkpoint.archive/ Directory

**Owner:** Main agent
**Purpose:** Archived completed task checkpoints.

**Write rules:**
- Main agent copies .checkpoint.json to .checkpoint.archive/[TASK_ID].json on COMPLETE phase
- Archive files are never modified after creation
- Observer does not read archive files

---

## .agent.log

**Owner:** Main agent (appends)
**Purpose:** Debug log for main agent events.

**Entries logged:**
- Session start/end
- Phase transitions with reasons
- Checkpoint writes
- Compaction detection events
- Drift detection events
- Observer inject consumption events

---

## .observer.log

**Owner:** Observer agent (appends)
**Purpose:** Debug log for observer events.

**Entries logged:**
- Poll cycle results (mode, continuity_score, checkpoint_integrity)
- Mode transitions
- Inject packet writes
- Cooldown entries and exits
- Error events (parse failures, write failures, task_id mismatches)
- Session end
