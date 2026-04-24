# Coordination Protocol: Main Agent ↔ Observer Agent
# Version: 2.0.0

---

## Overview

The coordination protocol is a deterministic, file-mediated protocol. There is no shared memory, no direct inter-process communication, and no dependency on runtime orchestration beyond what Mistral Vibe CLI provides natively.

All coordination occurs through filesystem reads and writes to the four state files.

---

## State Files by Owner and Access

| File | Owner (Writer) | Readers | Write Trigger |
|---|---|---|---|
| `.checkpoint.json` | Main agent | Main agent, Observer | After every atomic step |
| `.checkpoint.md` | Main agent | Observer (for cross-reference) | Same operation as .checkpoint.json |
| `.checkpoint.lock` | Main agent | Observer (liveness check) | Session start, refresh each step |
| `.observer-state.json` | Observer agent | Main agent (continuity_score only) | Every observer poll cycle |
| `.observer-inject.json` | Observer agent | Main agent | On intervention only |

Write conflicts are prevented by ownership rules. The main agent never writes observer files. The observer never writes main agent files. There is no file lock contention possible within this design.

---

## Full Coordination State Machine

```
SYSTEM STATE MACHINE: Dual-Agent Coordination

JOINT STATES:
  HEALTHY          Main executing, Observer passive
  DEGRADED         Main executing, Observer monitoring
  RECOVERING       Main recovering from failure, Observer active
  COMPACTED        Main post-compaction, Observer injecting
  HALTED           Main halted, Observer passive (no injection to send)
  COMPLETE         Main finished, Observer passive

─────────────────────────────────────────────────────
TRANSITIONS
─────────────────────────────────────────────────────

HEALTHY → DEGRADED
  Trigger: Observer computes continuity_score 60–84 OR dirty_resume = true
  Main agent action: None — continues execution normally
  Observer action: Set observer_mode = monitoring, poll more frequently

HEALTHY → COMPACTED
  Trigger: Observer detects compaction indicators (checkpoint stale, lock not refreshed)
  Main agent action: None — main agent is the entity that experienced compaction
  Observer action: Compute inject packet, write .observer-inject.json

DEGRADED → HEALTHY
  Trigger: Observer computes continuity_score >= 85 after 3 clean steps
  Main agent action: None
  Observer action: Set observer_mode = passive

DEGRADED → COMPACTED
  Trigger: Observer confirms compaction while in MONITORING mode
  Observer action: Write .observer-inject.json with RESUME_WITH_CAUTION

COMPACTED → RECOVERING
  Trigger: Main agent consumes .observer-inject.json (detected by file deletion)
  Main agent action: Consume inject packet, set observer_injection_consumed = true, execute next_step
  Observer action: Set observer_mode = COOLDOWN, increment clean_steps_since_last_injection counter

RECOVERING → HEALTHY
  Trigger: 3 consecutive clean steps post-injection, continuity_score >= 85
  Main agent action: Reset recovery_chain_depth = 0, clear post_compaction_resume flag
  Observer action: Set observer_mode = passive, reset injection cooldown counter

RECOVERING → HALTED
  Trigger: recovery_chain_depth >= 3 OR HALT_FOR_REVIEW directive consumed
  Main agent action: Write checkpoint with BLOCKED phase, halt
  Observer action: Remain passive — no injection when main agent is BLOCKED or FAILED

ANY → COMPLETE
  Trigger: Main agent sets phase = COMPLETE
  Main agent action: Archive checkpoint, delete .checkpoint.lock
  Observer action: Write final .observer-state.json with session_end = true, stop polling
```

---

## Signal Protocol

No signals are sent between agents directly. All state is communicated via file reads.

### Main Agent → Observer (via .checkpoint.json)

Main agent signals state by writing .checkpoint.json. Observer infers:

| Checkpoint state | Observer inference |
|---|---|
| `phase = BLOCKED` | Main agent is halted. Do not inject. |
| `phase = COMPLETE` | Session finished. Stop polling. |
| `session.post_compaction_resume = true` | Main agent detected compaction. Enter ACTIVE mode. |
| `session.observer_injection_consumed = true` | Inject packet was consumed. Start cooldown counter. |
| `session.recovery_chain_depth >= 2` | Main agent nearing halt threshold. Prepare inject. |
| `.observer-inject.json` deleted | Main agent consumed inject. Confirmed. |
| `.checkpoint.lock` age increasing | Main agent may be stalled or crashed. Monitor. |

