---
name: 02-unit-test-generation
description: Generate unit tests for each contract, invariant, boundary
---

# skill 2 — Unit Test Generation

**Trigger**: test_matrix.json from skill 01 marks a target as unit.

## Step-by-step instructions
1. For each unit target: identify module file, public functions, and invariants.
2. Generate positive tests for valid inputs and expected behaviors.
3. Generate negative tests for invalid inputs, boundary values, and reverts.
4. Include property-based checks (e.g., fuzz small numeric ranges) where applicable.
5. Write tests in the project's native testing framework (e.g., pytest, rust-test, hardhat).
6. Output to `tests/unit/<module>_test.<lang>` and register entry in test_manifest.json.
7. Ensure tests follow existing code patterns and conventions.
8. Add comprehensive test coverage for all function parameters.
9. Include setup and teardown logic for test isolation.
10. Validate tests against the original spec requirements.

## Test Generation Patterns
- **Constructor tests**: Initialize contract with various parameters
- **Function tests**: Test all public functions with valid/invalid inputs
- **Invariant tests**: Verify state invariants after each operation
- **Boundary tests**: Test min/max values, edge cases, overflow/underflow
- **Access control tests**: Verify permission requirements

## Output Structure
```
tests/
├── unit/
│   ├── Token_test.sol
│   ├── Voting_test.sol
│   └── math_utils_test.py
├── test_manifest.json
└── coverage_units.json
```

## test_manifest.json Format
```json
{
  "unit_tests": [
    {
      "target_id": "func-001",
      "file": "tests/unit/Token_test.sol",
      "test_name": "test_transfer_success",
      "priority": 1,
      "coverage": 0.95,
      "references": ["spec-001", "scenario-001"]
    }
  ]
}
```

## Quality Standards
- Follow existing code formatting and style
- Use descriptive test names
- Include comprehensive assertions
- Handle all revert conditions
- Test both success and failure paths
- Ensure test independence (no shared state)

## Framework Integration
- Support multiple testing frameworks (Hardhat, Foundry, Pytest)
- Auto-detect contract language (Solidity, Rust, Python)
- Generate appropriate test scaffolding
- Configure gas estimation and reporting

## Validation
- Run all unit tests to verify they pass
- Check coverage against spec requirements
- Ensure no test dependencies on external state
- Verify test execution time is reasonable

## Integration Points
Consumes test_matrix.json from skill 01.
Outputs tests to tests/unit/ directory.
Updates test_manifest.json with generated tests.
Provides input for skill 06 coverage validation.

## Best Practices
- Mirror existing test structure
- Maintain consistent naming conventions
- Include documentation comments
- Use parameterized tests where applicable
- Ensure tests are deterministic and fast