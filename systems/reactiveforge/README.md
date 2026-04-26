# ReactiveForge — Incident Response System

Detects trace anomalies, classifies failures, and drives automated
remediation through CodeForge + TestForge.

## Philosophy

ReactiveForge is a **workflow**, not magic. Every action is:
1. Evidence-based (no patching without proof)
2. Documented (trace events for all actions)
3. Verified (tests must pass before closing)
4. Transparent (user can see all steps)

## Input Artifacts

- `TRACE_AANOMALY.md` — REQUIRED (detected anomaly)
- `INCIDENT_REPORT.md` — REQUIRED (incident description)

## Output Artifacts

- `FIX_CANDIDATE.md` — candidate fix from research
- `REMEDIATION_REPORT.md` — applied fix and validation
- `INCIDENT_RESOLUTION.md` — final resolution document

## Workflow Steps

| Step | Description |
|------|-------------|
| 1. Detect Anomaly | Monitor traces for anomalies |
| 2. Classify Failure | Determine failure type (bug, perf, security) |
| 3. Create Research Tracks | Plan investigation (like ResearchForge) |
| 4. Spawn Subagents | Spawn subagents to investigate |
| 5. Synthesize Fix | Combine findings into candidate fix |
| 6. Invoke CodeForge | Apply fix via CodeForge |
| 7. Invoke TestForge | Validate fix via TestForge |
| 8. Verify Fix | Check tests pass |
| 9. Close or Escalate | Close incident or escalate to user |

## Gates

- `anomaly_detected` — TRACE_AANOMALY.md must exist
- `fix_synthesized` — FIX_CANDIDATE.md must exist
- `tests_pass` — All tests must pass after fix

## No Magic Policy

ReactiveForge does NOT:
- Patch code without evidence
- Skip verification steps
- Hide failures from the user
- Auto-deploy unverified fixes

## Handoff

On success, incident is **closed**.

On failure, **escalates to user** with:
- `INCIDENT_REPORT.md`
- `FIX_ATTEMPTS.md` — history of failed attempts

## Usage

```bash
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='reactiveforge'); \
          result = o.run_forge('reactiveforge', ctx)"
```
