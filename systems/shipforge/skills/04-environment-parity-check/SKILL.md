---
name: environment-parity-check
description: Compare dev/staging/prod environments
trigger: "/parity-check"
---

## Step-by-Step Instructions

1. **Discover Environment Configs**
   - Use `bash` to find config files:
     `find . -name "*.yaml" -o -name "*.yml" -o -name ".env*" -o -name "config.*"`
   - Use `read_file` to read each environment config
   - Classify: dev, staging, production, or unknown
   - Note: which configs have overrides for each environment

2. **Compare Port Configurations**
   - Extract port numbers from each environment config
   - Build comparison: `| Service | Dev Port | Staging Port | Prod Port | Match? |`
   - Flag: ports that differ between environments (may indicate misconfiguration)
   - Verify: are all exposed ports documented in MASTER_SPEC.md?

3. **Compare Environment Variables**
   - Extract env vars from each config (except actual secret values)
   - Build comparison: `| Variable | Dev | Staging | Prod | Match? |`
   - Flag: critical vars missing in any environment
   - Flag: vars with different formats between environments
   - Note: `DATABASE_URL` format should be consistent

4. **Compare Volume Mounts**
   - Extract volume paths and sizes from each config
   - Build comparison: `| Volume | Dev | Staging | Prod | Match? |`
   - Flag: production has smaller volumes than staging (risk of running out)
   - Verify: are all volumes documented in MASTER_SPEC.md?

5. **Compare Resource Limits**
   - Extract CPU/memory requests and limits
   - Build comparison: `| Service | Env | CPU (req/lim) | Memory (req/lim) |`
   - Flag: production has lower limits than staging (performance risk)
   - Flag: development has higher limits than production (cost inefficiency)

6. **Compare Security Configurations**
   - Check: is TLS enabled in production? (should be yes)
   - Check: are auth mechanisms consistent across environments?
   - Check: do all environments use secret management? (not hardcoded values)
   - Flag: production allows HTTP while staging uses HTTPS (misconfiguration)

7. **Generate PARITY_REPORT.md**
   - Use `write_file` to create `deploy/PARITY_REPORT.md`
   - Structure:
     ```markdown
     # Environment Parity Report
     ## Summary: N mismatches found
     ## Port Comparison
     | Service | Dev | Staging | Prod | Status |
     ## Environment Variables
     | Variable | Dev | Staging | Prod | Status |
     ## Volumes
     | Volume | Dev | Staging | Prod | Status |
     ## Resources
     | Service | Env | CPU | Memory | Status |
     ## Security
     - [ ] TLS enabled (prod)
     - [ ] Auth consistent
     - [ ] No hardcoded secrets
     ## Action Items
     1. [critical] Fix port mismatch for service X
     2. [medium] Align resource limits for service Y
     ```
   - Classify each mismatch: critical, high, medium, low

8. **Validate**
   - Use `read_file` to re-read PARITY_REPORT.md
   - Verify: are all environment configs compared?
   - Check: is the severity classification justified?
   - Flag: any environment with >3 critical mismatches (blocker for deployment)
