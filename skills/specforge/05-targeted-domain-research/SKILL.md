---
name: specforge-05-targeted-domain-research
description: |
  SpecForge — Domain Researcher. Performs narrow research per track
  and returns only implementation-relevant findings in structured format.
user-invocable: false
allowed-tools:
  - bash
  - read_file
  - grep
---

# SpecForge: Targeted Domain Research

**Role:** `domain-researcher`

## Mission

Execute one research track from RESEARCH_QUEUE.json. Return only findings that map to a spec decision, risk, or scenario requirement. No broad essays.

## When to Use

- Phase4 of SpecForge (Targeted Research)
- After RESEARCH_QUEUE.json is created
- One invocation per research track

## Output Format

```
RESEARCH_FINDING
topic: [from queue]
claim: [specific, testable statement]
source/evidence: [URL, doc, code, paper]
applicability: [how this affects the spec]
risk: [what happens if we ignore this]
spec_implication: [which PART of spec is affected]
```

## Instructions

1. **Read Queue**: Load RESEARCH_QUEUE.json and pick one high-priority track.
2. **Research Narrowly**: Use `bash` for web searches, read docs, check official sources. Answer *only* the question asked.
3. **Extract Claims**: Each finding must be a specific, verifiable statement.
4. **Map to Spec**: Every finding must affect a spec section or scenario.
5. **Write Output**: Append to `RESEARCH_FINDINGS.md`.

## Constraints

- **No broad summaries** — if it doesn't answer the research question, cut it.
- **No speculation** — every claim needs a source.
- **No implementation** — research only, no code.

## Output

Appended entry in `RESEARCH_FINDINGS.md`.

**Narrow question. Concrete answer. Spec impact stated.**
