# Vibe Continuity: Post-Compaction State Restoration

## Overview

This skill provides **automatic, passive state restoration** following context compaction events in Mistral Vibe 2.0. It ensures that long-horizon tasks maintain continuity even when the primary agent's context window is compacted.

## Components

### 1. Primary Skill (`SKILL.md`)
- **Location**: `~/.vibe/skills/vibe-continuity/SKILL.md`
- **Purpose**: Defines the continuity framework logic, activation criteria, and state restoration protocols
- **Format**: Agent Skills specification with YAML frontmatter

### 2. State Sentry Agent (`state-sentry.toml`)
- **Location**: `~/.vibe/agents/state-sentry.toml`
- **Purpose**: Passive subagent that performs on-demand state verification when invoked by primary agent
- **Model**: Devstral Small 2 (24B) - optimized for background tasks
- **Safety**: Read-only, green border indicator

### 3. Continuation Observer (`continuation-observer.toml`)
- **Location**: `~/.vibe/agents/continuation-observer.toml`
- **Purpose**: Passive monitoring agent that polls checkpoint files and injects resume packets
- **Model**: Devstral Small 2 (24B)
- **Safety**: Read-only, green border indicator

### 4. Configuration (`config.toml`)
- **Location**: `~/.vibe/config.toml`
- **Purpose**: Global Vibe 2.0 settings with optimized compaction thresholds

## Features

### ✅ Automatic Activation
- Detects compaction structurally (no user intervention)
- Activates when continuity score drops below threshold
- Handles "Compaction successful" markers automatically

### ✅ Passive Subagent Operation
- State Sentry runs in background without user prompts
- Auto-approve enabled for seamless operation
- Read-only by default (safe)

### ✅ Checkpoint-Based Memory
- Uses `.checkpoint.json` as ground truth
- Maintains `.observer-state.json` as shadow state
- Human-readable `.checkpoint.md` mirror

### ✅ Continuity Scoring
- 0-100 point system for state health
- Automatic degradation detection
- Threshold-based intervention

### ✅ Dependency Graph Rebinding
- Reads first/last 20 lines of key files
- Uses `grep` to trace imports and calls
- Reconstructs call graph after compaction

### ✅ Security & Safety
- Trust folder system prioritizes global skills
- Read-only permissions for subagents
- No destructive operations allowed
- Green border indicator in Vibe CLI

## Quick Start

```bash
# 1. Install Mistral Vibe 2.0
uv tool install mistral-vibe

# 2. Configure API key
mkdir -p ~/.vibe
echo "MISTRAL_API_KEY=your-key" > ~/.vibe/.env

# 3. Deploy continuity framework
# Files are already in place:
# - ~/.vibe/skills/vibe-continuity/
# - ~/.vibe/agents/state-sentry.toml
# - ~/.vibe/agents/continuation-observer.toml
# - ~/.vibe/config.toml (updated)

# 4. Start Vibe
vibe
```

## How It Works

### Compaction Detection

The system detects compaction through multiple structural indicators:

1. **Explicit markers**: "Compaction successful" in context
2. **State mismatch**: `.checkpoint.json` exists but agent has no memory of steps
3. **Summary blocks**: Last context message is a summary, not a tool result
4. **Continuity score**: Score drops below 85 points
5. **Dirty resume**: Lock file indicates unclean restart

### Restoration Process

```
1. Primary agent detects compaction
2. Primary invokes State Sentry via task tool
3. State Sentry:
   - Reads .checkpoint.json
   - Verifies file artifacts exist
   - Rebuilds dependency graph
   - Returns restoration status
4. Primary agent resumes from verified state
5. Observer continues monitoring in background
```

### Continuity Score Calculation

```
Base Score: 100

Deductions:
- -25: post_compaction_resume = true
- -20: dirty_resume = true
- -15: checkpoint missing/malformed
- -10: per unresolved invariant conflict
- -5:  session_count > 5
- -5:  last step > 30 minutes old

Bonuses:
+15: last 3 steps verified
+10: observer confirms integrity

Thresholds:
>= 85: HEALTHY (observer passive)
60-84: MONITORING (observer watching)
40-59: DEGRADED (observer injects)
< 40:  CRITICAL (halt required)
```

## File Structure

```
~/.vibe/
├── skills/
│   └── vibe-continuity/
│       ├── SKILL.md              # Main skill definition
│       └── observer-system-prompt.md  # Observer system prompt
├── agents/
│   ├── state-sentry.toml         # On-demand restoration agent
│   └── continuation-observer.toml # Background monitoring agent
└── config.toml                   # Global Vibe settings

Project Directory:
├── .checkpoint.json              # Main agent state (ground truth)
├── .checkpoint.md                # Human-readable mirror
├── .checkpoint.lock              # Session liveness
├── .observer-state.json          # Observer shadow state
├── .observer-inject.json         # Resume injection packet (temporary)
├── .state-sentry.log             # State Sentry logs
├── .observer.log                 # Observer logs
└── .checkpoint.archive/          # Completed task archives
```

