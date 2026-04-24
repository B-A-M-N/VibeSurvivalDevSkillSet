---
name: specforge-03-intent-gap-analysis
description: |
  SpecForge — Gap Analysis. Compares stated intent against existing implementation
  to find missing decisions, contradictions, and research needs.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - ask_user_question
  - bash
---

# SpecForge: Intent Gap Analysis

**Role:** `specforge-overseer` — Phase 3

## Mission

Compare what the user wants against what exists. Identify every gap, contradiction, and missing decision. This is the bridge between intent and spec.

## When to Use

- Phase 3 of SpecForge (Gap Analysis)
- After INTENT_LEDGER.md and IMPLEMENTATION_EVIDENCE_MAP.md exist
- Before any research or spec writing

## Comparison Framework

```
STATED_INTENT (from INTENT_LEDGER.md):
  - purpose
  - requirements
  - success criteria
  - boundaries

EXISTING_IMPLEMENTATION (from IMPLEMENTATION_EVIDENCE_MAP.md):
  - features
  - behavior
  - assumptions

GAPS:
  - missing features
  - missing requirements
  - undefined behavior
  - unhandled edge cases

CONTRADICTIONS:
  - intent says X, implementation does Y
  - docs disagree with code
  - conflicting requirements

RESEARCH_NEEDED:
  - unresolved technical questions
  - undefined user roles
  - missing data models
  - unclear authority boundaries
```

## Instructions

1. **Read Both Ledgers**: Load INTENT_LEDGER.md and IMPLEMENTATION_EVIDENCE_MAP.md.
2. **Line Up Comparisons**: For each intent item, check implementation status.
3. **Flag Gaps**: Anything in intent not in implementation = gap. Anything in implementation not in intent = potential accident.
4. **Identify Research Needs**: Convert gaps into research questions.
5. **Ask Unresolved Questions**: Use `ask_user_question` for blocking ambiguities.
6. **Write Output**: `SPEC_GAP_REPORT.md`.

## Output

`SPEC_GAP_REPORT.md` containing:
- Stated intent summary
- Existing implementation summary
- Gap list (with severity)
- Contradiction list
- Research queue (questions to answer)
- Blocking ambiguities (user must answer)

**Every gap is a spec decision waiting to happen.**
