# Scenario Validation Skill

name: 05-scenario-validation
description: Validate each fix option against SCENARIOS.md and MASTER_SPEC.md
trigger: when fix options are generated and ready to validate

## Step-by-Step Instructions

### 1. Load Reference Documents
- Read SCENARIOS.md for test scenarios
- Review MASTER_SPEC.md for requirements
- Identify relevant test cases
- Map scenarios to fix options

### 2. Map Fix to Scenarios
- Create matrix of fix options vs scenarios
- Identify which scenarios each fix affects
- Mark passing and failing scenarios
- Note edge cases

### 3. Execute Validation Tests
- Run scenario-specific tests
- Execute integration tests
- Verify backward compatibility
- Check performance impact

### 4. Analyze Results
- Document pass/fail status
- Identify unexpected behaviors
- Note side effects
- Validate fix scope

### 5. Update Documentation
```markdown
## Validation Matrix

| Fix Option | Scenario 1 | Scenario 2 | Scenario 3 | ... | Status |
|------------|------------|------------|------------|-----|--------|
| Option A   | ✓ Pass     | ✗ Fail     | ✓ Pass     |     | Needs Rework |
| Option B   | ✓ Pass     | ✓ Pass     | ✓ Pass     |     | Approved |

## Scenario Coverage
- **Covered**: Scenarios tested and passing
- **Partial**: Scenarios with issues
- **Not Covered**: Scenarios not addressed

## Test Results
- Unit tests: [pass/fail count]
- Integration tests: [pass/fail count]
- Regression tests: [pass/fail count]
- Performance tests: [metrics]
```

## Validation Techniques

### Functional Validation
- Test each scenario requirement
- Verify expected outcomes
- Check edge cases
- Validate error handling

### Non-Functional Validation
- Performance benchmarks
- Memory usage
- Response times
- Resource consumption

### Compatibility Testing
- Backward compatibility
- API compatibility
- Data format compatibility
- Version compatibility

## Tools for Validation
- Test frameworks
- Benchmark tools
- Monitoring tools
- Logging tools

## Decision Criteria

### Pass Conditions
- All critical scenarios pass
- No regression in existing scenarios
- Performance within acceptable limits
- No new errors introduced

### Fail Conditions
- Critical scenario fails
- Performance degradation > threshold
- New errors introduced
- Backward compatibility broken

## Documentation Output
- validation_matrix.md - Complete test results
- scenario_coverage.md - Coverage analysis
- performance_report.md - Performance metrics
- compatibility_report.md - Compatibility verification