### Observer → Main Agent (via .observer-inject.json)

Observer signals main agent only by writing .observer-inject.json.

Main agent signals consumption by deleting .observer-inject.json.

Main agent signals no injection present by finding .observer-inject.json absent at session start.

---

## Race Condition Analysis

### Scenario: Observer reads checkpoint while main agent is mid-write

```
Risk: Observer reads partial .checkpoint.json during a main agent write.
Mitigation:
  - Main agent writes .checkpoint.json then immediately parses it back (post-write verification)
  - If observer reads a partial write (parse fails): sets checkpoint_integrity = false
  - Observer does not inject based on a single parse failure
  - Observer injects only after 2+ consecutive parse failures
  → No race condition can cause a false inject or missed injection on a single-cycle glitch
```

### Scenario: Main agent starts new session while observer is computing inject

```
Risk: Observer writes .observer-inject.json after main agent has already started and passed the inject-check window.
Mitigation:
  - Main agent checks .observer-inject.json only at session start (READING_CHECKPOINT state)
  - If inject arrives after session start, it is consumed at next session start
  - This means one session may proceed without the inject — acceptable because:
    a. The inject packet is keyed to task_id; a stale inject for a prior session is discarded
    b. The observer's shadow state is refreshed each poll, so the next inject will be current
  → No unsafe action occurs; at worst, one session resumes from checkpoint directly
```

### Scenario: Multiple observer injections queued

```
Risk: Observer writes .observer-inject.json; main agent has not started yet; observer writes again.
Mitigation:
  - Observer checks for .observer-inject.json existence before writing
  - If file exists: observer does not overwrite
  - Main agent always deletes inject after consumption
  → Only one inject packet exists at any time
```

### Scenario: Main agent crashes without deleting .checkpoint.lock

```
Result: dirty_resume = true on next session
Mitigation: Handled by dirty_resume flag in checkpoint and continuity_score deduction
No additional coordination required
```

---

## Coordination During Phase Transitions

| Phase transition | Main agent action | Observer response |
|---|---|---|
| INIT → PLANNING | Write checkpoint with new phase | Observer begins tracking invariants[] |
| PLANNING → EXECUTING | Write checkpoint; invariants[] now locked | Observer records known_invariant_ids in shadow state |
| EXECUTING → BLOCKED | Write checkpoint with BLOCKED phase | Observer sets observer_mode = passive (no inject for BLOCKED) |
| EXECUTING → VERIFYING | Write checkpoint | Observer continues monitoring |
| VERIFYING → COMPLETE | Write checkpoint, archive | Observer writes final .observer-state.json, stops polling |
| ANY → FAILED | Write checkpoint with FAILED phase | Observer sets observer_mode = passive, logs session end |

---

## File Conflict Rules

| Conflict scenario | Resolution |
|---|---|
| Observer tries to write .checkpoint.json | FORBIDDEN — observer must not write this file |
| Main agent tries to write .observer-state.json | FORBIDDEN — main agent must not write this file |
| Both agents read .checkpoint.json simultaneously | No conflict — both are readers; filesystem read is non-destructive |
| Observer writes .observer-inject.json while main agent reads it | Atomic filesystem semantics assumed — write completes before read begins or after; partial reads surface as parse failures handled per race condition mitigation above |
| .checkpoint.lock missing at observer poll | Observer sets lock_stale = true; does not create the file; notifies via .observer-state.json |

---

## Coordination Protocol Summary (Deterministic Rules)

```
1. Only one agent writes each file. No exceptions.
2. All inter-agent signaling is via filesystem reads of owned files.
3. Observer never modifies task execution state. It copies it.
4. Main agent never modifies observer monitoring state. It writes checkpoint and reads score.
5. Inject packet is produced at most once per [post_injection_cooldown_steps] clean steps.
6. Inject packet is consumed at most once (deleted on consumption).
7. Observer halts injection after [max_injections_per_session] injections.
8. Main agent halts for HALT_FOR_REVIEW — it does not proceed without manual review.
9. No agent guesses. Observer waits for structural confirmation. Main agent halts on confusion.
10. Session end is clean only when .checkpoint.lock is deleted and phase = COMPLETE or FAILED.
```
