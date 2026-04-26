# Fix Option Generation Skill

name: 04-fix-option-generation

## Overview
This skill generates and analyzes multiple fix options for identified root causes. It evaluates tradeoffs and provides comprehensive analysis to select the optimal solution.

## Steps to Generate Fix Options

1. **Understand Root Cause Deeply**
   - Review ROOT_CAUSE_REPORT.md thoroughly
   - Identify the fundamental failure mechanism
   - Understand all contributing factors

2. **Brainstorm Multiple Approaches**
   - Generate at least 2 distinct fix strategies
   - Consider different levels of intervention
   - Explore both conservative and aggressive solutions

3. **Analyze Tradeoffs**
   - Evaluate complexity of implementation
   - Assess performance impact
   - Consider maintainability and future implications
   - Review risk factors for each approach

4. **Document Fix Options**
   - Provide detailed implementation steps
   - Include pros and cons for each approach
   - Recommend based on project constraints

## Output Generation

Create FIX_OPTIONS.md with the following structure:

```markdown
# Fix Options Analysis

## Root Cause Reference
- Primary Cause: [reference from ROOT_CAUSE_REPORT.md]
- Related Evidence: [links to evidence]

## Fix Option 1: [Descriptive Name]

### Description
Detailed explanation of the fix approach

### Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Continue with detailed steps]

### Pros
- [Pro 1]
- [Pro 2]
- [Pro 3]

### Cons
- [Con 1]
- [Con 2]
- [Con 3]

### Complexity Assessment
- Implementation Complexity: [Low/Medium/High]
- Testing Requirements: [Minimal/Moderate/Extensive]
- Risk Level: [Low/Medium/High]

### Performance Impact
- Expected Improvement: [quantitative if possible]
- Potential Side Effects: [list]

## Fix Option 2: [Descriptive Name]

### Description
Detailed explanation of the fix approach

### Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Continue with detailed steps]

### Pros
- [Pro 1]
- [Pro 2]
- [Pro 3]

### Cons
- [Con 1]
- [Con 2]
- [Con 3]

### Complexity Assessment
- Implementation Complexity: [Low/Medium/High]
- Testing Requirements: [Minimal/Moderate/Extensive]
- Risk Level: [Low/Medium/High]

### Performance Impact
- Expected Improvement: [quantitative if possible]
- Potential Side Effects: [list]

## Recommendation

### Selected Fix Option
- Chosen approach: [Option 1 or 2 or hybrid]
- Rationale: [why this option was selected]
- Priority: [High/Medium/Low]

### Alternative Consideration
- Why not the other option: [comparison]
- When to use alternative: [specific conditions]

## Validation Plan

### Testing Strategy
- Unit tests required: [list]
- Integration tests: [description]
- Regression test coverage: [scope]

### Success Criteria
- [Specific measurable outcomes]
- [Performance thresholds]
- [Quality gates]
```

## Best Practices

- Generate options that address different aspects of the problem
- Consider both quick fixes and long-term solutions
- Evaluate technical debt implications
- Balance development effort with benefit
- Document assumptions for each option

## Quality Checks

- [ ] Minimum 2 fix options documented
- [ ] Tradeoff analysis complete for each option
- [ ] Implementation steps are clear and actionable
- [ ] Recommendation justified with evidence
- [ ] FIX_OPTIONS.md properly formatted

## Common Approaches

### Quick Fixes
- Immediate patches
- Configuration changes
- Workarounds

### Comprehensive Fixes
- Architectural changes
- Refactoring
- New feature implementation
- Dependency updates

### Hybrid Approaches
- Short-term mitigation with long-term solution
- Phased implementation
- Gradual rollout strategies

## Decision Framework

Use this decision matrix when selecting between options:

| Criteria | Option 1 | Option 2 | Weight |
|----------|----------|----------|--------|
| Complexity | [rating] | [rating] | [weight] |
| Risk | [rating] | [rating] | [weight] |
| Benefit | [rating] | [rating] | [weight] |
| Time to Implement | [rating] | [rating] | [weight] |
| Maintainability | [rating] | [rating] | [weight] |

## Integration Points

This skill depends on:
- Root Cause Analysis: Provides the problem understanding
- Reproduction: Ensures fixes can be tested

And feeds into:
- Validation: Fix options are evaluated against scenarios
- Fix Application: Selected option is implemented