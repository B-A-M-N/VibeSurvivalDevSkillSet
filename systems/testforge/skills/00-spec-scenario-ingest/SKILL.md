---
name: 00-spec-scenario-ingest
description: Parse MASTER_SPEC.md + SCENARIOS.md, extract test targets
---

# skill 00 — Spec & Scenario Ingest

**Trigger**: orchestration start or spec/scenario change detected.

## Step-by-step instructions
1. Read MASTER_SPEC.md and locate: modules, contracts, invariants, boundaries, hard gates.
2. Read SCENARIOS.md and enumerate scenarios with IDs, severity, expected outcomes.
3. Emit normalized target list JSON to stdout: `{"spec_targets": [...], "scenario_targets": [...]}`.
4. Store parsed artifacts in `spec/` directory for downstream skills.
5. Extract test targets by identifying specific functions, parameters, and edge conditions.
6. Document hard gates that must be tested (e.g., access control, state transitions, value bounds).
7. Create mapping between spec requirements and scenario validations.
8. Generate TEST_TARGETS.md listing all identified test targets with priority levels.
9. Validate that all hard gates from spec are captured in target list.
10. Output structured data for downstream processing by test strategy skill.

## Expected Output Format
```json
{
  "spec_targets": [
    {"id": "mod-001", "type": "contract", "name": "Token", "hard_gates": ["access_control", "balance_invariant"]},
    {"id": "func-001", "type": "function", "module": "Token", "signature": "transfer(address,uint256)"}
  ],
  "scenario_targets": [
    {"id": "scn-001", "severity": "high", "description": "Insufficient balance transfer", "expected": "revert"}
  ]
}
```

## Hard Gates Identification
- Access control violations
- Balance invariants
- State machine transitions
- Input validation boundaries
- Reentrancy protections
- Fee calculations

## Validation Steps
- Verify each hard gate has corresponding test target
- Ensure scenario coverage for error conditions
- Confirm module dependencies are resolved
- Check boundary conditions are documented

## Integration Points
Outputs TEST_TARGETS.md for consumption by skill 01.
Ensures no hard gate is missed in test coverage.
Provides traceability from spec to test cases.

## Error Handling
- Log warnings for unspecified hard gates
- Flag scenarios without clear expected outcomes
- Report modules not covered by existing tests
- Halt on critical spec parsing errors