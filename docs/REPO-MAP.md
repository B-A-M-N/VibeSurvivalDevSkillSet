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

## Historical / Internal Material

- `archive/`
  Older or backup material. Not part of the core install path.
- `conductor/`
  Supporting material for the broader system. Useful, but not required for initial setup.
- `docs/architect_brain.md`
  More internal than beginner-facing. It is not an installed skill and should not be treated as part of the normal setup path.

## Files Most People Actually Need

If someone just wants to install the system, they usually need:

- some or all of `skills/`
- some or all of `agents/`
- some or all of `prompts/`
- `examples/`
- `README.md`

If someone wants to understand the theory, then they should also read `docs/`.
