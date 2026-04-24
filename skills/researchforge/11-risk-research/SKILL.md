---
name: researchforge-11-risk-research
description: |
  ResearchForge — Risk Research. Identifies security, performance,
  data loss, and operational risks related to the problem and solutions.
user-invocable: false
allowed-tools:
  - bash
  - read_file
  - grep
---

# ResearchForge: Risk Research

**Role:** `targeted-researcher` — Phase4 (risk assessment)

## Mission

Identify risks: security vulnerabilities, performance bottlenecks, data loss scenarios, and operational hazards. Every solution has risks — name them before they name you.

## When to Use

- Phase4 of ResearchForge (Targeted Research)
- When evaluating solution options
- Before recommending a path forward

## Research Template

```
RESEARCH_FINDING
==============

TRACK_ID: [RT-NNN from RESEARCH_PLAN.md]
QUESTION: [risk-related question]

RISK_CATEGORY: [security | performance | data_loss | operational | compliance | financial]

RISK:
  name: [specific risk]
  description: [what could go wrong]
  trigger: [what causes it to manifest]
  likelihood: high | medium | low
  impact: critical | high | medium | low
  cvss_score: [if security vulnerability, X.X format]

EVIDENCE:
  - source: [where this risk is documented]
    url: [link]
    confirms: [what it says about this risk]

MITIGATION:
  - strategy: [how to reduce likelihood or impact]
    cost: [effort/cost of mitigation]
    residual_risk: [what remains after mitigation]

DETECTION:
  - how to detect this risk has materialized
  - monitoring, alerting, or testing strategy
```

## Risk Categories

| Category | Examples |
|----------|---------|
| Security | SQL injection, XSS, auth bypass, data leak |
| Performance | Memory leak, O(n²) algorithm, blocking I/O |
| Data Loss | Corruption, race condition, missing backup |
| Operational | Single point of failure, no rollback, silent failure |
| Compliance | GDPR violation, audit trail missing, data retention |

## Instructions

1. **Read Research Plan**: Load RESEARCH_PLAN.md. Pick a risk-related track.
2. **Think Like an Attacker**: What could go wrong? What's the worst case?
3. **Search Vulnerability DBs**: CVE, OWASP, vendor advisories.
4. **Document Each Risk**: Category, likelihood, impact, evidence.
5. **Define Mitigation**: How to reduce risk? What's the residual?
6. **Write Output**: Append to `RESEARCH_FINDINGS.md`.

## Output

Appended entry in `RESEARCH_FINDINGS.md`.

**Unknown risks are unmanaged risks. Research them or wear them.**
