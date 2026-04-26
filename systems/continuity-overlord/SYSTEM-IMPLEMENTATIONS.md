# Continuity Overlord — System Implementation

## Overview

The Continuity Overlord system is a **control-plane** that governs execution, compaction recovery, drift monitoring, and multi-agent team orchestration. It is NOT a normal skill package — it is the governance layer that sits above execution.

The system coordinates skill packages across 4 agents and enforces discipline through a middleware layer that gates all delegation, detects drift, and manages phase transitions.

## System Type

```
continuity-overlord = Control-Plane System (governor)
  └── skill-forge = Runtime System (mode switch)
  └── researchforge/specforge = Pipeline Systems (sequential execution)
```

## Entrypoint

The system activates through the **main-agent** with `ContinuityOverlordMiddleware` injected into the agent loop. There is no single `SKILL.md` entrypoint — the middleware is the entrypoint.

Activation path:
1. `main-agent.toml` loads `vibe-continuity` skill
2. `systems/continuity-overlord/middleware.py` injects `ContinuityOverlordMiddleware` into the agent loop
3. Middleware enforces governance on every turn

## Control-Plane Middleware

`systems/continuity-overlord/middleware.py` — **the core enforcement layer**

This middleware runs in the main agent loop and governs the entire system:

| Function | Mechanism | Trigger |
|----------|------------|--------|
| **Gate delegation** | All `task()` / `Agent` calls routed through `overlord` | Every subagent spawn |
| **Drift detection** | Injects watchdog check every N turns | `turn_count % watchdog_interval == 0` |
| **Loop detection** | Tracks tool call patterns, breaks repeats | Same pattern >= `max_loop_iterations` |
| **Phase gating** | Enforces state-sentry verification between phases | Phase transitions |
| **Compaction recovery** | Auto-triggers `vibe-continuity` + `state-sentry` | "Compaction successful" detected |
| **Destructive gating** | Requires `pattern-prediction` before destructive Bash | `rm`, `git reset`, etc. |
| **Restore guarantees** | Checkpoint state via `get_state()` / `restore_state()` | Session resume |

## Agents

| Agent | TOML | Prompt | Role |
|-------|------|--------|------|
| `main-agent` | `agents/main-agent.toml` | `prompts/main.md` | Primary architect + middleware host |
| `watchdog` | `agents/watchdog.toml` | `prompts/watchdog.md` | Turn-by-turn drift detection, loop prevention, pattern prediction |
| `state-sentry` | `agents/state-sentry.toml` | `prompts/state-sentry.md` | Post-compaction state reconstruction, adversarial review |
| `overlord` | `agents/overlord.toml` | `prompts/overlord.md` | Supreme orchestrator — gates all Sub-Team delegation |

## Skill Packages (22 total)

These are the skill packages coordinated by the system, distributed across agents:

### Main-Agent (2 packages)

| Skill Package | Contents | Purpose |
|---------------|-----------|---------|
| `vibe-continuity` | `SKILL.md` | Restores state after compaction |
| `mistral-vibe-compaction-skill` | `SKILL.md`, `agent.toml`, `system-prompt.md`, `middleware.py`, schemas, docs | Full compaction recovery with checkpoint management |

### Watchdog (7 packages)

| Skill Package | Purpose |
|---------------|---------|
| `anti-loop-debug` | Detects and breaks infinite loops |
| `behavior-audit` | Audits agent behavior for drift |
| `pattern-prediction` | Predicts patterns and impact before execution |
| `focus-guard` | Guards against focus drift |
| `focus-master` | Master focus management |
| `tool-dominator` | Master tool usage patterns |
| `tool-primacy` | Establishes tool priority |

### State-Sentry (7 packages)

| Skill Package | Purpose |
|---------------|---------|
| `context-guardian` | Guards context boundaries |
| `memory-archivist` | Archives and retrieves memories |
| `constraint-enforcer` | Enforces system constraints |
| `code-quality` | Maintains code quality standards |
| `self-corrector` | Self-correcting behavior loops |
| `verification-enforcer` | Enforces verification gates |
| `verification-master` | Master verification workflows |

### Overlord (6 packages)

