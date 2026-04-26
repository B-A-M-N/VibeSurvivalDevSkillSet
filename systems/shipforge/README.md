# ShipForge — Deployment & CI/CD System

## Description
ShipForge handles CI/CD wiring, Dockerfile generation, deployment checklists, and environment parity checks. It consumes the spec's security and observability sections to configure deployment automatically.

## How It Maps to Mistral-Vibe Table
| Mistral-Vibe Component | ShipForge Equivalent |
|------------------------|---------------------|
| Spec Parser | 00-spec-deployment-survey |
| Dockerfile Builder | 01-dockerfile-generation |
| CI/CD Pipeline Generator | 02-ci-pipeline-generation |
| Deployment Config Generator | 03-deployment-config-generation |
| Environment Drift Detector | 04-environment-parity-check |
| Security Validator | 05-security-hardening-check |
| Deployment Checklist Generator | 06-deployment-checklist-generation |
| Deploy Orchestrator | shipforge-overseer |
| Build System Writer | shipforge-builder |
| Deploy Config Writer | shipforge-deployer |

## Architecture Flow
```
Spec → survey → Dockerfile → CI pipeline → deploy checklist → parity check → ship
[00-spec-deployment-survey] → [01-dockerfile-generation] → [02-ci-pipeline-generation]
      ↓                          ↓                          ↓
[05-security-hardening-check]  [06-deployment-checklist-generation]
      ↓                                                    ↓
[04-environment-parity-check] ←─────────────────────────┘
      ↓
   Deploy
```

## Agents Table
| Agent | Role | Model | Max Turns |
|-------|------|-------|-----------|
| shipforge-overseer | Orchestrator | hy3 | 60 |
| shipforge-builder | Build system writer | devstral-2 | N/A |
| shipforge-deployer | Deploy config writer | hy3 | 40 |

## Install Bash Commands
```bash
# Navigate to the system directory
cd /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/systems/shipforge

# Install required packages (if any)
# apt-get update && apt-get install -y jq yq 2>/dev/null || true

# Set up permissions
chmod +x systems/shipforge/*.sh 2>/dev/null || true
```

## config.toml Snippet
```toml
[shipforge]
  debug = false
  output_dir = "/home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/artifacts"

[shipforge.agents]
  overseer.model = "hy3"
  overseer.max_turns = 60
  builder.model = "devstral-2"
  deployer.model = "hy3"
  deployer.max_turns = 40

[shipforge.spec_paths]
  master = "/path/to/MASTER_SPEC.md"
  security = "/path/to/security.md"
  observability = "/path/to/observability.md"
```

## Phases Table (7 Phases)
| Phase | Name | Agent | Primary Skill |
|-------|------|-------|---------------|
| 1 | Spec Survey | shipforge-overseer | 00-spec-deployment-survey |
| 2 | Dockerfile Generation | shipforge-builder | 01-dockerfile-generation |
| 3 | CI Pipeline Generation | shipforge-builder | 02-ci-pipeline-generation |
| 4 | Deployment Config Generation | shipforge-deployer | 03-deployment-config-generation |
| 5 | Environment Parity Check | shipforge-deployer | 04-environment-parity-check |
| 6 | Security Hardening Check | shipforge-deployer | 05-security-hardening-check |
| 7 | Deployment Checklist Generation | shipforge-deployer | 06-deployment-checklist-generation |

## Core Doctrine
1. **Spec-Driven**: All configurations are generated from the master spec, with security and observability as primary inputs.
2. **Environment Parity**: Ensure dev, staging, and prod environments are consistent through automated checks.
3. **Minimal Docker Images**: Multi-stage builds with minimal base images for security and performance.
4. **CI/CD as Code**: Pipeline configurations are generated and version-controlled alongside application code.
5. **Declarative Deployments**: Use declarative configs (Kubernetes, docker-compose) for reproducible deployments.

## Output Artifacts
- `docker/Dockerfile` — Multi-stage Dockerfile
- `.github/workflows/deploy.yml` — GitHub Actions CI/CD pipeline
- `k8s/deployment.yaml` — Kubernetes deployment manifest
- `k8s/service.yaml` — Kubernetes service manifest
- `deploy/checklist.md` — Pre/post-deployment checklist
- `deploy/playbook.md` — Deployment runbook
- `env/parity-report.md` — Environment parity check results