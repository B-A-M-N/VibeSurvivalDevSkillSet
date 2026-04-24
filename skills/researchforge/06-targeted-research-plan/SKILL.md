---
name: researchforge-06-targeted-research-plan
description: |
  ResearchForge — Targeted Research Plan. Converts remaining
  unknowns into narrow research questions with expected outputs.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# ResearchForge: Targeted Research Plan

**Role:** `research-overseer` — Phase4 (planning)

## Mission

Convert remaining unknowns and disconfirmed hypotheses into a targeted research plan. No broad "learn about X" — narrow questions only.

## When to Use

- Phase4 of ResearchForge (Targeted Research)
- After disconfirmation narrows down the hypotheses
- When specific unknowns remain

## Research Plan Template

```
RESEARCH_PLAN.md
===============

UNKNOWN: [what we still don't know]
CURRENT_BEST_HYPOTHESIS: [H-NNN or "none remaining"]

RESEARCH_TRACKS:
  - id: RT-NNN
    question: [specific, narrow question]
    bad_example: "Research terminal streaming"
    good_example: "What causes xterm.js scrollback memory growth under long-running PTY streams?"
    expected_output: [what the answer looks like]
    source_type: OFFICIAL_DOC | UPSTREAM_SOURCE | EXPERT_ANALYSIS | REPRODUCTION
    priority: high | medium | low
    relates_to_hypothesis: [H-NNN or "general understanding"]

  - id: RT-NNN
    ...
```

## Quality Rules

| Bad Research Question | Good Research Question |
|---------------------|----------------------|
| Research terminal streaming | What causes xterm.js scrollback memory growth under long-running PTY streams? |
| Learn about OAuth2 | What is the PKCE flow for OAuth2 with single-page apps behind a reverse proxy? |
| Check API docs | What HTTP status does the Stripe API return for rate-limited webhook endpoints? |

## Instructions

1. **Read Hypotheses + Disconfirmation**: Load HYPOTHESIS_MATRIX.md and DISCONFIRMATION_REPORT.md.
2. **Identify Unknowns**: What still needs answering to confirm or deny the remaining hypotheses?
3. **Write Narrow Questions**: Each RT-NNN must be a specific question, not a topic.
4. **Define Expected Output**: What does the answer look like? How will we know it when we see it?
5. **Prioritize**: High = confirms/disconfirms active hypothesis. Medium = strengthens evidence. Low = nice to know.
6. **Write Output**: `RESEARCH_PLAN.md`.

## Output

`RESEARCH_PLAN.md` — prioritized, narrow research tracks.

**Broad research is procrastination. Narrow questions are progress.**
