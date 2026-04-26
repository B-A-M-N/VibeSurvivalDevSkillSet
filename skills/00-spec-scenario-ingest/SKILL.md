---
name: 00-spec-scenario-ingest
description: Parse MASTER_SPEC.md + SCENARIOS.md, extract test targets
trigger: orchestration start or spec/scenario change detected
---

# skill 00 — Spec & Scenario Ingest

## Step-by-step instructions
1. Read MASTER_SPEC.md and locate: modules, contracts, invariants, boundaries, hard gates.
2. Read SCENARIOS.md and enumerate scenarios with IDs, severity, expected outcomes.
3. Emit normalized target list JSON to stdout: `{"spec_targets": [...], "scenario_targets": [...]}`.
4. Store parsed artifacts in `spec/` directory for downstream skills.