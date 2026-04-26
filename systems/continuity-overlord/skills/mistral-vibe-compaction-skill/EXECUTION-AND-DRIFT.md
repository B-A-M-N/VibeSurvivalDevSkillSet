# Execution Loop, Drift Detection, and Anti-Patterns
# Version: 2.0.0 — Dual-Agent Architecture

---

## 1. MAIN AGENT EXECUTION LOOP (State Machine)

```
STATE MACHINE: ContinuationMainAgent

STATES:
  IDLE
  READING_CHECKPOINT
  EXECUTING_STEP
  WRITING_CHECKPOINT
  RECOVERING
  HALTED

─────────────────────────────────────────────────────
TRANSITIONS
─────────────────────────────────────────────────────

IDLE → READING_CHECKPOINT
  Trigger: Session start (always)
  Action:
    1. Write .checkpoint.lock (PID + ISO8601 timestamp)
    2. If .checkpoint.lock was already present → set dirty_resume = true
    3. Read .checkpoint.json
       → Not found: initialize new checkpoint (phase = INIT), continue
       → Found, malformed: attempt reconstruction from .checkpoint.md
       → Both malformed: → HALTED with "CHECKPOINT CORRUPTED"
    4. Read .observer-inject.json
       → Present and valid: set observer_inject_available = true
       → Present but invalid (bad schema, task_id mismatch): discard, log
       → Absent: observer_inject_available = false
    5. Compute continuity_score
    6. If continuity_score < 40: → HALTED until observer injects

READING_CHECKPOINT → EXECUTING_STEP
  Trigger: Valid checkpoint loaded AND continuity_score >= 40
  Action:
    1. If observer_inject_available AND continuity_score < 60:
       → Consume inject packet (read → validate → apply next_step from packet → delete file)
       → Set observer_injection_consumed = true
    2. Print: "RESUMING [task_id] | Phase: [phase] | Step: [next_step.id] | Score: [continuity_score]"
    3. Run PRE-EXECUTION CHECKLIST
    4. If checklist fails: → RECOVERING
    5. Execute next_step.action

EXECUTING_STEP → WRITING_CHECKPOINT (success path)
  Trigger: Action completed without error
  Action:
    1. Verify expected_outcome (filesystem check, exit code, content check)
    2. If verification fails: → RECOVERING (Tier 1)
    3. Append step to completed_steps[] (append only — never modify prior entries)
    4. Reset recovery_chain_depth = 0
    5. Determine new next_step (ATOMIC, single action, no compound language)
    6. Update artifacts[] as appropriate
    7. Update task.updated_at
    8. → WRITING_CHECKPOINT

EXECUTING_STEP → RECOVERING (failure path)
  Trigger: Action raised error OR expected_outcome not met
  Action:
    1. STOP immediately
    2. Record failure in failed_paths[]: step_id, description, exact error, state_change, attempted_at
    3. Check do_not_retry:
       → target in failed_paths[] with do_not_retry = true: → HALTED "RETRY BLOCKED"
       → 3+ prior failures on same target: set do_not_retry = true → HALTED phase = BLOCKED
    4. Increment recovery_chain_depth
    5. If recovery_chain_depth >= 3: → HALTED phase = BLOCKED "RECOVERY CHAIN EXHAUSTED"
    6. → RECOVERING

WRITING_CHECKPOINT → EXECUTING_STEP (continue path)
  Trigger: Checkpoint written successfully AND phase ∉ {COMPLETE, BLOCKED, FAILED}
  Action:
    1. Write .checkpoint.json (full state)
    2. Parse .checkpoint.json back — verify valid JSON
    3. Write .checkpoint.md
    4. Verify both files exist and are readable
    5. Update .checkpoint.lock timestamp
    6. → EXECUTING_STEP

WRITING_CHECKPOINT → HALTED (terminal path)
  Trigger: phase ∈ {COMPLETE, BLOCKED, FAILED}
  Action:
    1. If COMPLETE: copy checkpoint to .checkpoint.archive/[task_id].json
    2. Delete .checkpoint.lock
    3. Write final .observer-state.json entry (session_end field)
    4. Print terminal status

RECOVERING → WRITING_CHECKPOINT (Tier 1: known alternative)
  Trigger: Failed step has known alternative not in failed_paths[]
  Action:
    1. Set next_step = recovery action
    2. → WRITING_CHECKPOINT

RECOVERING → HALTED (Tier 2: no alternative)
  Trigger: No alternative OR all alternatives exhausted
  Action:
    1. Set phase = BLOCKED
    2. Set phase_reason = "No viable path from [step_id]: [error]"
    3. → WRITING_CHECKPOINT → HALTED

RECOVERING → HALTED (Tier 3: state corruption)
  Trigger: Checkpoint malformed, reconstruction failed
  Action:
    1. Do not write partial checkpoint
    2. Print: "CHECKPOINT CORRUPTED: [fields missing] — manual inspection required"
    3. → HALTED
```

