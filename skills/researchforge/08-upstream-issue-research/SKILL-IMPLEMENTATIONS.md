# 08-upstream-issue-research -- Implementation Guide
======================================================

## Pipeline Placement

**Phase:** Phase4: Targeted Research
**Agent:** researchforge-researcher
**Output:** RESEARCH_FINDINGS.md

## How This Skill Fits In The Pipeline

```
Phase4: Targeted Research
  Agent: researchforge-researcher
  Skill: 08-upstream-issue-research
  Output: RESEARCH_FINDINGS.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 08-upstream-issue-research
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
name = "researchforge-researcher"
model = "Mistral-Large"
system_prompt_id = "researchforge_researcher"
skill_files = [
  "skills/researchforge/08-upstream-issue-research/SKILL.md",
]
```

## Connects To

- **Previous:** `07-official-docs-research` (Phase4: Targeted Research)
- **Next:** `09-version-compatibility-research` (Phase4: Targeted Research)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-researcher orchestrate it
- Check the pipeline README for the full flow