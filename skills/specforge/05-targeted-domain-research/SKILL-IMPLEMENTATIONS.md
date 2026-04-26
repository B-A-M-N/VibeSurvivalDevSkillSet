# 05-targeted-domain-research -- Implementation Guide
=======================================================

## Pipeline Placement

**Phase:** Phase4: Research
**Agent:** specforge-analyst
**Output:** RESEARCH_FINDINGS.md

## How This Skill Fits In The Pipeline

```
Phase4: Research
  Agent: specforge-analyst
  Skill: 05-targeted-domain-research
  Output: RESEARCH_FINDINGS.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 05-targeted-domain-research
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
  "skills/specforge/05-targeted-domain-research/SKILL.md",
]
```

## Connects To

- **Previous:** `04-research-plan-generation` (Phase4: Research)
- **Next:** `06-requirement-normalization` (Phase5: Spec Construction)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-analyst orchestrate it
- Check the pipeline README for the full flow