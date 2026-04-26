---
name: 04-environment-parity-check
description: Verify environment consistency and parity across deployments
trigger: after 03-deployment-config-generation creates configs
---

# 04-Environment Parity Check

## Step-by-Step Instructions

1. **Environment Validation**
   - Compare dev/staging/production configurations
   - Verify resource allocation consistency
   - Check network policies across environments

2. **Parity Testing**
   - Run identical tests across all environments
   - Verify behavior consistency
   - Document any discrepancies

3. **Output Report**
   - `parity_report.md` — Parity validation results
   - Flag any environment-specific issues