---
name: 01-test-strategy-planning
description: Build a test matrix and prioritize by risk
trigger: after 00-spec-scenario-ingest emits its target list
---

# skill 1 — Test Strategy Planning

## Step-by-step instructions
1. Consume the target list from skill 00.
2. Classify each target: unit, integration, kill, fuzz.
3. Assign risk scores combining spec hard gate status and scenario severity.
4. Produce a prioritized test matrix mapping target → test_type → priority.
5. Emit matrix as `test_matrix.json` for testforge-generator consumption.