# Pro Setup

This is the full system approach.

Use it when you want a custom Vibe operating environment, not just some extra skills.

## What You Install

- all custom skills
- all custom agents
- all prompts
- selected config wiring
- role-based team agents

## Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a skills/* ~/.vibe/skills/
cp -a agents/*.toml ~/.vibe/agents/
cp -a prompts/*.md ~/.vibe/prompts/
cp -a config.toml ~/.vibe/config.toml
```

Optional config starting point:

- [config.toml](./config.toml)

## Role Layout

- `main-agent.toml`
  Primary continuity-aware execution profile.
- `watchdog.toml`
  Fast drift detection and behavioral guardrail.
- `state-sentry.toml`
  State recovery and post-compaction reconstruction.
- `team-dev.toml`
  Development-oriented specialist.
- `team-ops.toml`
  Operational / systems-oriented specialist.
- `team-verify.toml`
  Verification-oriented specialist.

## When This Makes Sense

- you already know how Vibe loads custom agents
- you want multiple specialized workers
- you are building your own house style on top of Vibe

## How To Build Your Own System From Here

1. define the main execution doctrine in a prompt
2. wrap it in a custom agent TOML
3. split specialized behaviors into separate skills
4. create subagents only when delegation adds clarity
5. keep roles narrow so the system stays understandable

## Example Design Pattern

One good pro-level pattern is:

- one orchestrator
- one continuity/recovery layer
- one verification specialist
- one implementation specialist
- one ops/systems specialist

That is enough to create a real agent system without turning the setup into an unreadable mess.
