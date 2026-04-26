---
name: 04-integration-test-generation
description: Generate integration tests for API, state machine, cross-module
---

# skill 4 — Integration Test Generation

**Trigger**: integration-priority entries from test_matrix.json.

## Step-by-step instructions
1. For each integration target: identify involved modules and the call sequence.
2. Mock or stub external dependencies; preserve state consistency across calls.
3. Write tests that exercise happy paths and failure paths across module boundaries.
4. Assert end-state, emitted events, and side effects; include gas/step checks where relevant.
5. Output to `integration_tests/<flow>_integration.<lang>` and register in test_manifest.json.
6. Test complex multi-step workflows and cross-contract interactions.
7. Include state transition verification between multiple operations.
8. Validate event emissions and their correctness.
9. Test failure recovery and rollback scenarios.
10. Ensure integration tests match real-world usage patterns.

## Integration Test Types
- **API integration**: Multi-function call sequences
- **State machine integration**: Cross-state transition validation
- **Cross-module integration**: Module-to-module communication
- **Event integration**: Event emission and handling verification
- **Recovery integration**: Failure recovery and rollback testing

## Output Structure
```
tests/
├── integration/
│   ├── token_transfer_integration.sol
│   ├── voting_workflow_integration.py
│   └── cross_module_flow_test.rs
├── test_manifest.json
└── integration_coverage.json
```

## test_manifest.json Integration Section
```json
{
  "integration_tests": [
    {
      "flow_id": "transfer-flow-001",
      "file": "tests/integration/token_transfer_integration.sol",
      "description": "Complete token transfer workflow",
      "modules_involved": ["Token", "Vault"],
      "steps": [
        {"action": "approve", "params": {}},
        {"action": "transferFrom", "params": {}}
      ],
      "expected_events": ["Transfer", "Approval"],
      "priority": 2
    }
  ]
}
```

## Test Design Patterns
- **Happy path tests**: Normal operation scenarios
- **Failure path tests**: Error conditions and rollbacks
- **Boundary integration tests**: Edge cases across modules
- **Sequential tests**: Multi-step operation flows
- **Concurrency tests**: Parallel operation interactions

## Mocking Strategy
- Stub external contract calls
- Simulate network conditions
- Control time and block variables
- Mock oracle responses
- Simulate gas price variations

## Validation Assertions
- Final state correctness
- Event emission verification
- Gas consumption limits
- Storage slot integrity
- Cross-module state consistency

## Integration Points
Consumes test_matrix.json from skill 01.
Coordinates with unit tests (skill 02) and kill tests (skill 03).
Outputs to tests/integration/ directory.
Updates test_manifest.json with integration test registrations.
Provides input for skill 06 coverage validation.

## Best Practices
- Test realistic usage scenarios
- Include comprehensive error handling
- Verify state cleanup after failures
- Test both forward and reverse flows
- Ensure backward compatibility in test design