# CodeForge — Spec-Driven Code Implementation System

Takes `MASTER_SPEC.md` (from SpecForge) and drives disciplined implementation across the codebase. Wires components, follows existing patterns, and validates invariants as it writes.

## How It Maps to Mistral-Vibe

| CodeForge Concept | Mistral-Vibe Component | File |
|-------------------|--------------------------|------|
| Skill (phase step) | `SkillManager` → `SKILL.md` | `systems/codeforge/skills/NN-*/SKILL.md` |
| Agent (role) | `AgentManager` → agent `TOML` + prompt | `systems/codeforge/agents/*.toml`, `systems/codeforge/prompts/*.md` |
| Overseer (orchestrator) | `AgentLoop.act()` + `MiddlewarePipeline` | `systems/codeforge/prompts/codeforge-overseer.md` |
| Implementation | `ToolManager` → `write_file`, `search_replace` | tools section in agent TOML |
| Invariant checking | Middleware injects invariant rules before writes | `vibe/core/middleware.py` |
| Subagent delegation | `task()` tool for parallel file work | `config.toml` subagent settings |

## Architecture Flow

```
MASTER_SPEC.md → AgentLoop.act("codeforge-00-spec-ingest")
         ↓
    MiddlewarePipeline: inject spec context + existing code survey
         ↓
    LLM: generates IMPLEMENTATION_PLAN.md
         ↓
    Subagent spawn: codeforge-implementer (file generation phase)
         ↓
    Subagent spawn: codeforge-implementer (integration wiring phase)
         ↓
    Invariant check: every write validated against spec invariants
         ↓
    Subagent spawn: codeforge-validator (cross-check spec compliance)
         ↓
    Handoff: IMPLEMENTATION_REPORT.md → TestForge
```

## Agents

| Agent | Role | Model Preference |
|-------|------|-----------------|
| `codeforge-overseer` | Orchestrates implementation, manages plan, gates phases | Strong reasoning (opus/hy3) |
| `codeforge-implementer` | Writes code, follows patterns, respects invariants | Fast + accurate (devstral-2) |
| `codeforge-validator` | Validates implementation against spec, checks invariants | Thorough (hy3/opus) |

## Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -a systems/codeforge/skills/* ~/.vibe/skills/
cp -a systems/codeforge/agents/* ~/.vibe/agents/
cp -a systems/codeforge/prompts/*.md ~/.vibe/prompts/
```

Then enable in `~/.vibe/config.toml`:

```toml
agent_paths = ["agents", "systems/specforge/agents", "systems/researchforge/agents", "systems/codeforge/agents"]
enabled_agents = [
  "codeforge-overseer",
  "codeforge-implementer",
  "codeforge-validator",
]
enabled_skills = [
  # CodeForge (7 skills)
  "codeforge-00-spec-ingest",
  "codeforge-01-codebase-survey",
  "codeforge-02-implementation-planning",
  "codeforge-03-file-generation",
  "codeforge-04-pattern-following",
  "codeforge-05-invariant-checking",
  "codeforge-06-integration",
  "codeforge-07-handoff-verification",
]
```

## Phases

| Phase | Skill(s) | Agent | Execution Model |
|-------|----------|-------|----------------|
| 1. Spec Ingest | `00-spec-ingest` | `codeforge-overseer` | Orient: parse MASTER_SPEC.md, extract contracts |
| 2. Codebase Survey | `01-codebase-survey` | `codeforge-implementer` | Execute: map existing code to spec sections |
| 3. Implementation Plan | `02-implementation-planning` | `codeforge-overseer` | Execute: ordered task list with dependencies |
| 4. File Generation | `03-file-generation`, `04-pattern-following` | `codeforge-implementer` | Subagent: parallel file creation |
| 5. Invariant Checking | `05-invariant-checking` | `codeforge-validator` | Middleware: every write checked |
| 6. Integration | `06-integration` | `codeforge-implementer` | Execute: wire components, connect APIs |
| 7. Handoff Verification | `07-handoff-verification` | `codeforge-validator` | Execute: spec compliance report |

## Core Doctrine

```
Spec is the contract.         (MASTER_SPEC.md is authoritative)
Patterns are binding.          (follow existing code patterns exactly)
Invariants are non-negotiable. (every write checked before commit)
Implementation is evidence.   (code must map to spec sections)
Handoff is documented.         (no silent passes to next system)
```

## Output Artifacts

- `IMPLEMENTATION_PLAN.md` — ordered tasks, dependencies, file targets
- `IMPLEMENTATION_REPORT.md` — what was built, what maps to spec, open items
- `INVARIANT_VIOLATIONS.md` — any invariant checks that failed during implementation
- Modified codebase — all implementation files wired and documented
