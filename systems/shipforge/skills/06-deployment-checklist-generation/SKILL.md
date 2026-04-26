---
name: deployment-checklist-generation
description: Generate pre/post deployment checklists
trigger: "security audit passed"
---

## Step-by-Step Instructions

1. **Read All Prerequisites**
   - Use `read_file` to read:
     - `deploy/DEPLOYMENT_REQUIREMENTS.md`
     - `deploy/PARITY_REPORT.md` (should have no critical issues)
     - `deploy/SECURITY_AUDIT.md` (should be PASS or only low/medium issues)
   - Verify: are all security and parity checks passed?
   - Gate: do NOT proceed if critical issues remain

2. **Generate Pre-Deployment Checklist**
   - Use `write_file` to create `deploy/DEPLOYMENT_RUNBOOK.md`
   - Pre-deployment section:
     ```markdown
     # Deployment Runbook
     ## Pre-Deployment Checklist
     ### Backup
     - [ ] Database backup completed (verify: `pg_dump...`)
     - [ ] Config files backed up (verify: `cp -r config/ config-backup/`)
     - [ ] Previous deployment artifacts saved (rollback preparation)
     ### Environment Check
     - [ ] Staging environment validated (all tests pass)
     - [ ] Environment variables set (verify: `echo $DATABASE_URL`)
     - [ ] Secrets properly injected (verify: `kubectl get secrets`)
     - [ ] Resource quotas sufficient (verify: `kubectl describe quota`)
     ### Migration
     - [ ] Database migrations ready (verify: `alembic heads` or equivalent)
     - [ ] Migration rollback script tested in staging
     - [ ] Schema changes backward-compatible (old code can read new schema)
     ### Final Approval
     - [ ] Code review approved
     - [ ] Security audit passed (SECURITY_AUDIT.md = PASS)
     - [ ] Stakeholder sign-off obtained
     ```

3. **Generate Post-Deployment Checklist**
   - Add to same DEPLOYMENT_RUNBOOK.md:
     ```markdown
     ## Post-Deployment Checklist
     ### Smoke Tests
     - [ ] Health endpoint responds: `curl <http://prod/health>`
     - [ ] Critical user journey works (login, main feature)
     - [ ] Database connectivity verified
     - [ ] External API integrations working
     ### Monitoring
     - [ ] Logs flowing to central system
     - [ ] Metrics being collected (verify: Prometheus target UP)
     - [ ] Alerts configured and tested
     - [ ] Error rates within normal range (<1%)
     ### Verification
     - [ ] Deployment successful (all pods running: `kubectl get pods`)
     - [ ] No new errors in logs (check: `kubectl logs deployment/app`)
     - [ ] Performance within SLA (response time <specified in MASTER_SPEC.md)
     ### Rollback Plan (if needed)
     1. `kubectl rollout undo deployment/<service>`
     2. `docker compose down && docker compose up -d`
     3. Restore database: `pg_restore backup_file`
     4. Verify rollback successful (re-run smoke tests)
     ```

4. **Add Contact Information**
   - Add to DEPLOYMENT_RUNBOOK.md:
     ```markdown
     ## Emergency Contacts
     - On-call: +1-xxx-xxx-xxxx (PagerDuty: <link>)
     - Engineering lead: name@company.com
     - Escalation: manager@company.com
     ## Escalation Procedure
     1. Detect issue (monitoring alert or user report)
     2. Assess severity (critical/high/medium/low)
     3. Execute rollback OR fix forward
     4. Post-mortem within 48 hours
     ```

5. **Add Environment-Specific Notes**
   - For each target environment (staging, production):
     - Specific commands for that environment
     - Known issues and workarounds
     - Environment-specific verification steps
     - Custom rollback procedures

6. **Generate Quick Reference**
   - Add to DEPLOYMENT_RUNBOOK.md:
     ```markdown
     ## Quick Reference
     ### Common Commands
     - Check status: `kubectl get pods -n production`
     - View logs: `kubectl logs -f deployment/app -n production`
     - Rollback: `kubectl rollout undo deployment/app`
     - Scale: `kubectl scale deployment/app --replicas=5`
     ### Useful Links
     - Monitoring: <monitoring-url>
     - Alerts: <alerts-url>
     - Docs: <runbook-url>
     ```

7. **Validate Runbook**
   - Use `read_file` to re-read DEPLOYMENT_RUNBOOK.md
   - Verify: are both pre and post checklists complete?
   - Check: are all commands copy-pasteable (no placeholders)?
   - Verify: does the rollback plan actually work? (test in staging)
   - Flag: any checklist item without clear success criteria
