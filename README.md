# Vibe Survival Dev Skill Set

A practical survival kit for understanding, extending, and actually using Mistral Vibe as a moddable coding-agent runtime.
!!DISCLAIMER: THE CONCEPTS HERE ARE BOTH ARCHITECTURALLY AND IMPLEMENTATION WISE, WRONG. THIS EXISTS SOLELY AS A CONCEPTUAL REPRESENTATION OF HOW THIS *COULD* WORK. THESE WILL ALL EVENTUALLY BE MADE AND IMPLEMENTED INTO FULL WORKING MISTRAL-VIBE WORKFLOWS AND DOCUMENTED: https://github.com/BAMN-LABs!!
[![GitHub stars](https://img.shields.io/github/stars/B-A-M-N/VibeSurvivalDevSkillSet?style=flat-square)](https://github.com/B-A-M-N/VibeSurvivalDevSkillSet)
[![License](https://img.shields.io/github/license/B-A-M-N/VibeSurvivalDevSkillSet?style=flat-square)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/B-A-M-N/VibeSurvivalDevSkillSet?style=flat-square)](https://github.com/B-A-M-N/VibeSurvivalDevSkillSet/commits/main)

## Table of Contents

- [What This Repo Is](#what-this-repo-is)
- [Why This Exists](#why-this-exists)
- [Not Just a Skill Pack](#not-just-a-skill-pack)
- [Start Here](#start-here)
- [What This Repo Contains](#what-this-repo-contains)
- [The Important Mental Model](#the-important-mental-model)
- [Why People Overlook Mistral-Vibe](#why-people-overlook-mistral-vibe)
- [How Vibe Finds This Stuff](#how-vibe-finds-this-stuff)
- [Setup Tiers](#setup-tier1-simple)
  - [Tier 1: Simple](#setup-tier1-simple)
  - [Tier 2: Advanced](#setup-tier2-advanced)
  - [Tier 3: Pro](#setup-tier3-pro)
- [Project-Local Install](#project-local-install-instead-of-global)
- [Recommended Rollout Path](#recommended-rollout-path)
- [Pipeline Tier 4: SpecForge](#pipeline-tier-4-specforge--specification-factory)
- [Pipeline Tier 5: ResearchForge](#pipeline-tier-5-researchforge--research-only-factory)
- [Pipeline Tier 6: SkillForge](#pipeline-tier-6-skillforge--interactive-skillagentloop-factory)
- [Pipeline Tier 7: CodeForge](#pipeline-tier-7-codeforge--implementation-factory)
- [Pipeline Tier 8: DebugForge](#pipeline-tier-8-debugforge--debugging-factory)
- [Pipeline Tier 9: DocForge](#pipeline-tier-9-docforge--documentation-factory)
- [Pipeline Tier 10: ShipForge](#pipeline-tier-10-shipforge--deployment-factory)
- [Pipeline Tier 11: TestForge](#pipeline-tier-11-testforge--test-generation-factory)
- [Pipeline Tier 12: ReactiveForge](#pipeline-tier-12-reactiveforge--reactive-middleware)
- [How To Create Your Own Specialized Loop](#how-to-create-your-own-specialized-loop)
- [Practical Notes](#practical-notes)
- [Suggested First Things To Read](#suggested-first-things-to-read)


---

## What This Repo Is

Mistral Vibe is extremely powerful, but the path to using it well is not obvious.

This repo exists because Vibe is not just "a coding agent."
It is closer to a moddable agent runtime.

That is why this project includes skills, agents, prompts, middleware, loops, and source-level patterns together. The goal is not to replace Vibe, but to show what becomes possible when you treat Vibe as an extensible system instead of a normal CLI coding assistant.

## Why This Exists

Mistral Vibe is one of the most capable and under-discussed coding agent runtimes available right now.

The problem is not lack of power.

The problem is discoverability.

Many of Vibe's strongest capabilities only become obvious once you understand how its prompts, skills, agents, middleware, and execution loop fit together. That learning curve is steep enough that people can easily miss what makes Vibe special.

This repo tries to make that path clearer.

## Not Just a Skill Pack

This repo contains skills, but it is not merely a skill pack.

A normal skill pack gives Vibe procedures to read.

This repo is different: it documents and demonstrates a broader way of thinking about Vibe as a customizable agent runtime. The included skills are examples of how to structure higher-level behavior, but the real lesson is the architecture around them.

## Start Here

If you want the shortest path to understanding:

1. Read [docs/START-HERE.md](./docs/START-HERE.md)
2. Read [docs/REPO-MAP.md](./docs/REPO-MAP.md)
3. If you want to know what is internal versus required, skim [docs/INTERNAL-NOTES.md](./docs/INTERNAL-NOTES.md)
4. Pick one example:
   - [examples/simple/README.md](./examples/simple/README.md)
   - [examples/advanced/README.md](./examples/advanced/README.md)
   - [examples/pro/README.md](./examples/pro/README.md)

## What This Repo Contains

- `skills/`
  Contains the specialized skill library: continuity, anti-loop, verification, orchestration, focus, and related helpers.
- `skills/mistral-vibe-compaction-skill/`
  Contains the deeper continuity framework docs and reference artifacts: observer spec, inject packet schema, state schema, execution-and-drift notes, and related design docs.
- `agents/`
  Contains the custom agent profiles:
  - `main-agent.toml`
  - `watchdog.toml`
  - `state-sentry.toml`
  - `team-dev.toml`
  - `team-ops.toml`
  - `team-verify.toml`
- `prompts/`
  Contains the prompts used by the main continuity loop and the supporting subagents.
- `systems/`
  Contains full pipeline systems (SpecForge, ResearchForge, SkillForge) with their own agents, prompts, and skills organized per system.
- `docs/`
  Contains deeper architecture and behavior docs if you want the full rationale, not just the install steps.
- `examples/`
  Contains copyable setup patterns for simple, advanced, and pro-level installs.
  Each example also includes a starter `config.toml`.

## The Important Mental Model

Mistral Vibe does not use skills the way a lot of other CLI agents do.

In practice, advanced behavior comes from the combination of:

1. a custom agent profile in `agents/*.toml`
2. a matching prompt in `prompts/*.md`
3. one or more skills in `skills/*/SKILL.md`
4. runtime discovery through either `~/.vibe/` or project-local `.vibe/`

That means "installing a skill system" is really "installing a runtime topology."

If you want:

- only better commands and workflows: install skills
- better continuity and compaction recovery: install skills + prompts + custom agents
- orchestrated teams and specialized loops: install the whole system

## Why People Overlook Mistral-Vibe

Most people overlook Vibe not because it's weak, but because using it well requires **mental model shifts** that clash with how they think about AI coding assistants.

You don't realize these shifts are needed until you've already built something on top of Vibe — and then they become obvious all at once.

---

### The 10 Non-Obvious Truths

**1. The agent is not the system — the loop is**

People think: `agent = intelligence`. Reality: `AgentLoop = system`. Behavior doesn't live in the agent. It emerges from the loop + constraints.

> Once you see this, you stop trying to "fix the agent" and start shaping the loop.

**2. Tools are the real execution engine**

The model never actually does anything. Tools do everything. Model = planner. Tools = executor. AgentLoop = bridge.

> If you control tools (and tool access), you control behavior more reliably than prompt engineering.

**3. Subagents are just tools with memory**

`task()` spawns another AgentLoop. Subagents = nested loops, not magical second brains.

> Multi-agent systems in Vibe are just composed loops. You don't need a new architecture — you compose loops.

**4. Middleware is the only enforcement layer**

Prompts advise. Skills suggest. Middleware enforces. Nothing else in Vibe can reliably block, modify, or audit behavior.

> Middleware is the only place you can guarantee outcomes. Everything else is advisory.

**5. State is leverage, not memory**

State only matters if something uses it to change behavior. Raw state = logs. State + middleware = leverage.

> Recent commands → drift detection. Files modified → verification gating. Errors → retry logic.

**6. Skills are triggers, not behavior**

In Vibe: `skill = structured prompt + activation condition`. Skills shape what the model *tries* to do. They don't enforce outcomes.

> Skills shape intent. Middleware enforces outcome. That distinction changes how you architect systems.

**7. Runtime topology is the real abstraction**

"Installing a skill system" is really "installing a runtime topology." Behavior = arrangement of loop + middleware + tools + agents + prompts.

> You don't build features — you assemble systems.

**8. There are two kinds of intelligence**

1. Execution intelligence (main agent, worker agents)
2. Governance intelligence (middleware + control agents)

Most people only think about (1). Your repo introduces (2): watchdog, state-sentry, overlord.

> You can separate "doing the work" from "deciding if the work is acceptable."

**9. The system is only as strong as its contracts**

Everything works because of stable contracts:

```
tool.execute(name, args) → result
middleware.on_* → decision
agent_loop → propose/execute cycle
```

Swap anything. Everything composes. Break the contracts, everything becomes fragile.

> Modularity comes from stable boundaries, not flexibility.

**10. You can control behavior without touching the model**

With this repo's approach:

- You didn't change the model
- You didn't fine-tune anything
- You didn't rewrite Vibe

But you changed behavior dramatically.

> You can build reliable systems *around* unreliable models. That's the whole point of the control-plane pattern.

---

### The Meta Insight

All 10 shifts collapse into one:

```
Mistral Vibe is not an AI system.
It is a control system that happens to use an AI model.
```

Most people are looking for "a better AI assistant." Vibe is actually "a moddable agent runtime with an AI frontend." Until you make that shift, the architecture won't click.

---

## How Vibe Finds This Stuff

Vibe can load custom assets from:

- project-local `.vibe/skills/`
- project-local `.vibe/agents/`
- project-local `.vibe/prompts/`
- project-local `.vibe/config.toml`
- global `~/.vibe/skills/`
- global `~/.vibe/agents/`
- global `~/.vibe/prompts/`
- global `~/.vibe/config.toml`

Recommended rule:

- use project-local `.vibe/` when the setup is tied to one repo
- use global `~/.vibe/` when you want the same system across projects

## Multi-Provider Configuration

Vibe supports multiple LLM providers in the same runtime. You can mix models from different providers (Mistral, OpenRouter, Anthropic, OpenAI) and assign them to different agents or subagents.

### Defining Providers

Each `[[providers]]` block registers a provider. The `api_style` and `backend` fields tell Vibe how to talk to the API:

```toml
[[providers]]
name = "mistral"
api_base = "https://api.mistral.ai/v1"
api_key_env_var = "MISTRAL_API_KEY"
api_style = "openai"
backend = "mistral"

[[providers]]
name = "openrouter"
api_base = "https://openrouter.ai/api/v1"
api_key_env_var = "OPENROUTER_API_KEY"
api_style = "openai"
backend = "openai"

[[providers]]
name = "anthropic"
api_base = "https://api.anthropic.com"
api_key_env_var = "ANTHROPIC_API_KEY"
api_style = "anthropic"
backend = "anthropic"
```

Key fields:
- `name` — referenced by `[[models]]` entries
- `api_base` — the endpoint URL
- `api_key_env_var` — environment variable holding the API key
- `api_style` — wire format: `"openai"` (OpenAI-compatible) or `"anthropic"`
- `backend` — which Vibe backend driver to use

### Defining Models

Each `[[models]]` entry maps a model name to a provider. Use `alias` for a short name you can reference elsewhere:

```toml
[[models]]
name = "mistral-large-latest"
provider = "mistral"
alias = "devstral-2"
temperature = 0.2
thinking = "off"

[[models]]
name = "tencent/hy3-preview:free"
provider = "openrouter"
alias = "hy3"
temperature = 0.2

[[models]]
name = "claude-opus-4-7"
provider = "anthropic"
alias = "opus"
temperature = 0.2
thinking = "on"
```

### Using Different Models for Main vs Subagents

Vibe lets you run your main agent on one model and subagents on another — useful when you want a cheaper/faster model for delegated work:

```toml
# Main agent model
active_model = "devstral-2"

[subagents]
enabled = true
default_model = "hy3"          # subagents use OpenRouter
max_concurrent = 3
```

### Per-Agent Model Override

Agent TOML files can also specify their own model, so you can build a team where each role uses the best-fit provider:

```toml
# agents/specforge-analyst.toml
name = "specforge-analyst"
model = "hy3"                    # OpenRouter for research tasks
```

### Environment Variables

Set your API keys before launching Vibe:

```bash
export MISTRAL_API_KEY="your-key-here"
export OPENROUTER_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
```

Or use a `.env` file in your project root (Vibe will pick it up automatically).

## Setup Tier 1: Simple

**Concept:** Foundational skill pack for coding agent discipline. No architectural changes to Vibe's core loop.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|----------|--------------------------|------|
| Skill (procedure) | `SkillManager` → `SKILL.md` | `skills/<name>/SKILL.md` |
| Activation | Prompt injection via `MiddlewarePipeline` | `vibe/core/middleware.py` |

### Architecture Flow

```
User → AgentLoop.act(prompt)
         ↓
    Core skills available (anti-loop-debug, behavior-audit, focus-master, ...)
         ↓
    AgentLoop executes with improved turn discipline
```

### Install

```bash
mkdir -p ~/.vibe/skills
cp -a skills/anti-loop-debug ~/.vibe/skills/
cp -a skills/behavior-audit ~/.vibe/skills/
cp -a skills/focus-master ~/.vibe/skills/
cp -a skills/verification-master ~/.vibe/skills/
cp -a skills/overlord ~/.vibe/skills/
# Extended core library (recommended):
cp -a skills/context-guardian ~/.vibe/skills/
cp -a skills/pattern-prediction ~/.vibe/skills/
cp -a skills/task-decomposer ~/.vibe/skills/
cp -a skills/tool-primacy ~/.vibe/skills/
cp -a skills/tool-dominator ~/.vibe/skills/
cp -a skills/verification-enforcer ~/.vibe/skills/
```

### Core Skills Included

| Skill | Purpose |
|-------|---------|
| `anti-loop-debug` | Break repetitive failure cycles |
| `behavior-audit` | Audit agent behavior for drift |
| `focus-master` | Maintain focus on goal |
| `verification-master` | Enforce verification before success claims |
| `overlord` | Lightweight orchestration |
| `context-guardian` | Protect context from pollution |
| `pattern-prediction` | Predict and avoid known pitfalls |
| `task-decomposer` | Break work into manageable tasks |
| `tool-primacy` | Ensure tool correctness |
| `tool-dominator` | Advanced tool control |
| `verification-enforcer` | Hard verification gating |

### What This Gives You

- Stronger turn discipline
- Fewer repeated failures
- Better verification habits
- Lightweight orchestration help
- Context protection
- Task decomposition
- Pattern prediction
- Tool correctness enforcement

### What It Does Not Give You

- Automatic compaction recovery
- Custom subagent loops
- Continuous drift monitoring
- Multi-agent team coordination
- Pipeline forge systems (SpecForge, ResearchForge, etc.)

---

## Setup Tier 2: Advanced

**Concept:** Adds continuity-aware execution with checkpointing, watchdog drift checks, and state-sentry recovery. Introduces custom agent profiles and prompts.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|----------|--------------------------|------|
| Agent profile | `AgentManager` → `TOML` + prompt | `agents/main-agent.toml`, `prompts/main.md` |
| Watchdog subagent | `AgentLoop` → `ToolManager.execute()` → `task()` | `agents/watchdog.toml`, `prompts/watchdog.md` |
| State-sentry subagent | Same as above | `agents/state-sentry.toml`, `prompts/state-sentry.md` |
| Continuity skill | `SkillManager` → `SKILL.md` | `skills/vibe-continuity/SKILL.md` |

### Architecture Flow

```
User → AgentLoop.act(prompt) with continuity-agent profile
         ↓
    MiddlewarePipeline injects continuity rules
         ↓
    Watchdog subagent monitors for drift
         ↓
    State-sentry recovers from compaction if needed
```

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a skills/* ~/.vibe/skills/
cp -a agents/main-agent.toml ~/.vibe/agents/
cp -a agents/watchdog.toml ~/.vibe/agents/
cp -a agents/state-sentry.toml ~/.vibe/agents/
cp -a prompts/main.md ~/.vibe/prompts/
cp -a prompts/watchdog.md ~/.vibe/prompts/
cp -a prompts/state-sentry.md ~/.vibe/prompts/
```

### Agents Included

- `main-agent` — primary continuity-aware agent
- `watchdog` — drift detection and correction
- `state-sentry` — checkpoint recovery and state reconstruction

### What This Gives You

- A main execution agent with continuity rules
- A `watchdog` subagent for drift checks
- A `state-sentry` subagent for recovery and reconstruction
- Prompt-level rules for checkpoint-first execution
- Continuity skill (`vibe-continuity`)
- Expanded core skill library

### What This Does Not Yet Give You

- A full multi-agent team system
- Separate operational roles like dev/ops/verify specialization
- Pipeline forge systems (SpecForge, ResearchForge, etc.)

---

## Setup Tier 3: Pro

**Concept:** Full multi-agent team with specialized roles (dev, ops, verify), shared skill library, continuity middleware, and persistent state files.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|----------|--------------------------|------|
| Team agents | `AgentManager` → `TOML` + prompt | `agents/team-*.toml`, `prompts/team-*.md` |
| Skill library | `SkillManager` → `SKILL.md` | `skills/*/SKILL.md` |
| Middleware | `MiddlewarePipeline` | `systems/core/middleware/*.py` |
| Continuity | `vibe-continuity` skill | `skills/vibe-continuity/` |

### Architecture Flow

```
User → AgentLoop.act(prompt) with team-agent profile
         ↓
    MiddlewarePipeline (continuity, drift, verification)
         ↓
    Team agents delegate via subagents (dev, ops, verify)
         ↓
    Shared skill library provides procedures
         ↓
    Persistent state files track progress
```

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a skills/* ~/.vibe/skills/
cp -a agents/*.toml ~/.vibe/agents/
cp -a prompts/*.md ~/.vibe/prompts/
cp -a config.toml ~/.vibe/config.toml
```

### Team Agents Included

- `team-dev` — development specialization
- `team-ops` — operations specialization
- `team-verify` — verification specialization
- `watchdog` — drift detection
- `state-sentry` — recovery

### What This Gives You

- A comprehensive skill library
- A continuity loop with checkpointing
- Specialist subagents (dev, ops, verify)
- Team-oriented agent profiles
- A base you can keep extending into your own system
- Middleware primitives (drift, gating, verification, tracing)
- Runtime adapter pattern (`systems/core/adapters/`)

### Prerequisites

- You understand how custom agents in Vibe override runtime behavior
- You are comfortable editing prompts and TOML
- You want specialized team roles

---

## Project-Local Install Instead of Global

If you want a repo-specific setup instead of modifying `~/.vibe`, install into the project:

```bash
mkdir -p .vibe/skills .vibe/agents .vibe/prompts
cp -a skills/* .vibe/skills/
cp -a agents/*.toml .vibe/agents/
cp -a prompts/*.md .vibe/prompts/
cp -a config.toml .vibe/config.toml
```

This is the safer option when:

- you are experimenting
- you want different behavior per repository
- you are trying to preserve a specific setup through repo updates

## Recommended Rollout Path

If you are new to this, do not jump straight to the full system.

Start here:

1. Install 3 to 5 core skills.
2. Run them manually until you understand what each one changes.
3. Add `watchdog` and `state-sentry`.
4. Move to the full continuity loop only after the prompt and checkpoint behavior make sense to you.
5. Add team agents only when you know what responsibility each one owns.

The examples directory follows this same path:

- [simple](./examples/simple/README.md)
- [advanced](./examples/advanced/README.md)
- [pro](./examples/pro/README.md)

## Pipeline Tier 4: SpecForge — Specification Factory

Turns vague product intent into enforceable application contracts and scenario sheets, using the Mistral-Vibe AgentLoop + SkillManager architecture.

### How It Maps to Mistral-Vibe

| SpecForge Concept | Mistral-Vibe Component | File |
|-------------------|--------------------------|------|
| Skill (phase step) | `SkillManager` → `SKILL.md` | `systems/specforge/skills/NN-*/SKILL.md` |
| Agent (role) | `AgentManager` → agent `TOML` + prompt | `systems/specforge/agents/*.toml`, `systems/specforge/prompts/*.md` |
| Overseer (orchestrator) | `AgentLoop.act()` with `MiddlewarePipeline` | `systems/specforge/prompts/specforge-overseer.md` |
| Subagent delegation | `AgentLoop` → `ToolManager.execute()` → `task()` | `config.toml` subagent settings |
| Orient/Plan/Execute | `MiddlewarePipeline` (Orient) → plan → execute | `vibe/core/middleware.py` |
| Turn-based execution | `AgentLoop` message loop + event streaming | `vibe/core/agent_loop.py` |

### Architecture Flow

```
User → AgentLoop.act(prompt)
         ↓
    MiddlewarePipeline.before_turn()
         ↓ (Orient: inject system prompt + skills)
    LLM stream_completion()
         ↓ (Plan: skill triggers middleware check)
    ToolManager.execute() → task() subagent spawn
         ↓
    SpecForge skill runs (e.g., specforge-06-requirement-normalization)
         ↓
    MessageList updated, next turn or yield AssistantEvent
```

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/specforge/skills/* ~/.vibe/skills/
cp -a systems/specforge/agents/* ~/.vibe/agents/
cp -a systems/specforge/prompts/*.md ~/.vibe/prompts/
```

Then enable in `~/.vibe/config.toml`:

```toml
agent_paths = ["agents", "systems/specforge/agents"]
enabled_agents = [
  "specforge-overseer",
  "specforge-analyst",
  "specforge-architect",
]
enabled_skills = [
  "specforge-00-intake-goal-clarification",
  # ... through 22-final-spec-assembly
]
```

### SpecForge Phases (mapped to Mistral-Vibe execution)

| Phase | Skill(s) | Agent | Execution Model |
|-------|----------|-------|----------------|
| 1. Intake | `00-intake-goal-clarification` | `specforge-overseer` | Orient: clarify intent via `ask_user_question` |
| 2. Evidence Review | `01-existing-document-review`, `02-implementation-survey` | `specforge-analyst` | Subagent spawned via `task()` |
| 3. Gap Analysis | `03-intent-gap-analysis` | `specforge-overseer` | Execute: compare ledgers |
| 4. Targeted Research | `04-research-plan-generation`, `05-targeted-domain-research` | `specforge-analyst` | Subagent loop with `bash` |
| 5. Spec Construction | `06-18` (all spec parts) | `specforge-architect` | Execute: writes `MASTER_SPEC.md` |
| 6. Scenario Generation | `19-scenario-matrix`, `20-kill-test-generation` | `specforge-architect` | Execute: writes `SCENARIOS.md` |
| 7. Adversarial Review | `21-adversarial-spec-review` | `specforge-overseer` | Orient: middleware injects review checklist |

### Core Doctrine

```
Intent is normative.           (user intent drives everything)
Research is advisory.           (findings inform, don't dictate)
Implementation is evidence.       (existing code is descriptive, not truth)
The spec is authoritative.        (only after adversarial review)
```

### Output Artifacts

- `MASTER_SPEC.md` — 16 PARTs (contract, goals, roles, data models, state machines, API, UI, security, observability, invariants, hard gates, conflict resolution, conformance)
- `SCENARIOS.md` — exhaustive scenarios: kill tests, happy paths, edge cases, permission failures, API violations, security boundary tests
- `INTENT_LEDGER.md`, `IMPLEMENTATION_EVIDENCE_MAP.md`, `SPEC_GAP_REPORT.md`, `RESEARCH_FINDINGS.md` — intermediate artifacts

---

## Pipeline Tier 5: ResearchForge — Research-Only Factory

Solves complex issues through disciplined research. Produces a grounded research packet. No code changes. Maps to the same Mistral-Vibe AgentLoop architecture.

### How It Maps to Mistral-Vibe

| ResearchForge Concept | Mistral-Vibe Component | File |
|------------------------|--------------------------|------|
| Skill (research step) | `SkillManager` → `SKILL.md` | `systems/researchforge/skills/NN-*/SKILL.md` |
| Agent (role) | `AgentManager` → agent `TOML` + prompt | `systems/researchforge/agents/*.toml`, `systems/researchforge/prompts/*.md` |
| Overseer (orchestrator) | `AgentLoop.act()` + `MiddlewarePipeline` | `systems/researchforge/prompts/researchforge-overseer.md` |
| Evidence collection | `ToolManager` → `read_file`, `grep`, `bash` | tools section in agent TOML |
| Hypothesis builder | LLM reasoning via `stream_completion()` | `vibe/core/agent_loop.py` |
| Targeted researcher | Subagent via `task()` tool | `researchforge-researcher` agent |
| Final packet assembly | `write_file` (ask permission) | Phase 8 output |

### Architecture Flow

```
Problem → AgentLoop.act("researchforge-00-problem-intake")
         ↓
    MiddlewarePipeline: inject Orient context (OS, git, tools available)
         ↓
    LLM: generates PROBLEM_FRAME.md (structured output)
         ↓
    Subagent spawn: researchforge-evidence (evidence + hypotheses)
         ↓
    Subagent spawn: researchforge-researcher (official docs, upstream issues)
         ↓
    Subagent spawn: researchforge-synthesizer (solution options + validation)
         ↓
    Adversarial review: REJECT if evidence weak
         ↓
    Final packet: FINAL_RESEARCH_PACKET.md
```

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/researchforge/skills/* ~/.vibe/skills/
cp -a systems/researchforge/agents/* ~/.vibe/agents/
cp -a systems/researchforge/prompts/*.md ~/.vibe/prompts/
```

Then enable in `~/.vibe/config.toml`:

```toml
agent_paths = ["agents", "systems/specforge/agents", "systems/researchforge/agents"]
enabled_agents = [
  "specforge-overseer", "specforge-analyst", "specforge-architect",
  "researchforge-overseer", "researchforge-evidence",
  "researchforge-researcher", "researchforge-synthesizer",
]
enabled_skills = [
  # SpecForge (23 skills)
  "specforge-00-intake-goal-clarification",
  # ... through 22-final-spec-assembly
  # ResearchForge (17 skills)
  "researchforge-00-problem-intake",
  # ... through 16-adversarial-research-review
]
```

### ResearchForge Phases (mapped to Mistral-Vibe execution)

| Phase | Skill(s) | Agent | Execution Model |
|-------|----------|-------|----------------|
| 1. Frame Problem | `00-problem-intake`, `01-context-map` | `researchforge-overseer` | Orient: clarify via `ask_user_question` |
| 2. Evidence Ledger | `02-evidence-collection`, `03-source-quality-check` | `researchforge-evidence` | Subagent: collect + classify |
| 3. Hypotheses | `04-hypothesis-generation`, `05-hypothesis-disconfirmation` | `researchforge-evidence` | Execute: build + falsify |
| 4. Targeted Research | `06-targeted-research-plan`, `07-11` (docs, issues, versions, patterns, risks) | `researchforge-researcher` | Subagent loop with `bash` |
| 5. Contradiction Hunt | `12-contradiction-hunt` | `researchforge-evidence` | Execute: find weaknesses |
| 6. Solution Options | `13-solution-option-synthesis` | `researchforge-synthesizer` | Execute: synthesize min 2 options |
| 7. Validation Plan | `14-validation-plan-generation` | `researchforge-synthesizer` | Execute: define proof |
| 8. Final Packet | `15-final-research-packet` | `researchforge-synthesizer` | Execute: assemble + `write_file` |

### Core Doctrine

```
Problem first.               (PROBLEM_FRAME.md must be coherent)
Evidence second.             (collect before hypothesizing)
Hypotheses third.            (every hypothesis needs disconfirmation criteria)
Recommendations last.         (no recommendation without evidence)
No implementation.            (research only, no code changes)
```

### Output Artifacts

- `FINAL_RESEARCH_PACKET.md` — Problem Frame, Context Map, Evidence Ledger, Hypothesis Matrix, Research Findings, Contradiction Report, Solution Options, Validation Plan, Confidence Assessment
- `RESEARCH_REVIEW.md` — PASS/REJECT verdict with audit details

---

## Pipeline Tier 6: SkillForge — Interactive Skill/Agent/Loop Factory

Interactive assistant for creating, debugging, and installing mistral-vibe skills, agents, loops, and workflows. Uses runtime activation with hard gating and transactional staging.

### How It Maps to Mistral-Vibe

| SkillForge Concept | Mistral-Vibe Component | File |
|---------------------|--------------------------|------|
| Skill (entry point) | `SkillManager` → `SKILL.md` with `activation.type: runtime` | `systems/skill-forge/skills/SKILL.md` |
| Agent (forge loop) | `AgentManager` → agent `TOML` + prompt | `systems/skill-forge/agents/skill-forge-agent.toml`, `systems/skill-forge/prompts/skill-forge-system.md` |
| Middleware (hard gating) | `MiddlewarePipeline` → custom middleware | `systems/skill-forge/skills/skill-forge/middleware.py:SkillForgeMiddleware` |
| Runtime switch | `AgentLoop` entrypoint/exitpoint hooks | `systems/skill-forge/skills/skill-forge/agent_loop.py` |
| Staging | Transactional file staging before install | `~/.vibe/skill-forge-state/staging/<session_id>/` |
| State snapshot | Pre/post runtime state persistence | `~/.vibe/skill-forge-state/current_session.json` |

### Architecture Flow

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
    ┌─────────────────────────────────────┐
    │  Controlled Loop (SkillForgeMiddleware enforces gating):  │
    │     Phase1: Goal Elicitation         │
    │     Phase2: Requirements Gathering  │
    │     Phase3: Construction (staged)   │
    │     Phase4: Functional Verification  │
    │     Phase5: Install / Validate      │
    └─────────────────────────────────────┘
         ↓
    exit_skill_forge()
         ↓
    Commit OR Discard staged artifacts
         ↓
    Restore middleware stack (live objects)
         ↓
    Restore agent profile
```

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/skill-forge/skills/* ~/.vibe/skills/
cp -a systems/skill-forge/agents/* ~/.vibe/agents/
cp -a systems/skill-forge/prompts/* ~/.vibe/prompts/
```

Then enable in `~/.vibe/config.toml`:

```toml
agent_paths = ["agents", "systems/specforge/agents", "systems/researchforge/agents", "systems/skill-forge/agents"]
enabled_agents = [
  "specforge-overseer", "specforge-analyst", "specforge-architect",
  "researchforge-overseer", "researchforge-evidence",
  "researchforge-researcher", "researchforge-synthesizer",
  "skill-forge-agent",
]
enabled_skills = [
  # SpecForge (23 skills)
  "specforge-00-intake-goal-clarification",
  # ... through 22-final-spec-assembly
  # ResearchForge (17 skills)
  "researchforge-00-problem-intake",
  # ... through 16-adversarial-research-review
  # SkillForge
  "skill-forge",
]
```

### SkillForge Phases (interactive, hard-gated)

| Phase | Action | Agent | Gating |
|-------|--------|-------|--------|
| 1. Goal Elicitation | Create new component vs. debug existing | `skill-forge-agent` | `AskUserQuestion` required |
| 2. Requirements Gathering | Elicit names, tools, configs, validate | `skill-forge-agent` | Confirmation required |
| 3. Construction | Create files in staging (not live paths) | `skill-forge-agent` | Confirmation required |
| 4. Functional Verification | Discovery, invocation, agent, integration tests | `skill-forge-agent` | Confirmation required |
| 5. Install/Validate | Run validation pipeline, prompt user for action | `skill-forge-agent` | Apply/Save/Discard/Continue |

### Exit Actions

| User Choice | Behavior |
|-------------|----------|
| **Apply** | Commit staged artifacts to live paths, restore previous runtime |
| **Save only** | Keep in `saved/<label>/` for later reuse, stay in forge or exit |
| **Discard** | Save to `saved/discarded-<id>/` for refinement, restore previous runtime |
| **Continue** | Return to Phase 1 with a new goal |

### Core Doctrine

```
Runtime activation.         (intercepted before normal skill execution)
Hard gating.                (middleware blocks turns until user confirms)
Transactional staging.       (nothing touches live paths until Apply)
Stateful restore.            (exact middleware + agent + config reconstruction)
Discarded work is preserved. (nothing is deleted, everything is saved)
```

### Output Artifacts

- Staged components in `~/.vibe/skill-forge-state/staging/<session_id>/`
- Saved/reusable components in `~/.vibe/skill-forge-state/saved/<label>/`
- Runtime snapshot in `~/.vibe/skill-forge-state/current_session.json`
- On Apply: live installation into `~/.vibe/skills/`, `~/.vibe/agents/`, `~/.vibe/prompts/`

### Generalized Pattern

SkillForge implements a reusable pattern for runtime-activated skills:

1. **Snapshot** — save current runtime state (middleware, agent, config)
2. **Swap** — inject custom middleware + switch agent profile
3. **Execute** — run controlled loop with hard gating
4. **Restore** — deterministically reconstruct previous runtime

Any skill can adopt this pattern by setting `activation.type: runtime` and providing `entrypoint`/`exitpoint` hooks.

---
---
## Pipeline Tier 7: CodeForge — Implementation Factory

Turns approved specs into running code. Multi-agent pipeline: overseer plans, implementer writes, validator verifies.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|---------|----------------------|------|
| Skill (phase) | `SkillManager` → `SKILL.md` | `systems/codeforge/skills/NN-*/SKILL.md` |
| Overseer agent | `AgentManager` → TOML + prompt | `systems/codeforge/agents/codeforge-overseer.toml` |
| Implementer | Subagent via `task()` | `systems/codeforge/agents/codeforge-implementer.toml` |
| Validator | Subagent via `task()` | `systems/codeforge/agents/codeforge-validator.toml` |

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/codeforge/skills/* ~/.vibe/skills/
cp -a systems/codeforge/agents/* ~/.vibe/agents/
cp -a systems/codeforge/prompts/* ~/.vibe/prompts/
```

### Phases

| Phase | Skill | Agent |
|-------|-------|--------|
| 1. Spec Ingest | `00-spec-ingest` | `codeforge-overseer` |
| 2. Codebase Survey | `01-codebase-survey` | `codeforge-overseer` |
| 3. Implementation Planning | `02-implementation-planning` | `codeforge-overseer` |
| 4. File Generation | `03-file-generation` | `codeforge-implementer` |
| 5. Pattern Following | `04-pattern-following` | `codeforge-implementer` |
| 6. Integration | `06-integration` | `codeforge-implementer` |
| 7. Handoff Verification | `07-handoff-verification` | `codeforge-validator` |

### Output Artifacts

- `IMPLEMENTATION.md` — code files, integration notes, test results
- `HANDOFF_REPORT.md` — verification results, conformance checklist

---

## Pipeline Tier 8: DebugForge — Debugging Factory

Reproduces, isolates, and fixes bugs through disciplined bisection and root-cause analysis.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|---------|----------------------|------|
| Skill (phase) | `SkillManager` → `SKILL.md` | `systems/debugforge/skills/NN-*/SKILL.md` |
| Overseer | `AgentManager` → TOML + prompt | `systems/debugforge/agents/debugforge-overseer.toml` |
| Reproducer | Subagent via `task()` | `systems/debugforge/agents/debugforge-reproducer.toml` |
| Fixer | Subagent via `task()` | `systems/debugforge/agents/debugforge-fixer.toml` |

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/debugforge/skills/* ~/.vibe/skills/
cp -a systems/debugforge/agents/* ~/.vibe/agents/
cp -a systems/debugforge/prompts/* ~/.vibe/prompts/
```

### Phases

| Phase | Skill | Agent |
|-------|-------|--------|
| 1. Issue Intake | `00-issue-intake` | `debugforge-overseer` |
| 2. Reproduction | `01-reproduction` | `debugforge-reproducer` |
| 3. Bisection Isolation | `02-bisection-isolation` | `debugforge-reproducer` |
| 4. Root Cause Analysis | `03-root-cause-analysis` | `debugforge-overseer` |
| 5. Fix Option Generation | `04-fix-option-generation` | `debugforge-overseer` |
| 6. Scenario Validation | `05-scenario-validation` | `debugforge-fixer` |
| 7. Fix Application | `06-fix-application` | `debugforge-fixer` |

### Output Artifacts

- `FIX_REPORT.md` — root cause, fix applied, scenario validation results
- `REPRODUCTION_STEPS.md` — minimal steps to reproduce the issue

---

## Pipeline Tier 9: DocForge — Documentation Factory

Generates API docs, architecture diagrams, inline docstrings, and README sync. No code changes.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|---------|----------------------|------|
| Skill (phase) | `SkillManager` → `SKILL.md` | `systems/docforge/skills/NN-*/SKILL.md` |
| Overseer | `AgentManager` → TOML + prompt | `systems/docforge/agents/docforge-overseer.toml` |
| APIDoc generator | Subagent via `task()` | `systems/docforge/agents/docforge-apidoc.toml` |
| Diagrams generator | Subagent via `task()` | `systems/docforge/agents/docforge-diagrams.toml` |

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/docforge/skills/* ~/.vibe/skills/
cp -a systems/docforge/agents/* ~/.vibe/agents/
cp -a systems/docforge/prompts/* ~/.vibe/prompts/
```

### Phases

| Phase | Skill | Agent |
|-------|-------|--------|
| 1. Codebase Doc Survey | `00-codebase-doc-survey` | `docforge-overseer` |
| 2. API Reference Gen | `01-api-reference-generation` | `docforge-apidoc` |
| 3. Inline Docstring Gen | `02-inline-docstring-generation` | `docforge-apidoc` |
| 4. Architecture Diagrams | `03-architecture-diagram-generation` | `docforge-diagrams` |
| 5. README Sync | `04-readme-sync` | `docforge-overseer` |
| 6. Doc Continuity Check | `05-doc-continuity-check` | `docforge-overseer` |

### Output Artifacts

- `API_REFERENCE.md` — generated API documentation
- `ARCHITECTURE_DIAGRAMS.md` — system diagrams
- Updated inline docstrings across the codebase
- `README_SYNC_REPORT.md`

---

## Pipeline Tier 10: ShipForge — Deployment Factory

Generates Dockerfiles, CI pipelines, deployment configs, and environment parity checks.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|---------|----------------------|------|
| Skill (phase) | `SkillManager` → `SKILL.md` | `systems/shipforge/skills/NN-*/SKILL.md` |
| Overseer | `AgentManager` → TOML + prompt | `systems/shipforge/agents/shipforge-overseer.toml` |
| Builder | Subagent via `task()` | `systems/shipforge/agents/shipforge-builder.toml` |
| Deployer | Subagent via `task()` | `systems/shipforge/agents/shipforge-deployer.toml` |

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/shipforge/skills/* ~/.vibe/skills/
cp -a systems/shipforge/agents/* ~/.vibe/agents/
cp -a systems/shipforge/prompts/* ~/.vibe/prompts/
```

### Phases

| Phase | Skill | Agent |
|-------|-------|--------|
| 1. Spec Deployment Survey | `00-spec-deployment-survey` | `shipforge-overseer` |
| 2. Dockerfile Generation | `01-dockerfile-generation` | `shipforge-builder` |
| 3. CI Pipeline Generation | `02-ci-pipeline-generation` | `shipforge-builder` |
| 4. Deployment Config Gen | `03-deployment-config-generation` | `shipforge-builder` |
| 5. Environment Parity Check | `04-environment-parity-check` | `shipforge-deployer` |
| 6. Security Hardening Check | `05-security-hardening-check` | `shipforge-deployer` |
| 7. Deployment Checklist | `06-deployment-checklist-generation` | `shipforge-overseer` |

### Output Artifacts

- `Dockerfile`, `docker-compose.yml` — container definitions
- `.github/workflows/ci.yml` — CI pipeline
- `deploy/`, `k8s/` — deployment configs
- `DEPLOYMENT_CHECKLIST.md`

---

## Pipeline Tier 11: TestForge — Test Generation Factory

Generates unit, integration, kill, and fuzz tests from spec scenarios.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|---------|----------------------|------|
| Skill (phase) | `SkillManager` → `SKILL.md` | `systems/testforge/skills/NN-*/SKILL.md` |
| Overseer | `AgentManager` → TOML + prompt | `systems/testforge/agents/testforge-overseer.toml` |
| Generator | Subagent via `task()` | `systems/testforge/agents/testforge-generator.toml` |
| Coverage | Subagent via `task()` | `systems/testforge/agents/testforge-coverage.toml` |

### Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/testforge/skills/* ~/.vibe/skills/
cp -a systems/testforge/agents/* ~/.vibe/agents/
cp -a systems/testforge/prompts/* ~/.vibe/prompts/
```

### Phases

| Phase | Skill | Agent |
|-------|-------|--------|
| 1. Spec Scenario Ingest | `00-spec-scenario-ingest` | `testforge-overseer` |
| 2. Test Strategy Planning | `01-test-strategy-planning` | `testforge-overseer` |
| 3. Unit Test Generation | `02-unit-test-generation` | `testforge-generator` |
| 4. Integration Test Generation | `04-integration-test-generation` | `testforge-generator` |
| 5. Kill Test Generation | `03-kill-test-generation` | `testforge-generator` |
| 6. Fuzz Target Generation | `05-fuzz-target-generation` | `testforge-generator` |
| 7. Coverage Validation | `06-coverage-validation` | `testforge-coverage` |

### Output Artifacts

- `tests/unit/` — unit test suites
- `tests/integration/` — integration tests
- `tests/kill/` — kill test scenarios
- `COVERAGE_REPORT.md`

---

## Pipeline Tier 12: ReactiveForge — Reactive Middleware

Runtime middleware layer that reacts to events in the agent loop. Uses the adapter pattern from `systems/core/adapters/`.

### Concept

Intercepts tool calls, commands, and messages in real-time. Provides reactive gating, automatic drift correction, and state injection without forking Vibe.

### How It Maps to Mistral-Vibe

| Concept | Mistral-Vibe Component | File |
|---------|----------------------|------|
| Adapter | `MiddlewarePipeline` → adapter classes | `systems/core/adapters/` |
| Tracing | `Middleware` → `TracingMiddleware` | `systems/core/middleware/tracing.py` |
| Drift detection | `Middleware` → `DriftMiddleware` | `systems/core/middleware/drift.py` |
| Gating | `Middleware` → `GatingMiddleware` | `systems/core/middleware/gating.py` |
| State injection | `Middleware` → `StateInjectionMiddleware` | `systems/core/middleware/state_injection.py` |

### Install

```bash
mkdir -p ~/.vibe/systems/core/adapters ~/.vibe/systems/core/middleware
cp -a systems/core/adapters/* ~/.vibe/systems/core/adapters/
cp -a systems/core/middleware/* ~/.vibe/systems/core/middleware/
```

### Usage

```python
from systems.core.adapters import install_control_plane

agent_loop = install_control_plane(
    agent_loop=base_agent_loop,
    middleware=my_middleware_pipeline,
    context=my_forge_context,
)
```

### What This Gives You

- Reactive interception of all tool calls, commands, file ops
- Middleware pipeline with tracing, drift, gating, verification, state injection
- Pluggable architecture — add/remove middleware without touching Vibe core
- Portable control-plane layer that proves the pattern outside Vibe

---


## Runtime Adapter Pattern (Control-Plane Integration)

The cleanest way to integrate a control plane into Mistral Vibe **without forking or patching core code** is to wrap Vibe's runtime objects at the instance level.

### Concept

Instead of editing `vibe/core/agent_loop.py` or `vibe/core/tool_manager.py`, you wrap the live objects so every call passes through your middleware before reaching the real Vibe internals:

```
Vibe AgentLoop
   ↓
MiddlewareAgentLoop wrapper (optional)
   ↓
Vibe ToolManager replaced with MiddlewareToolManager
   ↓
MiddlewarePipeline (Tracing / Drift / Verification / Gating / State)
   ↓
Original Vibe ToolManager (actual execution)
```

### Wrap ToolManager (minimum viable integration)

This is the most important adapter. Replace the agent loop's `tool_manager` with a wrapped version that intercepts all tool calls:

```python
from systems.core.adapters import MiddlewareToolManager

agent_loop.tool_manager = MiddlewareToolManager(
    base_tool_manager=agent_loop.tool_manager,
    middleware=my_middleware_pipeline,
    context=my_forge_context,
)
```

Once wrapped, every tool call (`bash`, `write_file`, `edit_file`, etc.) passes through your middleware before execution. This gives you:

- tool call gating (block/modify)
- command logging and validation
- file operation interception
- post-execution result inspection
- state injection into the message list

### Wrap AgentLoop (turn-level control)

If you need turn-level state injection or message stream interception, wrap the agent loop itself:

```python
from systems.core.adapters import MiddlewareAgentLoop, wrap_agent_loop

agent_loop = wrap_agent_loop(
    base_agent_loop=agent_loop,
    middleware=my_middleware_pipeline,
    context=my_forge_context,
)
```

The wrapper overrides `act()` to inject state before each turn and (if `act()` yields events) to intercept individual messages in the stream.

### Adapter Source Layout

```
systems/core/adapters/
  __init__.py
  tool_manager_adapter.py      # MiddlewareToolManager
  agent_loop_adapter.py        # MiddlewareAgentLoop
  install.py                    # factory: wrap_agent_loop()
```

### Install Helper

The `install.py` factory makes this a one-liner:

```python
from systems.core.adapters.install import install_control_plane

agent_loop = install_control_plane(
    agent_loop=base_agent_loop,
    middleware=my_middleware_pipeline,
    context=my_forge_context,
)
```

### Key Rules

- **Instance wrapping only** — never monkeypatch classes globally (`AgentLoop.act = ...`). Always wrap at the instance level so the original Vibe code stays untouched and reversible.
- **`__getattr__` passthrough** — adapters forward any attribute they don't explicitly override to the real Vibe object, so you only intercept choke points.
- **No core edits** — if you find yourself editing `vibe/core/agent_loop.py`, stop. The point is to prove the control-plane pattern *outside* Vibe, not to fork it.

### What This Proves

This approach turns the repo from "cool architecture documents" into a **portable, plug-compatible control-plane layer** that:

- demonstrates observable, enforceable runtime behavior
- can be removed without touching Vibe source
- is testable independently of Vibe internals
- can be upstreamed later as a middleware proposal without dragging along fork complexity

---

## How To Create Your Own Specialized Loop

The clean way to build your own system is:

1. decide the behavioral problem you want to solve
2. write the rule in a prompt if it is always-on behavior
3. write it as a skill if it should be invoked on demand
4. create a custom agent TOML if the behavior needs a dedicated runtime identity
5. add supporting subagents only when the main agent should delegate instead of doing the work inline

Use this rule of thumb:

- prompt = always-on operating doctrine (injected by `MiddlewarePipeline` in `vibe/core/middleware.py`)
- skill = reusable procedure (`SkillManager` parses `SKILL.md` via `parse_skill_command` in `vibe/core/skills/manager.py`)
- agent TOML = runtime personality/configuration wrapper (`AgentManager` loads from `agents/*.toml`)
- subagent = specialized delegated worker (`AgentLoop` → `ToolManager.execute()` → `task()` tool)

### Example: Simple Custom Loop

Goal:
- force better verification before claiming success

Shape:
- one skill: `my-verification-gate`
- no custom agents
- no custom prompts

### Example: Advanced Custom Loop

Goal:
- detect drift after long sessions and recover from compaction

Shape:
- one main prompt
- one primary custom agent
- two subagents:
  - drift checker
  - state reconstructor
- a few skills for anti-loop and verification

### Example: Pro Custom System

Goal:
- run an entire engineering workflow with separate operating roles

Shape:
- one primary orchestrator
- multiple role agents
- shared prompts
- shared skill library
- continuity and verification middleware concepts
- persistent state files and recovery rules

## Practical Notes

- `~/.vibe/AGENTS.md` is optional. Many advanced behaviors can live entirely in prompts, skills, and agent TOMLs.
- The continuity system here is opinionated. You should trim it if it is too strict for your workflow.
- Do not publish secrets, API keys, logs, checkpoints, or local databases with your skill repo.
- If you fork this into your own system, rename the agents, prompts, and skills to reflect your actual operating model instead of leaving them as cargo-cult artifacts.

## Suggested First Things To Read

- [docs/START-HERE.md](./docs/START-HERE.md)
- [docs/REPO-MAP.md](./docs/REPO-MAP.md)
- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- [docs/SUBAGENT-ORCHESTRATION.md](./docs/SUBAGENT-ORCHESTRATION.md)
- [docs/EXECUTION-AND-DRIFT.md](./docs/EXECUTION-AND-DRIFT.md)
- [docs/USER_GUIDE.md](./docs/USER_GUIDE.md)
- [skills/mistral-vibe-compaction-skill/SKILL.md](./skills/mistral-vibe-compaction-skill/SKILL.md)
