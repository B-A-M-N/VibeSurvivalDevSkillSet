# Isolation Skill

name: 02-bisection-isolation

## Overview
This skill isolates root causes through systematic analysis of code changes, git history, and component interactions. It narrows down the search space to identify the specific cause of the bug.

## Steps to Isolate Root Cause

1. **Git History Analysis**
   - Examine recent commits in the affected module
   - Use git log with targeted filtering
   - Identify changes that correlate with bug introduction

2. **Git Bisection Process**
   - Mark known good and bad commits
   - Systemically test intermediate commits
   - Narrow down to specific commit causing issue
   - Document bisection process and results

3. **Component Analysis**
   - Trace code execution path for the bug
   - Identify function calls and dependencies
   - Analyze recent modifications to critical paths

4. **Change Impact Assessment**
   - Review code diffs for suspicious changes
   - Check configuration modifications
   - Analyze dependency version changes

5. **Suspicious Pattern Recognition**
   - Look for recent refactoring that might introduce bugs
   - Identify error handling changes
   - Check for race conditions or timing issues

## Output Generation

Create ISOLATION_REPORT.md with the following structure:

```markdown
# Isolation Report

## Git Analysis
- Repository: [repository name]
- Analysis Period: [date range]
- Total Commits Analyzed: [count]

## Bisection Results
- Good Commit: [hash] - [description]
- Bad Commit: [hash] - [description]
- Bisection Path: [list of tested commits]

## Suspicious Commits
- Commit Hash: [hash]
- Author: [author]
- Date: [date]
- Message: [commit message]
- Changed Files: [file list]
- Impact Analysis: [why this is suspicious]

## Component Isolation
- Primary Component: [identified component]
- Secondary Components: [related affected components]
- Call Graph: [execution path analysis]

## Root Cause Hypothesis
- Proposed Cause: [hypothesis]
- Evidence: [supporting evidence]
- Confidence Level: [high/medium/low]
```

## Best Practices

- Use systematic approach rather than random guessing
- Document all tested commits and results
- Verify bisection results with multiple test cases
- Consider environmental factors beyond code changes
- Validate isolation hypothesis with targeted testing

## Quality Checks

- [ ] Git log thoroughly analyzed
- [ ] Bisection performed correctly
- [ ] Suspicious commits identified
- [ ] Component isolation documented
- [ ] ISOLATION_REPORT.md generated

## Advanced Techniques

- **Binary Search Optimization**: Use midpoint testing to minimize iterations
- **Historical Pattern Matching**: Compare with similar past bugs
- **Dependency Analysis**: Track third-party library changes
- **Configuration Drift Detection**: Identify environment differences
- **Performance Regression Analysis**: Check for timing-related issues

## Integration with Other Skills

This skill works with:
- Issue Intake: Provides context for severity assessment
- Reproduction: Validates reproduction steps
- Root Cause Analysis: Feeds into deeper investigation

## Common Challenges

- Incomplete git history
- Missing test coverage for certain scenarios
- Intermittent bugs that don't reproduce consistently
- Large codebases making analysis time-consuming
- Complex dependency chains