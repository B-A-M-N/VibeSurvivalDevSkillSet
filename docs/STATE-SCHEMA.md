# State Schema: Dual-Agent Continuation Enforcement System
# Version: 2.0.0

## Overview

Four files are maintained across the dual-agent system:

| File | Owner | Purpose |
|---|---|---|
| `.checkpoint.json` | Main agent | Ground truth execution state |
| `.checkpoint.md` | Main agent | Human-readable mirror |
| `.observer-state.json` | Observer agent | Shadow continuity state |
| `.observer-inject.json` | Observer agent | Resume injection packet (consumed once) |

Rules:
- `.checkpoint.json` wins over `.checkpoint.md` on inconsistency.
- Observer NEVER writes to `.checkpoint.json`, `.checkpoint.md`, or `.checkpoint.lock`.
- Main agent NEVER writes to `.observer-state.json`.
- Main agent deletes `.observer-inject.json` after consumption.
- Both `.checkpoint.json` and `.checkpoint.md` must be written atomically in the same operation.

---

## 1. MAIN CHECKPOINT SCHEMA (.checkpoint.json)

### Full Schema

```json
{
  "schema_version": "2.0.0",

  "task": {
    "id": "string (required) — timestamp slug, e.g. 20240415-refactor-auth",
    "objective": "string (required) — single sentence, immutable after PLANNING phase",
    "created_at": "ISO8601 (required)",
    "updated_at": "ISO8601 (required) — updated on every checkpoint write"
  },

  "execution": {
    "phase": "string (required) — one of: INIT | PLANNING | EXECUTING | BLOCKED | VERIFYING | COMPLETE | FAILED",
    "phase_entered_at": "ISO8601 (required)",
    "phase_reason": "string (required on transition)"
  },

  "next_step": {
    "id": "string (required) — sequential integer as string, e.g. '007'",
    "description": "string (required) — ATOMIC action, max 120 chars, no compound language",
    "action_type": "string (required) — one of: create_file | modify_file | delete_file | run_command | verify | read_file | checkpoint_only",
    "target": "string (required) — exact file path or exact command string",
    "expected_outcome": "string (required) — verifiable success condition",
    "preconditions": ["string (optional)"],
    "timeout_seconds": "integer (optional) — for shell commands"
  },

  "completed_steps": [
    {
      "id": "string",
      "description": "string",
      "action_type": "string",
      "target": "string",
      "outcome": "string — actual verified result",
      "completed_at": "ISO8601",
      "duration_seconds": "integer (optional)"
    }
  ],

  "failed_paths": [
    {
      "step_id": "string",
      "description": "string",
      "error": "string — exact error or output",
      "state_change": "string — what DID change, including partial changes",
      "attempted_at": "ISO8601",
      "do_not_retry": "boolean"
    }
  ],

  "artifacts": {
    "created": [
      {
        "path": "string",
        "description": "string",
        "created_at": "ISO8601",
        "hash": "string (optional) — sha256 for integrity"
      }
    ],
    "modified": [
      {
        "path": "string",
        "description": "string — what changed",
        "modified_at": "ISO8601"
      }
    ],
    "deleted": [
      {
        "path": "string",
        "deleted_at": "ISO8601"
      }
    ]
  },

  "constraints": {
    "technology": ["string"],
    "architecture": ["string"],
    "file_structure": ["string"],
    "api_contracts": ["string"],
    "security": ["string"],
    "performance": ["string"],
    "other": ["string"]
  },

  "invariants": [
    {
      "id": "string — e.g. INV-001",
      "description": "string",
      "rationale": "string — why this invariant exists; required",
      "locked_at": "ISO8601"
    }
  ],

  "invariant_conflicts": [
    {
      "invariant_id": "string",
      "conflict_description": "string",
      "detected_at": "ISO8601",
      "resolution": "string or null — null means BLOCKED"
    }
  ],

  "session": {
    "post_compaction_resume": "boolean",
    "dirty_resume": "boolean",
    "session_count": "integer",
    "last_session_started_at": "ISO8601",
    "compaction_suspect_count": "integer — incremented on suspected compaction events",
    "recovery_chain_depth": "integer — consecutive recoveries without a clean step",
    "continuity_score": "integer (0–100) — computed at session start",
    "observer_injection_consumed": "boolean — true if .observer-inject.json was consumed this session"
  }
}
```

### Required Fields

```
task.id
task.objective
task.created_at
task.updated_at
execution.phase
execution.phase_entered_at
next_step.id
next_step.description
next_step.action_type
next_step.target
next_step.expected_outcome
session.continuity_score
```

### Update Rules

