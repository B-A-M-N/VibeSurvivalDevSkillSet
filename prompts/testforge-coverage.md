# testforge-coverage.md
Analyze coverage and surface gaps relative to spec and scenarios.

1) Collect executed traces
   - Aggregate coverage data from unit_tests, kill_tests, integration_tests, fuzz_targets.
   - Normalize by source file and line/branch IDs.

2) Map to spec & scenarios
   - For each requirement in MASTER_SPEC.md, verify at least one test exercises it.
   - For each entry in SCENARIOS.md, verify a kill or fuzz target covers the edge case.

3) Compute gaps
   - Produce gaps.md listing uncovered spec IDs, scenario IDs, and suggested test types.
   - Highlight spec hard gates that remain unmet.

4) Report output
   - Generate HTML summary and coverage.json with per-target coverage ratios.
   - Fail if any hard gate coverage < 100%.