---
name: researchforge-10-architecture-pattern-research
description: |
  ResearchForge — Architecture Pattern Research. Finds proven
  patterns, anti-patterns, and best practices for the problem space.
user-invocable: false
allowed-tools:
  - bash
  - read_file
  - grep
---

# ResearchForge: Architecture Pattern Research

**Role:** `targeted-researcher` — Phase4 (patterns)

## Mission

Find proven architecture patterns and anti-patterns that apply to the problem. Don't reinvent — stand on documented shoulders.

## When to Use

- Phase4 of ResearchForge (Targeted Research)
- When the solution likely involves architectural changes
- When looking for best practices

## Research Template

```
RESEARCH_FINDING
==============

TRACK_ID: [RT-NNN from RESEARCH_PLAN.md]
QUESTION: [pattern-related question]

ANSWER: [which pattern applies, or "none found"]

PATTERN:
  name: [pattern name, e.g., Circuit Breaker, Retry with Backoff]
  category: [resilience | scalability | security | performance | data]
  description: [what it does]
  when_to_use: [problem context]
  when_not_to_use: [avoid this when]

SOURCE:
  name: [book, blog, docs, paper]
  url: [exact URL]
  type: OFFICIAL_DOC | EXPERT_ANALYSIS | SECONDARY_SOURCE
  authority: HIGH | MEDIUM | LOW

APPLICABILITY:
  fits: [why this applies to our problem]
  limitations: [why it might not work here]
  adaptation_needed: [how to adjust for our context]

ANTI_PATTERN:
  name: [what NOT to do]
  symptom: [how it manifests]
  why_bad: [negative consequence]
```

## Patterns to Consider

- **Resilience**: Circuit Breaker, Retry/Backoff, Bulkhead, Timeout, Fallback
- **Scalability**: Load Balancer, Sharding, Caching, Async Processing
- **Security**: Defense in Depth, Principle of Least Privilege, Zero Trust
- **Performance**: Connection Pooling, Lazy Loading, Pagination, Indexing
- **Data**: CQRS, Event Sourcing, Saga, Repository, Unit of Work

## Instructions

1. **Read Research Plan**: Load RESEARCH_PLAN.md. Pick a pattern-related track.
2. **Search Authoritative Sources**: Architecture guides, pattern catalogs, vendor best practices.
3. **Match to Problem**: Does this pattern fit our context? What's the adaptation?
4. **Note Anti-Patterns**: What should we avoid?
5. **Write Output**: Append to `RESEARCH_FINDINGS.md`.

## Output

Appended entry in `RESEARCH_FINDINGS.md`.

**Proven patterns save time. Anti-patterns save disasters.**
