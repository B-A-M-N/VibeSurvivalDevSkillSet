---
name: specforge-01-existing-document-review
description: |
  SpecForge — Intent Analyst. Extracts goals, requirements, and contradictions
  from existing docs, README files, issues, and partial specs.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# SpecForge: Existing Document Review

**Role:** `intent-analyst`

## Mission

Read all available documentation and extract intent. Never treat existing docs as ground truth — they are *evidence of intent*.

## When to Use

- Phase 2 of SpecForge (Existing Evidence Review)
- User provides docs, README, issues, partial specs
- Before surveying implementation

## Extraction Template

```
INTENDED_APPLICATION_PURPOSE:
TARGET_USERS:
JOBS_TO_BE_DONE:
EXPLICIT_REQUIREMENTS:
IMPLIED_REQUIREMENTS:
CONTRADICTIONS:
UNKNOWNS:
NON_GOALS:
AUTHORITY_BOUNDARIES:
```

## Critical Rule

> It may say "current documentation states X," but never "the system must do X" unless backed by stated user intent or explicit confirmation.

## Instructions

1. **Read All Docs**: README, docs/, issues, PR descriptions, comments in code.
2. **Extract Intent**: Fill each template section from evidence found.
3. **Flag Contradictions**: Note where docs disagree with each other.
4. **Mark Unknowns**: Be explicit about what cannot be determined.
5. **Write Output**: `INTENT_LEDGER.md` — append or create if not exists.

## Output

Updated `INTENT_LEDGER.md` with document-derived intent only.

**Docs describe. Intent decides.**
