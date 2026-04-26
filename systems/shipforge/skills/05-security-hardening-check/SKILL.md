---
name: security-hardening-check
description: Validate deploy configs against spec security
trigger: "deployment configs ready"
---

## Step-by-Step Instructions

1. **Read Security Spec**
   - Use `read_file` to read MASTER_SPEC.md Security section
   - Extract: authentication method, encryption requirements, access controls
   - Extract: CORS policy, rate limiting, IP whitelisting
   - Note: compliance requirements (GDPR, HIPAA, SOC2, etc.)

2. **Check for Hardcoded Secrets**
   - Use `bash` to scan all deploy configs:
     `grep -rn "password\|secret\|key\|token\|api_key" deploy/ --include="*.yaml" --include="*.yml"`
   - Use `bash` to scan Dockerfile: `grep -n "ENV.*PASSWORD\|ENV.*SECRET" Dockerfile`
   - Flag: any actual secret values (not just variable names)
   - Flag: `ENV SECRET=actual_value` (should use runtime injection)

3. **Validate Authentication**
   - Check: is authentication required for all external endpoints?
   - Verify: does the auth method match MASTER_SPEC.md?
   - Check: are auth tokens properly validated (not just checked for existence)?
   - Flag: endpoints without auth in production configs

4. **Validate Encryption**
   - Check: is TLS/SSL enabled for all external traffic?
   - Verify: is encryption at rest configured for databases?
   - Check: are certificates properly referenced (not self-signed in prod)?
   - Flag: HTTP (not HTTPS) in production ingress/configs

5. **Check Access Controls**
   - Verify: are CORS policies configured (if web app)?
   - Check: are rate limits configured (prevent abuse)?
   - Verify: is IP whitelisting used for admin endpoints?
   - Flag: endpoints accessible without any access control

6. **Scan for Known Vulnerabilities**
   - Use `bash` to check base images: `grep "FROM" Dockerfile`
   - Flag: images using `latest` tag (unpinned)
   - Flag: images with known vulnerabilities (check against known CVE databases)
   - Recommend: specific version tags for all base images

7. **Check Logging and Monitoring**
   - Verify: are security events logged? (auth failures, access violations)
   - Check: is log data sanitized (no secrets in logs)?
   - Verify: are security metrics collected (failed logins, etc.)?
   - Flag: no security logging in production configs

8. **Check Compliance (if applicable)**
   - GDPR: is user data deletion possible? (endpoint exists?)
   - HIPAA: is PHI encrypted at rest and in transit?
   - SOC2: are access logs retained for audit?
   - Flag: any compliance requirement not met in configs

9. **Generate SECURITY_AUDIT.md**
   - Use `write_file` to create `deploy/SECURITY_AUDIT.md`
   - Structure:
     ```markdown
     # Security Audit Report
     ## Summary: PASS/FAIL (N critical issues)
     ## Hardcoded Secrets
     | File | Line | Issue | Severity |
     ## Authentication
     - [PASS/FAIL] All endpoints protected
     ## Encryption
     - [PASS/FAIL] TLS enabled for all external traffic
     ## Access Controls
     | Check | Status | Details |
     ## Vulnerabilities
     | Image | Issue | Severity |
     ## Compliance
     | Requirement | Status | Notes |
     ## Recommendations
     1. [critical] Remove hardcoded secret in Dockerfile:42
     2. [high] Enable TLS in production ingress
     ```
   - Assign severity: critical (blocks deployment), high, medium, low

10. **Validate**
    - Use `read_file` to re-read SECURITY_AUDIT.md
    - Verify: are all MASTER_SPEC.md security requirements checked?
    - Check: are critical issues truly blocking?
    - Flag: any audit item without clear evidence or fix recommendation
