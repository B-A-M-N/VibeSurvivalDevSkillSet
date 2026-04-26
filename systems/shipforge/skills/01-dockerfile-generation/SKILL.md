---
name: dockerfile-generation
description: Generate multi-stage Dockerfile
trigger: "DEPLOYMENT_REQUIREMENTS.md ready"
---

## Step-by-Step Instructions

1. **Read Requirements**
   - Use `read_file` to read `deploy/DEPLOYMENT_REQUIREMENTS.md`
   - Note: base image needed (Python, Node, Go, etc.)
   - Note: runtime version, system dependencies
   - Check MASTER_SPEC.md for any special build requirements

2. **Choose Base Image**
   - Select minimal base: `python:3.11-slim`, `node:20-alpine`, `golang:1.21-alpine`
   - Prefer `-alpine` or `-slim` variants for smaller images
   - Use specific version tags (not `latest`) for reproducibility

3. **Design Multi-Stage Build**
   - Stage 1 (`builder`): all build tools, compilations, dependency installation
     - Copy dependency files (`requirements.txt`, `package.json`, `go.mod`)
     - Install dependencies
     - Copy source code
     - Run build commands (compile, bundle, etc.)
   - Stage 2 (`runtime`): only runtime dependencies
     - Copy artifacts from `builder` stage using `COPY --from=builder`
     - Do NOT copy build tools or source unnecessarily

4. **Configure Non-Root User**
   - Add group and user: `RUN addgroup -S appgroup && adduser -S -G appgroup appuser`
   - Switch: `USER appuser`
   - Ensure files have correct ownership: `RUN chown -R appuser:appgroup /app`

5. **Add Healthcheck**
   - Use `HEALTHCHECK` instruction:
     ```dockerfile
     HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
       CMD curl -f <http://localhost:8080/health> || exit 1
     ```
   - Match the health endpoint from MASTER_SPEC.md Observability section
   - Set appropriate interval and timeout based on service startup time

6. **Set Environment Variables**
   - Use `ENV` for non-sensitive defaults
   - Document sensitive vars: `# Set at runtime: DATABASE_URL, SECRET_KEY`
   - Do NOT put secrets in Dockerfile (use runtime env or secrets management)

7. **Optimize Layers**
   - Order: dependency installation BEFORE copying source (better caching)
   - Combine RUN commands: `RUN apt-get update && apt-get install -y pkg1 pkg2 && rm -rf /var/lib/apt/lists/*`
   - Clean up in same layer: don't leave build artifacts

8. **Generate Dockerfile**
   - Use `write_file` to create `Dockerfile` in project root
   - Include comments explaining each section
   - Set `EXPOSE` for documented ports
   - Set proper `WORKDIR` (e.g., `/app`)
   - Set `CMD` or `ENTRYPOINT` matching MASTER_SPEC.md startup command

9. **Validate**
   - Use `bash` to test build: `docker build -t test-image .`
   - Check image size: `docker images test-image`
   - Verify non-root: `docker run --rm test-image whoami`
   - Verify healthcheck: `docker run --rm test-image curl -f <http://localhost:8080/health>`
