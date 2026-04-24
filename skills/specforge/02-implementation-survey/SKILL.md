---
name: specforge-02-implementation-survey
description: |
  SpecForge — Implementation Surveyor. Maps existing repo structure, code,
  API, schema, tests, and UI to understand what is built — not what should be.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
  - task
---

# SpecForge: Implementation Survey

**Role:** `implementation-surveyor`

## Mission

Map what actually exists in the codebase/repo. This is *descriptive evidence*, not normative truth. The gap between intent and implementation is where specs are born.

## When to Use

- Phase 2 of SpecForge (Existing Evidence Review)
- After intent analysis is complete
- Before gap analysis

## Survey Template

```
IMPLEMENTED_FEATURES:
PARTIALLY_IMPLEMENTED_FEATURES:
MISSING_FEATURES:
INCONSISTENT_BEHAVIOR:
CURRENT_ARCHITECTURE_ASSUMPTIONS:
LIKELY_HIDDEN_REQUIREMENTS:
RISKY_ACCIDENTAL_BEHAVIOR:
```

## Instructions

1. **Scan Repository**: Use `bash` to `find`, `ls`, and explore structure.
2. **Read Key Files**: Entry points, configs, schema definitions, API routes, tests.
3. **Map Features**: Catalog what exists vs what intent says should exist.
4. **Flag Risks**: Note behavior that looks accidental, not designed.
5. **Write Output**: `IMPLEMENTATION_EVIDENCE_MAP.md`.

## Critical Rule

> Existing implementation is **descriptive evidence**, not normative truth.

The spec architect will later decide what to keep, change, or discard. Your job is only to document what is.

## Output

`IMPLEMENTATION_EVIDENCE_MAP.md` — the evidence ledger of what exists.

**Map what is. The spec decides what should be.**
