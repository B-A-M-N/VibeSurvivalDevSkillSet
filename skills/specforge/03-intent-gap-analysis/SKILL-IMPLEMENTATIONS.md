# 03-intent-gap-analysis -- Implementation Guide
==================================================

## Pipeline Placement

**Phase:** Phase3: Gap Analysis
**Agent:** specforge-overseer
**Output:** SPEC_GAP_REPORT.md

## How This Skill Fits In The Pipeline

```
Phase3: Gap Analysis
  Agent: specforge-overseer
  Skill: 03-intent-gap-analysis
  Output: SPEC_GAP_REPORT.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 03-intent-gap-analysis
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
  "skills/specforge/03-intent-gap-analysis/SKILL.md",
]
```

## Connects To

- **Previous:** `02-implementation-survey` (Phase2: Evidence)
- **Next:** `04-research-plan-generation` (Phase4: Research)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-overseer orchestrate it
- Check the pipeline README for the full flow