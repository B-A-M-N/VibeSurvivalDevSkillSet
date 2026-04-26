---
name: spec-deployment-survey
description: Parse MASTER_SPEC.md for deployment requirements
trigger: "MASTER_SPEC.md updated or /shipforge"
---

## Step-by-Step Instructions

1. **Read MASTER_SPEC.md**
   - Use `read_file` to read the full MASTER_SPEC.md
   - Locate sections: Security, Observability, Deployment, Environment, Dependencies
   - Note the overall architecture (monolith, microservices, serverless)

2. **Extract Environment Requirements**
   - Parse for: OS, runtime version, language version
   - Extract: port numbers, volume mounts, environment variables
   - Note: which ports are internal vs exposed
   - Build table: `| Service | Port | Purpose | Internal/External |`

3. **Extract Security Requirements**
   - Use `read_file` to read Security section of MASTER_SPEC.md
   - Note: authentication method (JWT, OAuth, API key, etc.)
   - Note: encryption requirements (at rest, in transit)
   - Note: secret management (env vars, vault, config maps)
   - Note: CORS, rate limiting, IP whitelisting

4. **Extract Observability Requirements**
   - Note: logging format (JSON, text), destination (stdout, file, service)
   - Note: metrics collection (Prometheus, StatsD, custom)
   - Note: tracing requirements (OpenTelemetry, etc.)
   - Note: health check endpoints and expected responses

5. **Extract Resource Requirements**
   - CPU: requests and limits per service
   - Memory: requests and limits per service
   - Storage: type (SSD, HDD), size, mount paths
   - Replicas: minimum and maximum per service

6. **Extract Dependency Services**
   - Databases: type, version, connection strings format
   - Message queues: type, version, queue names
   - External APIs: base URLs, auth methods
   - Caches: type (Redis, Memcached), eviction policies

7. **Generate DEPLOYMENT_REQUIREMENTS.md**
   - Use `write_file` to create `deploy/DEPLOYMENT_REQUIREMENTS.md`
   - Structure:
     ```markdown
     # Deployment Requirements
     ## Environment
     | Variable | Value | Source (spec section) |
     ## Ports
     | Service | Port | Internal/External | Purpose |
     ## Security
     - Auth: ...
     - Encryption: ...
     ## Resources
     | Service | CPU | Memory | Replicas |
     ## Dependencies
     | Service | Type | Version | Connection |
     ```
   - Include cross-references to MASTER_SPEC.md section numbers

8. **Validate**
   - Use `read_file` to re-read DEPLOYMENT_REQUIREMENTS.md
   - Verify: all sections from spec are covered?
   - Check: are all ports, volumes, secrets documented?
   - Flag: any spec section that references deployment but isn't captured
