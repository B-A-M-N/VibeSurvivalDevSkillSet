---
name: researchforge-16-adversarial-research-review
description: |
  ResearchForge — Adversarial Research Review. Final quality gate
  that rejects the packet if recommendations lack evidence or sources are weak.
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
  - ask_user_question
---

# ResearchForge: Adversarial Research Review

**Role:** `research-reviewer` — Final Quality Gate

## Mission

Final quality gate for the research packet. Reject if the packet is weak. No weak sources, no speculation, no untestable recommendations.

## When to Use

- After FINAL_RESEARCH_PACKET.md is assembled
- Before handing off to implementation/spec team
- When you suspect the packet is overconfident

## Rejection Checklist

```
RESEARCH_REVIEW.md
===============

PACKET_QUALITY: PASS | REJECT

REJECT_IF_ANY:
  [ ] Recommendation lacks evidence
  [ ] Problem framing is vague
  [ ] Sources are weak (too many LOW confidence)
  [ ] Contradictions are unresolved
  [ ] Confidence is overstated (high confidence, weak evidence)
  [ ] No validation path exists
  [ ] Solution is actually speculation
  [ ] Hypothesis without disconfirmation criteria
  [ ] Broad research instead of narrow questions
  [ ] Implementation changes snuck in (research only!)
  [ ] Solution has no fallback plan
  [ ] Remaining unknowns are critical but unaddressed
```

## Confidence Audit

```
CONFIDENCE_AUDIT:

High confidence claims:
  - claim: [statement]
    evidence_strength: HIGH | MEDIUM | LOW
    passes_audit: YES | NO (explain why)

Medium confidence claims:
  - claim: [statement]
    evidence_strength: HIGH | MEDIUM | LOW
    passes_audit: YES | NO (explain why)

Low confidence claims:
  - claim: [statement]
    evidence_strength: LOW
    acceptable: YES (explicitly marked low) | NO (should be higher)
```

## Source Quality Audit

```
SOURCE_AUDIT:

Official/Upstream sources: [count]
Secondary sources: [count]
Assumptions: [count]

Verdict:
  - Strong: >70% official/upstream sources
  - Moderate: 40-70% official/upstream
  - Weak: <40% official/upstream — REJECT
```

## Instructions

1. **Read Packet**: Load FINAL_RESEARCH_PACKET.md in full.
2. **Run Rejection Checklist**: Check every item. Any FAIL = REJECT.
3. **Audit Confidence**: Does confidence match evidence strength?
4. **Audit Sources**: Is the source mix strong enough?
5. **Write Review**: `RESEARCH_REVIEW.md` with PASS/REJECT verdict.
6. **If REJECT**: List specific fixes needed, which artifacts to update.
7. **If PASS**: Packet is ready for handoff.

## Output

`RESEARCH_REVIEW.md` with PASS/REJECT verdict and audit details.

**A weak research packet poisons the well. Reject early, fix fast.**
