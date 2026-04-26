---
name: ci-pipeline-generation
description: Generate CI config
trigger: "Dockerfile ready"
---

## Step-by-Step Instructions

1. **Read Context**
   - Use `read_file` to read `deploy/DEPLOYMENT_REQUIREMENTS.md`
   - Use `read_file` to read Dockerfile (if exists)
   - Note: test commands, build commands, deployment targets
   - Check MASTER_SPEC.md for CI/CD requirements

2. **Choose CI Platform**
   - Default: GitHub Actions (`.github/workflows/`)
   - Alternative: GitLab CI (`.gitlab-ci.yml`)
   - Alternative: CircleCI (`.circleci/config.yml`)
   - Match whatever the repo already uses (check with `bash`: `ls -la .github .gitlab-ci.yml .circleci 2>/dev/null`)

3. **Define Pipeline Stages**
   - Stage 1: `lint` — code quality checks
     - Python: `flake8`, `pylint`, or `ruff`
     - Node: `eslint`, `prettier`
   - Stage 2: `test` — run test suite
     - Use `bash`: `pytest --covr=src --covr-report=term-missing`
     - Upload coverage: `codecov` or `coverage` action
   - Stage 3: `build` — build Docker image
     - Use `docker/build-push-action` for GitHub Actions
     - Tag: `type/date-time` or `{{github.sha}}`
   - Stage 4: `scan` — security scanning
     - Use `aquasecurity/trivy-action` for image scanning
     - Scan for CVEs in dependencies
   - Stage 5: `deploy` — deploy to target environment
     - Only on `main`/`master` branch or tagged releases
     - Use environment-specific secrets

4. **Configure Matrix Builds (if needed)**
   - Multiple OS: `ubuntu-latest`, `windows-latest`, `macos-latest`
   - Multiple versions: `python: ["3.9", "3.10", "3.11"]`
   - Use `strategy.matrix` in GitHub Actions

5. **Add Security Scanning**
   - Dependency scanning: `ossf/scorecard-action` or `snyk/actions-docker`
   - Secret scanning: `trufflesecurity/trufflehog` or `gitleaks/gitleaks-action`
   - SAST: `github/codeql-action` for code analysis
   - Generate security report artifact

6. **Configure Artifacts**
   - Store build logs: `actions/upload-artifact`
   - Store test results: JUnit XML, coverage reports
   - Store Docker images: only on successful build

7. **Set Up Notifications**
   - On failure: notify via Slack, email, or GitHub issues
   - On success: optional notification
   - Use secrets for webhook URLs

8. **Generate Workflow File**
   - Use `write_file` to create `.github/workflows/ci.yml`
   - Structure:
     ```yaml
     name: CI/CD Pipeline
     on: [push, pull_request]
     jobs:
       lint: ...
       test: ...
       build: ...
       scan: ...
       deploy:
         if: github.ref == 'refs/heads/main'
     ```
   - Use `${{ secrets.NAME }}` for all credentials
   - Set `timeout-minutes: 30` per job

9. **Validate**
   - Use `bash` to check YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`
   - Verify: are all stages covered?
   - Check: are secrets referenced but not hardcoded?
   - Test dry-run if GitHub CLI available: `gh workflow run ci.yml`
