---
name: spec-ingest
description: Parse MASTER_SPEC.md, extract contracts, data models, API specs, state machines, invariants, hard gates
trigger: parse master specification and extract all technical requirements
---

## Step-by-Step Instructions

### 1. Read MASTER_SPEC.md Completely
- Load and read the entire MASTER_SPEC.md file
- Identify the document structure and sections
- Note the file encoding and formatting

### 2. Extract Contracts
- Find all service contracts and agreements
- Document contract parties, terms, and obligations
- Identify any API-level contracts or SLAs

### 3. Extract Data Models
- Identify all data structures and schemas
- Document fields, types, constraints, and relationships
- Note required vs optional fields
- Extract validation rules

### 4. Extract API Specifications
- Document all API endpoints, methods, and parameters
- Extract request/response schemas
- Note authentication and authorization requirements
- Document rate limits and quotas

### 5. Identify State Machines
- Find all stateful processes and workflows
- Document states, transitions, and triggers
- Note business rules governing transitions
- Identify initial and terminal states

### 6. Extract Invariants
- Identify constraints that must always hold
- Document business rules and validation requirements
- Note cross-field and cross-entity constraints
- Extract timing and sequencing requirements

### 7. Identify Hard Gates
- Find critical milestones and deadlines
- Document blocking dependencies
- Identify integration points with external systems
- Note regulatory or compliance requirements

### 8. Output Structured Data
- Create structured representation of all extracted information
- Use consistent naming and categorization
- Ensure no information loss during extraction
- Prepare for downstream processing by other agents