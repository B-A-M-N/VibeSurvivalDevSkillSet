# DebugForge — Issue Remediation System

Takes `ISSUE.md` and `FAILING_TESTS.md`, triages the failure,
isolates root cause, and produces a fix.

## Input Artifacts

- `ISSUE.md` — REQUIRED (issue description)
- `FAILING_TESTS.md` — REQUIRED (failing test list)
- `IMPLEMENTATION_REPORT.md` — Optional (context from CodeForge)

## Output Artifacts

- `ROOT_CAUSE_ANALYSIS.md` — root cause analysis
- `FIX_OPTIONS.md` — candidate fix options
- `FIX_REPORT.md` — applied fix and validation results

## Phases (Skills)

| Phase | Skill | Description |
|-------|------|-------------|
| 1 | `debugforge-00-issue-intake` | Parse issue, extract symptoms |
| 2 | `debugforge-01-reproduction` | Reproduce the issue |
| 3 | `debugforge-02-bisection-isolation` | Bisect to isolate cause |
| 4 | `debugforge-03-root-cause-analysis` | Analyze root cause |
| 5 | `debugforge-04-fix-option-generation` | Generate fix options |
| 6 | `debugforge-05-fix-application` | Apply the chosen fix |
| 7 | `debugforge-06-validation` | Validate the fix |

## Gates

- `issue_defined` — ISSUE.md and FAILING_TESTS.md must exist
- `root_cause_found` — ROOT_CAUSE_ANALYSIS.md must exist
- `fix_applied` — FIX_REPORT.md must exist

## Handoff

On successful completion, hands off to **CodeForge** with:
- `FIX_REPORT.md`

On failure, escalates to **ReactiveForge** for incident response.

## Usage

```bash
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='debugforge'); \
          result = o.run_forge('debugforge', ctx)"
```
