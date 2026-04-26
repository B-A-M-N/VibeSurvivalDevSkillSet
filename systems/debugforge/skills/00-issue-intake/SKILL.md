# Issue Intake Skill

name: issue-intake

## Overview
This skill parses incoming issue reports, extracts critical information, and classifies the issue for proper debugging workflow. It serves as the entry point for the DebugForge bug resolution pipeline.

## Steps to Parse Issue Report

1. **Extract Issue Metadata**
   - Parse title, description, and any attached files
   - Identify timestamp and reporter information
   - Extract environment details (OS, version, configuration)

2. **Extract Reproduction Steps**
   - Look for step-by-step instructions in the issue body
   - Identify commands, code snippets, and configuration changes
   - Capture any error messages or stack traces

3. **Classify Severity Levels**
   - **Critical**: System crashes, data loss, security vulnerabilities
   - **High**: Major functionality broken, blocking workflows
   - **Medium**: Partial functionality loss, degraded performance
   - **Low**: Cosmetic issues, minor inconveniences

4. **Identify Affected Components**
   - Module names, service names, or file paths mentioned
   - API endpoints or database tables involved
   - Configuration sections impacted

5. **Extract Key Technical Details**
   - Error codes and exception types
   - Version numbers and build identifiers
   - Log file snippets and diagnostic data

## Output Generation

Create ISSUE_ANALYSIS.md with the following structure:

```markdown
# Issue Analysis Report

## Summary
Brief description of the issue

## Severity Classification
- Level: Critical/High/Medium/Low
- Justification: Why this severity level

## Affected Components
- Component 1: Description
- Component 2: Description

## Key Technical Details
- Error messages and codes
- Version information
- Environment details

## Reproduction Steps
Numbered steps to reproduce the issue

## Related Artifacts
- Log files, screenshots, configuration samples
```

## Best Practices

- Always verify extracted information with the reporter
- Use consistent severity classification across all issues
- Document assumptions made during analysis
- Tag related issues for pattern recognition

## Quality Checks

- [ ] All mandatory fields extracted
- [ ] Severity classification justified
- [ ] Components clearly identified
- [ ] Reproduction steps are complete
- [ ] ISSUE_ANALYSIS.md generated correctly

## Integration Points

This skill feeds directly into the reproduction phase and provides structured input for root cause analysis. The output format must be compatible with downstream processing tools.

## Common Issues

- Incomplete reproduction steps
- Ambiguous severity classifications
- Missing component identification
- Unclear error message extraction

## Automation Hints

Consider implementing regex patterns for common error formats and automated parsing of structured log files to speed up the intake process.