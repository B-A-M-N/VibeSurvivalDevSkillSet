# Reproduction Skill

name: 01-reproduction

## Overview
This skill reliably reproduces bugs and creates minimal test cases. It ensures deterministic reproduction steps that can be automated and verified consistently.

## Steps to Reproduce Bug Reliably

1. **Environment Setup**
   - Recreate the exact environment from the issue report
   - Match OS version, dependencies, and configuration
   - Set up any required test data or fixtures

2. **Follow Extraction Steps**
   - Execute reproduction steps from ISSUE_ANALYSIS.md
   - Verify each step produces expected intermediate results
   - Document any deviations or unexpected behaviors

3. **Ensure Deterministic Reproduction**
   - Run reproduction steps multiple times to verify consistency
   - Identify and control for non-deterministic factors
   - Document conditions that affect reproducibility

4. **Create Minimal Reproduction Case**
   - Strip away non-essential code and configuration
   - Isolate the core issue to smallest possible example
   - Remove dependencies that don't contribute to the bug

5. **Document Reproduction Steps**
   - Create numbered, executable steps
   - Include exact commands and expected outputs
   - Document any required setup or prerequisites

## Output Generation

Create REPRODUCTION.md with the following structure:

```markdown
# Reproduction Case

## Environment Setup
- OS: [version]
- Dependencies: [versions]
- Configuration: [key settings]

## Minimal Reproduction Steps
1. [First step with exact command/action]
2. [Second step with expected outcome]
3. [Continue with numbered steps]

## Expected Behavior
What should happen when following these steps correctly

## Actual Behavior
What currently happens

## Deterministic Verification
- Test run count: [number]
- Success rate: [percentage]
- Conditions for consistent reproduction
```

## Best Practices

- Ensure each step is atomic and verifiable
- Use exact versions and configurations
- Test reproduction in clean environments
- Document both success and failure paths
- Make reproduction scriptable for automation

## Quality Checks

- [ ] Steps can be reproduced consistently
- [ ] Minimal case isolates the core issue
- [ ] All commands are exact and testable
- [ ] Environment setup is complete
- [ ] REPRODUCTION.md is properly formatted

## Automation Integration

The reproduction steps should be convertible to automated test scripts. Consider:
- Shell scripts for command-line reproduction
- Unit tests for code-level issues
- Integration tests for system-level bugs
- CI/CD pipeline integration for regression testing

## Common Pitfalls

- Non-deterministic reproduction steps
- Missing environment dependencies
- Overly complex minimal cases
- Inconsistent test data
- Unclear success/failure criteria