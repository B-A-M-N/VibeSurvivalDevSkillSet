---
name: researchforge-02-evidence-collection
description: |
  ResearchForge — Evidence Collection. Collects existing evidence
  from docs, logs, code, issues, and official sources.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# ResearchForge: Evidence Collection

**Role:** `evidence-collector` — Phase2

## Mission

Collect all existing evidence. Docs, logs, code comments, issue threads, error traces, configs. Evidence is collected, NOT interpreted yet.

## When to Use

- Phase2 of ResearchForge (Build Evidence Ledger)
- After PROBLEM_FRAME.md and CONTEXT_MAP.md are complete
- Before generating hypotheses

## Evidence Classification

```
DIRECT_OBSERVATION > OFFICIAL_DOC > UPSTREAM_SOURCE > REPRODUCTION > SECONDARY_SOURCE > ASSUMPTION
```

## Evidence Ledger Template

```
EVIDENCE_LEDGER.md
==================

CLAIM: [statement being evidenced]
SOURCE: [where this comes from]
  type: DIRECT_OBSERVATION | OFFICIAL_DOC | UPSTREAM_SOURCE | REPRODUCTION | LOG_TRACE | CODE_BEHAVIOR | EXPERT_ANALYSIS | SECONDARY_SOURCE | ASSUMPTION
CONFIDENCE: high | medium | low
RELEVANCE: [how this relates to the problem]
CONTRADICTIONS: [other evidence that conflicts with this]
NOTES: [additional context]
```

## Sources to Check

- **Docs**: README, docs/, wikis, architecture docs
- **Logs**: application logs, error logs, access logs
- **Code Comments**: TODO, FIXME, comments explaining why
- **Issue Threads**: GitHub issues, Jira, support tickets
- **Error Traces**: stack traces, core dumps, error messages
- **Configs**: .env, config files, deployment configs
- **Examples**: sample inputs/outputs, test cases
- **Prior Attempts**: previous fixes, workarounds tried
- **Official Documentation**: vendor docs, RFCs, standards
- **Upstream Discussions**: GitHub discussions, mailing lists

## Instructions

1. **Read Problem Frame**: Understand what evidence is relevant.
2. **Collect Systematically**: Go through each source type listed above.
3. **Classify Each Claim**: Use the confidence hierarchy. No "medium" for everything.
4. **Note Contradictions**: If evidence A says X and evidence B says Y, note it.
5. **Don't Explain Yet**: Collect only. Save interpretation for hypothesis phase.
6. **Write Output**: `EVIDENCE_LEDGER.md`.

## Output

`EVIDENCE_LEDGER.md` — the evidence base for hypothesis generation.

**Evidence without confidence is hearsay. Classify or discard.**
