---
name: 04-integration-test-generation
description: Generate integration tests for API, state machine, cross-module
trigger: after 03-deployment-config-generation creates configs
---

# skill 4 — Integration Test Generation

**Trigger**: integration-priority entries from test_matrix.json.

## Step-by-step instructions
1. For each integration target: identify involved modules and the call sequence.
2. Mock or stub external dependencies; preserve state consistency across calls.
3. Write tests that exercise happy paths and failure paths across module boundaries.
4. Assert end-state, emitted events, and side effects; include gas/step checks where relevant.
5. Output to `integration_tests/<flow>_integration.<lang>` and register in test_manifest.json.