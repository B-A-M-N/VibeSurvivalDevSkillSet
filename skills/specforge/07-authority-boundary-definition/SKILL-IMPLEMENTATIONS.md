# 07-authority-boundary-definition -- Implementation Guide
============================================================

## Pipeline Placement

**Phase:** Phase5: Spec Construction
**Agent:** specforge-architect
**Output:** MASTER_SPEC.md (PART 6)

## How This Skill Fits In The Pipeline

```
Phase5: Spec Construction
  Agent: specforge-architect
  Skill: 07-authority-boundary-definition
  Output: MASTER_SPEC.md (PART 6)
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 07-authority-boundary-definition
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
name = "specforge-architect"
model = "Mistral-Large"
system_prompt_id = "specforge_architect"
skill_files = [
  "skills/specforge/07-authority-boundary-definition/SKILL.md",
]
```

## Connects To

- **Previous:** `06-requirement-normalization` (Phase5: Spec Construction)
- **Next:** `08-data-model-specification` (Phase5: Spec Construction)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-architect orchestrate it
- Check the pipeline README for the full flow