| Field | Rule |
|---|---|
| `task.id` | Set once at INIT. Never changed. |
| `task.objective` | Set once at INIT/PLANNING. Immutable after PLANNING. |
| `task.updated_at` | Updated on every checkpoint write. |
| `execution.phase` | Set on transition only. No regression without explicit reason. |
| `next_step` | Replaced completely after every step execution. |
| `completed_steps` | Append only. Never modified after written. |
| `failed_paths` | Append only. `do_not_retry` may be set true, never reversed. |
| `invariants` | Append during PLANNING only. Never modified. |
| `invariant_conflicts` | Append only. Never removed. |
| `artifacts.*` | Append only. |
| `session.continuity_score` | Recomputed at every session start. |
| `session.recovery_chain_depth` | Incremented on each recovery; reset to 0 on clean step. |
| `session.compaction_suspect_count` | Incremented on suspicion; reset to 0 after clean confirmed-non-compaction step. |

---

## 2. OBSERVER STATE SCHEMA (.observer-state.json)

Observer writes this file. Main agent reads it (for continuity_score computation only).

```json
{
  "schema_version": "2.0.0",
  "task_id": "string — must match .checkpoint.json task.id",
  "updated_at": "ISO8601",

  "health": {
    "continuity_score": "integer (0–100)",
    "score_computed_at": "ISO8601",
    "checkpoint_integrity": "boolean — did .checkpoint.json parse cleanly on last read",
    "last_checkpoint_read_at": "ISO8601",
    "last_lock_seen_at": "ISO8601",
    "lock_age_seconds": "integer — age of .checkpoint.lock at last poll",
    "lock_stale": "boolean — true if lock_age_seconds > max_checkpoint_age_seconds"
  },

  "compaction": {
    "suspected_count": "integer — total suspicion events this session",
    "confirmed_count": "integer — total confirmed compaction events this session",
    "last_confirmed_at": "ISO8601 or null",
    "post_compaction_resume_active": "boolean"
  },

  "intervention": {
    "total_injections_this_session": "integer",
    "last_injection_at": "ISO8601 or null",
    "clean_steps_since_last_injection": "integer",
    "observer_mode": "passive | monitoring | active",
    "intervention_blocked_until_clean_steps": "integer — cooldown remaining"
  },

  "shadow_state": {
    "last_verified_step_id": "string — highest step ID from completed_steps with verified outcome",
    "last_verified_step_description": "string",
    "last_verified_at": "ISO8601",
    "known_invariant_ids": ["string"],
    "known_failed_targets": ["string — targets with do_not_retry = true"],
    "phase": "string",
    "next_step_id": "string",
    "next_step_description": "string",
    "next_step_target": "string"
  }
}
```

### Observer Write Rules

- Observer writes `.observer-state.json` on every poll.
- Observer writes `.observer-inject.json` only when intervention criteria are met (see OBSERVER-SPEC.md).
- Observer NEVER writes to `.checkpoint.json`, `.checkpoint.md`, `.checkpoint.lock`.

---

## 3. OBSERVER INJECT PACKET SCHEMA (.observer-inject.json)

This file is written by the observer and consumed (read + deleted) by the main agent at session start.

It is the minimal recovery artifact sufficient to resume execution without triggering re-analysis.

```json
{
  "schema_version": "2.0.0",
  "generated_at": "ISO8601",
  "generated_by": "observer-agent",
  "trigger_reason": "string — e.g. 'compaction_confirmed | continuity_score_below_threshold | dirty_resume'",
  "task_id": "string — must match .checkpoint.json task.id",

  "resume": {
    "phase": "string",
    "next_step": {
      "id": "string",
      "description": "string",
      "action_type": "string",
      "target": "string",
      "expected_outcome": "string"
    },
    "last_verified_step": {
      "id": "string",
      "description": "string",
      "outcome": "string",
      "completed_at": "ISO8601"
    }
  },

  "constraints": {
    "invariant_summary": [
      {
        "id": "string",
        "description": "string"
      }
    ],
    "banned_targets": ["string — targets with do_not_retry = true"],
    "active_invariant_conflicts": [
      {
        "invariant_id": "string",
        "conflict_description": "string"
      }
    ]
  },

  "risk_flags": {
    "dirty_resume": "boolean",
    "post_compaction_resume": "boolean",
    "recovery_mode_active": "boolean",
    "recovery_chain_depth": "integer",
    "continuity_score": "integer"
  },

  "directive": "string — one of: RESUME_NORMAL | RESUME_WITH_CAUTION | HALT_FOR_REVIEW"
}
```

### Inject Packet Rules

- `task_id` must match `.checkpoint.json task.id`. If mismatch: main agent discards packet.
- Packet is consumed exactly once. Main agent deletes it after reading.
- Packet does not replace `.checkpoint.json`. It supplements it.
- If `directive = HALT_FOR_REVIEW`: main agent halts and prints inject packet reason before any execution.
- If `directive = RESUME_WITH_CAUTION`: main agent proceeds from packet's `next_step` but increments `recovery_chain_depth`.
- If `directive = RESUME_NORMAL`: main agent proceeds from packet's `next_step` with standard execution.

---

## 4. MARKDOWN CHECKPOINT SCHEMA (.checkpoint.md)

