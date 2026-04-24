# Start Here

This repo can look bigger than it really is.

The short version:

- `skills/` are reusable behaviors
- `agents/` are custom Vibe agent profiles
- `prompts/` are system prompts those agents use
- `config.toml` is optional runtime wiring
- `examples/` shows how to install this at different complexity levels

If you are new to custom Vibe setups, do this in order:

1. Read [../README.md](../README.md)
2. Read [REPO-MAP.md](./REPO-MAP.md)
3. Skim [INTERNAL-NOTES.md](./INTERNAL-NOTES.md) if you want to know what can be ignored at first
4. Pick one example:
   - [../examples/simple/README.md](../examples/simple/README.md)
   - [../examples/advanced/README.md](../examples/advanced/README.md)
   - [../examples/pro/README.md](../examples/pro/README.md)

## Which Level Should You Start With?

Use `simple` if:

- you only want a few better skills
- you do not want to change your whole runtime
- you are still learning how Vibe loads custom behavior

Use `advanced` if:

- you want continuity and compaction recovery
- you want `watchdog` and `state-sentry`
- you are comfortable with custom agents and prompts

Use `pro` if:

- you want a full role-based system
- you want multiple custom agents
- you plan to design your own specialized loops

## Common Mistakes

- Installing only `SKILL.md` files and expecting the whole system to work
- Copying prompts without copying the matching agent TOMLs
- Using global `~/.vibe` for experiments you should keep project-local
- Treating continuity behavior as "just a prompt" instead of a prompt + agent + skill pattern

## Recommended First Test

Before installing everything, test one small step:

1. copy one skill into `~/.vibe/skills/`
2. launch Vibe
3. confirm the skill appears
4. use it manually once

If that works, move up one tier. That keeps the system understandable instead of turning into mystery behavior all at once.
