---
name: researchforge-08-upstream-issue-research
description: |
  ResearchForge — Upstream Issue Research. Searches issue trackers,
  PR comments, and mailing lists for known bugs and solutions.
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Grep
---

# ResearchForge: Upstream Issue Research

**Role:** `targeted-researcher` — Phase4 (upstream sources)

## Mission

Search upstream issue trackers, PR discussions, and mailing lists. Find known bugs, workarounds, and solutions that match the problem.

## When to Use

- Phase4 of ResearchForge (Targeted Research)
- When the problem might be an upstream bug
- When looking for workarounds or patches

## Research Template

```
RESEARCH_FINDING
==============

TRACK_ID: [RT-NNN from RESEARCH_PLAN.md]
QUESTION: [the narrow question being answered]

ANSWER: [what upstream says about this issue]

SOURCE:
  type: GitHub Issue | GitHub PR | GitLab Issue | Mailing List | Changelog
  url: [exact URL to issue/PR/thread]
  title: [issue or thread title]
  status: open | closed | merged | wontfix | duplicate
  date: [created date]
  authority: HIGH (first-hand reports from users/developers)

EVIDENCE:
  - quote: "[relevant comment from maintainer]"
    author: [who said it]
    role: maintainer | contributor | user
  - quote: "[workaround mentioned]"
    author: [who said it]

BUG_CONFIRMED: true | false
  issue_number: [#NNN]
  fixed_in_version: [version where it was fixed, if any]
  workaround: [temporary fix, if available]

CONFIDENCE: high | medium | low
APPLICABILITY: [how this relates to our problem]
NEXT_QUESTION: [does this lead to a patch? workaround?]
```

## Upstream Sources

- **GitHub Issues**: `is:issue repo:owner/name [search terms]`
- **GitHub PRs**: `is:pr repo:owner/name [search terms]`
- **GitLab Issues/MRs**: Similar search syntax
- **Mailing Lists**: Archives for the project
- **Changelogs**: Look for "Fixed", "Bugfix" sections
- **Stack Overflow**: Only when linked from official sources

## Instructions

1. **Read Research Plan**: Load RESEARCH_PLAN.md. Pick a track about bugs or behavior.
2. **Search Upstream**: Use `bash` to query GitHub CLI (`gh`) or web search.
3. **Find Matching Issues**: Same error message? Same symptom? Same component?
4. **Extract Workarounds**: What did people do to fix or mitigate?
5. **Check Status**: Is it fixed? Won't fix? Duplicate?
6. **Write Output**: Append to `RESEARCH_FINDINGS.md`.

## Output

Appended entry in `RESEARCH_FINDINGS.md`.

**Upstream bugs are someone else's battle. Find the scar, learn from it.**
