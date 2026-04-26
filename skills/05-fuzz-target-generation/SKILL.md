---
name: 05-fuzz-target-generation
description: Generate fuzz targets for input validation, boundary conditions
trigger: when integration tests are generated
---

# skill 5 — Fuzz Target Generation

**Trigger**: fuzz-priority entries from test_matrix.json and uncovered boundary conditions.

## Step-by-step instructions
1. Identify functions/API endpoints that accept external input.
2. Create seed corpus from SCENARIOS values and spec examples.
3. Define dictionary entries, max_length, and validity constraints.
4. Instrument code for coverage-guided fuzzing (e.g., afl, libFuzzer, or foundry fuzz).
5. Write a fuzz target harness that calls the target with mutated inputs.
6. Output as `fuzz_targets/<target>.fuzz` and register in test_manifest.json.