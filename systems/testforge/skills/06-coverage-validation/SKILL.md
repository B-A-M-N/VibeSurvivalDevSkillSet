---
name: 06-coverage-validation
description: Check test coverage against spec hard gates, report gaps
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
7. Validate that all critical paths are covered by at least one test type.
8. Generate coverage summaries per test category (unit, kill, integration, fuzz).
9. Identify coverage gaps and recommend additional test generation.
10. Produce final coverage report with pass/fail status.

## Coverage Analysis Process
- Parse coverage traces from test execution
- Map executed code to spec requirements
- Calculate coverage percentages per module
- Identify uncovered hard gates and scenarios
- Generate gap analysis with remediation suggestions

## Output Structure
```
coverage_report/
├── index.html
├── coverage.json
├── gaps.md
├── unit_coverage.json
├── integration_coverage.json
├── kill_coverage.json
└── fuzz_coverage.json
```

## coverage.json Format
```json
{
  "summary": {
    "total_requirements": 45,
    "covered_requirements": 42,
    "coverage_percentage": 93.33,
    "hard_gates_covered": 18,
    "hard_gates_total": 20,
    "hard_gates_uncovered": 2
  },
  "modules": {
    "Token": {
      "coverage": 95.5,
      "hard_gates": ["access_control", "balance_invariant"],
      "uncovered_gates": ["reentrancy_protection"]
    }
  }
}
```

## gaps.md Format
```markdown
# Coverage Gaps Report

## Critical Gaps (Hard Gates Uncovered)
1. **Reentrancy Protection** (spec-req-003)
   - Missing test: kill test for reentrant calls
   - Suggested test type: kill test
   - Priority: Critical

## Major Gaps
1. **Edge Case: Zero Amount Transfer**
   - Missing scenario: scn-005
   - Suggested test type: unit test

## Recommendations
- Add kill test for reentrancy scenarios
- Expand unit tests for boundary conditions
- Include fuzz testing for input validation
```

## Validation Rules
- **Hard Gate Coverage**: Must achieve 100% coverage
- **Critical Path Coverage**: Minimum 95%
- **Overall Coverage**: Minimum 85%
- **Error Path Coverage**: Minimum 80%

## Integration Points
Consumes coverage data from all test generation skills (02-05).
Generates comprehensive coverage_report/ directory.
Outputs gaps.md for remediation planning.
Provides pass/fail status to testforge-overseer.
Updates coverage statistics in test_manifest.json.

## Quality Gates
- All hard gates must be 100% covered
- Critical paths must exceed 95% coverage
- Overall coverage must meet minimum thresholds
- Any uncovered hard gate causes pipeline failure

## Reporting Features
- HTML report for human review
- JSON report for machine processing
- Gap analysis with remediation suggestions
- Per-test-type coverage breakdown
- Historical coverage trends

## Best Practices
- Run coverage validation after all test generations complete
- Prioritize hard gate coverage over other metrics
- Provide actionable gap remediation suggestions
- Track coverage improvements across iterations
- Integrate with CI/CD pipeline for automated checks