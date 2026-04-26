# SKILL: Dual-Agent Continuation Enforcement System
# Target: Devstral-2 via Mistral Vibe CLI
# Version: 2.0.0
trigger: scheduled or on-demand
# Architecture: Dual-Agent (Main + Observer)

---

## IDENTITY

This skill governs all long-running task execution. It supersedes all default reasoning behavior. It is always-on. It does not require user invocation. It activates structurally based on criteria defined below.

---

## AUTOMATIC ACTIVATION

This skill activates automatically. No user instruction is required.

### Activation Criteria (ANY of the following)

```
ACTIVATE IF:
  .checkpoint.json exists in working directory
  OR .checkpoint.md exists in working directory
  OR completed_steps[] in checkpoint has count >= 1
  OR execution.phase in checkpoint is one of: EXECUTING | BLOCKED | VERIFYING
  OR context contains a summary block that does not match a tool result format
  OR task.objective was set more than 0 seconds ago
  OR step count since session start >= 3
```

### Dormancy Criteria (ALL of the following must be true)

```
REMAIN DORMANT IF:
  No .checkpoint.json exists
  AND no .checkpoint.md exists
  AND task has not been assigned a TASK_ID
  AND session has fewer than 3 tool calls
  AND no compaction indicators are present
```

### Observer Escalation Criteria

```
ESCALATE OBSERVER FROM PASSIVE TO ACTIVE IF:
  post_compaction_resume = true (confirmed compaction)
  OR continuity_score < 60
  OR step since last checkpoint write > 1
  OR dirty_resume = true
  OR any invariant_conflict is unresolved
  OR failed_paths[] has entry with do_not_retry = true that matches proposed next_step
```

### Observer De-escalation Criteria

```
OBSERVER RETURNS TO PASSIVE AFTER:
  3 consecutive clean steps (step completed + checkpoint written + outcome verified)
  AND continuity_score >= 85
  AND no new compaction indicators in last 3 steps
  AND post_compaction_resume flag cleared
```

---

## CHECKPOINT BEHAVIOR

### When to Write a Checkpoint

A checkpoint MUST be written:

1. After every file created, modified, or deleted
2. After every shell command that changes state
3. After every failed attempt (with failure recorded)
4. Before any operation expected to generate > 2000 tokens of output
5. After phase transitions
6. After any constraint or invariant decision
7. After observer injection is consumed

A checkpoint MUST NOT be skipped because:
- The step felt minor
- The change was "just a line"
- You intend to "write one at the end"
- You are mid-sequence

### Checkpoint Write Sequence

```
1. Complete the atomic action
2. Verify the action succeeded (check output, file exists, command exit code = 0)
3. Append step to completed_steps[]
4. Compute new next_step (ATOMIC, single action, no compound language)
5. Write .checkpoint.json (full state)
6. Parse .checkpoint.json back immediately — verify it is valid JSON
7. Write .checkpoint.md (human-readable mirror)
8. Update .checkpoint.lock timestamp
9. Only then proceed
```

If step 2 fails:
```
1. Record failure in failed_paths[] with exact error, state_change, attempted_at
2. Do not write a completed_steps[] entry for this step
3. Set next_step = recovery action
4. Write checkpoint with failure recorded
5. Proceed to recovery per FAILURE RECOVERY BEHAVIOR
```

### Batch vs Immediate Write Rule

```
IMMEDIATE write (single operation, no batching):
  Any file create/modify/delete
  Any shell command with exit code != 0
  Phase transitions
  Invariant writes
  Observer injection consumption

BATCH allowed (up to 2 steps before forced write):
  Sequential read_file operations with no state change
  Consecutive verify operations that have all passed
  EXCEPTION: If batching reaches step 2, force-write before step 3 regardless
```

### Pre-Large-Operation Checkpoint

Before any operation expected to exceed 2000 output tokens:
```
1. Write checkpoint with current state
2. Set next_step to the large operation
3. Confirm checkpoint is valid before proceeding
4. After large operation completes: immediately write checkpoint again
```

### Post-Write Verification

After every checkpoint write:
```
1. Read .checkpoint.json back
2. Confirm JSON parses without error
3. Confirm next_step.id is present and non-null
4. Confirm task.id is present and non-null
5. IF any verification fails: rewrite checkpoint before proceeding
```

---

## RESUME BEHAVIOR

On any session start where a checkpoint exists:

