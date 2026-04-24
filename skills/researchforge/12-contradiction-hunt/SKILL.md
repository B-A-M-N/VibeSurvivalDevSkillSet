---
name: researchforge-12-contradiction-hunt
description: |
  ResearchForge — Contradiction Hunt. Actively looks for reasons
  the current theory is wrong, unsupported assumptions, and weak claims.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# ResearchForge: Contradiction Hunt

**Role:** `contradiction-hunter` — Phase5

## Mission

Actively look for reasons the current theory is wrong. Find unsupported assumptions, stale docs, version mismatches, misleading symptoms, and overfitted explanations.

## When to Use

- Phase5 of ResearchForge (Contradiction Pass)
- After research findings are collected
- Before synthesizing solution options

## Contradiction Report Template

```
CONTRADICTION_REPORT.md
======================

UNSUPPORTED_ASSUMPTIONS:
  - assumption: [what we're assuming without evidence]
    why_weak: [no evidence, or evidence is low-confidence]
    contradicts: [evidence ID that disproves this]

STALE_DOCS:
  - claim: [what doc says]
    doc_date: [when doc was written]
    current_version: [what we're running]
    mismatch: [how it's wrong now]

VERSION_MISMATCHES:
  - expectation: [what we think happens, based on version X docs]
    reality: [what actually happens in version Y]
    source: [where expectation came from]

MILEADING_SYMPTOMS:
  - symptom: [what we observe]
    false_conclusion: [what it seems to mean]
    actual_cause: [what it actually means]
    why_misleading: [correlation vs causation]

FALSE_CORRELATIONS:
  - observation: [A and B happen together]
    correlation: [A causes B?]
    reality: [C causes both A and B]
    evidence: [why this is false correlation]

CARGO_CULT_FIXES:
  - fix: [common "solution" found online]
    why_wrong: [doesn't address root cause]
    correct_fix: [what actually solves it]

OVERFITTED_EXPLANATIONS:
  - hypothesis: [H-NNN overfitted to one observation]
    why_overfitted: [ignores contrary evidence]
    broader_view: [what a general explanation looks like]
```

## Instructions

1. **Read Everything**: Load HYPOTHESIS_MATRIX.md, RESEARCH_FINDINGS.md, EVIDENCE_LEDGER.md.
2. **Hunt Contradictions**: For each hypothesis, what evidence contradicts it?
3. **Check Staleness**: Are docs/versions aligned with reality?
4. **Question Symptoms**: Does the error message really mean what we think?
5. **Flag Cargo Cult**: Popular fixes that don't address root cause.
6. **Write Output**: `CONTRADICTION_REPORT.md`.

## Output

`CONTRADICTION_REPORT.md` — known weaknesses in the current theory.

**If you can't find a reason you're wrong, you're not looking hard enough.**
