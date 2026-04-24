---
name: specforge-04-research-plan-generation
description: |
  SpecForge — Research Planner. Converts spec gaps into a prioritized
  research queue with one focused question per unknown.
user-invocable: false
allowed-tools:
  - read_file
  - bash
  - grep
---

# SpecForge: Research Plan Generation

**Role:** `research-planner`

## Mission

Turn the gap report into a structured research queue. Each unknown becomes one narrow research track with a specific question.

## When to Use

- Phase 4 of SpecForge (Targeted Research)
- After SPEC_GAP_REPORT.md identifies research needs
- Before launching domain-researcher agents

## Research Track Template

```json
{
  "topic": "role-based permission model",
  "reason": "application requires multiple user classes but no authority model exists",
  "required_output": "permission matrix implications for spec",
  "priority": "high|medium|low",
  "spec_impact": "which spec section this affects"
}
```

## Research Categories (use as needed)

- authentication models
- data model design
- UI workflows
- user roles and permissions
- scheduling/background jobs
- observability
- failure recovery
- security constraints
- API contract conventions
- storage strategy
- deployment assumptions
- test/scenario coverage patterns

## Instructions

1. **Read Gap Report**: Load SPEC_GAP_REPORT.md.
2. **Convert Each Gap**: One research track per unknown. Never bundle multiple questions.
3. **Prioritize**: High = blocks spec writing. Medium = affects design. Low = nice to know.
4. **Define Output**: Each track must specify what the answer looks like.
5. **Write Output**: `RESEARCH_QUEUE.json`.

## Output

`RESEARCH_QUEUE.json` — prioritized list of research tracks.

Example:
```json
[
  {
    "topic": "session-based auth for SPAs",
    "reason": "intent requires persistent login but no auth model defined",
    "required_output": "recommended auth flow with token lifecycle",
    "priority": "high",
    "spec_impact": "PART 6 — Permissions and Authority Boundaries"
  }
]
```

**Narrow questions. Actionable answers. No essays.**
