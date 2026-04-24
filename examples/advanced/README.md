# Advanced Setup

This is the continuity-aware setup.

Use it when you want Vibe to behave less like a single stateless assistant and more like a guarded execution loop with recovery support.

## What You Install

- the skill library
- `main-agent.toml`
- `watchdog.toml`
- `state-sentry.toml`
- their matching prompts

## Install

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

Optional config starting point:

- [config.toml](./config.toml)

## What This Adds

- a main execution profile
- a fast drift-checking subagent
- a deeper state-reconstruction subagent
- prompt-level continuity rules

## How To Think About It

- `watchdog` is the quick verifier
- `state-sentry` is the recovery/reconstruction worker
- the main agent remains the executor

## Suggested Config Pattern

Keep your normal config, then selectively copy in only the settings you actually want from `config.toml`.

Do not blindly replace your entire existing config unless you know what each setting does.

## Best First Test

Run a task that spans multiple files, then intentionally pause and resume. Confirm that the continuity-oriented behavior is actually helping instead of just adding friction.
