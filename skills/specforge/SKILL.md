---
name: specforge
description: Specification and scenario analysis skill for test generation
trigger: during spec to implementation
---

# SpecForge Skill

## Overview
SpecForge is a specialized skill for transforming specifications and scenarios into comprehensive test suites. It bridges the gap between requirements documentation and executable tests.

## Trigger
- `specforge-overseer` during planning phases
- `specforge-validator` during coverage validation
- `specforge-generator` during test generation

## Step-by-Step Instructions

### 1. Existing Document Review
- Analyze MASTER_SPEC.md for hard gates and requirements
- Review SCENARIOS.md for edge cases and scenarios
- Identify testable contracts and invariants

### 2. Implementation Survey
- Examine codebase structure and architecture
- Identify modules, APIs, and state machines
- Document public interfaces and contracts

### 3. Intent Gap Analysis
- Compare implementation against specification intent
- Identify missing requirements or misinterpretations
- Document gaps between spec and implementation

### 4. Research Plan Generation
- Develop targeted research questions
- Plan investigation strategy for uncovered requirements
- Prioritize areas needing deeper analysis

### 5. Targeted Domain Research
- Investigate domain-specific constraints and patterns
- Analyze similar systems and best practices
- Gather domain knowledge for test design

### 6. Requirement Normalization
- Convert specifications into testable requirements
- Normalize scenario definitions
- Create unambiguous test criteria

### 7. Authority Boundary Definition
- Establish clear boundaries of system responsibility
- Define interfaces and integration points
- Document access control and permissions

### 8. Data Model Specification
- Document data structures and relationships
- Define validation rules and constraints
- Specify data lifecycle and transformations

### 9. Execution Flow Specification
- Map out system workflows and processes
- Define state transitions
- Document error handling paths

### 10. State Machine Specification
- Model system states and transitions
- Define valid state changes
- Document state invariants

### 11. API Contract Specification
- Document API endpoints and contracts
- Define request/response formats
- Specify error conditions and constraints

### 12. UI Behavior Specification
- Define user interaction patterns
- Document expected behaviors
- Specify accessibility requirements

### 13. Security Permission Specification
- Document security requirements and permissions
- Define authentication and authorization rules
- Specify security constraints

### 14. Observability Specification
- Define logging and monitoring requirements
- Document metrics and telemetry needs
- Specify alerting criteria

### 15. Error Handling Specification
- Document error conditions and handling strategies
- Define recovery mechanisms
- Specify error reporting requirements

### 16. Invariant Generation
- Extract system invariants from specifications
- Define consistency rules
- Create invariant tests

### 17. Hard Gate Definition
- Identify critical requirements that cannot be violated
- Define coverage thresholds
- Establish pass/fail criteria

### 18. Conflict Resolution Layer
- Detect and resolve requirement conflicts
- Handle ambiguous specifications
- Document resolution decisions

### 19. Scenario Matrix Generation
- Create comprehensive scenario coverage matrix
- Map scenarios to requirements
- Prioritize scenario execution

### 20. Kill Test Generation
- Generate tests from SCENARIOS.md edge cases
- Create failure mode tests
- Design boundary condition tests

## Best Practices
- Always validate against both MASTER_SPEC.md and SCENARIOS.md
- Generate tests that are atomic and independently executable
- Maintain traceability from tests to requirements
- Use existing test patterns in the codebase
- Prioritize tests based on risk and coverage impact