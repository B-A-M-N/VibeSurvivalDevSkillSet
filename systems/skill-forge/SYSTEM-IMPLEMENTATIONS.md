# SkillForge — System Implementation

## Overview

SkillForge is an interactive workflow skill for creating, testing, and installing mistral-vibe skills, agents, loops, and workflows. It uses runtime activation with hard gating and transactional staging to safely build new components.

## Agent

| Agent | TOML | Prompt | Role |
|-------|------|--------|------|
| `skill-forge-agent` | `agents/skill-forge-agent.toml` | `prompts/skill-forge-system.md` | Guides user through skill/agent creation workflow |

## Skill Package: `skill-forge`

The `skill-forge` package is a runtime-activated workflow skill. `SKILL.md` is the entrypoint that defines activation behavior. The remaining files implement the controlled loop, gating, and staging logic.

| File | Role |
|------|------|
| `SKILL.md` | Entrypoint — defines skill metadata, activation type (`runtime`), entrypoint/exitpoint hooks |
| `agent_loop.py` | Execution logic — `enter_skill_forge()` and `exit_skill_forge()` manage runtime transitions |
| `middleware.py` | Enforcement layer — `SkillForgeMiddleware` enforces hard gating and user confirmation per turn |
| `core_patch.py` | System patches — integrates runtime activation into the core system |
| `agent_loop_patch.py` | Loop patches — modifies agent loop for controlled execution |
| `agent_loop_patch.txt` | Patch reference — human-readable diff of agent loop changes |
| `__init__.py` | Package init — exposes the skill module |
| `SKILL-IMPLEMENTATIONS.md` | Documents how the skill package works as a system component |

## Architecture

```
User: /skill-forge
  ↓
SkillManager.intercept() → activation.type = "runtime"
  ↓
enter_skill_forge()                     [agent_loop.py]
  ↓
Snapshot current runtime (middleware stack, agent profile, config)
  ↓
Clear middleware pipeline (save live objects for same-process restore)
  ↓
Inject SkillForgeMiddleware             [middleware.py]
  ↓
Switch to skill-forge-agent profile
  ↓
┌──────────────────────────────────────────┐
│  Controlled Loop (SkillForgeMiddleware  │
│  enforces gating per turn):              │
│     Phase 1: Goal Elicitation            │
│     Phase 2: Requirements Gathering     │
│     Phase 3: Construction (staged)      │
│     Phase 4: Functional Verification     │
│     Phase 5: Install / Validate         │
└──────────────────────────────────────────┘
  ↓
exit_skill_forge()                     [agent_loop.py]
  ↓
Commit OR Discard staged artifacts
  ↓
Restore middleware stack (live objects)
  ↓
Restore agent profile
```

## Controlled Loop Phases

### Phase 1: Goal Elicitation
```
skill-forge agent prompts user for:
  - Component type (skill, agent, prompt, loop)
  - Purpose and description
  - Target use cases
Output: Goal statement captured
```

### Phase 2: Requirements Gathering
```
skill-forge agent collects:
  - Tool requirements
  - Permission needs
  - Agent type (for agents)
  - Skill activation type
  - User-invocable flag
Output: Requirements document
```

### Phase 3: Construction (Staged)
```
skill-forge agent builds artifacts:
  - Generates SKILL.md with frontmatter
  - Generates agent.toml (if agent)
  - Generates prompt.md (if prompt)
Output: Staged in ~/.vibe/skill-forge-state/staging/<id>/
```

### Phase 4: Functional Verification
```
skill-forge agent verifies:
  - Syntax checks
  - Frontmatter validation
  - Tool permission consistency
  - Required file presence
Output: Verification report
```

### Phase 5: Install / Validate
```
User chooses exit action:
  - Apply: Commit staged → live paths, restore runtime
  - Save only: Keep in saved/<label>/, exit or stay
  - Discard: Save to saved/discarded-<id>/, restore runtime
  - Continue: Return to Phase 1
```

## Exit Actions

| Choice | Behavior |
|--------|-----------|
| **Apply** | Commit staged → live paths, restore runtime |
| **Save only** | Keep in `saved/<label>/`, exit or stay |
| **Discard** | Save to `saved/discarded-<id>/`, restore runtime |
| **Continue** | Return to Phase 1 |

## Runtime Execution Model

SkillForge operates as a controlled runtime mode. These four phases define HOW it works:

1. **Snapshot** — save current runtime state (middleware stack, agent profile, config)
2. **Swap** — inject SkillForgeMiddleware (hard gating) + switch to skill-forge-agent profile
3. **Execute** — run guided, gated workflow (Goal → Requirements → Construction → Verification → Install)
4. **Restore** — deterministically reconstruct previous runtime (commit/discard staged artifacts, restore middleware, restore agent)

---

## What SkillForge Produces

SkillForge is a forge/installer environment for Vibe extension artifacts. It stages, validates, and installs:

| Artifact Type | Format | Staging Path |
|---------------|--------|--------------|
| Skill | `SKILL.md` (+ optional `middleware.py`, `agent_loop.py`, scripts) | `~/.vibe/skill-forge-state/staging/<id>/skills/<name>/` |
| Agent | `agents/<name>.toml` | `~/.vibe/skill-forge-state/staging/<id>/agents/` |
| Prompt | `prompts/<name>.md` | `~/.vibe/skill-forge-state/staging/<id>/prompts/` |
| Config | `config.toml` additions | `~/.vibe/skill-forge-state/staging/<id>/` |
| Middleware | `middleware.py` | Inside skill package or as standalone |
| Workflow/Loop | config definitions | `~/.vibe/skill-forge-state/staging/<id>/` |

SkillForge can generate and validate runtime-activated skills when appropriate, but it is not limited to runtime skills and should not be treated as the canonical runtime-skill pattern. It is a standalone system for safely authoring and installing Vibe extension artifacts.
