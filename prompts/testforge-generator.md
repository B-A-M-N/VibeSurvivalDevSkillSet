# testforge-generator.md
Write comprehensive tests from parsed spec and scenario targets.

1) Unit tests (skill 02)
   - For each module/contract: preconditions, invariants, boundary values.
   - Include property-based variants and negative cases.
   - Output: unit_tests/<module>_test.<lang>.

2) Kill tests (skill 03)
   - For each SCENARIO: reproduce the edge case, assert failure or safe state.
   - Name: <scenario_id>_kill.<lang>.
   - Include resource exhaustion, invalid casts, timing/ordering quirks.

3) Integration tests (skill 04)
   - Cross-module flows, API request/response chains, state machine transitions.
   - Mock external dependencies; assert end-state and side effects.
   - Output: integration_tests/<flow>_integration.<lang>.

4) Fuzz targets (skill 05)
   - Build seed corpus from scenario values; instrument code for coverage.
   - Define max_length, dict entries, and validity constraints.
   - Output: fuzz_targets/<target>.fuzz.

5) Artifact metadata
   - Each file includes header with source spec/scenario IDs and generation timestamp.
   - Register path in test_manifest.json.