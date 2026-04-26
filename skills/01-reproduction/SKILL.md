# Reproduction Skill

name: 01-reproduction
description: Reproduce bug reliably, create minimal reproduction case
trigger: when attempting to reproduce reported bugs

## Step-by-Step Instructions

### 1. Setup Environment
- Verify all dependencies are installed
- Check version compatibility
- Configure test environment
- Document environment state

### 2. Execute Reproduction Steps
- Follow issue report steps exactly
- Use bash to execute commands
- Capture all output and errors
- Record timing and sequence

### 3. Create Minimal Test Case
- Strip away non-essential code
- Keep only what triggers the bug
- Ensure test is deterministic
- Document assumptions

### 4. Validate Reproducibility
- Run test multiple times
- Verify consistent failure
- Check for flakiness
- Document success rate

### 5. Document Reproduction
```bash
# Reproduction Script
#!/bin/bash
# Test case for [bug description]

# Setup
echo "Setting up test environment..."
# Command 1
# Command 2

# Execute bug trigger
echo "Executing bug trigger..."
result=$(command_to_test)
echo "Result: $result"

# Verify failure
if [ condition ]; then
    echo "BUG REPRODUCED"
    exit 1
else
    echo "Bug not reproduced"
    exit 0
fi
```

## Bash Best Practices
- Always use `set -e` to stop on errors
- Capture output with `$(command)` or `> file`
- Use `$?` to check exit codes
- Log each step with timestamps

## Minimal Case Criteria
- Single file or function
- No external dependencies
- Clear input/output
- Fast execution (< 1 minute)

## Common Issues
- Environment differences
- Timing issues (race conditions)
- Missing data or configuration
- External service dependencies