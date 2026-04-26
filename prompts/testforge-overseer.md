# testforge-overseer.md
Plan a complete test matrix and orchestrate the pipeline.

1) Parse inputs
   - Load MASTER_SPEC.md and SCENARIOS.md via skill 00.
   - Extract concrete targets: modules, APIs, state transitions, invariants, boundary conditions.

2) Build test matrix
   - Use skill 01 to map each target to test types: unit / integration / kill / fuzz.
   - Prioritize by risk (spec hard gates, SCENARIOS severity, recent change).

3) Delegate generation
   - Assign unit tests → testforge-generator.
   - Assign kill & integration tests → testforge-generator.
   - Assign fuzz targets → testforge-generator.

4) Coverage gating
   - After each generation burst, request coverage report from testforge-coverage.
   - If coverage gaps remain against spec hard gates, create remediation tasks and re-delegate.

5) Finalize
   - Collect manifests, merge into test_manifest.json.
   - Produce gaps.md and coverage_report/.
   - Declare pipeline complete only when all hard gates pass.