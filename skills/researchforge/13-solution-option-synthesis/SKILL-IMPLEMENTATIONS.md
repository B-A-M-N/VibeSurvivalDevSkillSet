# 13-solution-option-synthesis -- Implementation Guide
========================================================

## Pipeline Placement

**Phase:** Phase6: Solution Options
**Agent:** researchforge-synthesizer
**Output:** SOLUTION_OPTIONS.md

## How This Skill Fits In The Pipeline

```
Phase6: Solution Options
  Agent: researchforge-synthesizer
  Skill: 13-solution-option-synthesis
  Output: SOLUTION_OPTIONS.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 13-solution-option-synthesis
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
  "skills/researchforge/13-solution-option-synthesis/SKILL.md",
]
```

## Connects To

- **Previous:** `12-contradiction-hunt` (Phase5: Contradiction Hunt)
- **Next:** `14-validation-plan-generation` (Phase7: Validation Plan)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-synthesizer orchestrate it
- Check the pipeline README for the full flow