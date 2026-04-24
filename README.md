# Survival DevEngineer Skill Repo

This repository is a practical add-on layer for **Mistral Vibe**. It packages custom skills, custom agent profiles, custom prompts, and a continuity-oriented execution style that sits on top of the normal Vibe runtime.

The point of this repo is not "one magic prompt." The point is to make it clear how advanced Vibe setups actually work:

- `skills/` adds reusable skill packs
- `agents/` adds custom agent profiles via TOML
- `prompts/` adds custom system prompts used by those agents
- `config.toml` can enable the right runtime defaults
- project-local `.vibe/` or global `~/.vibe/` placement determines where Vibe discovers everything

If you only copy `SKILL.md` files and skip the agent and prompt wiring, you are not installing the full system.

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

## Setup Tier 1: Simple

Use this if you just want better skills without changing your entire execution model.

Install:

```bash
mkdir -p ~/.vibe/skills
cp -a skills/anti-loop-debug ~/.vibe/skills/
cp -a skills/behavior-audit ~/.vibe/skills/
cp -a skills/focus-master ~/.vibe/skills/
cp -a skills/verification-master ~/.vibe/skills/
cp -a skills/overlord ~/.vibe/skills/
```

Good starter set:

- `behavior-audit`
- `anti-loop-debug`
- `focus-master`
- `verification-master`
- `overlord`

What this gives you:

- stronger turn discipline
- fewer repeated failures
- better verification habits
- lightweight orchestration help

What it does not give you:

- automatic compaction recovery
- custom subagent loops
- continuous drift monitoring

## Setup Tier 2: Advanced

Use this if you want continuity-aware execution and subagent-assisted recovery.

Install:

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

Then either:

- select the custom agent directly when you launch Vibe, or
- fold the relevant values into your `~/.vibe/config.toml`

What this gives you:

- a main execution agent with continuity rules
- a `watchdog` subagent for drift checks
- a `state-sentry` subagent for recovery and reconstruction
- prompt-level rules for checkpoint-first execution

What this does not yet give you:

- a full multi-agent team system
- separate operational roles like dev/ops/verify specialization

## Setup Tier 3: Pro

Use this if you want a complete agent system rather than a few isolated enhancements.

Install the entire runtime layer:

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a skills/* ~/.vibe/skills/
cp -a agents/*.toml ~/.vibe/agents/
cp -a prompts/*.md ~/.vibe/prompts/
cp -a config.toml ~/.vibe/config.toml
```

This tier assumes:

- you understand how custom agents in Vibe override runtime behavior
- you are comfortable editing prompts and TOML
- you want specialized team roles such as:
  - dev
  - ops
  - verify
  - watchdog
  - state-sentry

What this gives you:

- a skill library
- a continuity loop
- specialist subagents
- team-oriented agent profiles
- a base you can keep extending into your own system

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

## How To Create Your Own Specialized Loop

The clean way to build your own system is:

1. decide the behavioral problem you want to solve
2. write the rule in a prompt if it is always-on behavior
3. write it as a skill if it should be invoked on demand
4. create a custom agent TOML if the behavior needs a dedicated runtime identity
5. add supporting subagents only when the main agent should delegate instead of doing the work inline

Use this rule of thumb:

- prompt = always-on operating doctrine
- skill = reusable procedure
- agent TOML = runtime personality/configuration wrapper
- subagent = specialized delegated worker

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

## Why This Repo Exists

Mistral Vibe is unusually powerful once you understand the layering model, but that power is easy to miss because the setup is not obvious from the outside.

The common failure modes are:

- copying only skills and wondering why the full behavior is missing
- copying prompts without wiring the agent profile
- creating custom agents without understanding how prompts and skills are discovered
- treating compaction recovery as "just a prompt" instead of a full operating pattern

This repo is meant to make that model visible and reusable.

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

## Minimal Publish Checklist

Before pushing this repo to GitHub:

- review `config.toml` for machine-specific paths or private values
- make sure `.gemini_security/`, logs, and databases are ignored
- verify your prompts do not contain secrets or personal identifiers
- decide whether you want this repo to represent:
  - the exact system you run
  - a cleaned-up template others can adopt

If you want a portable public version, prefer the second option.
