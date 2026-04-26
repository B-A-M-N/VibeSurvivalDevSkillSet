# 05-hypothesis-disconfirmation -- Implementation Guide
=========================================================

## Pipeline Placement

**Phase:** Phase3: Hypotheses
**Agent:** researchforge-evidence
**Output:** DISCONFIRMATION_REPORT.md

## How This Skill Fits In The Pipeline

```
Phase3: Hypotheses
  Agent: researchforge-evidence
  Skill: 05-hypothesis-disconfirmation
  Output: DISCONFIRMATION_REPORT.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 05-hypothesis-disconfirmation
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
name = "researchforge-evidence"
model = "Mistral-Large"
system_prompt_id = "researchforge_evidence"
skill_files = [
  "skills/researchforge/05-hypothesis-disconfirmation/SKILL.md",
]
```

## Connects To

- **Previous:** `04-hypothesis-generation` (Phase3: Hypotheses)
- **Next:** `06-targeted-research-plan` (Phase4: Targeted Research)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-evidence orchestrate it
- Check the pipeline README for the full flow