---
name: 02-ci-pipeline-generation
description: Generate CI config (GitHub Actions, etc.) from build/test/deploy steps
trigger: when CI/CD workflows need to be created based on build and deployment requirements
---

# 02-CI Pipeline Generation

## Trigger
When CI/CD workflows need to be created based on build and deployment requirements.

## Step-by-Step Instructions

1. **Analyze Build Requirements**
   - Review Dockerfile build process
   - Identify build stages and dependencies
   - Determine test requirements

2. **Design Pipeline Stages**
   - Stage 1: Checkout and Setup
     - Clone repository
     - Install dependencies
   - Stage 2: Build
     - Compile code
     - Create Docker images
   - Stage 3: Test
     - Unit tests
     - Integration tests
     - Security scans
   - Stage 4: Deploy to Staging
     - Apply deployment configs
     - Run integration tests
   - Stage 5: Parity Check
     - Verify environment consistency
     - Validate configurations
   - Stage 6: Deploy to Production
     - Conditional deployment
     - Manual approval required

3. **Configure Pipeline Triggers**
   - On push to main branch
   - On pull request merge
   - On scheduled intervals (for maintenance)
   - Manual trigger option

4. **Implement Environment-Specific Configs**
   - Create separate workflows for each environment
   - Use environment variables for configuration
   - Implement approval gates for production

5. **Add Security Scanning**
   - Integrate vulnerability scanning
   - Implement dependency checks
   - Add compliance validation

6. **Generate CI Configuration Files**
   - Create `.github/workflows/deploy.yml`
   - Configure jobs and steps
   - Set up secrets management

7. **Validate Pipeline Configuration**
   - Syntax check
   - Test pipeline structure
   - Verify stage dependencies
   - Ensure proper error handling

8. **Output Artifacts**
   - `.github/workflows/deploy.yml` — GitHub Actions pipeline
   - `.gitlab-ci.yml` — GitLab CI (if applicable)
   - `ci/pipeline-config.yaml` — Pipeline configuration