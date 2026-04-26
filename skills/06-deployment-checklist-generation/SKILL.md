---
name: 06-deployment-checklist-generation
description: Generate pre/post deployment checklists, runbooks
trigger: before deployment to verify readiness
---

# 06-Deployment Checklist Generation

## Trigger
When deployment checklists and runbooks need to be created for deployment operations.

## Step-by-Step Instructions

1. **Gather Deployment Requirements**
   - Review deployment specifications
   - Identify critical deployment steps
   - Extract rollback procedures
   - Document approval requirements

2. **Create Pre-Deployment Checklist**
   - Environment validation
   - Resource availability check
   - Backup verification
   - Security scan results review
   - Configuration validation
   - Team notification

3. **Document Deployment Steps**
   - Container image deployment
   - Configuration application
   - Service initialization
   - Health check validation
   - Traffic routing configuration
   - Monitoring setup

4. **Generate Post-Deployment Checklist**
   - Health verification
   - Performance monitoring
   - Log collection
   - Alert configuration
   - User acceptance testing
   - Documentation update

5. **Create Rollback Procedures**
   - Identify rollback triggers
   - Document rollback steps
   - Create automated rollback scripts
   - Define rollback approval process
   - Test rollback procedures

6. **Generate Runbook**
   - Document deployment process
   - Include troubleshooting steps
   - Create escalation procedures
   - Define communication plan
   - Add verification steps

7. **Validate Checklists**
   - Review completeness
   - Test procedures
   - Verify accuracy
   - Get team approval

8. **Output Artifacts**
   - `deploy/checklist.md` — Deployment checklist
   - `deploy/playbook.md` — Deployment runbook
   - `deploy/rollback.md` — Rollback procedures