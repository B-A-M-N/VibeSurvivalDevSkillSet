---
name: 02-unit-test-generation
description: Generate unit tests for each contract, invariant, boundary
trigger: test_matrix.json from skill 01 marks a target as unit
---

# skill 2 — Unit Test Generation

## Step-by-step instructions
1. For each unit target: identify module file, public functions, and invariants.
2. Generate positive tests for valid inputs and expected behaviors.
3. Generate negative tests for invalid inputs, boundary values, and reverts.
4. Include property-based checks (e.g., fuzz small numeric ranges) where applicable.
5. Write tests in the project's native testing framework (e.g., pytest, rust-test, hardhat).
6. Output to `unit_tests/<module>_test.<lang>` and register entry in test_manifest.json.