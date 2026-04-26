# 01-existing-document-review -- Implementation Guide
=======================================================

## Pipeline Placement

**Phase:** Phase2: Evidence
**Agent:** specforge-analyst
**Output:** IMPLEMENTATION_EVIDENCE_MAP.md

## How This Skill Fits In The Pipeline

```
Phase2: Evidence
  Agent: specforge-analyst
  Skill: 01-existing-document-review
  Output: IMPLEMENTATION_EVIDENCE_MAP.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 01-existing-document-review
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
name = "specforge-analyst"
model = "Mistral-Large"
system_prompt_id = "specforge_analyst"
skill_files = [
  "skills/specforge/01-existing-document-review/SKILL.md",
]
```

## Connects To

- **Previous:** `00-intake-goal-clarification` (Phase1: Intake)
- **Next:** `02-implementation-survey` (Phase2: Evidence)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-analyst orchestrate it
- Check the pipeline README for the full flow