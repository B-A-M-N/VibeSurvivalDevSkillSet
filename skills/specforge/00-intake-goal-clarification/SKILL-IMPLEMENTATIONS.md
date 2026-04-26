# 00-intake-goal-clarification -- Implementation Guide
========================================================

## Pipeline Placement

**Phase:** Phase1: Intake
**Agent:** specforge-overseer
**Output:** INTENT_LEDGER.md

## How This Skill Fits In The Pipeline

```
Phase1: Intake
  Agent: specforge-overseer
  Skill: 00-intake-goal-clarification
  Output: INTENT_LEDGER.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 00-intake-goal-clarification
description: |
  [Brief description of what this skill does in the pipeline]
user-invocable: false  # These are pipeline-internal
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
name = "specforge-overseer"
model = "Mistral-Large"
system_prompt_id = "specforge_overseer"
skill_files = [
  "skills/specforge/00-intake-goal-clarification/SKILL.md",
]
```

## Connects To

- **Next:** `01-existing-document-review` (Phase2: Evidence)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-overseer orchestrate it
- Check the pipeline README for the full flow