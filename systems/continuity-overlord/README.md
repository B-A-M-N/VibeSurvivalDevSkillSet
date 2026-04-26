# Continuity & Overlord System
# 22 Skills — 4 Agents

Complete agent system for continuity-aware execution, compaction recovery, drift monitoring, and multi-agent team orchestration.

## What's Included

| Type | Files | Count |
|------|-------|-------|
| Skills | 22 total (see list below) | 22 skills |
| Agents | `main-agent.toml`, `watchdog.toml`, `state-sentry.toml`, `overlord.toml` | 4 agents |
| Prompts | `main.md`, `watchdog.md`, `state-sentry.md`, `overlord.md` | 4 prompts |
| Docs | `mistral-vibe-compaction-skill/` extras | 7 files |

### Skill Distribution by Agent

| Agent | Skills | Count |
|-------|--------|-------|
| **main-agent** | `vibe-continuity` | 1 |
| **watchdog** | `anti-loop-debug`, `behavior-audit`, `pattern-prediction`, `focus-guard`, `focus-master`, `tool-dominator`, `tool-primacy` | 7 |
| **state-sentry** | `context-guardian`, `memory-archivist`, `constraint-enforcer`, `code-quality`, `self-corrector`, `verification-enforcer`, `verification-master` | 7 |
| **overlord** | `overlord`, `git-integrator`, `multi-file-coordinator`, `meta-optimizer`, `task-decomposer`, `test-runner` | 6 |

### Full Skill List (22)

1. `anti-loop-debug` — detects and breaks infinite loops
2. `behavior-audit` — audits agent behavior for drift
3. `code-quality` — maintains code quality standards
4. `constraint-enforcer` — enforces system constraints
5. `context-guardian` — guards context boundaries
6. `focus-guard` — guards against focus drift
7. `focus-master` — master focus management
8. `git-integrator` — git operations and integration
9. `memory-archivist` — archives and retrieves memories
10. `meta-optimizer` — optimizes meta-workflows
11. `mistral-vibe-compaction-skill` — compaction recovery (extra docs in folder)
12. `multi-file-coordinator` — coordinates multi-file operations
13. `overlord` — supreme orchestrator for distributed team harness
14. `pattern-prediction` — predicts patterns and issues
15. `self-corrector` — self-correcting behavior loops
16. `task-decomposer` — breaks down complex tasks
17. `test-runner` — test execution and reporting
18. `tool-dominator` — master tool usage patterns
19. `tool-primacy` — establishes tool priority
20. `verification-enforcer` — enforces verification gates
21. `verification-master` — master verification workflows
22. `vibe-continuity` — restores state after compaction

## Architecture

```
Main Agent (continuation-main) — 1 skill: vibe-continuity
  ├── /vibe-continuity (compaction recovery)
  │     → task(agent="state-sentry", task="Verify state")
  │     → Reads .checkpoint.json → Returns next_step
  │
  ├── watchdog agent — 7 skills: anti-loop-debug, behavior-audit,
  │     pattern-prediction, focus-guard, focus-master,
  │     tool-dominator, tool-primacy
  │     → Turn-by-turn drift detection
  │     → Every N turns: mandatory self-check
  │     → Triggers anti-loop-debug on stall
  │
  ├── state-sentry agent — 7 skills: context-guardian, memory-archivist,
  │     constraint-enforcer, code-quality, self-corrector,
  │     verification-enforcer, verification-master
  │     → Post-compaction reconstruction
  │     → Verifies file artifacts exist
  │     → Rebuilds mental model from checkpoint
  │
  └── overlord agent — 6 skills: overlord, git-integrator,
        multi-file-coordinator, meta-optimizer, task-decomposer,
        test-runner
        → Supreme orchestrator for distributed team harness
        → Resolves cross-agent conflicts
        → Selects optimal Sub-Team for specialized tasks
        └── Team Sub-Agents (delegated by overlord):
             ├── team-dev (coding & refactoring)
             ├── team-ops (infrastructure & git)
             └── team-verify (adversarial audit & verification)
```

## Execution Graph

```
Session Start / Compaction Event
  ↓
Main Agent reads .checkpoint.json
  ↓
IF "Compaction successful":
  → /vibe-continuity
  → task(agent="state-sentry", task="Verify state")
  → Consume report, resume from next_step
  ↓
Each N turns:
  → task(agent="watchdog", task="Drift check")
  ↓
On complex task:
  → /overlord
  → Delegate to team-dev / team-ops / team-verify
  ↓
Task complete:
  → Update .checkpoint.json
  → Resume main loop
```

## Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts

# 22 skills
for s in anti-loop-debug behavior-audit code-quality constraint-enforcer \
  context-guardian focus-guard focus-master git-integrator \
  memory-archivist meta-optimizer mistral-vibe-compaction-skill \
  multi-file-coordinator overlord pattern-prediction self-corrector \
  task-decomposer test-runner tool-dominator tool-primacy \
  verification-enforcer verification-master vibe-continuity; do
  cp -r skills/$s ~/.vibe/skills/
done

# 4 agents
cp agents/main-agent.toml ~/.vibe/agents/
cp agents/watchdog.toml ~/.vibe/agents/
cp agents/state-sentry.toml ~/.vibe/agents/
cp agents/overlord.toml ~/.vibe/agents/

# 4 prompts
cp prompts/main.md ~/.vibe/prompts/
cp prompts/watchdog.md ~/.vibe/prompts/
cp prompts/state-sentry.md ~/.vibe/prompts/
cp prompts/overlord.md ~/.vibe/prompts/

# Config
cp config.toml ~/.vibe/config.toml
```

Enable in `~/.vibe/config.toml`:
```toml
agent_paths = ["agents"]
enabled_agents = [
  "continuation-main",
  "watchdog",
  "state-sentry",
  "overlord",
  "team-dev",
  "team-ops",
  "team-verify",
]
enabled_skills = [
  "anti-loop-debug", "behavior-audit", "code-quality",
  "constraint-enforcer", "context-guardian", "focus-guard",
  "focus-master", "git-integrator", "memory-archivist",
  "meta-optimizer", "mistral-vibe-compaction-skill",
  "multi-file-coordinator", "overlord", "pattern-prediction",
  "self-corrector", "task-decomposer", "test-runner",
  "tool-dominator", "tool-primacy", "verification-enforcer",
  "verification-master", "vibe-continuity",
]
```

## Key Behaviors

| Behavior | Mechanism | Agent | Trigger |
|-----------|------------|-------|--------|
| Compaction Recovery | `vibe-continuity` → `state-sentry` subagent | main-agent | After "Compaction successful" |
| Drift Detection | Monitors turn-by-turn | watchdog | Every N turns |
| State Reconstruction | Reads `.checkpoint.json` | state-sentry | Session resume / post-compaction |
| Team Delegation | `overlord` dispatches to sub-agents | overlord | Complex multi-role tasks |
| Code Review | Adversarial audit | team-verify | After implementation |

## Core Principles

- **Checkpoint is truth** — `.checkpoint.json` is the ground state
- **Watchdog is governor** — enforces velocity limits, pattern checks
- **Skills are brakes** — `anti-loop-debug`, `pattern-prediction`, `vibe-continuity`
- **Overlord delegates** — never do sub-agent work yourself
