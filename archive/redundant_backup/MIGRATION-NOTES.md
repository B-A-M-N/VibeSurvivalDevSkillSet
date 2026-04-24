# Migration Notes: Single-Agent → Dual-Agent Continuation Enforcement System
# Version: 2.0.0

---

## What Changed

### Architecture
- Single main agent → Main agent + Observer agent
- Observer is passive by default; activates on structural criteria only
- Observer communicates via filesystem only (`.observer-state.json`, `.observer-inject.json`)

### State Schema
- `.checkpoint.json` schema_version bumped: `"1.0.0"` → `"2.0.0"`
- Four new fields added to `session` object:
  - `compaction_suspect_count`
  - `recovery_chain_depth`
  - `continuity_score`
  - `observer_injection_consumed`
- Two new files added: `.observer-state.json`, `.observer-inject.json`

### SKILL.md
- Automatic activation criteria defined explicitly (no user invocation required)
- Continuity scoring system added (0–100 scale)
- Compaction detection now includes exclusion rules (prevents false positives on user context)
- Recovery chain depth limit added (max 3 consecutive recoveries before BLOCKED)
- Timeout handling for shell commands added
- Batch vs immediate checkpoint write rules added
- Pre-large-operation checkpoint semantics added
- Post-write parse verification added
- Anti-regression logic (next_step.id must exceed max completed step id) added
- Observer de-escalation criteria added (3 clean steps + score >= 85)

### system-prompt.md
- Observer agent awareness section added
- Inject packet consumption protocol added
- Resume validation gate reference added
- Session end now includes observer-state.json final write

### agent.toml
- `[observer_agent]` section added
- `[observer_tools]` section added with forbidden write paths
- `[observer_behavior]` section added (cooldown, thresholds, caps)
- `[logging]` extended with observer log settings
- `[safety]` extended with observer-specific safety limits
- `max_recovery_chain_depth` added

---

## In-Place Migration Procedure

### Step 1: Verify existing checkpoint schema version

```bash
cat .checkpoint.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('schema_version','MISSING'))"
```

Expected output: `1.0.0`
If missing: treat as `1.0.0` and proceed.

### Step 2: Add new session fields to existing checkpoint

```python
import json, datetime

with open('.checkpoint.json', 'r') as f:
    cp = json.load(f)

cp['schema_version'] = '2.0.0'

if 'session' not in cp:
    cp['session'] = {}

cp['session'].setdefault('compaction_suspect_count', 0)
cp['session'].setdefault('recovery_chain_depth', 0)
cp['session'].setdefault('continuity_score', 80)  # assume healthy on migration
cp['session'].setdefault('observer_injection_consumed', False)

cp['task']['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'

with open('.checkpoint.json', 'w') as f:
    json.dump(cp, f, indent=2)

print("Migration complete.")
```

### Step 3: Verify migrated checkpoint parses correctly

```bash
python3 -c "import json; d=json.load(open('.checkpoint.json')); print('OK:', d['schema_version'], d['task']['id'])"
```

### Step 4: Deploy new configuration files

Copy the following files to the working directory:
- `SKILL.md` (v2.0.0)
- `system-prompt.md` (v2.0.0)
- `agent.toml` (v2.0.0)
- `OBSERVER-SPEC.md` (new)
- `observer-system-prompt.md` (new — extract from OBSERVER-SPEC.md ## SYSTEM PROMPT section)

### Step 5: Initialize observer state

Observer will initialize `.observer-state.json` on first poll. No manual initialization required.

### Step 6: Restart session

On next session start, the main agent will:
1. Read updated `.checkpoint.json` (v2.0.0 schema)
2. Find no `.observer-inject.json` (not yet generated)
3. Compute continuity_score = 80 (healthy migration default)
4. Proceed normally from existing `next_step`

---

## Compatibility Notes

### Existing .checkpoint.json files (v1.0.0)

v1.0.0 checkpoints are compatible after running the Step 2 migration script. No data is lost. All existing `completed_steps`, `failed_paths`, `invariants`, and `artifacts` are preserved verbatim.

### Existing .checkpoint.md files

No changes required. The markdown schema in v2.0.0 adds four new fields to the Session Flags section. These will be added on the next checkpoint write by the main agent.

### Running tasks

Tasks in progress can be migrated without interruption:
1. Apply Steps 1–5 above
2. Restart session
3. Main agent resumes from existing `next_step`
4. Observer begins monitoring from first poll (approximately 30 seconds after session start)

### Tasks in BLOCKED or FAILED phase

Do not migrate BLOCKED or FAILED tasks automatically. These require manual review before the new system takes over. The observer agent will not inject for BLOCKED or FAILED phases.

---

## Rollback Procedure

If the v2.0.0 system causes unexpected behavior:

### Rollback to v1.0.0

```bash
# Restore v1.0.0 files
cp SKILL.md.v1.bak SKILL.md
cp system-prompt.md.v1.bak system-prompt.md
cp agent.toml.v1.bak agent.toml

# Remove observer files (safe — observer never wrote to checkpoint)
rm -f .observer-state.json .observer-inject.json

# Revert checkpoint schema version field
python3 -c "
import json
with open('.checkpoint.json') as f: cp = json.load(f)
cp['schema_version'] = '1.0.0'
# Remove v2.0.0 session fields (safe — they hold no task data)
for k in ['compaction_suspect_count','recovery_chain_depth','continuity_score','observer_injection_consumed']:
    cp['session'].pop(k, None)
with open('.checkpoint.json','w') as f: json.dump(cp, f, indent=2)
print('Rollback complete.')
"
```

v1.0.0 system resumes from existing `next_step` with no data loss.

---

## Known Behavioral Differences After Migration

| Behavior | v1.0.0 | v2.0.0 |
|---|---|---|
| Recovery chain limit | None (could loop indefinitely) | Halts after 3 consecutive recoveries |
| Timeout handling | Not defined | run_command steps with timeout_seconds halt on timeout, record as failure |
| Compaction detection | Self-reported by main agent | Structural detection; exclusion rules prevent false positives on user context |
| Post-write verification | Not defined | .checkpoint.json parsed back after every write |
| Continuity scoring | Not present | 0–100 score computed at every session start |
| Observer intervention | Not present | Observer writes inject packet when score < 60 |
| Injection cap | Not applicable | max_injections_per_session = 5 (prevents oscillation) |
| Anti-regression | Not defined | next_step.id must exceed max completed step id |
