---
name: deployment-config-generation
description: Generate k8s/docker-compose configs
trigger: "CI pipeline ready"
---

## Step-by-Step Instructions

1. **Read Requirements**
   - Use `read_file` to read `deploy/DEPLOYMENT_REQUIREMENTS.md`
   - Note: target platform (Kubernetes, Docker Compose, ECS, etc.)
   - Check MASTER_SPEC.md for deployment architecture (single service vs microservices)

2. **For Kubernetes Deployments:**
   a. **Generate Deployment Manifests**
      - Use `write_file` to create `deploy/k8s/<service>-deployment.yaml`
      - Include: `apiVersion: apps/v1`, `kind: Deployment`
      - Set: `metadata.name`, `spec.replicas`, `spec.selector`
      - Configure: `containers[].name`, `image`, `ports[]`
      - Add: `resources.requests` and `resources.limits` (CPU/memory)
      - Set: `imagePullPolicy: Always` or `IfNotPresent`

   b. **Add Health Probes**
      - Liveness: `httpGet.path: /health`, `httpGet.port: 8080`
      - Readiness: same or different endpoint based on MASTER_SPEC.md
      - Set `initialDelaySeconds: 30`, `periodSeconds: 10`

   c. **Generate Service Manifests**
      - Use `write_file` to create `deploy/k8s/<service>-service.yaml`
      - Set: `type: ClusterIP` (internal) or `LoadBalancer` (external)
      - Map: `ports[].port` → `targetPort`

   d. **Add ConfigMaps and Secrets**
      - Use `write_file` to create `deploy/k8s/configmap.yaml`
      - Store non-sensitive env vars
      - Use `write_file` to create `deploy/k8s/secrets.yaml`
      - Store sensitive data (use `stringData` for readability during generation)

   e. **Generate Ingress (if external)**
      - Create `deploy/k8s/ingress.yaml`
      - Set: `rules[].host`, `paths[].backend.serviceName`
      - Configure TLS if MASTER_SPEC.md requires encryption in transit

3. **For Docker Compose Deployments:**
   a. **Generate docker-compose.yml**
      - Use `write_file` to create `docker-compose.yml`
      - Define services matching DEPLOYMENT_REQUIREMENTS.md
      - Set: `image`, `ports`, `volumes`, `environment`
      - Configure: `depends_on`, `restart: unless-stopped`

   b. **Add Volume Mounts**
      - Define named volumes: `volumes:` section
      - Map: `volumes: [].path: /data` in service definition

   c. **Configure Networks (if multi-service)**
      - Define custom network: `networks: app-net: driver: bridge`
      - Assign each service to the network

4. **Set Resource Limits (Both Platforms)**
   - CPU: requests (guaranteed), limits (ceiling)
   - Memory: requests and limits in MiB
   - Replicas: minimum for HA (≥2 for production)

5. **Add Environment Variables**
   - Use `read_file` to read service code for required env vars
   - Set non-sensitive defaults in config
   - Document sensitive vars: `# Set at runtime: DATABASE_URL`
   - Never put actual secrets in config files

6. **Validate Manifests**
   - For K8s: use `bash`: `kubectl apply --dry-run=client -f deploy/k8s/`
   - For Compose: use `bash`: `docker-compose config`
   - Check: are all ports, volumes, env vars covered?
   - Verify: do resource limits match DEPLOYMENT_REQUIREMENTS.md?
