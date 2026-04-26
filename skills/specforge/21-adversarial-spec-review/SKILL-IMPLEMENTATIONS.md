# 21-adversarial-spec-review -- Implementation Guide
======================================================

## Pipeline Placement

**Phase:** Phase7: Adversarial Review
**Agent:** specforge-overseer
**Output:** ADVERSARIAL_REVIEW.md

## How This Skill Fits In The Pipeline

```
Phase7: Adversarial Review
  Agent: specforge-overseer
  Skill: 21-adversarial-spec-review
  Output: ADVERSARIAL_REVIEW.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 21-adversarial-spec-review
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
  "skills/specforge/21-adversarial-spec-review/SKILL.md",
]
```

## Connects To

- **Previous:** `20-kill-test-generation` (Phase6: Scenarios)
- **Next:** `22-final-spec-assembly` (Phase8: Final Assembly)

## Combine With Other Systems

**Part of:** SpecForge System (pipeline skill)

- **ResearchForge** -- use research findings to inform spec writing
- **SkillForge** -- package this spec skill as a reusable component
- **Continuity System** -- ensure spec work survives compaction

## Tips

- This skill runs as part of the SpecForge pipeline
- Do not invoke directly -- let specforge-overseer orchestrate it
- Check the pipeline README for the full flow