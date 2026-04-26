# TestForge — Test Generation and Validation System

Takes `IMPLEMENTATION_REPORT.md` (from CodeForge) and generates
comprehensive tests, then validates coverage.

## Input Artifacts

- `IMPLEMENTATION_REPORT.md` — REQUIRED (produced by CodeForge)
- `MASTER_SPEC.md` — REQUIRED (produced by SpecForge)

## Output Artifacts

- `TEST_REPORT.md` — test results and coverage report
- `UNIT_TESTS.md` — unit test definitions
- `INTEGRATION_TESTS.md` — integration test definitions
- `COVERAGE_REPORT.md` — coverage analysis

## Phases (Skills)

| Phase | Skill | Description |
|-------|------|-------------|
| 1 | `testforge-01-test-strategy-planning` | Plan test strategy |
| 2 | `testforge-02-unit-test-generation` | Generate unit tests |
| 3 | `testforge-03-integration-test-generation` | Generate integration tests |
| 4 | `testforge-04-kill-test-generation` | Generate kill/edge case tests |
| 5 | `testforge-05-fuzz-target-generation` | Generate fuzz targets |
| 6 | `testforge-06-coverage-validation` | Validate coverage thresholds |
| 7 | `testforge-07-test-execution` | Execute all tests |
| 8 | `testforge-08-coverage-report` | Generate coverage report |

## Gates

- `implementation_ready` — IMPLEMENTATION_REPORT.md must exist
- `tests_pass` — All tests must pass
- `coverage_met` — Coverage threshold must be met

## Handoff

On successful completion, hands off to **DocForge** with:
- `TEST_REPORT.md`
- `COVERAGE_REPORT.md`

## Usage

```bash
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='testforge'); \
          result = o.run_forge('testforge', ctx)"
```
