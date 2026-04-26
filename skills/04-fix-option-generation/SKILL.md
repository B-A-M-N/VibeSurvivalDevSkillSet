# Fix Option Generation Skill

name: 04-fix-option-generation
description: Generate minimum 2 fix options with tradeoff analysis
trigger: when root cause is understood and ready to fix

## Step-by-Step Instructions

### 1. Analyze Fix Approaches
- Consider multiple angles to the problem
- Evaluate different strategies
- Think about short-term vs long-term fixes
- Consider code quality and maintainability

### 2. Generate Fix Options
**Option 1: Direct Fix**
- Minimal change to fix the issue
- Fast to implement
- May have limited scope

**Option 2: Comprehensive Fix**
- Addresses root cause and related issues
- More robust solution
- Takes more time

**Option 3: Workaround**
- Quick mitigation
- Not ideal long-term
- Buys time for proper fix

### 3. Evaluate Tradeoffs
Create comparison table:
```markdown
| Option | Speed | Safety | Complexity | Risk | Best For |
|--------|-------|--------|------------|------|----------|
| Direct | High | Medium | Low | Medium | Quick patches |
| Comprehensive | Low | High | High | Low | Production fixes |
| Workaround | Very High | Low | Very Low | High | Emergency |
```

### 4. Select Primary and Fallback
- Choose primary option based on evaluation
- Identify fallback if primary fails
- Document decision rationale

### 5. Plan Implementation
- Break down implementation steps
- Identify test requirements
- Plan rollback if needed
- Estimate time and resources

## Fix Evaluation Criteria

### Speed
- How quickly can this be implemented?
- Are there dependencies?
- How long to test?

### Safety
- Risk of breaking other things?
- Test coverage needed?
- Rollback complexity?

### Complexity
- Code changes required?
- Learning curve?
- Maintenance burden?

### Risk
- Probability of success
- Impact if it fails
- Side effects

## Deliverables
```markdown
## Fix Options

### Option 1: [Title]
- **Approach**: [Description]
- **Pros**: [benefits]
- **Cons**: [drawbacks]
- **Complexity**: [rating]
- **Estimated Time**: [duration]

### Option 2: [Title]
- **Approach**: [Description]
- **Pros**: [benefits]
- **Cons**: [drawbacks]
- **Complexity**: [rating]
- **Estimated Time**: [duration]

### Recommended: [Option X]
- **Reasoning**: [why chosen]
- **Fallback**: [Option Y if fails]

## Implementation Plan
1. [Step 1]
2. [Step 2]
...

## Testing Strategy
- Unit tests
- Integration tests
- Regression tests
- Scenario validation
```

## Common Fix Types
- **Configuration**: Environment or config changes
- **Code Logic**: Algorithm or control flow fixes
- **Dependencies**: Version or library updates
- **Data**: Schema or data structure changes
- **Performance**: Optimization strategies

## Decision Framework
1. What's the simplest fix that works?
2. What's the most maintainable?
3. What's the safest?
4. Balance these factors based on context