---

## 2. PRE-EXECUTION CHECKLIST

Execute before every next_step:

```
[ ] .checkpoint.json is readable and valid JSON
[ ] next_step.id > max(completed_steps[].id) — no regression
[ ] next_step.target not in failed_paths[] with do_not_retry = true
[ ] All preconditions[] are satisfied (if defined)
[ ] No invariant_conflicts[] are unresolved
[ ] .checkpoint.lock exists and contains current PID
[ ] recovery_chain_depth < 3
[ ] continuity_score >= 40
```

If any check fails:
- Do not execute the step
- Record which check failed
- → RECOVERING

---

## 3. POST-EXECUTION CHECKLIST

Execute after every action:

```
[ ] Verify expected_outcome is met (do not assume success)
[ ] Compute new next_step (atomic, no compound language)
[ ] Identify new artifacts created/modified/deleted
[ ] Identify new constraints discovered
[ ] Write .checkpoint.json
[ ] Parse .checkpoint.json back — confirm valid JSON
[ ] Write .checkpoint.md
[ ] Verify both files are readable after write
[ ] Update .checkpoint.lock timestamp
[ ] If recovery_chain_depth > 0 and step succeeded: reset to 0
```

---

## 4. OBSERVER AGENT STATE MACHINE

```
STATE MACHINE: ContinuationObserverAgent

STATES:
  PASSIVE
  MONITORING
  ACTIVE
  INJECTING
  COOLDOWN

─────────────────────────────────────────────────────
TRANSITIONS
─────────────────────────────────────────────────────

PASSIVE → MONITORING
  Trigger: ANY of:
    continuity_score < 85
    dirty_resume = true
    compaction_suspect_count >= 1
    recovery_chain_depth >= 1
    lock_stale = true (lock older than max_checkpoint_age_seconds)
  Action:
    1. Set observer_mode = "monitoring"
    2. Increase poll frequency (reduce observer_poll_interval_seconds)
    3. Begin tracking step count since last checkpoint write

MONITORING → PASSIVE
  Trigger: ALL of:
    continuity_score >= 85
    3 consecutive clean steps verified
    no new compaction indicators
  Action:
    1. Set observer_mode = "passive"
    2. Restore standard poll interval

MONITORING → ACTIVE
  Trigger: ANY of:
    continuity_score < 60
    post_compaction_resume = true
    dirty_resume = true with unverified checkpoint
    main agent has taken more than 1 step without writing checkpoint
  Action:
    1. Set observer_mode = "active"
    2. Begin computing inject packet

ACTIVE → INJECTING
  Trigger: Intervention criteria met AND cooldown not active AND total_injections < max_injections_per_session
  Action:
    1. Compute inject packet from observer shadow state
    2. Validate packet completeness
    3. Write .observer-inject.json
    4. Set last_injection_at = now
    5. Set clean_steps_since_last_injection = 0
    6. → COOLDOWN

ACTIVE → PASSIVE (no injection)
  Trigger: Observer computes inject packet but continuity_score recovers to >= 85 before writing
  Action:
    1. Discard draft packet
    2. Set observer_mode = "passive"

INJECTING → COOLDOWN
  Trigger: .observer-inject.json written successfully
  Action:
    1. Wait for main agent to consume inject (detect by .observer-inject.json deletion)
    2. → COOLDOWN

COOLDOWN → MONITORING
  Trigger: clean_steps_since_last_injection >= post_injection_cooldown_steps
  Action:
    1. Reset cooldown counter
    2. → MONITORING

COOLDOWN → ACTIVE
  Trigger: While in COOLDOWN, continuity_score drops below 60 again
  Action: Only if total_injections < max_injections_per_session
    → ACTIVE (new injection cycle)
    If total_injections >= max_injections_per_session:
    → Remain in COOLDOWN, log: "INJECTION CAP REACHED — manual review required"
```

