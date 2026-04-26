# Issue Intake Skill

name: 00-issue-intake
description: Parse issue report, extract repro steps, classify severity
trigger: when parsing bug reports or issue tickets

## Step-by-Step Instructions

### 1. Parse Issue Report
- Extract title, description, and any error messages
- Identify affected components or services
- Capture stack traces and error codes
- Note environment details (OS, version, config)

### 2. Extract Reproduction Steps
- List all commands executed
- Identify preconditions and setup requirements
- Capture exact error messages
- Document expected vs actual behavior

### 3. Classify Severity
- **Critical**: System down, data loss, security issue
- **High**: Major functionality broken, blocking work
- **Medium**: Partial functionality, workaround available
- **Low**: Cosmetic, minor inconvenience

### 4. Create Structured Report
```markdown
# Bug Report

## Summary
[One-line description]

## Severity
[Critical/High/Medium/Low]

## Components
[Affected modules/services]

## Reproduction Steps
1. Step 1
2. Step 2
...

## Expected Behavior
[...]

## Actual Behavior
[...]

## Error Messages
[Stack traces, error codes]

## Environment
[Version, OS, Config]
```

### 5. Generate Initial Hypothesis
- What is the likely root cause?
- What recent changes could affect this?
- What are the potential fix directions?

## Common Patterns
- Missing dependencies
- Configuration errors
- Race conditions
- Memory leaks
- API changes
- Version mismatches