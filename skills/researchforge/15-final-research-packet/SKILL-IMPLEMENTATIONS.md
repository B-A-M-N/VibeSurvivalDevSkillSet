# 15-final-research-packet -- Implementation Guide
====================================================

## Pipeline Placement

**Phase:** Phase8: Final Packet
**Agent:** researchforge-synthesizer
**Output:** FINAL_RESEARCH_PACKET.md

## How This Skill Fits In The Pipeline

```
Phase8: Final Packet
  Agent: researchforge-synthesizer
  Skill: 15-final-research-packet
  Output: FINAL_RESEARCH_PACKET.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 15-final-research-packet
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
name = "researchforge-synthesizer"
model = "Mistral-Large"
system_prompt_id = "researchforge_synthesizer"
skill_files = [
  "skills/researchforge/15-final-research-packet/SKILL.md",
]
```

## Connects To

- **Previous:** `14-validation-plan-generation` (Phase7: Validation Plan)
- **Next:** `16-adversarial-research-review` (Phase9: Adversarial Review)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-synthesizer orchestrate it
- Check the pipeline README for the full flow