# Root Cause Analysis Skill

name: 03-root-cause-analysis
description: Deep analysis of root cause, gather evidence
trigger: when isolated bug to specific code change

## Step-by-Step Instructions

### 1. Deep Code Analysis
- Examine the isolated change line-by-line
- Trace variable states through execution
- Understand the control flow
- Identify data dependencies

### 2. Gather Evidence
- Collect logs and error messages
- Take stack traces
- Capture variable dumps
- Record test results

### 3. Formulate Hypothesis
- What is the actual root cause?
- Why does this change break behavior?
- What are the contributing factors?
- How does it propagate through the system?

### 4. Validate Hypothesis
- Create targeted tests to prove/disprove
- Reproduce with evidence
- Check edge cases
- Verify understanding

### 5. Document Analysis
```markdown
## Root Cause Analysis

### Problem Statement
[Brief description of the bug]

### Evidence
- Log files: [path/to/logs]
- Stack traces: [captured errors]
- Variable dumps: [key states]
- Test results: [outcomes]

### Analysis
**Root Cause**: [Detailed explanation]

**Code Impact**:
```diff
[git diff showing the problematic change]
```

**Why It Breaks**:
1. Factor 1
2. Factor 2
3. Factor 3

### Proof
- Reproduction case: [link to reproduction]
- Failing test: [test details]
- Verification: [how we know]

### Related Code
- Affected files: [list]
- Dependencies: [what else is impacted]
- Side effects: [potential issues]
```

## Analysis Techniques
- **Static Analysis**: Read code without executing
- **Dynamic Analysis**: Execute and observe
- **Logging**: Add strategic log points
- **Debugging**: Step through execution
- **Code Review**: Peer examination

## Evidence Types
- Console output
- Log files
- Memory dumps
- Performance metrics
- Test results

## Documentation Standards
- Be thorough but concise
- Include reproducible examples
- Link related artifacts
- Mark assumptions and limitations