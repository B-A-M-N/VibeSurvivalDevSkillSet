# TestForge — System Implementations Checklist

## Component Inventory

### Specification & Scenario Layer
- [ ] MASTER_SPEC.md — canonical spec with hard gates & thresholds
- [ ] SCENARIOS.md — scenario definitions mapping to edge cases and kill conditions

### Parsing & Ingestion
- [ ] spec_parser (skill 00) — extracts test targets from MASTER_SPEC.md
- [ ] scenario_parser (skill 00) — parses SCENARIOS.md into executable scenarios

### Test Strategy & Planning
- [ ] test_strategy_planner (skill 01) — builds test matrix, prioritizes by risk

### Test Generation
- [ ] unit_generator (skill 02) — generates unit tests for contracts, invariants, boundaries
- [ ] kill_generator (skill 03) — generates kill tests from SCENARIOS.md edge cases
- [ ] integration_generator (skill 04) — generates integration tests for API & state machine
- [ ] fuzz_generator (skill 05) — generates fuzz targets for input validation

### Coverage & Validation
- [ ] coverage_validator (skill 06) — validates coverage against spec hard gates

### Orchestration & Reporting
- [ ] testforge-overseer — coordinates phases, delegates, gates completion
- [ ] test_manifest.json — inventory of all generated tests
- [ ] coverage_report/ — HTML + JSON coverage artifacts
- [ ] gaps.md — uncovered spec requirements

### File Conventions
- Unit tests: unit_tests/<module>_test.<lang>
- Kill tests: kill_tests/<scenario_id>_kill.<lang>
- Integration tests: integration_tests/<flow>_integration.<lang>
- Fuzz targets: fuzz_targets/<target>.fuzz
- Coverage: coverage_report/index.html & coverage_report/coverage.json
- Gaps: gaps.md

## Ready State
All components are defined and checklist is actionable.