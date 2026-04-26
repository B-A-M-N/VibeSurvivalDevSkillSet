# 19-scenario-matrix-generation -- Implementation Guide
=========================================================

## Pipeline Placement

**Phase:** Phase6: Scenarios
**Agent:** specforge-architect
**Output:** SCENARIOS.md

## How This Skill Fits In The Pipeline

```
Phase6: Scenarios
  Agent: specforge-architect
  Skill: 19-scenario-matrix-generation
  Output: SCENARIOS.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 19-scenario-matrix-generation
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
  "skills/specforge/19-scenario-matrix-generation/SKILL.md",
]
```

## Connects To

- **Previous:** `18-conflict-resolution-layer` (Phase5: Spec Construction)
- **Next:** `20-kill-test-generation` (Phase6: Scenarios)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-architect orchestrate it
- Check the pipeline README for the full flow