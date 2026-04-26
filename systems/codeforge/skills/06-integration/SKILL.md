---
name: integration
description: Wire components together, connect APIs, ensure cross-module compatibility
trigger: need to integrate multiple components into working system
---

## Step-by-Step Instructions

### 1. Interface Analysis
- Document all module interfaces and APIs
- Extract input/output specifications
- Note data formats and protocols
- Identify integration points and touchpoints

### 2. Dependency Management
- Map module dependencies and relationships
- Document initialization order and dependencies
- Extract shared service requirements
- Note circular dependency risks

### 3. Connection Planning
- Plan how modules will communicate
- Document message formats and protocols
- Extract error handling and retry strategies
- Note monitoring and logging requirements

### 4. Integration Testing Strategy
- Create integration test plans for each connection
- Document expected behavior at integration points
- Prepare test cases for failure scenarios
- Plan for gradual integration vs. big bang

### 5. Cross-Module Validation
- Verify data consistency across modules
- Check API compatibility between modules
- Document data transformation requirements
- Ensure protocol compliance

### 6. Configuration Management
- Document configuration requirements per module
- Extract environment-specific settings
- Note secrets and credential management
- Plan for configuration validation

### 7. Integration Implementation
- Implement connections following documented patterns
- Apply error handling and resilience patterns
- Monitor integration health and performance
- Log integration events and metrics

### 8. Integration Verification
- Run comprehensive integration tests
- Verify all integration points work correctly
- Check performance and reliability
- Prepare integration handoff documentation