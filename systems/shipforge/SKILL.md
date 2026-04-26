# ShipForge — Deployment Preparation System

Takes `DOC_REPORT.md` (from DocForge) and prepares
deployment configs, CI pipelines, and checklists.

## Input Artifacts

- `DOC_REPORT.md` — REQUIRED (produced by DocForge)

## Output Artifacts

- `DEPLOY_REPORT.md` — deployment report
- `DOCKERFILE` — container definition
- `CI_PIPELINE.yml` — CI/CD pipeline
- `DEPLOYMENT_CHECKLIST.md` — pre-deploy checklist

## Phases (Skills)

| Phase | Skill | Description |
|-------|------|-------------|
| 1 | `shipforge-01-dockerfile-generation` | Generate Dockerfile |
| 2 | `shipforge-02-ci-pipeline-generation` | Generate CI pipeline |
| 3 | `shipforge-03-deployment-config-generation` | Generate deployment configs |
| 4 | `shipforge-04-environment-parity-check` | Check env parity |
| 5 | `shipforge-05-security-hardening-check` | Security hardening check |
| 6 | `shipforge-06-deployment-checklist-generation` | Generate checklist |
| 7 | `shipforge-07-ship` | Execute deployment |

## Gates

- `docs_ready` — DOC_REPORT.md must exist
- `deploy_ready` — DEPLOY_REPORT.md must exist
- `checklist_complete` — DEPLOYMENT_CHECKLIST.md must exist

## Handoff

On successful completion, the deployment is complete.

## Usage

```bash
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='shipforge'); \
          result = o.run_forge('shipforge', ctx)"
```
