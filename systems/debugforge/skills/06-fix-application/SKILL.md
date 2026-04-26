# Fix Application Skill

name: 06-fix-application

## Overview
This skill applies the selected fix to the codebase, verifies its effectiveness, and ensures comprehensive test coverage. It bridges the gap between planning and implementation.

## Steps to Apply Fix and Verify

1. **Apply the Chosen Fix**
   - Implement the selected fix option from FIX_OPTIONS.md
   - Make minimal, focused changes
   - Follow coding standards and best practices

2. **Initial Verification**
   - Run the fix against the original reproduction case
   - Verify the issue is resolved
   - Check for immediate side effects

3. **Comprehensive Test Execution**
   - Run all SCENARIOS.md tests
   - Execute existing test suite
   - Verify no regressions introduced

4. **Update Test Coverage**
   - Add new test cases for the fix
   - Update existing tests if needed
   - Ensure edge cases are covered

5. **Regression Testing**
   - Run full test suite
   - Validate all scenarios pass
   - Check performance metrics

## Output Generation

Create FIX_APPLICATION_REPORT.md with the following structure:

```markdown
# Fix Application Report

## Implementation Summary
- Fix Applied: [fix option description]
- Files Modified: [file list]
- Lines Changed: [count]
- Implementation Date: [date]

## Verification Results

### Original Issue Resolution
- Issue Status: [RESOLVED/PENDING]
- Verification Steps: [steps taken]
- Evidence: [logs, screenshots, test results]

### Test Results

#### SCENARIOS.md Tests
- Total Scenarios: [count]
- Passing: [count]
- Failing: [count]
- Failed Details: [list with fixes]

#### Regression Test Results
- Total Tests: [count]
- Passing: [count]
- Failing: [count]
- New Failures: [list]

#### Performance Tests
- Baseline Performance: [metrics]
- Post-Fix Performance: [metrics]
- Improvement: [measurement]
- Regression: [none/significant/minor]

### Edge Case Testing
- Edge Cases Tested: [count]
- All Passed: [yes/no]
- Edge Case Results: [summary]

## Code Quality

### Code Review
- Code Style: [compliant/non-compliant]
- Documentation: [adequate/inadequate]
- Error Handling: [proper/needs improvement]
- Performance: [acceptable/needs optimization]

### Test Coverage
- Unit Tests: [percentage]% coverage
- Integration Tests: [coverage status]
- Scenario Coverage: [percentage]% scenarios covered

## Deployment Considerations

### Rollback Plan
- Steps to revert if issues arise
- Backup procedures
- Monitoring requirements

### Deployment Strategy
- Staged rollout plan
- Monitoring checkpoints
- Success criteria

## Recommendations

### Immediate Actions
- [Action 1]
- [Action 2]
- [Action 3]

### Long-term Improvements
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

## Quality Checks

- [ ] Fix implemented correctly
- [ ] All scenarios pass
- [ ] No regressions introduced
- [ ] Tests updated
- [ ] FIX_APPLICATION_REPORT.md generated

## Common Issues

- Fix introduces new bugs
- Performance degradation
- Incomplete test coverage
- Integration conflicts
- Unexpected side effects

## Continuous Monitoring

After deployment:
- Monitor error logs
- Track performance metrics
- Collect user feedback
- Prepare for hotfix if needed

## Integration Points

This skill depends on:
- Fix Option Selection: Provides the fix to implement
- Validation: Ensures fix passes all tests

And feeds into:
- Monitoring: Track fix effectiveness
- Documentation: Update project records