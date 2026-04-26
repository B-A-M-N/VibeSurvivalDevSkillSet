---
name: 01-test-strategy-planning
description: Build a test matrix and prioritize by risk
---

# skill 1 — Test Strategy Planning

**Trigger**: after 00-spec-scenario-ingest emits its target list.

## Step-by-step instructions
1. Consume the target list from skill 00.
2. Classify each target: unit, integration, kill, fuzz.
3. Assign risk scores combining spec hard gate status and scenario severity.
4. Produce a prioritized test matrix mapping target → test_type → priority.
5. Output TEST_STRATEGY.md with detailed test planning.
6. Map tests to spec sections for traceability.
7. Identify dependencies between test cases.
8. Determine test execution order based on risk and dependencies.
9. Set coverage thresholds for each test type.
10. Generate test execution plan with resource allocation.

## Test Classification Strategy
- **Unit tests**: Individual functions, contract methods, invariants
- **Integration tests**: Cross-module interactions, API flows
- **Kill tests**: Edge cases, error conditions, failure modes
- **Fuzz tests**: Random input validation, boundary conditions

## Risk Assessment Matrix
| Risk Level | Criteria | Priority |
|------------|----------|----------|
| Critical | Hard gate failure, security issue | 1 |
| High | Core functionality, frequently used | 2 |
| Medium | Edge cases, rarely used paths | 3 |
| Low | Cosmetic, non-essential | 4 |

## Test Matrix Structure
```json
{
  "test_matrix": [
    {
      "target_id": "mod-001",
      "test_type": "unit",
      "priority": 1,
      "spec_section": "access_control",
      "scenario_refs": ["scn-001", "scn-002"],
      "hard_gate": true
    }
  ]
}
```

## Priority Assignment Rules
1. All hard gates must have priority 1 or 2
2. Security-related scenarios get highest priority
3. Core business logic tested before edge cases
4. Integration tests before unit tests when they reveal architectural issues

## Output Files
- TEST_STRATEGY.md: Complete test matrix and plan
- test_matrix.json: Machine-readable test matrix
- execution_plan.yaml: Detailed test execution schedule

## Quality Gates
- 100% coverage of hard gates
- At least one test per module
- Error path coverage minimum 80%
- Integration tests for all cross-module interfaces

## Integration Points
Consumes output from skill 00.
Outputs test_matrix.json for skill 02-05.
Generates TEST_STRATEGY.md for documentation.

## Validation
- Verify all hard gates have test assignments
- Check priority consistency across test types
- Validate dependency ordering
- Ensure resource allocation is realistic