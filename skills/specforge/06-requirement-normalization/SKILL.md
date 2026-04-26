---
name: specforge-06-requirement-normalization
description: |
  SpecForge — Requirement Normalization. Converts raw intent, research findings,
  and implementation evidence into normalized, testable requirements.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# SpecForge: Requirement Normalization

**Role:** `spec-architect` — Phase5 Prep

## Mission

Convert raw inputs (intent, research, evidence) into normalized requirements. Each requirement must be testable, unambiguous, and traceable to a source.

## When to Use

- After research findings are complete
- Before writing the master spec
- When requirements are vague, conflicting, or untestable

## Normalization Rules

1. **Testable**: Must be verifiable by observation or test.
2. **Unambiguous**: One interpretation only.
3. **Traceable**: Links to intent, research, or evidence.
4. **Atomic**: One requirement per statement.
5. **No TBD**: Either decide or mark as user-decision-required.

## Requirement Template

```
REQ-[NNN]
source: INTENT | RESEARCH | EVIDENCE | USER
statement: [normalized requirement]
testability: [how to verify]
priority: MUST | SHOULD | MAY
spec_section: [PART X]
conflicts_with: [other REQ-IDs, if any]
```

## Instructions

1. **Gather Inputs**: Read INTENT_LEDGER.md, RESEARCH_FINDINGS.md, IMPLEMENTATION_EVIDENCE_MAP.md.
2. **Normalize Each**: Convert every intent item, research implication, and evidence-based need into REQ-NNN format.
3. **Resolve Conflicts**: If two requirements conflict, flag for user decision.
4. **Write Output**: `NORMALIZED_REQUIREMENTS.md`.

## Output

`NORMALIZED_REQUIREMENTS.md` — the canonical, testable requirement set.

**Vague requirements breed vague specs. Normalize or die.**