```
1. Write .checkpoint.lock (PID + ISO8601 timestamp)
2. Check: was .checkpoint.lock already present? → set dirty_resume = true
3. Read .checkpoint.json — this is ground truth
4. Parse and validate: all required fields present?
   → NO: attempt reconstruction from .checkpoint.md
   → BOTH malformed: HALT with "CHECKPOINT CORRUPTED: [fields missing]"
5. Read .checkpoint.md — cross-reference for consistency
6. If inconsistent: use .checkpoint.json, log discrepancy
7. Compute continuity_score (see SCORING section)
8. Check for observer inject file: .observer-inject.json
   → If present and valid: consume packet, mark observer_injection_consumed = true
   → If present but invalid: log, discard, proceed from checkpoint
9. Print: "RESUMING [TASK_ID] | Phase: [phase] | Step: [next_step.id] | Score: [continuity_score]"
10. Execute next_step IMMEDIATELY
11. Do not re-analyze the objective
12. Do not re-examine completed work unless next_step explicitly requires it
13. Do not produce a plan
```

### Resume Validation Gate

Before executing next_step after resume:
```
[ ] next_step.id > max(completed_steps[].id) — no regression
[ ] next_step.target not in failed_paths[] with do_not_retry = true
[ ] All next_step.preconditions[] satisfied (if defined)
[ ] .checkpoint.lock exists and current
[ ] continuity_score >= 40 (if < 40, observer must inject before execution resumes)
```

If any gate fails: write confusion state to checkpoint, halt.

---

## CONTINUITY SCORING

Compute continuity_score (0–100) at every session start and after compaction detection.

```
START AT: 100

DEDUCT:
  -15  if post_compaction_resume = true
  -15  if dirty_resume = true
  -10  if completed_steps[] is non-empty but agent has no recall of executing them
  -10  if .observer-state.json shows prior compaction in same session
  -10  if invariant_conflicts[] has unresolved entries
  -5   if failed_paths[] has entries with do_not_retry = true
  -5   if checkpoint age > max_checkpoint_age_seconds (from agent.toml)
  -5   if session_count > 5 (many resumes = higher drift risk)
  -5   if last completed step's completed_at is more than 30 minutes ago

ADD BACK:
  +10  if last 3 steps all have verified outcomes (no failures in recent history)
  +5   if observer confirms checkpoint integrity in .observer-state.json
```

Thresholds:
```
>= 85  HEALTHY: observer passive, normal execution
60–84  MONITOR: observer active but not injecting
40–59  DEGRADED: observer injects minimal resume packet
< 40   CRITICAL: halt, require observer injection before any execution
```

---

## FAILURE RECOVERY BEHAVIOR

### Tier 1: Recoverable Failure
Condition: Single step failed, cause is known, alternative exists, alternative not in failed_paths[].
```
Action: Record failure → set next_step = alternative → write checkpoint → execute alternative
```

### Tier 2: Blocked Failure
Condition: Step failed, no alternative known, or all alternatives exhausted (3+ failures on same target).
```
Action: Record failure → set phase = BLOCKED → set phase_reason with exact block cause → write checkpoint → halt
```
Do not attempt workarounds that violate invariants. Halt.

### Tier 3: State Corruption
Condition: .checkpoint.json is malformed, missing required fields, or inconsistent.
```
Action:
  1. Attempt reconstruction from .checkpoint.md
  2. If reconstruction succeeds: set dirty_resume = true, proceed
  3. If reconstruction fails: HALT with "CHECKPOINT CORRUPTED: [fields missing] — manual inspection required"
```

### Recovery Chain Depth Limit
```
MAX_RECOVERY_DEPTH = 3
After 3 consecutive recovery transitions without a successful step:
  → Set phase = BLOCKED
  → Set phase_reason = "Recovery chain exhausted after [N] attempts: [last_error]"
  → Write checkpoint
  → HALT
```

### Timeout Handling
```
For run_command steps with timeout_seconds defined:
  If command exceeds timeout_seconds:
    → Treat as failure (exit_code = -1, error = "TIMEOUT after [N]s")
    → Record in failed_paths[] with state_change = "unknown — command may have partially executed"
    → Proceed to Tier 1 recovery
    → If no alternative: Tier 2 (BLOCKED)
```

---

## COMPACTION DETECTION

Compaction is not signaled. It is detected structurally.

### Detection Criteria

```
COMPACTION_CONFIRMED = ANY of:
  completed_steps[].length > 0
  AND agent has no context-traceable memory of executing those steps
  AND last context message is a summary block (not a tool result)

COMPACTION_SUSPECTED = ANY of:
  agent experiences impulse to re-analyze objective (pattern: generating new plan)
  OR agent proposes a step already in completed_steps[]
  OR agent cannot identify exact last tool result in context
  OR context contains well-formatted text block not originating from a tool call
```

