---
name: implementation-planning
description: Build ordered implementation plan with dependencies, file targets, and verification criteria
---

## Steps to Build Implementation Plan

1. **Priority Assessment**
   - Rank spec requirements by criticality and dependencies
   - Identify must-have vs nice-to-have features
   - Determine blocking relationships between requirements
   - Set phase-based priorities (Phase 1: core, Phase 2: enhancements, Phase 3: polish)

2. **Dependency Mapping**
   - Document all dependencies between requirements
   - Identify which features depend on others
   - Note integration points and shared components
   - Extract prerequisite requirements with explicit ordering

3. **File Target Identification**
   - Map each requirement to specific files that need changes/creation
   - Identify new files needed for each feature with full paths
   - Document modification requirements for existing files
   - Note configuration and resource files (YAML, JSON, env files)

4. **Implementation Sequencing**
   - Create ordered list of implementation tasks with dependencies
   - Group related tasks into logical phases
   - Ensure prerequisites are completed before dependent tasks
   - Plan for parallelizable work where possible (independent modules)

5. **Verification Criteria Definition**
   - Define acceptance criteria for each implementation task
   - Specify test cases and validation methods (unit, integration, contract)
   - Document invariants that must be maintained after each change
   - Set performance and quality thresholds (latency, memory, throughput)

6. **Risk Assessment**
   - Identify potential implementation challenges (legacy constraints, tech debt)
   - Document technical debt and future considerations
   - Plan for edge cases and error handling scenarios
   - Note rollback or recovery strategies for failed deployments

7. **Resource Estimation**
   - Estimate effort for each task (hours/days)
   - Identify required skills and tools (language-specific, frameworks)
   - Note external dependencies and constraints (APIs, third-party services)
   - Plan for review and testing phases (code review, QA, UAT)

8. **Plan Documentation**
   - Create detailed implementation plan document (IMPLEMENTATION_PLAN.md)
   - Include timeline, milestones, and deliverables with dates
   - Document decision points and approval gates
   - Prepare handoff materials for implementation agents and validators

## Output: IMPLEMENTATION_PLAN.md

The output `IMPLEMENTATION_PLAN.md` should contain:
- Executive summary with scope and timeline
- Phase breakdown with dependencies and ordering
- File change matrix (requirement → files)
- Task checklist with owners and deadlines
- Verification criteria per phase
- Risk register and mitigation plans
- Rollout strategy and rollback plan