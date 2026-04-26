---
name: 05-security-hardening-check
description: Validate deploy configs against spec security section
trigger: after security review and before deployment
---

# 05-Security Hardening Check

## Trigger
When deployment configurations need security validation against spec requirements.

## Step-by-Step Instructions

1. **Extract Security Requirements**
   - Parse security.md for security policies
   - Identify required security contexts
   - Document container security standards
   - Extract secrets management requirements

2. **Review Deployment Configurations**
   - Examine Kubernetes manifests
   - Review Docker configurations
   - Check CI/CD pipeline security settings
   - Validate environment variables

3. **Validate Security Contexts**
   - Ensure containers run as non-root
   - Verify read-only filesystems
   - Check privileged container settings
   - Validate security capabilities
   - Review AppArmor/SELinux configurations

4. **Check Resource Limits**
   - Verify CPU and memory limits
   - Ensure resource requests are set
   - Validate limits are appropriate
   - Check for missing resource constraints

5. **Validate Network Security**
   - Review network policies
   - Check ingress/egress rules
   - Validate service exposure settings
   - Verify network segmentation

6. **Check Secrets Management**
   - Ensure secrets are properly defined
   - Validate secret references
   - Check encryption at rest
   - Review access controls

7. **Perform Security Scanning**
   - Run vulnerability scans on images
   - Check for known CVEs
   - Validate dependency security
   - Review image provenance

8. **Generate Security Report**
   - Document validation results
   - Flag security issues
   - Provide remediation steps
   - Create security compliance status

9. **Output Artifacts**
   - `security/validation-report.md`
   - `security/compliance-status.json`
   - `security/remediation-plan.md`