| Skill Package | Purpose |
|---------------|---------|
| `overlord` | Supreme orchestrator for distributed team harness |
| `git-integrator` | Git operations and integration |
| `multi-file-coordinator` | Coordinates multi-file operations |
| `meta-optimizer` | Optimizes meta-workflows |
| `task-decomposer` | Breaks down complex tasks |
| `test-runner` | Test execution and reporting |

## Agent Skill Mapping

```
main-agent (hosts middleware)
├── vibe-continuity
└── mistral-vibe-compaction-skill

watchdog (7 packages)
├── anti-loop-debug
├── behavior-audit
├── pattern-prediction
├── focus-guard
├── focus-master
├── tool-dominator
└── tool-primacy

state-sentry (7 packages)
├── context-guardian
├── memory-archivist
├── constraint-enforcer
├── code-quality
├── self-corrector
├── verification-enforcer
└── verification-master

overlord (6 packages)
├── overlord
├── git-integrator
├── multi-file-coordinator
├── meta-optimizer
├── task-decomposer
└── test-runner
```

## Middleware Installation

The `ContinuityOverlordMiddleware` is installed into the main agent loop at startup:

```python
from systems.continuity-overlord.middleware import inject_middleware

# In agent loop initialization:
agent_loop = inject_middleware(agent_loop)
```

This wraps `pre_turn()` and `post_turn()` with control-plane enforcement:
- Turn counting and interval checks
- Watchdog drift detection triggers
- Overlord delegation audits
- Loop detection and anti-loop triggers
- Compaction recovery auto-triggers

## Execution Flow (with Middleware Enforcement)

### 1. Session Start / Compaction Recovery

```
Session Start
  ↓
main-agent reads .checkpoint.json
  ↓
ContinuityOverlordMiddleware.pre_turn() checks state
  ↓
IF "Compaction successful":
  → /vibe-continuity (skill package)
  → task(agent="state-sentry", task="Verify state")
  → state-sentry reads checkpoint + inspects filesystem
  → Returns: continuity_status, current_objective, next_verified_step
  → main-agent resumes from next_verified_step
```

### 2. Turn-by-Turn (Middleware Enforced)

```
Every N turns (watched by middleware):
  → middleware injects watchdog check
  → task(agent="watchdog", task="Drift check")
  → watchdog activates: behavior-audit, pattern-prediction, anti-loop-debug
  → If drift detected: adjust plan, kill runaway loops
  → If stall detected: anti-loop-debug triggers new path

Every M turns (watched by middleware):
  → middleware injects overlord audit
  → /overlord to delegate complex tasks
```

### 3. Team Delegation (Gated by Middleware)

```
Complex task encountered
  ↓
ContinuityOverlordMiddleware intercepts task() call
  ↓
Middleware CHECK: Is this coming from overlord?
  ├── YES → Allow delegation
  └── NO → Redirect to overlord agent
  ↓
overlord agent selects optimal Sub-Team:
  ├── team-dev: Heavy coding, refactoring, implementation
  ├── team-ops: Git operations, filesystem, tooling
  └── team-verify: Adversarial audit, verification, logic checks
  ↓
Synthesize reports → Verify evidence → Mark task complete
```

## Key Behaviors

| Behavior | Mechanism | Trigger |
|-----------|------------|--------|
| **Compaction Recovery** | `vibe-continuity` → `state-sentry` | After "Compaction successful" |
| **Drift Detection** | Middleware + `watchdog` + 7 skill packages | Every N turns |
| **Loop Prevention** | Middleware detects → `anti-loop-debug` | Repeated tool pattern |
| **Impact Prediction** | Middleware gating → `pattern-prediction` | Before destructive commands |
| **Team Delegation** | Middleware gates → `overlord` → Sub-Teams | Complex multi-role tasks |
| **State Verification** | `state-sentry` | Session resume / phase transitions |

## Core Principles

- **Checkpoint is truth** — `.checkpoint.json` is the ground state
- **Watchdog is governor** — enforces velocity limits, pattern checks
- **Middleware is authority** — all enforcement flows through the control plane
- **Skills are brakes** — `anti-loop-debug`, `pattern-prediction`, `vibe-continuity`
- **Overlord delegates** — never do sub-agent work yourself
- **Evidence mandate** — never claim "done" without file verification |
