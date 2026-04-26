---
name: 03-kill-test-generation
description: Generate tests for kill scenarios and failure modes
trigger: when unit tests are generated
---

# 03-Kill Test Generation

## Step-by-Step Instructions

1. **Identify Kill Scenarios**
   - Determine failure modes from spec requirements
   - Identify resource exhaustion patterns
   - Document expected failure behaviors

2. **Generate Kill Tests**
   - Create tests that trigger resource limits
   - Test timeout handling
   - Verify graceful degradation
   - Validate error recovery

3. **Output Test Files**
   - `kill_tests/<module>_kill_test.<lang>`
   - Register in test_manifest.json with kill type