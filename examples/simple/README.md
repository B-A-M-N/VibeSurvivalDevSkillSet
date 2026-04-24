# Simple Setup

This is the lowest-friction version.

Use it when you want better behavior, but you do not want to replace your whole Vibe runtime model.

## What You Install

- a few high-value skills
- no custom agents
- no custom prompts

## Good Starter Skills

- `behavior-audit`
- `anti-loop-debug`
- `focus-master`
- `verification-master`
- `overlord`

## Install

```bash
mkdir -p ~/.vibe/skills
cp -a skills/behavior-audit ~/.vibe/skills/
cp -a skills/anti-loop-debug ~/.vibe/skills/
cp -a skills/focus-master ~/.vibe/skills/
cp -a skills/verification-master ~/.vibe/skills/
cp -a skills/overlord ~/.vibe/skills/
```

Optional config starting point:

- [config.toml](./config.toml)

## What This Changes

- you get stronger manual workflows
- you can invoke skills on demand
- you do not change the main Vibe execution loop

## What This Does Not Change

- no automatic compaction recovery
- no custom subagent orchestration
- no team roles

## Best First Test

Launch Vibe and manually use one of the installed skills against a real task. If you do not understand what changed, stay at this level longer before moving on.
