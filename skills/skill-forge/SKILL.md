---
name: skill-forge
description: |
trigger: when creating new skills
  Interactive assistant for creating, testing, and installing mistral-vibe skills, agents, loops, and workflows.
  Debug user-created skills with step-by-step interactive guidance. Enforces hard gating via custom middleware.
  Saves and restores existing agent loops and middleware with labeled persistence.
  Uses runtime activation: intercepted before normal skill execution for deterministic mode switch.
user-invocable: true
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Write
  - Edit
  - Skill
  - Agent
  - EnterPlanMode
  - ExitPlanMode
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - TaskStop
  - WebFetch
  - WebSearch
  - PushNotification
  - CronCreate
  - CronDelete
  - CronList
  - ScheduleWakeup
  - NotebookEdit
  - RemoteTrigger
  - EnterWorktree
  - ExitWorktree
  - Monitor
activation:
  type: runtime
  entrypoint: skills.skill-forge.agent_loop:enter_skill_forge
  exitpoint: skills.skill-forge.agent_loop:exit_skill_forge
---

# Skill Forge

Interactive skill/agent/loop/workflow creation and debugging assistant with hard gating and state persistence.

## When to Use
- Creating new mistral-vibe skills, agents, loops, or workflows.
- Debugging user-created skills that aren't working as intended.
- Needing step-by-step interactive guidance for skill development.

## What Gets Created (File Formats)

### Skill (SKILL.md)
A skill lives in `skills/<name>/SKILL.md` with YAML frontmatter + markdown body:

```markdown
---
name: my-skill
description: |
  What this skill does, in plain sentences.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  # only list tools the skill actually needs
activation:
  type: command          # or "runtime" for mode-switching skills
---

# My Skill

What the agent should do when this skill is invoked.
List concrete steps. Reference actual tool names.
```

Rules:
- `name` must be lowercase with hyphens only (`my-skill`, not `MySkill`)
- `description` is required — used in skill listings
- `allowed-tools` restricts what tools the skill can call
- `user-invocable: true` means users can trigger it with `/my-skill`
- `activation.type: runtime` is for skills that take over the agent loop (like skill-forge itself)

### Agent (agents/<name>.toml)
An agent profile that wraps a system prompt + tool set + behavior settings:

```toml
name = "my-agent"
system_prompt = "my-agent-system"
model = "devstral-2"
temperature = 0.1
max_tokens = 4096
thinking = "off"

[tools]
allowed = [
    "Bash",
    "Read",
    "Write",
    "Skill",
]

[behavior]
auto_continue = false
max_iterations = 50
require_user_confirmation = true

[middleware]
custom_middleware = "skills/my-skill/middleware.py:MyMiddleware"
load_on_invoke = true
stash_existing = true
```

Rules:
- `system_prompt` must match a file in `prompts/<system_prompt>.md`
- `custom_middleware` is optional — only if the agent needs gating/hooks
- `stash_existing = true` saves and restores the previous middleware stack
- `load_on_invoke = true` means middleware only loads when this agent runs

### Prompt (prompts/<name>.md)
The system prompt that controls agent behavior:

```markdown
You are the My Agent assistant — brief description of role.

## Principles
1. **Rule one** — explain it clearly
2. **Rule two** — explain it clearly

## Steps
### Step 1: Do something
Concrete instruction with tool names.

### Step 2: Do something else
Wait for user confirmation before proceeding.

## Important
- Use AskUserQuestion for user choices, never assume
- Name actual tools (Bash, Read, Write), not placeholders
```

Rules:
- Keep it short — the model reads this every turn
- Name concrete tools, not abstract descriptions
- Use `AskUserQuestion` for any user choice, never free-form guessing

### Loop/Workflow (config.toml additions)
A loop ties agents + skills + middleware into a coordinated system:

```toml
agent_paths = ["agents", "agents/my-system"]
enabled_agents = ["my-overseer", "my-worker"]
enabled_skills = ["my-skill", "my-other-skill"]

[middleware]
enabled = ["tool_use", "custom"]
custom_path = "skills/my-system/middleware.py"
```

---

## Interactive Workflow (After Activation)

The runtime calls `enter_skill_forge()` which:
1. **Saves** current state to `~/.vibe/skill-forge-state/current_session.json`
2. **Clears** middleware pipeline (saves live objects for restore)
3. **Loads** `SkillForgeMiddleware` into pipeline
4. **Switches** to `skill-forge-agent` loop
5. **Stages** all new artifacts to `~/.vibe/skill-forge-state/staging/<session_id>/`

### Phase1: Goal Elicitation
Ask user to choose:
- Create new: skill / agent / loop+agents+skills / workflow
- Debug existing component

### Phase2: Requirements Gathering
For **skills**: name (lowercase-hyphens), description, allowed tools, user-invocable flag, activation type.
For **agents**: name, system_prompt filename, model, temperature, tools, middleware needs.
For **loops**: which agents + skills to wire together, middleware chain, config.toml changes.

Validate inputs. Wait for confirmation.

### Phase3: Construction
Create files in **staging** (NOT live paths):

| Component | Staging Path | Live Path (on Apply) |
|-----------|--------------|----------------------|
| Skill | `staging/skills/<name>/SKILL.md` | `~/.vibe/skills/<name>/SKILL.md` |
| Agent | `staging/agents/<name>.toml` | `~/.vibe/agents/<name>.toml` |
| Prompt | `staging/prompts/<name>.md` | `~/.vibe/prompts/<name>.md` |
| Config | `staging/config.toml` | `~/.vibe/config.toml` (merged) |

Wait for confirmation.

### Phase4: Functional Verification
Test beyond syntax:
1. **Discovery** — `vibe skill list` shows the skill
2. **Invocation** — `/skill-name` triggers the skill
3. **Agent** — `vibe --agent my-agent` loads the agent profile
4. **Integration** — agent + skill + middleware work together without errors

Wait for confirmation.

### Phase5: Install or Save
Run validation on staged artifacts. Then prompt user:

| Choice | What Happens |
|--------|---------------|
| **Apply** | Copy staging → live paths, restore previous runtime |
| **Save only** | Keep staging in `saved/<label>/`, exit or stay in forge |
| **Discard** | Save to `saved/discarded-<id>/`, restore previous runtime |
| **Continue** | Return to Phase1 with a new goal |

---

## Hard Gating Rules
- Middleware blocks turns until user confirms via `AskUserQuestion`
- No skipping phases without user confirmation
- No information dumping: provide only current phase info
- Ask clarifying questions if user input is ambiguous

## State Persistence
- **Staging**: `~/.vibe/skill-forge-state/staging/<session_id>/`
- **Saved**: `~/.vibe/skill-forge-state/saved/<label>/` (includes discarded work)
- **Current state**: `~/.vibe/skill-forge-state/current_session.json`
- **Live objects** saved for same-process restore (fast path)
- **Disk descriptors** for crash/restart recovery
- Restored exactly on cleanup, preserving integrity
- Discarded work is saved (not deleted) for later use/refinement
