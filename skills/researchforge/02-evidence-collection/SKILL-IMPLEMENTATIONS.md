# 02-evidence-collection -- Implementation Guide
==================================================

## Pipeline Placement

**Phase:** Phase2: Evidence Ledger
**Agent:** researchforge-evidence
**Output:** EVIDENCE_LEDGER.md

## How This Skill Fits In The Pipeline

```
Phase2: Evidence Ledger
  Agent: researchforge-evidence
  Skill: 02-evidence-collection
  Output: EVIDENCE_LEDGER.md
```

## Proper Implementation

### SKILL.md Frontmatter
```yaml
---
name: 02-evidence-collection
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
  "skills/researchforge/02-evidence-collection/SKILL.md",
]
```

## Connects To

- **Previous:** `01-context-map` (Phase1: Frame Problem)
- **Next:** `03-source-quality-check` (Phase2: Evidence Ledger)

## Combine With Other Systems

**Part of:** ResearchForge System (Pipeline skill)

- **SpecForge** -- feed research into spec generation
- **SkillForge** -- package this skill as a reusable component
- **Continuity System** -- ensure research work survives compaction

## Tips

- This skill runs as part of the ResearchForge pipeline
- Do not invoke directly -- let researchforge-evidence orchestrate it
- Check the pipeline README for the full flow