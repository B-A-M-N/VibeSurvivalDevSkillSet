---
name: 03-kill-test-generation
description: Generate kill tests from SCENARIOS.md edge cases
---

# skill 3 — Kill Test Generation

**Trigger**: targets in SCENARIOS.md requiring kill/exception validation.

## Step-by-step instructions
1. Iterate over scenario entries; for each, derive an edge-case condition.
2. Write a test that reproduces the scenario and asserts a safe failure (revert, graceful fallback, or controlled state).
3. Name the test file `<scenario_id>_kill.<lang>` and include the scenario reference in header.
4. Ensure kill tests are isolated and do not depend on external state.
5. Register each kill test path in test_manifest.json.
6. Test all error conditions including invalid inputs, unauthorized access, and state violations.
7. Include tests for reentrancy, overflow/underflow, and timestamp dependency.
8. Validate that failures are safe and don't leave system in inconsistent state.
9. Test permission escalation attempts and access control bypasses.
10. Verify that all scenario failure conditions are properly handled.

## Kill Test Categories
- **Error path tests**: Invalid inputs, missing parameters, wrong types
- **Permission tests**: Unauthorized access, privilege escalation
- **State violation tests**: Invalid state transitions, pre-condition failures
- **Resource exhaustion tests**: Gas limits, storage limits, recursion depth
- **Edge case tests**: Boundary values, null inputs, empty collections

## Output Structure
```
tests/
├── kill/
│   ├── scenario_scn-001_kill.sol
│   ├── scenario_scn-002_kill.py
│   └── reentrancy_attack_test.sol
├── test_manifest.json
└── kill_coverage.json
```

## Test Naming Convention
- Format: `<scenario_id>_<type>_kill.<extension>`
- Example: `scn-001_revert_kill.sol`
- Example: `scn-002_unauthorized_kill.py`

## test_manifest.json Kill Section
```json
{
  "kill_tests": [
    {
      "scenario_id": "scn-001",
      "file": "tests/kill/scenario_scn-001_kill.sol",
      "test_name": "test_insufficient_balance_revert",
      "severity": "high",
      "expected_behavior": "revert",
      "coverage_impact": 0.90
    }
  ]
}
```

## Safety Validation
- All kill tests must assert safe failure modes
- Verify no state corruption on failure
- Ensure proper error messages are emitted
- Check that fallback functions work correctly
- Test contract cleanup on revert

## Edge Case Coverage
- Integer overflow/underflow at boundaries
- Division by zero
- Null address interactions
- Empty array operations
- Maximum gas limit scenarios
- Timestamp manipulation
- Block number dependencies

## Integration Points
Consumes SCENARIOS.md for edge case definitions.
Works alongside unit test generation (skill 02).
Outputs to tests/kill/ directory.
Updates test_manifest.json with kill test registrations.
Provides input for skill 06 coverage validation.

## Best Practices
- Isolate kill tests from main test flows
- Use consistent failure assertions
- Include scenario reference in test documentation
- Ensure tests are repeatable and deterministic
- Validate that failures don't compromise system integrity