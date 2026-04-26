# Validation Skill

name: 05-scenario-validation

## Overview
This skill validates fix options against project specifications and scenarios. It ensures solutions meet requirements and handle edge cases properly before implementation.

## Steps to Validate Fix Options

1. **Review Specification Documents**
   - Study SCENARIOS.md thoroughly
   - Review MASTER_SPEC.md requirements
   - Identify all acceptance criteria

2. **Test Against Scenarios**
   - Execute each fix option against all documented scenarios
   - Verify behavior matches expected outcomes
   - Document any discrepancies or edge cases

3. **Validate Against Specifications**
   - Check compliance with MASTER_SPEC.md
   - Ensure all requirements are satisfied
   - Verify no regression in existing functionality

4. **Edge Case Testing**
   - Test boundary conditions
   - Validate error handling
   - Check performance under stress

5. **Comprehensive Test Execution**
   - Run existing test suite
   - Execute new test cases for fix
   - Verify integration with existing code

## Output Generation

Create VALIDATION_REPORT.md with the following structure:

```markdown
# Validation Report

## Fix Option Validation

### Fix Option: [Option Name]
- Validation Status: [PASS/FAIL]
- Overall Score: [percentage]

## Scenario Testing Results

### Scenario 1: [Scenario Name]
- Status: [PASS/FAIL]
- Expected Behavior: [description]
- Actual Behavior: [description]
- Issues Found: [list]

### Scenario 2: [Scenario Name]
- Status: [PASS/FAIL]
- Expected Behavior: [description]
- Actual Behavior: [description]
- Issues Found: [list]

## Specification Compliance

### MASTER_SPEC.md Requirements
- [Requirement 1]: [PASS/FAIL]
- [Requirement 2]: [PASS/FAIL]
- [Requirement 3]: [PASS/FAIL]

### SCENARIOS.md Coverage
- [Scenario Category]: [coverage percentage]
- Missing Scenarios: [list]
- Edge Cases Tested: [count]

## Test Results Summary

### Passing Tests
- Total Passing: [count]
- Success Rate: [percentage]

### Failing Tests
- Total Failing: [count]
- Failure Details: [summary]

### Performance Metrics
- Execution Time: [duration]
- Resource Usage: [metrics]
- Memory Consumption: [measurements]

## Recommendations

### Selection Recommendation
- Recommended Fix: [option name]
- Justification: [why this passed validation]
- Risk Assessment: [low/medium/high]

### Required Fixes
- Issues to address before implementation
- Additional testing needed
- Specification gaps to resolve
```

## Best Practices

- Test each scenario systematically
- Document both positive and negative test results
- Validate edge cases thoroughly
- Ensure backward compatibility
- Measure performance impact

## Quality Checks

- [ ] All scenarios tested
- [ ] Specification requirements verified
- [ ] Edge cases covered
- [ ] Performance validated
- [ ] VALIDATION_REPORT.md generated

## Testing Strategies

### Unit Testing
- Test individual functions
- Verify fix correctness
- Check error handling

### Integration Testing
- Test component interactions
- Verify system behavior
- Check data flow

### Regression Testing
- Ensure no new bugs introduced
- Validate existing functionality
- Test backward compatibility

### Performance Testing
- Measure execution time
- Test under load
- Check resource usage

## Common Validation Issues

- Incomplete scenario coverage
- Missing edge cases
- Performance regression
- Specification non-compliance
- Integration conflicts

## Automation Opportunities

Consider implementing:
- Automated scenario testing
- Continuous validation in CI/CD
- Performance regression detection
- Specification compliance checking

## Integration Points

This skill depends on:
- Fix Option Generation: Provides options to validate
- Root Cause Analysis: Ensures fixes address root cause

And feeds into:
- Fix Application: Validated fixes are implemented
- Quality Assurance: Results inform testing strategy