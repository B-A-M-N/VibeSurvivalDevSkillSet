---
name: researchforge-07-official-docs-research
description: |
  ResearchForge — Official Docs Research. Researches official
  documentation, RFCs, and standards for authoritative answers.
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Grep
---

# ResearchForge: Official Docs Research

**Role:** `targeted-researcher` — Phase4 (official sources)

## Mission

Research official documentation, RFCs, and standards. Find authoritative answers to research questions. No Stack Overflow guesses — go to the source.

## When to Use

- Phase4 of ResearchForge (Targeted Research)
- When a research track requires authoritative answers
- Before trusting third-party tutorials or blog posts

## Research Template

```
RESEARCH_FINDING
==============

TRACK_ID: [RT-NNN from RESEARCH_PLAN.md]
QUESTION: [the narrow question being answered]

ANSWER: [specific, direct answer to the question]

SOURCE:
  name: [official doc name]
  url: [exact URL]
  section: [specific section or page]
  last_updated: [date if available]
  authority: HIGH (official docs get highest authority)

EVIDENCE:
  - quote: "[exact text from docs]"
    context: [surrounding context]
  - quote: "[another relevant excerpt]"

CONFIDENCE: high | medium | low
  reasoning: [why this confidence level]

APPLICABILITY:
  applies_to: [which hypothesis or problem aspect]
  limitation: [when this doesn't apply]

NEXT_QUESTION: [what this answer leads to next, if anything]
```

## Official Sources to Check

- **Vendor Docs**: Official API docs, SDK documentation, configuration guides
- **RFCs/Standards**: IETF RFCs, W3C specs, ISO standards
- **Man Pages**: `man` pages for system calls, commands
- **Language Specs**: Language reference manuals, type system docs
- **Git Repo Docs**: Official README, CONTRIBUTING, ARCHITECTURE docs in repo

## Instructions

1. **Read Research Plan**: Load RESEARCH_PLAN.md. Pick one track.
2. **Go to Source**: Don't Google — go directly to official docs.
3. **Extract Quotes**: Exact text that answers the question. No paraphrase without quote.
4. **Check Date**: When was this doc last updated? Is it current?
5. **Map to Problem**: How does this answer affect the hypothesis or solution?
6. **Write Output**: Append to `RESEARCH_FINDINGS.md`.

## Output

Appended entry in `RESEARCH_FINDINGS.md`.

**Official docs are the gold standard. Secondary sources are silver. Everything else is copper.**
