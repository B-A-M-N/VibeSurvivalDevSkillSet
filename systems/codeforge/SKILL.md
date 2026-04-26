# CodeForge — Spec-Driven Code Implementation

Takes `MASTER_SPEC.md` (from SpecForge) and drives disciplined implementation across the codebase.

## Input Artifacts

- `MASTER_SPEC.md` — REQUIRED (produced by SpecForge)

## Output Artifacts

- `IMPLEMENTATION_PLAN.md` — ordered tasks, dependencies, file targets
- `IMPLEMENTATION_REPORT.md` — what was built, what maps to spec, open items
- `INVARIANT_VIOLATIONS.md` — any invariant checks that failed
- Modified codebase — all implementation files wired and documented

## Phases (Skills)

| Phase | Skill | Agent | Description |
|-------|------|-------|-------------|
| 1 | `codeforge-00-spec-ingest` | codeforge-overseer | Parse MASTER_SPEC.md, extract contracts |
| 2 | `codeforge-01-codebase-survey` | codeforge-implementer | Map existing code to spec sections |
| 3 | `codeforge-02-implementation-planning` | codeforge-overseer | Generate ordered task list |
| 4 | `codeforge-03-file-generation` | codeforge-implementer | Parallel file creation |
| 5 | `codeforge-04-pattern-following` | codeforge-implementer | Follow existing patterns |
| 6 | `codeforge-05-invariant-checking` | codeforge-validator | Every write checked against spec |
| 7 | `codeforge-06-integration` | codeforge-implementer | Wire components, connect APIs |
| 8 | `codeforge-07-handoff-verification` | codeforge-validator | Spec compliance report |

## Gates

- `spec_present` — MASTER_SPEC.md must exist before any phase runs
- `implementation_complete` — IMPLEMENTATION_REPORT.md must exist before handoff

## Handoff

On successful completion, hands off to **TestForge** with:
- `IMPLEMENTATION_REPORT.md`
- Modified codebase

## Core Doctrine

```
Spec is the contract.         (MASTER_SPEC.md is authoritative)
Patterns are binding.          (follow existing code patterns exactly)
Invariants are non-negotiable.  (every write checked before commit)
Implementation is evidence.    (code must map to spec sections)
Handoff is documented.         (no silent passes to next system)
```

## Usage

```bash
# Run via orchestrator
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='codeforge'); \
          result = o.run_forge('codeforge', ctx)"
```

## Agent Loop

The `agent_loop.py` provides:
- `enter_codeforge()` — validates MASTER_SPEC.md exists
- `exit_codeforge()` — validates IMPLEMENTATION_REPORT.md exists
- `run_phase(phase, context)` — runs a single phase with gate checks
