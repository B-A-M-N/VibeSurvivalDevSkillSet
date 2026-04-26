# 12-contradiction-hunt -- Implementation Guide
=================================================

## Pipeline Placement

**Phase:** Phase5: Contradiction Hunt
**Agent:** researchforge-evidence
**Output:** CONTRADICTION_REPORT.md

## How This Skill Fits In The Pipeline

```
Phase5: Contradiction Hunt
  Agent: researchforge-evidence
  Skill: 12-contradiction-hunt
  Output: CONTRADICTION_REPORT.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 12-contradiction-hunt
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
  "skills/researchforge/12-contradiction-hunt/SKILL.md",
]
```

## Connects To

- **Previous:** `11-risk-research` (Phase4: Targeted Research)
- **Next:** `13-solution-option-synthesis` (Phase6: Solution Options)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-evidence orchestrate it
- Check the pipeline README for the full flow