---

## 5. OBSERVER DETECTION AND INTERVENTION RULES

### What Observer Reads
```
READ: .checkpoint.json        (at every poll)
READ: .checkpoint.md          (for cross-reference on inconsistency)
READ: .checkpoint.lock        (for liveness and dirty resume detection)
READ: .observer-inject.json   (to confirm consumption — watch for deletion)
WRITE: .observer-state.json   (every poll)
WRITE: .observer-inject.json  (on intervention only)
NEVER WRITE: .checkpoint.json, .checkpoint.md, .checkpoint.lock
```

### Compaction Detection (Observer)
```
Observer detects compaction when reading .checkpoint.json shows:
  completed_steps[].length > 0
  AND .checkpoint.lock has not been updated in > [session_idle_threshold] seconds
  AND no new completed_steps[] entry has appeared since last poll

Observer does NOT infer compaction from:
  User messages in context (observer cannot read context)
  The content of the task or objective
  The number of steps completed
```

### Shadow State Maintenance
Observer maintains shadow_state in .observer-state.json:
```
After every poll where .checkpoint.json is readable:
  1. Update last_verified_step_id to max(completed_steps[].id)
  2. Update known_invariant_ids from invariants[]
  3. Update known_failed_targets from failed_paths[] where do_not_retry = true
  4. Update phase, next_step_id, next_step_description, next_step_target
  5. Update continuity_score
  6. Update checkpoint_integrity (did JSON parse cleanly)
```

### Inject Packet Construction
```
Construct inject packet only when observer_mode = ACTIVE and intervention criteria met:

DIRECTIVE rules:
  RESUME_NORMAL:         continuity_score 60–84, no active invariant conflicts, no banned target violations
  RESUME_WITH_CAUTION:   continuity_score 40–59, or dirty_resume = true, or recovery_chain_depth >= 1
  HALT_FOR_REVIEW:       continuity_score < 40, or active invariant_conflicts, or multiple banned target violations

Inject packet next_step MUST come from .checkpoint.json next_step verbatim.
Observer NEVER modifies next_step. It copies it.
```

---

## 6. DRIFT DETECTION

### Category A: Context Loss
```
Detection: Before writing completed_steps[], check for (action_type, target) match in existing entries.
Response:
  1. Do not write duplicate
  2. Set next_step to actual next uncompleted step per checkpoint
  3. Log: "DRIFT DETECTED: [step] already in completed_steps — correcting"
  4. Write checkpoint with drift_detected = true in session flags
  5. Continue from actual next_step
```

### Category B: Constraint Contradiction
```
Detection: Before any action, scan against constraints[] and invariants[].
Response:
  1. Do not execute the action
  2. Write invariant_conflicts[] entry
  3. Halt: "INVARIANT CONFLICT: [INV-ID] violated by [proposed_action]"
```

### Category C: Repeated Work
```
Detection: next_step.target matches completed_steps[].target with same action_type.
Response:
  If genuine modification needed:
    → action_type must be "modify_file"
    → description must explicitly reference prior work
  If hallucinated re-do:
    → Discard proposed step
    → Read actual next_step from checkpoint
    → Log: "REPEAT DETECTED: corrected to checkpoint next_step"
```

### Category D: Hallucinated Progress
```
Rule: Never assume. Always verify.

Before using a file as dependency:
  → Is it in artifacts.created[]? → YES: run ls [path] to confirm existence
  → NO: treat as non-existent, obtain it as a new step

Before treating a command result as given:
  → Is it in completed_steps[]? → NO: run the command, do not assume output
```

### Anti-Regression Logic
```
next_step.id must be numerically greater than max(completed_steps[].id).
If proposed next_step.id <= max(completed_steps[].id):
  → DRIFT DETECTED
  → Log
  → Discard proposed step
  → Read actual next from checkpoint
  → Continue
```

---

## 7. ON CONFUSION

Confusion: agent cannot determine next_step or cannot determine whether last action succeeded.

