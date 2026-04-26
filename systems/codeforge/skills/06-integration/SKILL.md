---
name: integration
description: Wire components together, connect APIs, ensure cross-module compatibility
---

## Steps to Wire Components and Ensure Integration

1. **Interface Analysis**
   - Document all module interfaces and APIs with full signatures
   - Extract input/output specifications (schemas, types, formats)
   - Note data formats and protocols (REST, gRPC, message queues)
   - Identify integration points and touchpoints with spec mappings

2. **Dependency Management**
   - Map module dependencies and relationships (dependency graph)
   - Document initialization order and dependencies (topological sort)
   - Extract shared service requirements (databases, caches, message brokers)
   - Note circular dependency risks and mitigation strategies

3. **Connection Planning**
   - Plan how modules will communicate (sync vs async, protocols)
   - Document message formats and protocols (JSON schema, Protobuf)
   - Extract error handling and retry strategies (backoff, circuit breakers)
   - Note monitoring and logging requirements (metrics, tracing)

4. **Integration Testing Strategy**
   - Create integration test plans for each connection (contract tests)
   - Document expected behavior at integration points (happy path, edge cases)
   - Prepare test cases for failure scenarios (network, timeout, data corruption)
   - Plan for gradual integration (canary, blue-green) vs. big bang

5. **Cross-Module Validation**
   - Verify data consistency across modules (eventual vs strong consistency)
   - Check API compatibility between modules (versioning, backward compat)
   - Document data transformation requirements (mapping, enrichment)
   - Ensure protocol compliance (HTTP standards, message formats)

6. **Configuration Management**
   - Document configuration requirements per module (env vars, config files)
   - Extract environment-specific settings (dev, staging, prod)
   - Note secrets and credential management (vault, encrypted env vars)
   - Plan for configuration validation (schema validation, required fields)

7. **Integration Implementation**
   - Implement connections following documented patterns (adapter, facade)
   - Apply error handling and resilience patterns (retry, fallback)
   - Monitor integration health and performance (latency, error rates)
   - Log integration events and metrics (structured logging, correlation IDs)

8. **Integration Verification**
   - Run comprehensive integration tests (end-to-end scenarios)
   - Verify all integration points work correctly (contract compliance)
   - Check performance and reliability (SLA verification)
   - Prepare integration handoff documentation (runbooks, monitoring dashboards)

## Integration Checkpoints

- **Phase 1**: Unit tests pass with invariants enforced
- **Phase 2**: Component integration tests pass
- **Phase 3**: End-to-end integration tests pass
- **Phase 4**: Performance and load tests pass
- **Phase 5**: Security and compliance checks pass
- **Phase 6**: Production readiness review