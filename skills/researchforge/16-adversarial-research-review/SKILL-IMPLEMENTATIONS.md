# 16-adversarial-research-review -- Implementation Guide
==========================================================

## Pipeline Placement

**Phase:** Phase9: Adversarial Review
**Agent:** researchforge-overseer
**Output:** RESEARCH_REVIEW.md

## How This Skill Fits In The Pipeline

```
Phase9: Adversarial Review
  Agent: researchforge-overseer
  Skill: 16-adversarial-research-review
  Output: RESEARCH_REVIEW.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 16-adversarial-research-review
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
name = "researchforge-overseer"
model = "Mistral-Large"
system_prompt_id = "researchforge_overseer"
skill_files = [
  "skills/researchforge/16-adversarial-research-review/SKILL.md",
]
```

## Connects To

- **Previous:** `15-final-research-packet` (Phase8: Final Packet)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-overseer orchestrate it
- Check the pipeline README for the full flow