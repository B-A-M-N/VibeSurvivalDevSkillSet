# 11-api-contract-specification -- Implementation Guide
=========================================================

## Pipeline Placement

**Phase:** Phase5: Spec Construction
**Agent:** specforge-architect
**Output:** MASTER_SPEC.md (PART 7)

## How This Skill Fits In The Pipeline

```
Phase5: Spec Construction
  Agent: specforge-architect
  Skill: 11-api-contract-specification
  Output: MASTER_SPEC.md (PART 7)
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 11-api-contract-specification
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
  "skills/specforge/11-api-contract-specification/SKILL.md",
]
```

## Connects To

- **Previous:** `10-state-machine-specification` (Phase5: Spec Construction)
- **Next:** `12-ui-behavior-specification` (Phase5: Spec Construction)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-architect orchestrate it
- Check the pipeline README for the full flow