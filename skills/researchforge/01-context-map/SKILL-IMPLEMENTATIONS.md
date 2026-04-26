# 01-context-map -- Implementation Guide
==========================================

## Pipeline Placement

**Phase:** Phase1: Frame Problem
**Agent:** researchforge-overseer
**Output:** CONTEXT_MAP.md

## How This Skill Fits In The Pipeline

```
Phase1: Frame Problem
  Agent: researchforge-overseer
  Skill: 01-context-map
  Output: CONTEXT_MAP.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 01-context-map
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
  "skills/researchforge/01-context-map/SKILL.md",
]
```

## Connects To

- **Previous:** `00-problem-intake` (Phase1: Frame Problem)
- **Next:** `02-evidence-collection` (Phase2: Evidence Ledger)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-overseer orchestrate it
- Check the pipeline README for the full flow