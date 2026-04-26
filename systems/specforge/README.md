# SpecForge System

Turns vague product intent into enforceable application contracts and scenario sheets.

## What's Included

| Type | Files | Count |
|------|-------|-------|
| Skills | `skills/specforge/00-*` through `22-*` | 23 skills |
| Agents | `agents/specforge/overseer.toml`, `analyst.toml`, `architect.toml` | 3 agents |
| Prompts | `prompts/specforge-overseer.md`, `analyst.md`, `architect.md` | 3 prompts |

## Architecture

```
User Input → SpecForge Overseer (specforge-overseer)
  ├── Phase1: Intake (skill 00-intake-goal-clarification)
  │     → Output: INTENT_LEDGER.md
  ├── Phase2: Evidence Review (delegate to specforge-analyst)
  │     → Output: IMPLEMENTATION_EVIDENCE_MAP.md
  ├── Phase3: Gap Analysis (overseer)
  │     → Output: SPEC_GAP_REPORT.md
  ├── Phase4: Targeted Research (delegate to specforge-analyst)
  │     → Output: RESEARCH_FINDINGS.md
  ├── Phase5: Spec Construction (delegate to specforge-architect)
  │     → Output: MASTER_SPEC.md (16 PARTs)
  ├── Phase6: Scenario Generation (delegate to specforge-architect)
  │     → Output: SCENARIOS.md
  ├── Phase7: Adversarial Review (overseer + adversarial skill)
  │     → Output: ADVERSARIAL_REVIEW.md
  └── Phase8: Final Assembly (specforge-architect)
        → Output: Final MASTER_SPEC.md + SCENARIOS.md
```

## Execution Graph

```
User → AgentLoop.act(prompt)
         ↓
    MiddlewarePipeline.before_turn()
         ↓ (Orient: inject system prompt + skills)
    LLM stream_completion()
         ↓ (Plan: skill triggers middleware check)
    ToolManager.execute() → task() subagent spawn
         ↓
    SpecForge skill runs (e.g., specforge-06-requirement-normalization)
         ↓
    MessageList updated, next turn or yield AssistantEvent
```

## Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -r skills/specforge/* ~/.vibe/skills/
cp -r agents/specforge/* ~/.vibe/agents/
cp prompts/specforge-*.md ~/.vibe/prompts/
```

Enable in `~/.vibe/config.toml`:
```toml
agent_paths = ["agents", "agents/specforge"]
enabled_agents = ["specforge-overseer", "specforge-analyst", "specforge-architect"]
enabled_skills = [
  "specforge-00-intake-goal-clarification",
  # ... through 22-final-spec-assembly
]
```

## Phases

1. **Intake** — clarify intent (`specforge-00-intake-goal-clarification`)
2. **Evidence Review** — survey existing docs/code (`01-existing-document-review`, `02-implementation-survey`)
3. **Gap Analysis** — compare intent vs evidence (`03-intent-gap-analysis`)
4. **Targeted Research** — research plan + domain research (`04-research-plan-generation`, `05-targeted-domain-research`)
5. **Spec Construction** — data models, state machines, APIs, UI, security (`06-requirement-normalization` through `18-conflict-resolution-layer`)
6. **Scenario Generation** — scenarios + kill tests (`19-scenario-matrix-generation`, `20-kill-test-generation`)
7. **Adversarial Review** — adversarial spec review (`21-adversarial-spec-review`)
8. **Final Assembly** — assemble final spec (`22-final-spec-assembly`)

## Output Artifacts

- `MASTER_SPEC.md` — 16 PARTs (contract, goals, roles, data models, state machines, API, UI, security, observability, invariants, hard gates, conflict resolution, conformance)
- `SCENARIOS.md` — exhaustive scenarios: kill tests, happy paths, edge cases, permission failures, API violations, security boundary tests
- `INTENT_LEDGER.md`, `IMPLEMENTATION_EVIDENCE_MAP.md`, `SPEC_GAP_REPORT.md`, `RESEARCH_FINDINGS.md` — intermediate artifacts

## Core Doctrine

```
Intent is normative.           (user intent drives everything)
Research is advisory.           (findings inform, don't dictate)
Implementation is evidence.       (existing code is descriptive, not truth)
The spec is authoritative.        (only after adversarial review)
```