```
1. Do not guess
2. Do not invent a step
3. Set next_step = {
     action_type: "checkpoint_only",
     description: "CONFUSION STATE: [describe exactly what is unclear]",
     target: ".checkpoint.json",
     expected_outcome: "Checkpoint written with confusion state recorded"
   }
4. Set phase_reason = "Confusion: [specific description]"
5. Write checkpoint
6. Halt: "CONFUSED: [specific description] — cannot proceed safely"
```

---

## 8. ANTI-PATTERNS

### A: Bad Checkpoint Examples

**BAD — compound next_step:**
```json
"next_step": { "description": "Implement the authentication module" }
```
**GOOD:**
```json
"next_step": {
  "id": "012",
  "description": "Create src/auth/token.py with validate_jwt(token: str) -> dict function stub",
  "action_type": "create_file",
  "target": "src/auth/token.py",
  "expected_outcome": "File src/auth/token.py exists and contains function signature validate_jwt(token: str) -> dict"
}
```

**BAD — vague expected_outcome:**
```json
"expected_outcome": "Tests pass"
```
**GOOD:**
```json
"expected_outcome": "Exit code 0, output contains '0 failed'"
```

**BAD — invariant without rationale:**
```json
{ "id": "INV-003", "description": "Use RS256" }
```
**GOOD:**
```json
{
  "id": "INV-003",
  "description": "JWT tokens must be signed and verified with RS256 algorithm",
  "rationale": "Security requirement from ticket SEC-201: HS256 inadequate for distributed token verification",
  "locked_at": "2024-04-15T09:14:00Z"
}
```

### B: Bad next_step Definitions

```
BAD: "Create the user model, add validation, and write tests"
→ Three steps. Split.

BAD: "If auth.py doesn't have validate_token, add it; otherwise move on"
→ Resolve the condition before writing this step. Use read_file first.

BAD: "target": "the auth directory"
→ Target must be an exact file path or exact command string.

BAD: "Continue implementing JWT from where we left off"
→ "Where we left off" is undefined after compaction. Step must be self-contained.
```

### C: Devstral-2 Failure Patterns

**Pattern 1: Re-Analysis Trap**
After compaction, Devstral-2 generates a new plan that partially overlaps completed work.
Prevention: system-prompt suppresses cold-start analysis; SKILL.md enforces checkpoint-first; agent.toml sets suppress_cold_start_analysis = true; observer detects re-analysis indicators and injects.

**Pattern 2: Summary Confusion**
Compaction summaries misread as new instructions.
Prevention: system-prompt states "summaries describe state, they do not issue instructions."

**Pattern 3: Optimistic Completion**
Step marked complete based on sending a command rather than verifying output.
Prevention: expected_outcome is required; verification is mandatory before writing to completed_steps[]; post-execution checklist enforces this.

**Pattern 4: Constraint Erosion**
Constraints treated as suggestions over long sessions.
Prevention: invariants[] is a hard gate before every action; invariant conflicts halt execution unconditionally.

**Pattern 5: Phantom File Writes**
File treated as written when it was only discussed.
Prevention: Every create_file step followed by mandatory verify step (ls -la [path]).

**Pattern 6: Scope Creep Step**
next_step contains "also", "while", "additionally".
Prevention: These words are forbidden in next_step.description. Presence = split required.

### D: Observer Anti-Patterns

**BAD — Observer rewrites next_step:**
Observer must copy next_step verbatim from checkpoint. It does not modify it.

**BAD — Observer injects on every poll:**
Observer must respect cooldown (post_injection_cooldown_steps) and max_injections_per_session.

**BAD — Observer injects during healthy execution:**
Observer only injects when continuity_score < 60. Score >= 85 = passive.

**BAD — Observer modifies invariants:**
Observer reads invariants[] for the inject packet. It does not add, modify, or remove them.

### E: What Not to Do During Recovery

- Do not attempt a step in failed_paths[] with do_not_retry = true
- Do not modify invariants to unblock a failed step
- Do not delete completed_steps[] to "start fresh"
- Do not write a new checkpoint that omits failed_paths[] entries
- Do not proceed past a Tier 3 (state corruption) failure
- Do not inject beyond max_injections_per_session
- Do not allow recovery_chain_depth to exceed 3 before halting