Human-readable mirror of `.checkpoint.json`. Must be written in the same operation. Not a summary — a parallel representation.

```markdown
# Checkpoint: [TASK_ID]
**Phase:** [PHASE]
**Last Updated:** [ISO8601]
**Session Count:** [N]
**Continuity Score:** [N]

---

## Objective
[Single sentence — verbatim from task.objective]

---

## Next Step
**Step ID:** [id]
**Action:** [action_type] → [target]
**Description:** [description]
**Expected Outcome:** [expected_outcome]

---

## Invariants
[For each:]
- **[INV-ID]**: [description]
  *Rationale:* [rationale]
  *Locked:* [locked_at]

---

## Constraints
**Technology:** [list]
**Architecture:** [list]
**File Structure:** [list]
**API Contracts:** [list]

---

## Completed Steps
[For each:]
- **[id]** `[action_type]` → `[target]`: [outcome] *(completed [timestamp])*

---

## Failed Paths
[For each:]
- **[step_id]** `[description]`: [error]
  State changed: [state_change]
  Do not retry: [true/false]

---

## Artifacts

### Created
[path] — [description] *(created [timestamp])*

### Modified
[path] — [description] *(modified [timestamp])*

### Deleted
[path] *(deleted [timestamp])*

---

## Session Flags
- Post-compaction resume: [true/false]
- Dirty resume: [true/false]
- Compaction suspect count: [N]
- Recovery chain depth: [N]
- Observer injection consumed: [true/false]
```

---

## 5. CONSISTENCY RULES

1. Every required field in `.checkpoint.json` must have a corresponding entry in `.checkpoint.md`.
2. `task.id` must match in both files.
3. `next_step.description` in JSON must match **Next Step Description** in markdown verbatim.
4. `completed_steps` count must match Completed Steps entries count.
5. `invariants` count must match invariant list count.
6. Both files must be written in the same checkpoint operation: write JSON → verify JSON parses → write MD → verify both exist.
7. `.observer-state.json` task_id must match `.checkpoint.json` task.id at all times.
8. `.observer-inject.json` task_id must match `.checkpoint.json` task.id or it is discarded.

---

## 6. EXAMPLE: MINIMAL VALID CHECKPOINT (step 7 of execution, post-compaction session)

```json
{
  "schema_version": "2.0.0",
  "task": {
    "id": "20240415-refactor-auth",
    "objective": "Refactor authentication module to use JWT tokens instead of session cookies.",
    "created_at": "2024-04-15T09:00:00Z",
    "updated_at": "2024-04-15T11:23:41Z"
  },
  "execution": {
    "phase": "EXECUTING",
    "phase_entered_at": "2024-04-15T09:15:00Z",
    "phase_reason": "Planning complete, invariants locked, starting implementation."
  },
  "next_step": {
    "id": "008",
    "description": "Create src/auth/token.py with validate_jwt() function using PyJWT library",
    "action_type": "create_file",
    "target": "src/auth/token.py",
    "expected_outcome": "File exists at src/auth/token.py, contains validate_jwt function, imports PyJWT"
  },
  "completed_steps": [
    {
      "id": "001",
      "description": "Read existing auth/session.py",
      "action_type": "read_file",
      "target": "src/auth/session.py",
      "outcome": "Read 247 lines. Identified 3 functions to replace.",
      "completed_at": "2024-04-15T09:16:00Z"
    },
    {
      "id": "002",
      "description": "Create src/auth/ directory",
      "action_type": "run_command",
      "target": "mkdir -p src/auth",
      "outcome": "Exit code 0. Directory created.",
      "completed_at": "2024-04-15T09:17:00Z"
    }
  ],
  "failed_paths": [],
  "artifacts": {
    "created": [],
    "modified": [],
    "deleted": []
  },
  "constraints": {
    "technology": ["Python 3.11", "PyJWT 2.8+"],
    "architecture": ["JWT validation must be stateless"],
    "file_structure": ["Auth logic in src/auth/", "Tests in tests/auth/"],
    "api_contracts": ["validate_token(token: str) -> dict signature must be preserved"],
    "security": ["Tokens must be verified with RS256, not HS256"],
    "performance": [],
    "other": []
  },
  "invariants": [
    {
      "id": "INV-001",
      "description": "JWT tokens must be signed and verified with RS256 algorithm. HS256 is not acceptable.",
      "rationale": "Security requirement: shared secret algorithms are inadequate for distributed token verification.",
      "locked_at": "2024-04-15T09:14:00Z"
    }
  ],
  "invariant_conflicts": [],
  "session": {
    "post_compaction_resume": true,
    "dirty_resume": false,
    "session_count": 3,
    "last_session_started_at": "2024-04-15T11:20:00Z",
    "compaction_suspect_count": 1,
    "recovery_chain_depth": 0,
    "continuity_score": 70,
    "observer_injection_consumed": true
  }
}
```
