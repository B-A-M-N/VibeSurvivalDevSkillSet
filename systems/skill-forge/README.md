# SkillForge System

Interactive assistant for creating, testing, and installing mistral-vibe skills, agents, loops, and workflows. Uses runtime activation with hard gating and transactional staging.

## What's Included

| Type | Files | Count |
|------|-------|-------|
| Skill | `skills/skill-forge/SKILL.md` + middleware.py + agent_loop.py | 1 skill |
| Agent | `agents/skill-forge-agent.toml` | 1 agent |
| Prompt | `prompts/skill-forge-system.md` | 1 prompt |

## Architecture

```
User: /skill-forge
  ↓
SkillManager.intercept() → activation.type = "runtime"
  ↓
enter_skill_forge()
  ↓
Snapshot current runtime (middleware stack, agent profile, config)
  ↓
Clear middleware pipeline (save live objects for same-process restore)
  ↓
Inject SkillForgeMiddleware (hard gating)
  ↓
Switch to skill-forge-agent profile
  ↓
┌──────────────────────────────────────────┐
│  Controlled Loop (SkillForgeMiddleware  │
│  enforces gating per turn):              │
│     Phase1: Goal Elicitation             │
│     Phase2: Requirements Gathering      │
│     Phase3: Construction (staged)       │
│     Phase4: Functional Verification      │
│     Phase5: Install / Validate          │
└──────────────────────────────────────────┘
  ↓
exit_skill_forge()
  ↓
Commit OR Discard staged artifacts
  ↓
Restore middleware stack (live objects)
  ↓
Restore agent profile
```

## Execution Graph

```
User: /skill-forge
  ↓
RuntimeActivation (SkillManager intercepts)
  ↓
enter_skill_forge()

Runtime Transition:
  ├─ Snapshot current runtime (middleware, agent, config)
  ├─ Clear middleware pipeline (save live objects for same-process restore)
  ├─ Inject SkillForgeMiddleware
  ├─ Switch to skill-forge agent profile
  └─ Enter controlled loop

Controlled Loop:
  SkillForgeMiddleware (hard gating, enforces user confirmation)
     ↓
  skill-forge agent (guided workflow)
     ↓
  staged artifact generation (skills/, agents/, prompts/)

Exit:
  exit_skill_forge()
     ↓
  Commit OR Discard staged artifacts
     ↓
  Restore middleware stack (live objects)
     ↓
  Restore agent profile
     └─ Cleanup runtime state
```

## Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -r skills/skill-forge ~/.vibe/skills/
cp agents/skill-forge-agent.toml ~/.vibe/agents/
cp prompts/skill-forge-system.md ~/.vibe/prompts/
```

Enable in `~/.vibe/config.toml`:
```toml
enabled_agents = ["skill-forge-agent"]
enabled_skills = ["skill-forge"]
```

## What You Can Create

| Component | Format | Staging Path |
|------------|--------|--------------|
| Skill | `SKILL.md` with YAML frontmatter | `~/.vibe/skill-forge-state/staging/<id>/skills/<name>/` |
| Agent | `agents/<name>.toml` | `~/.vibe/skill-forge-state/staging/<id>/agents/` |
| Prompt | `prompts/<name>.md` | `~/.vibe/skill-forge-state/staging/<id>/prompts/` |
| Loop/Workflow | `config.toml` additions | `~/.vibe/skill-forge-state/staging/<id>/` |

## Exit Actions

| Choice | Behavior |
|--------|-----------|
| **Apply** | Commit staged → live paths, restore runtime |
| **Save only** | Keep in `saved/<label>/`, exit or stay |
| **Discard** | Save to `saved/discarded-<id>/`, restore runtime |
| **Continue** | Return to Phase1 |

## Generalized Pattern

SkillForge implements a reusable pattern for runtime-activated skills:

1. **Snapshot** — save current runtime state
2. **Swap** — inject custom middleware + switch agent profile
3. **Execute** — run controlled loop with hard gating
4. **Restore** — deterministically reconstruct previous runtime

Any skill can adopt this pattern by setting `activation.type: runtime` and providing `entrypoint`/`exitpoint` hooks.
