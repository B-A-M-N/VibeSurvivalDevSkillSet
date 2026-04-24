# Internal Notes

This file exists so people looking at the repo can separate the install surface from private or more experimental material.

## Not Part of the Core Install Path

These items are useful context, but they are not required for someone just trying to use the skill system:

- `docs/architect_brain.md`
- `archive/`
- `conductor/`

## Why This Matters

Without this distinction, people tend to assume every file in the repo is part of the setup process, which makes the whole system seem more complicated than it actually is.

The real install surface is still:

- `skills/`
- `agents/`
- `prompts/`
- optional `config.toml`
- `examples/`

Everything else is support material, reference material, or internal history.
