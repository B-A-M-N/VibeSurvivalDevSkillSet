---
name: 01-dockerfile-generation
description: Generate Dockerfile from spec and codebase, multi-stage, minimal
trigger: when build artifacts need to be created from source code and spec requirements
---

# 01-Dockerfile Generation

## Trigger
When build artifacts need to be created from source code and spec requirements.

## Step-by-Step Instructions

1. **Analyze Codebase Structure**
   - Identify application entry points
   - Determine build requirements
   - Locate dependencies and configuration files

2. **Review Spec Requirements**
   - Extract build constraints from spec
   - Identify required base images
   - Document security requirements

3. **Design Multi-Stage Dockerfile**
   - Stage 1: Build environment
     - Install build dependencies
     - Compile source code
     - Run tests
   - Stage 2: Runtime environment
     - Use minimal base image
     - Copy only necessary artifacts
     - Set non-root user
   - Stage 3 (optional): Security scanning
     - Scan for vulnerabilities
     - Verify dependencies

4. **Implement Security Best Practices**
   - Use distroless or alpine base images
   - Set resource limits
   - Implement health checks
   - Configure read-only filesystem where possible

5. **Apply Environment-Specific Configurations**
   - Use build arguments for environment variables
   - Generate environment-specific Dockerfiles
   - Optimize for production vs development

6. **Generate Dockerfile**
   - Write multi-stage Dockerfile to `docker/Dockerfile`
   - Include build instructions
   - Document image purpose and version

7. **Validate Dockerfile**
   - Syntax check
   - Security scan
   - Build test (if possible)
   - Verify against spec requirements

8. **Output Artifacts**
   - `docker/Dockerfile` — Multi-stage Dockerfile
   - `docker/README.md` — Build instructions
   - `docker/build.sh` — Build automation script