## Configuration Options

### Compaction Threshold (config.toml)

```toml
[context]
# For Devstral-2 (256K tokens): 80% of window
auto_compact_threshold = 209715  # 0.8 * 262144

# For Devstral Small 2 (128K tokens):
auto_compact_threshold = 104857  # 0.8 * 131072
```

### Subagent Models

For best results, use Devstral Small 2 (24B) for subagents:
- Lower cost: $0.10/$0.30 per million tokens
- Runs on RTX 4090 with high throughput (~1,300 tok/s)
- Perfect for background state verification

### Local Deployment

To run models locally:

```toml
# In continuation-observer.toml or state-sentry.toml
[agent]
model = "devstral-small-latest"
model_provider = "local"
model_path = "/path/to/devstral-small-latest.Q4_K_M.gguf"
```

Requirements:
- vLLM: `pip install vllm` (recommended for production)
- Or llama.cpp for consumer GPUs

## Devstral-2 Specific Rules

### Force Execution Directives

1. **Tool Primacy**: MUST use tools over verbal explanations
2. **Passive Verification**: After compaction, MUST use State Sentry
3. **Structured Continuity**: Every post-compaction turn MUST check todo
4. **No Re-analysis**: Cannot generate new plans after compaction
5. **Atomic Steps**: next_step MUST be single action
6. **Verification Required**: Step complete ONLY when expected_outcome verified

### Forbidden Patterns

- ❌ "Let me re-analyze the codebase"
- ❌ "Where was I?"
- ❌ "I'll start by understanding the project structure"
- ❌ "also", "additionally", "and" in step descriptions
- ❌ Marking step complete without verification
- ❌ Treating file as written when only discussed

## Testing

To test the continuity framework:

```bash
# 1. Start a long-running task
vibe

# 2. In the session, simulate compaction by:
#    - Generating many tool calls
#    - Creating many files
#    - Running complex analysis

# 3. Force compaction manually (if needed):
#    Continue the conversation until token count approaches threshold

# 4. Verify:
#    - State Sentry is invoked automatically
#    - Observer monitor runs in background
#    - Primary agent resumes from checkpoint
#    - No tasks are lost
```

## Compatibility

| Model | Role | Recommended | Notes |
|-------|------|-------------|-------|
| Devstral-2 (123B) | Primary Architect | ✅ Yes | Complex reasoning, multi-file tasks |
| Devstral Small 2 (24B) | Subagent | ✅ Yes | Fast, cost-effective for background tasks |
| Local models | Subagent | ✅ Yes | Use vLLM or llama.cpp |

## Performance

| Component | Interval | Throughput | Latency |
|-----------|----------|------------|---------|
| Observer Poll | 30s (10s degraded) | 1 poll/interval | < 1s |
| State Sentry | On-demand | ~50 file reads | < 5s |
| Checkpoint Write | After every action | 1 write | < 1s |

## Troubleshooting

### Observer not activating
- Check `~/.vibe/agents/continuation-observer.toml` exists
- Verify `enabled = true` in config
- Check logs in `.observer.log`

### State Sentry not invoked
- Check `~/.vibe/agents/state-sentry.toml` exists
- Verify `auto_approve = true`
- Check ` continuum_config.toml` has `tools.task.permission = "always"`

### Continuity score too low
- Check `.checkpoint.json` is valid JSON
- Verify `.checkpoint.lock` is being updated
- Review `failed_paths[]` entries

### Injection packets not consumed
- Main agent should delete `.observer-inject.json` after reading
- Check main agent has permission to read inject file
- Verify task_id matches between checkpoint and inject

## Version History

- **v2.1.0** (2026-04-20): Initial Vibe 2.0 optimized release
  - Full Agent Skills specification compliance
  - Native subagent integration via task tool
  - Optimized for Devstral-2 model family
  - Security enhancements (trust folder system)

## References

- [Mistral Vibe 2.0 Documentation](https://docs.mistral.ai/mistral-vibe)
- [Agent Skills Specification](https://laurentkempe.com/2026/01/27/Agent-Skills-From-Claude-to-Open-Standard/)
- [Devstral-2 Model Family](https://mistral.ai/news/mistral-vibe-2-0)

## License

Apache 2.0 - Open Source

---

**Maintainer**: This system is designed to be self-maintaining. The observer and state sentry agents will keep the primary agent on track automatically.
