---
name: 06-coverage-validation
description: Check test coverage against spec hard gates, report gaps
trigger: after all tests pass, verify coverage
---

# skill 6 — Coverage Validation

**Trigger**: after all test generations complete and manifest is assembled.

## Step-by-step instructions
1. Collect coverage traces from all test artifacts (unit, kill, integration, fuzz).
2. Map coverage to MASTER_SPEC.md requirement IDs and SCENARIOS.md IDs.
3. Compute coverage ratios per target and overall; flag any spec hard gate < 100%.
4. Produce gaps.md listing uncovered spec/scenario IDs and suggested test types.
5. Generate coverage_report/index.html and coverage_report/coverage.json.
6. If any hard gate fails, halt pipeline and report to testforge-overseer.