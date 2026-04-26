---
name: researchforge-09-version-compatibility-research
description: |
  ResearchForge — Version Compatibility Research. Checks
  version-specific behavior, breaking changes, and compatibility matrices.
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Grep
---

# ResearchForge: Version Compatibility Research

**Role:** `targeted-researcher` — Phase4 (version checks)

## Mission

Check version-specific behavior, breaking changes, and compatibility. "It works on my machine" is often a version mismatch.

## When to Use

- Phase4 of ResearchForge (Targeted Research)
- When the problem might be version-related
- When upgrading/downgrading is a possible solution

## Research Template

```
RESEARCH_FINDING
==============

TRACK_ID: [RT-NNN from RESEARCH_PLAN.md]
QUESTION: [version-specific question]

ANSWER: [how behavior differs across versions]

SOURCE:
  name: [changelog | release notes | migration guide]
  url: [exact URL]
  versions_covered: [X.Y.Z to A.B.C]

VERSION_BEHAVIOR:
  - version: [X.Y.Z]
    behavior: [what happens in this version]
    supports_feature: true | false
    known_issues: [bugs in this version]

  - version: [A.B.C]
    behavior: [what happens in this version]
    supports_feature: true | false
    known_issues: [bugs in this version]

BREAKING_CHANGES:
  - introduced_in: [version]
    change: [what changed]
    migration: [how to adapt]

COMPATIBILITY_MATRIX:
  component: [library or system]
  works_with: [list of compatible versions]
  breaks_with: [list of incompatible versions]

CONFIDENCE: high | medium | low
APPLICABILITY: [our installed version is X, so...]
```

## Instructions

1. **Read Research Plan**: Load RESEARCH_PLAN.md. Pick a version-related track.
2. **Check Installed Version**: What are we running? `bash` to check.
3. **Read Changelogs**: Find breaking changes between versions.
4. **Build Matrix**: Which versions work with our dependencies?
5. **Check Migration Guides**: If upgrade is the solution, what's the path?
6. **Write Output**: Append to `RESEARCH_FINDINGS.md`.

## Output

Appended entry in `RESEARCH_FINDINGS.md`.

**Version mismatches are silent killers. Pin them down.**
