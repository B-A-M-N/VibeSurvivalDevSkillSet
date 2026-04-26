# 14-validation-plan-generation -- Implementation Guide
=========================================================

## Pipeline Placement

**Phase:** Phase7: Validation Plan
**Agent:** researchforge-synthesizer
**Output:** VALIDATION_PLAN.md

## How This Skill Fits In The Pipeline

```
Phase7: Validation Plan
  Agent: researchforge-synthesizer
  Skill: 14-validation-plan-generation
  Output: VALIDATION_PLAN.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 14-validation-plan-generation
description: |
  [Description of what this skill does in the ResearchForge pipeline]
user-invocable: false  # Pipeline-internal
allowed-tools:
  - Read
  - Grep
  - Bash
  - Write
  - Agent  # for subagent delegation
---
```

### Agent TOML (Partial)
```toml
[agent]
name = "researchforge-synthesizer"
model = "Mistral-Large"
system_prompt_id = "researchforge_synthesizer"
skill_files = [
  "skills/researchforge/14-validation-plan-generation/SKILL.md",
]
```

## Connects To

- **Previous:** `13-solution-option-synthesis` (Phase6: Solution Options)
- **Next:** `15-final-research-packet` (Phase8: Final Packet)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-synthesizer orchestrate it
- Check the pipeline README for the full flow