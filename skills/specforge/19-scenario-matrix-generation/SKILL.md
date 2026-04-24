---
name: specforge-19-scenario-matrix-generation
description: |
  SpecForge — Scenario Matrix Generation. Creates exhaustive scenario
  coverage matrix mapping requirements to test scenarios.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# SpecForge: Scenario Matrix Generation

**Role:** `scenario-engineer` — Phase6

## Mission

Turn the master spec into a scenario coverage matrix. Every requirement, invariant, and error condition gets one or more scenarios.

## When to Use

- Phase 6 of SpecForge (Scenario Sheet Construction)
- After MASTER_SPEC.md is complete
- Before writing individual scenario sheets

## Coverage Matrix Template

```
COVERAGE_MATRIX:

REQUIREMENT: [REQ-ID or description from spec]
  SCENARIO_IDS:
    - [SCN-XXX] (happy path)
    - [SCN-YYY] (edge case)
  INVARIANTS_COVERED: [INV-NNN list]
  COVERAGE_STATUS: complete | partial | missing

INVARIANT: [INV-NNN]
  SCENARIO_IDS:
    - [SCN-XXX] (preserves invariant)
    - [SCN-ZZZ] (kill test — breaks invariant)
  COVERAGE_STATUS: complete | partial | missing

ERROR: [ERROR_CODE]
  SCENARIO_IDS:
    - [SCN-AAA] (triggers error)
    - [SCN-BBB] (recovery test)
  COVERAGE_STATUS: complete | partial | missing
```

## Scenario Categories (must all be covered)

- kill tests (break the invariant deliberately)
- happy paths (normal flow)
- invalid inputs (bad data)
- degraded states (system partially down)
- permission failures (unauthorized access)
- replay/retry behavior (idempotency)
- state transition failures (invalid transitions)
- data integrity failures (corruption, constraints)
- UI edge cases (loading, empty, error states)
- API contract violations (wrong params, auth)
- security boundary tests (privilege escalation)
- migration/versioning tests (backwards compatibility)
- adversarial misuse cases (malicious input)

## Instructions

1. **Read Master Spec**: Load MASTER_SPEC.md.
2. **Map Requirements → Scenarios**: Each REQ gets at least one happy path + one edge case.
3. **Map Invariants → Scenarios**: Each INV gets a preservation test + a kill test.
4. **Map Errors → Scenarios**: Each ERROR gets a trigger test + recovery test.
5. **Fill Matrix**: Use the COVERAGE_MATRIX template.
6. **Find Gaps**: Any requirement/invariant/error with no scenarios = gap.
7. **Write Output**: `SCENARIO_MATRIX.md`.

## Output

`SCENARIO_MATRIX.md` — the coverage map linking spec to scenarios.

**Every requirement needs a scenario. Every invariant needs a kill test.**