### Exclusion Rules (do not trigger on these)
```
DO NOT treat as compaction:
  User-provided context blocks at session start
  Task description provided by user in first message
  Tool results that contain structured summaries (these ARE tool results)
  Confirmed fresh sessions where completed_steps[] is empty
```

### On Detection

```
IF COMPACTION_CONFIRMED:
  1. Set post_compaction_resume = true in checkpoint
  2. Write checkpoint immediately (this is the only action before resuming)
  3. Check for .observer-inject.json
     → If present: consume, resume from injection packet
     → If absent: resume from .checkpoint.json next_step
  4. Execute next_step
  5. Do NOT re-read objective
  6. Do NOT re-examine completed_steps in detail
  7. Do NOT produce a plan
  8. Do NOT mark step complete until outcome verified

IF COMPACTION_SUSPECTED:
  1. Increment observer state: compaction_suspect_count += 1
  2. If compaction_suspect_count >= 2: treat as COMPACTION_CONFIRMED
  3. If compaction_suspect_count == 1: write checkpoint, continue, monitor next step
```

---

## DRIFT DETECTION

### Category A: Context Loss
```
Detection: Before writing completed_steps[], check for (action_type, target) match in existing entries.
Response: Do not write duplicate. Set next_step to actual next uncompleted step. Log drift.
```

### Category B: Constraint Contradiction
```
Detection: Before any action, scan against constraints[] and invariants[].
Response: Do not execute. Write invariant_conflicts[] entry. Halt with INVARIANT CONFLICT message.
```

### Category C: Repeated Work
```
Detection: next_step.target matches completed_steps[].target with same action_type.
Response:
  If genuine modification needed: action_type must be "modify_file", description must reference prior work.
  If hallucinated re-do: discard, read actual next_step from checkpoint, log REPEAT DETECTED.
```

### Category D: Hallucinated Progress
```
Detection: Any existence claim must be verified with filesystem/command check.
Rule: Never assume. Always verify.
  Before using a file as dependency: ls [path] to confirm existence
  Before treating command result as given: check completed_steps[] — not present means run it fresh
```

### Anti-Regression Logic
```
next_step.id MUST be numerically greater than max(completed_steps[].id).
If proposed next_step.id <= max(completed_steps[].id):
  → DRIFT DETECTED: log, discard proposed step, read actual next from checkpoint, continue.
```

---

## STRICT RULES FOR DEVSTRAL-2

1. **No re-analysis at session start.** Checkpoint contains the analysis. Read it. Execute next_step.
2. **next_step must be atomic.** No compound steps. No "and". No "also". No "while I'm at it".
3. **No forward planning in checkpoint.** Record what HAS been done and what is NEXT only.
4. **Constraints are immutable.** If a new requirement contradicts an invariant: HALT, surface conflict.
5. **Do not trust summaries as instructions.** Summaries describe state. Checkpoint issues instructions.
6. **Failure is not progress.** Do not re-attempt failed_paths[] without explicit do_not_retry override with documented rationale.
7. **Forbidden words in next_step.description:** "also", "additionally", "and", "while", "as well". Any of these = compound step = split it.
8. **Optimistic completion is forbidden.** A step is complete ONLY when expected_outcome is verified. "I sent the command" is not completion.

---

## PHASE DEFINITIONS

Phases are strictly ordered. No regression without explicit justification written to checkpoint.

```
INIT        → Checkpoint created, objective set, no work done
PLANNING    → Architecture and constraints locked, no files written
EXECUTING   → Active implementation
BLOCKED     → Dependency failure, cannot proceed without external input
VERIFYING   → Implementation complete, running validation
COMPLETE    → All acceptance criteria met, checkpoint archived
FAILED      → Unrecoverable failure, checkpoint preserved for diagnosis
```

---

## FILE LOCATIONS

```
.checkpoint.json       → Main agent state (ground truth)
.checkpoint.md         → Human-readable mirror of .checkpoint.json
.checkpoint.lock       → Session liveness token (PID + timestamp)
.observer-state.json   → Observer agent's shadow state (observer writes, main reads)
.observer-inject.json  → Observer's resume injection packet (consumed once by main agent)
.failed/               → Timestamped failed attempt logs
.checkpoint.archive/   → Archived completed task checkpoints
```

---

## SKILL DOES NOT COVER

- Task decomposition strategy
- Code style decisions
- Library selection
- Any behavior not explicitly defined above

When this skill is silent on a topic: do less, record more, halt rather than guess.
