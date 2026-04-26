# ReactiveForge — Incident Response System

Detects trace anomalies, classifies failures, and drives automated
remediation through CodeForge + TestForge.

## Input Artifacts

- `TRACE_AANOMALY.md` — REQUIRED (detected anomaly)
- `INCIDENT_REPORT.md` — REQUIRED (incident description)

## Output Artifacts

- `FIX_CANDIDATE.md` — candidate fix from research
- `REMEDIATION_REPORT.md` — applied fix and validation
- `INCIDENT_RESOLUTION.md` — final resolution document

## Workflow (Not Magic)

ReactiveForge is a **workflow**, not magic:

1. **Detect** — monitor traces for anomalies (via TracingMiddleware)
2. **Classify** — determine failure type (bug, perf, security)
3. **Research** — create research tracks (like ResearchForge)
4. **Subagents** — spawn subagents to investigate
5. **Synthesize** — combine findings into candidate fix
6. **CodeForge** — invoke CodeForge to apply fix
7. **TestForge** — invoke TestForge to validate
8. **Verify** — check tests pass
9. **Close** — if verified, close incident
10. **Escalate** — if not fixed, escalate to user

## Gates

- `anomaly_detected` — TRACE_AANOMALY.md must exist
- `fix_synthesized` — FIX_CANDIDATE.md must exist
- `tests_pass` — all tests must pass after fix

## Handoff

On success, incident is closed.

On failure, escalates to **user** with:
- `INCIDENT_REPORT.md`
- `FIX_ATTEMPTS.md` — history of failed attempts

## No Magic Policy

ReactiveForge does NOT:
- Patch code without evidence
- Skip verification steps
- Hide failures from the user
- Auto-deploy unverified fixes

Every action is documented in trace and requires evidence.

## Usage

```bash
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='reactiveforge'); \
          result = o.run_forge('reactiveforge', ctx)"
```
