# 00-problem-intake -- Implementation Guide
=============================================

## Pipeline Placement

**Phase:** Phase1: Frame Problem
**Agent:** researchforge-overseer
**Output:** PROBLEM_FRAME.md, CONTEXT_MAP.md

## How This Skill Fits In The Pipeline

```
Phase1: Frame Problem
  Agent: researchforge-overseer
  Skill: 00-problem-intake
  Output: PROBLEM_FRAME.md, CONTEXT_MAP.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 00-problem-intake
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
name = "researchforge-overseer"
model = "Mistral-Large"
system_prompt_id = "researchforge_overseer"
skill_files = [
  "skills/researchforge/00-problem-intake/SKILL.md",
]
```

## Connects To

- **Next:** `01-context-map` (Phase1: Frame Problem)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-overseer orchestrate it
- Check the pipeline README for the full flow