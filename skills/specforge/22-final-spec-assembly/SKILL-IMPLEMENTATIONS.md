# 22-final-spec-assembly -- Implementation Guide
==================================================

## Pipeline Placement

**Phase:** Phase8: Final Assembly
**Agent:** specforge-architect
**Output:** MASTER_SPEC.md + SCENARIOS.md

## How This Skill Fits In The Pipeline

```
Phase8: Final Assembly
  Agent: specforge-architect
  Skill: 22-final-spec-assembly
  Output: MASTER_SPEC.md + SCENARIOS.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 22-final-spec-assembly
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
  "skills/specforge/22-final-spec-assembly/SKILL.md",
]
```

## Connects To

- **Previous:** `21-adversarial-spec-review` (Phase7: Adversarial Review)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-architect orchestrate it
- Check the pipeline README for the full flow