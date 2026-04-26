---
name: 00-spec-deployment-survey
description: Parse MASTER_SPEC.md for security, observability, and deployment requirements
trigger: docforge-overseer during phase 2
---

# 00-Spec Deployment Survey

## Step-by-Step Instructions

1. **Locate Specification Files**
   - Find `MASTER_SPEC.md` in the project root
   - Locate `security.md` and `observability.md` if separate
   - Verify file existence and accessibility

2. **Parse Deployment Requirements**
   - Extract deployment sections from MASTER_SPEC.md
   - Identify environment specifications (dev, staging, prod)
   - Document deployment constraints and limitations

3. **Extract Security Requirements**
   - Read security.md for container security policies
   - Identify required security contexts
   - Extract secrets management requirements
   - Document RBAC and network policies

4. **Extract Observability Requirements**
   - Read observability.md for logging standards
   - Identify metrics collection requirements
   - Extract tracing and monitoring specifications
   - Document alerting and notification requirements

5. **Generate Structured Requirements Document**
   - Create JSON/YAML output with parsed requirements
   - Include environment-specific configurations
   - Document security constraints
   - Store in `/home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/artifacts/requirements/`

6. **Validate Spec Completeness**
   - Check for missing security sections
   - Verify observability requirements are defined
   - Flag deprecated or unclear specifications
   - Generate warnings for missing information

7. **Output Artifacts**
   - `spec-requirements.json` — Parsed requirements
   - `security-requirements.md` — Security constraints
   - `observability-requirements.md` — Monitoring requirements