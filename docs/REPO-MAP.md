# Repo Map

This is the practical map of the repository.

## Runtime Assets

- `skills/`
  The custom skill library. Each subdirectory is one skill.
- `agents/`
  Custom Vibe agent profiles in TOML.
- `prompts/`
  Prompt files referenced by the custom agents.
- `config.toml`
  Optional config overlay you can copy into `~/.vibe/config.toml` or adapt into your own config.

## Guides

- `README.md`
  Main public-facing setup guide.
- `docs/START-HERE.md`
  Fast orientation for new users.
- `docs/INTERNAL-NOTES.md`
  Explains which files are support/internal material rather than part of the normal install path.
- `examples/`
  Copyable install patterns for different complexity levels.

## Deep Reference Docs

These are useful once you already understand the basics.

- `docs/ARCHITECTURE.md`
- `docs/SUBAGENT-ORCHESTRATION.md`
- `docs/EXECUTION-AND-DRIFT.md`
- `docs/OBSERVER-SPEC.md`
- `docs/STATE-SCHEMA.md`
- `docs/INJECT-PACKET-SCHEMA.md`
- `docs/COORDINATION-PROTOCOL.md`

## Internal / Advanced Material

The remaining `docs/` files are mostly reference material rather than installation steps.
Use them when you want the deeper protocol and architecture details, not when you are just trying to get the system running for the first time.

## Files Most People Actually Need

If someone just wants to install the system, they usually need:

- some or all of `skills/`
- some or all of `agents/`
- some or all of `prompts/`
- `examples/`
- `README.md`

If someone wants to understand the theory, then they should also read `docs/`.
