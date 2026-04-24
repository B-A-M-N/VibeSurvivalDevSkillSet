# Observer Injection Packet Schema
# File: .observer-inject.json
# Version: 2.0.0
# Written by: Observer agent
# Consumed by: Main agent (read once, then deleted)

---

## Purpose

The inject packet is the minimal recovery artifact the observer provides to the main agent after a continuity loss event (compaction, dirty resume, or severe continuity degradation).

It must be:
- Minimal — contain only what is needed to resume without re-analysis
- Deterministic — no ambiguous fields, no optional narrative
- Non-conversational — no explanatory prose, no suggestions, no "you might want to"
- Self-contained — sufficient to resume execution from a cold-start context

---

## Full Schema

```json
{
  "schema_version": "2.0.0",
  "generated_at": "ISO8601",
  "generated_by": "continuation-observer",

  "trigger_reason": "string — one of: compaction_confirmed | continuity_score_below_threshold | dirty_resume | checkpoint_unreadable",

  "task_id": "string — MUST match .checkpoint.json task.id; if mismatch, main agent discards packet",

  "resume": {
    "phase": "string — current execution phase",
    "next_step": {
      "id": "string — copied verbatim from .checkpoint.json next_step.id",
      "description": "string — copied verbatim from .checkpoint.json next_step.description",
      "action_type": "string — copied verbatim",
      "target": "string — copied verbatim",
      "expected_outcome": "string — copied verbatim",
      "preconditions": ["string — copied verbatim if present"],
      "timeout_seconds": "integer — copied verbatim if present"
    },
    "last_verified_step": {
      "id": "string — highest step ID in completed_steps[] with verified outcome",
      "description": "string",
      "outcome": "string",
      "completed_at": "ISO8601"
    }
  },

  "constraints": {
    "invariant_summary": [
      {
        "id": "string — e.g. INV-001",
        "description": "string — copied verbatim from invariants[]"
      }
    ],
    "banned_targets": [
      "string — targets from failed_paths[] where do_not_retry = true"
    ],
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
    "continuity_score": "integer (0–100)"
  },

  "directive": "string — one of: RESUME_NORMAL | RESUME_WITH_CAUTION | HALT_FOR_REVIEW"
}
```

---

## Field Rules

| Field | Rule |
|---|---|
| `schema_version` | Must be "2.0.0" |
| `task_id` | Must match .checkpoint.json task.id exactly; mismatch = packet discarded |
| `resume.next_step` | Copied verbatim from .checkpoint.json. Never modified by observer. |
| `resume.last_verified_step` | Must be a real entry from completed_steps[]. Not synthesized. |
| `constraints.invariant_summary` | Contains only invariants already in .checkpoint.json invariants[]. Observer adds nothing. |
| `constraints.banned_targets` | Contains only do_not_retry = true entries from failed_paths[]. Observer adds nothing. |
| `directive` | Computed per OBSERVER-SPEC.md directive computation rules. |

---

## Directive Semantics

### RESUME_NORMAL
```
Main agent action:
  1. Use resume.next_step as next action
  2. Proceed with standard execution
  3. Do not increment recovery_chain_depth
```

### RESUME_WITH_CAUTION
```
Main agent action:
  1. Use resume.next_step as next action
  2. Increment recovery_chain_depth by 1
  3. Run full pre-execution checklist before executing
  4. Verify expected_outcome with extra strictness
  5. If recovery_chain_depth reaches 3: BLOCKED, halt
```

### HALT_FOR_REVIEW
```
Main agent action:
  1. Do NOT execute any step
  2. Print: "HALT_FOR_REVIEW: [trigger_reason] | Score: [risk_flags.continuity_score]"
  3. Write checkpoint with phase_reason = "Observer halted for review: [trigger_reason]"
  4. Halt
```

---

## Consumption Protocol (Main Agent)

```
1. Read .observer-inject.json
2. Parse JSON — if invalid JSON: discard, log, proceed from .checkpoint.json only
3. Validate task_id matches .checkpoint.json task.id — if mismatch: discard, log
4. Validate schema_version = "2.0.0" — if mismatch: discard, log
5. Apply directive (see Directive Semantics above)
6. Delete .observer-inject.json
7. Write checkpoint with observer_injection_consumed = true
8. Proceed from resume.next_step (or halt if directive = HALT_FOR_REVIEW)
```

---

## Example: Minimal Valid Inject Packet (post-compaction, healthy recovery)

```json
{
  "schema_version": "2.0.0",
  "generated_at": "2024-04-15T11:22:05Z",
  "generated_by": "continuation-observer",
  "trigger_reason": "compaction_confirmed",
  "task_id": "20240415-refactor-auth",
  "resume": {
    "phase": "EXECUTING",
    "next_step": {
      "id": "008",
      "description": "Create src/auth/token.py with validate_jwt() function using PyJWT library",
      "action_type": "create_file",
      "target": "src/auth/token.py",
      "expected_outcome": "File exists at src/auth/token.py, contains validate_jwt function, imports PyJWT"
    },
    "last_verified_step": {
      "id": "007",
      "description": "Verify mkdir -p src/auth created the directory",
      "outcome": "Exit code 0. ls -la src/auth shows directory exists.",
      "completed_at": "2024-04-15T11:19:00Z"
    }
  },
  "constraints": {
    "invariant_summary": [
      {
        "id": "INV-001",
        "description": "JWT tokens must be signed and verified with RS256 algorithm. HS256 is not acceptable."
      }
    ],
    "banned_targets": [],
    "active_invariant_conflicts": []
  },
  "risk_flags": {
    "dirty_resume": false,
    "post_compaction_resume": true,
    "recovery_mode_active": false,
    "recovery_chain_depth": 0,
    "continuity_score": 55
  },
  "directive": "RESUME_WITH_CAUTION"
}
```

---

## Example: Inject Packet Requiring Halt

```json
{
  "schema_version": "2.0.0",
  "generated_at": "2024-04-15T13:05:00Z",
  "generated_by": "continuation-observer",
  "trigger_reason": "checkpoint_unreadable",
  "task_id": "20240415-refactor-auth",
  "resume": {
    "phase": "EXECUTING",
    "next_step": {
      "id": "012",
      "description": "Run pytest tests/auth/ -v and verify exit code 0",
      "action_type": "run_command",
      "target": "pytest tests/auth/ -v --tb=short",
      "expected_outcome": "Exit code 0, output contains '0 failed'"
    },
    "last_verified_step": {
      "id": "011",
      "description": "Create tests/auth/test_token.py with validate_jwt test cases",
      "outcome": "File created. ls -la tests/auth/test_token.py confirmed.",
      "completed_at": "2024-04-15T12:58:00Z"
    }
  },
  "constraints": {
    "invariant_summary": [
      {
        "id": "INV-001",
        "description": "JWT tokens must be signed and verified with RS256 algorithm. HS256 is not acceptable."
      }
    ],
    "banned_targets": ["src/auth/session.py"],
    "active_invariant_conflicts": [
      {
        "invariant_id": "INV-001",
        "conflict_description": "Proposed step 011-b would have used HS256 — blocked"
      }
    ]
  },
  "risk_flags": {
    "dirty_resume": true,
    "post_compaction_resume": true,
    "recovery_mode_active": true,
    "recovery_chain_depth": 2,
    "continuity_score": 30
  },
  "directive": "HALT_FOR_REVIEW"
}
```
