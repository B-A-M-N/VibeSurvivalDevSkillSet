---
name: researchforge-03-source-quality-check
description: |
  ResearchForge — Source Quality Check. Audits evidence sources
  for staleness, authority, and contradictions.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# ResearchForge: Source Quality Check

**Role:** `contradiction-hunter` — Phase2 (quality gate)

## Mission

Audit the evidence ledger. Find stale docs, weak sources, version mismatches, and contradictions. Bad evidence leads to bad hypotheses.

## When to Use

- After EVIDENCE_LEDGER.md is populated
- Before generating hypotheses
- When evidence seems contradictory or shaky

## Quality Checklist

```
SOURCE_QUALITY_REPORT.md
======================

STALE_SOURCES:
  [ ] Docs written for version X, but running version Y
  [ ] Links to 404 pages or deprecated endpoints
  [ ] References to deprecated features or APIs
  [ ] Config examples that no longer apply

WEAK_SOURCES:
  [ ] Blog posts without dates
  [ ] Stack Overflow answers > 2 years old
  [ ] Assumptions passed off as facts
  [ ] Second-hand reports without original evidence

VERSION_MISMATCHES:
  [ ] Doc says version A, installed is version B
  [ ] Code uses API v1, docs show v2
  [ ] Dependency versions in conflict

CONTRADICTIONS:
  [ ] Evidence A says X, Evidence B says not-X
  [ ] Two config files disagree
  [ ] Doc says "supported", code throws "not implemented"
  [ ] Log says success, but error returned

MISSING_SOURCES:
  [ ] No official docs for critical component
  [ ] Version not pinned anywhere
  [ ] No error message documentation
```

## Instructions

1. **Read Evidence Ledger**: Load EVIDENCE_LEDGER.md.
2. **Check Each Source**: For each evidence entry, verify:
   - Is the source still valid? (stale?)
   - Is the source authoritative? (weak?)
   - Does the version match reality? (mismatch?)
   - Does it contradict other evidence?
3. **Flag Weak Evidence**: Mark low-confidence or contradictory evidence for extra scrutiny.
4. **Recommend Actions**: For each issue, recommend: verify, replace, or discard.
5. **Write Output**: `SOURCE_QUALITY_REPORT.md`.

## Output

`SOURCE_QUALITY_REPORT.md` — evidence quality audit.

**Weak evidence corrupts research. Audit before you hypothesize.**
