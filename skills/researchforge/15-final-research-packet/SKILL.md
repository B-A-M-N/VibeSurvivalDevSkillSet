---
name: researchforge-15-final-research-packet
description: |
  ResearchForge — Final Research Packet. Assembles all research
  into a structured packet for use by implementation/spec agents.
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Bash
  - Write
---

# ResearchForge: Final Research Packet

**Role:** `solution-synthesizer` + `research-reviewer` — Phase8

## Mission

Assemble all research into a structured packet that another agent/person can use to act. No recommendation without evidence. No hypothesis without disconfirmation.

## When to Use

- Phase8 of ResearchForge (Final Packet)
- After VALIDATION_PLAN.md is complete
- Before handing off to implementation/spec team

## Final Packet Structure

```
FINAL_RESEARCH_PACKET.md
=======================

1. PROBLEM_FRAME.md (included)
   - Observed issue
   - Desired outcome
   - Success criteria
   - Non-goals

2. CONTEXT_MAP.md (included)
   - Component map
   - Dependency graph
   - External services
   - Environment

3. EVIDENCE_LEDGER.md (included)
   - All evidence with confidence levels
   - Source quality report

4. HYPOTHESIS_MATRIX.md (included)
   - All hypotheses with disconfirmation results
   - Updated confidence levels

5. RESEARCH_FINDINGS.md (included)
   - All targeted research results
   - Official docs, upstream issues, version checks
   - Patterns and risks identified

6. CONTRADICTION_REPORT.md (included)
   - Unsupported assumptions
   - Stale docs and version mismatches
   - False correlations

7. SOLUTION_OPTIONS.md (included)
   - Option A: [summary]
     - Evidence basis
     - Risk assessment
     - Fallback plan
   - Option B: [summary]
     - ...

8. VALIDATION_PLAN.md (included)
   - Tests to run
   - Expected results
   - Rollback criteria

9. REMAINING_UNKNOWNS
   - [what we stil don't know]
   - [gaps that remain]

10. CONFIDENCE_ASSESSMENT
    - Overall confidence: high | medium | low
    - Reasoning: [why this confidence]
    - Evidence strength: [strong | moderate | weak]
    - Outstanding risks: [what could still go wrong]
```

## Quality Gate (Research Reviewer)

Before finalizing, check:
- [ ] Every recommendation has evidence
- [ ] Every hypothesis has disconfirmation criteria
- [ ] No source treated as equal (confidence hierarchy respected)
- [ ] No implementation changes (research only)
- [ ] No broad research (all questions were narrow)
- [ ] Confidence level matches evidence quality
- [ ] Problem frame is coherent
- [ ] Solution has fallback plan

## Instructions

1. **Gather All Artifacts**: Load all .md files listed above.
2. **Review Quality Gate**: Run the checklist. Fix any failures.
3. **Assemble Packet**: Combine into `FINAL_RESEARCH_PACKET.md`.
4. **Write Output**: Save to project root or `research/` directory.

## Output

`FINAL_RESEARCH_PACKET.md` — the complete, actionable research packet.

**The research packet is the foundation. Build on rock, not sand.**
