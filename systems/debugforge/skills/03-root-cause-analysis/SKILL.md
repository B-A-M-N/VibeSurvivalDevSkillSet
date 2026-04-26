# Root Cause Analysis Skill

name: 03-root-cause-analysis

## Overview
This skill performs deep analysis of root causes by gathering and examining evidence from logs, application state, error messages, and code paths. It provides comprehensive understanding of why a bug occurs.

## Steps for Deep Root Cause Analysis

1. **Evidence Collection**
   - Gather all relevant logs from the time of failure
   - Capture application state at the point of failure
   - Collect error messages, stack traces, and core dumps
   - Document environmental conditions during failure

2. **Code Path Analysis**
   - Trace the execution path that led to the failure
   - Identify function calls and their interactions
   - Analyze conditional logic and state changes
   - Map data flow through the system

3. **State Examination**
   - Inspect variable values at critical points
   - Check database state and transaction status
   - Analyze memory usage and resource allocation
   - Review configuration and settings

4. **Mechanism Identification**
   - Determine the fundamental cause of the failure
   - Distinguish symptoms from root causes
   - Identify contributing factors and their relationships
   - Assess whether issue is systemic or isolated

5. **Validation and Testing**
   - Create targeted tests to verify root cause hypothesis
   - Test fixes against identified root cause
   - Ensure understanding is comprehensive and accurate

## Output Generation

Create ROOT_CAUSE_REPORT.md with the following structure:

```markdown
# Root Cause Analysis Report

## Problem Summary
Brief description of the observed failure

## Evidence Collection
### Log Analysis
- Log files examined: [list]
- Key error patterns: [patterns]
- Time range analyzed: [range]

### Stack Trace Analysis
- Primary exception: [exception type]
- Call stack: [full stack trace]
- Error location: [file:line]

### State Examination
- Variable states at failure: [key variables]
- Database state: [relevant database information]
- System resources: [memory, file handles, etc.]

## Root Cause Identification

### Primary Cause
- Direct cause: [technical explanation]
- Contributing factors: [list]
- Failure mechanism: [how it happened]

### Secondary Factors
- Related issues that exacerbated the problem
- Environmental conditions that enabled the bug
- Design or architectural weaknesses

## Verification

### Hypothesis Testing
- Tests performed: [list]
- Results: [pass/fail]
- Confidence level: [high/medium/low]

### Prevention Analysis
- What should have been caught
- Missing safeguards
- Process improvements needed
```

## Best Practices

- Document all evidence systematically
- Maintain chronological order of analysis
- Distinguish correlation from causation
- Validate findings with multiple evidence sources
- Consider alternative explanations

## Quality Checks

- [ ] All evidence collected and documented
- [ ] Code path fully traced
- [ ] State examination complete
- [ ] Root cause clearly identified
- [ ] ROOT_CAUSE_REPORT.md generated

## Analytical Techniques

- **Timeline Analysis**: Reconstruct events in chronological order
- **Pattern Recognition**: Identify recurring themes or symptoms
- **Divide and Conquer**: Isolate subsystems to narrow scope
- **Fault Tree Analysis**: Map failure propagation paths
- **State Comparison**: Compare working vs. failing states

## Common Challenges

- Insufficient logging or unclear error messages
- Intermittent issues that are hard to reproduce
- Complex interactions making isolation difficult
- Legacy code without clear documentation
- Time pressure to resolve issues quickly

## Integration Points

This skill builds on:
- Issue Intake: Provides context from ISSUE_ANALYSIS.md
- Reproduction: Uses REPRODUCTION.md steps
- Isolation: Leverages ISOLATION_REPORT.md findings

And feeds into:
- Fix Generation: Provides context for solution design
- Validation: Informs test case creation