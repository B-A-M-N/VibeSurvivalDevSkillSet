# ShipForge System Implementations

## Overview
This document details the implementation strategies and integration points for the ShipForge deployment system.

## Integration Points

### Spec Consumption
- **Location**: `skills/00-spec-deployment-survey/SKILL.md`
- **Function**: Parses `MASTER_SPEC.md` for security and observability requirements
- **Output**: Structured requirements document used by downstream agents

### Dockerfile Generation
- **Location**: `skills/01-dockerfile-generation/SKILL.md`
- **Function**: Creates multi-stage Dockerfiles based on spec requirements and codebase analysis
- **Features**:
  - Minimal base images (distroless when possible)
  - Security scanning integration
  - Environment-specific optimizations

### CI Pipeline Configuration
- **Location**: `skills/02-ci-pipeline-generation/SKILL.md`
- **Function**: Generates CI workflows (GitHub Actions, GitLab CI, etc.)
- **Pipeline Stages**:
  1. Build and test
  2. Security scanning
  3. Docker image build
  4. Deploy to staging
  5. Environment parity verification
  6. Deploy to production (with approval)

### Deployment Configuration
- **Location**: `skills/03-deployment-config-generation/SKILL.md`
- **Function**: Creates Kubernetes manifests, docker-compose files, and PaaS configurations
- **Template Variables**:
  - Environment name
  - Resource limits
  - Environment variables
  - Security contexts

### Environment Parity
- **Location**: `skills/04-environment-parity-check/SKILL.md`
- **Function**: Compares configurations across environments
- **Check Categories**:
  - Resource allocation
  - Environment variables
  - Security settings
  - Network policies
  - Scaling configurations

### Security Hardening
- **Location**: `skills/05-security-hardening-check/SKILL.md`
- **Function**: Validates deployment configs against security specifications
- **Validation Points**:
  - Run as non-root user
  - Read-only filesystem where appropriate
  - Resource limits set
  - No privileged containers
  - Security contexts defined

### Deployment Checklist
- **Location**: `skills/06-deployment-checklist-generation/SKILL.md`
- **Function**: Generates pre and post-deployment checklists
- **Checklist Categories**:
  - Pre-deployment validation
  - Deployment steps
  - Post-deployment verification
  - Rollback procedures

## Agent Orchestration

### shipforge-overseer
- **Responsibilities**:
  - Coordinate workflow between agents
  - Manage state transitions
  - Handle error recovery
  - Enforce turn limits (max 60)
- **Communication**: Acts as message broker between agents

### shipforge-builder
- **Responsibilities**:
  - Generate all build artifacts
  - Write files based on spec
  - Handle Docker and CI configurations
  - Unlimited turns for complex builds

### shipforge-deployer
- **Responsibilities**:
  - Create deployment configurations
  - Generate environment templates
  - Write deployment checklists
  - Enforce turn limits (max 40)

## File Generation Strategy

### Static Files
- Generated once based on spec
- Version controlled with application code

### Dynamic Files
- Generated per environment
- Include environment-specific variables

### Template Files
- Use Go templates or similar
- Support variable substitution
- Allow for custom overrides

## Error Handling

### Spec Parsing Errors
- Log warnings, continue with defaults
- Flag missing security/observability sections

### Generation Failures
- Rollback to last known good state
- Generate error report
- Notify overseer agent

### Validation Failures
- Halt deployment pipeline
- Generate remediation checklist
- Notify deployer agent

## Artifact Storage
- All generated artifacts stored in `/artifacts/`
- Organized by environment and phase
- Includes checksums for verification
- Retention policy: 90 days