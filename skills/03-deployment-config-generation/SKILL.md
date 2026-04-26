---
name: 03-deployment-config-generation
description: Parse MASTER_SPEC.md for deployment, security, and observability configs
trigger: after 02-ci-pipeline-generation emits its pipeline config
---

# 03-Deployment Config Generation

## Step-by-Step Instructions

1. **Parse Deployment Requirements**
   - Extract deployment sections from MASTER_SPEC.md
   - Identify environment specifications (dev, staging, prod)
   - Document deployment constraints and limitations

2. **Extract Security Requirements**
   - Read security.md for container security policies
   - Identify required security contexts
   - Extract secrets management requirements
   - Document RBAC and network policies

3. **Extract Observability Requirements**
   - Read observability.md for logging standards
   - Identify metrics collection requirements
   - Extract tracing and monitoring specifications
   - Document alerting and notification requirements

4. **Generate Structured Configs**
   - Create JSON/YAML output with parsed requirements
   - Include environment-specific configurations
   - Document security constraints
   - Store in appropriate deployment directories