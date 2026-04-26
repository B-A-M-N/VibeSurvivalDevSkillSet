---
name: specforge-22-final-spec-assembly
description: |
  SpecForge — Final Spec Assembly. Combines all spec parts and
  scenarios into the authoritative specification document.
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Bash
  - Write
---

# SpecForge: Final Spec Assembly

**Role:** `spec-architect` + `scenario-engineer` — Final Assembly

## Mission

Combine all spec parts, scenarios, and review findings into the final authoritative specification. This is the contract that drives implementation.

## When to Use

- After Phase7 Adversarial Review passes (or issues are fixed)
- When MASTER_SPEC.md and SCENARIOS.md are complete and reviewed
- Before handing off to implementation team

## Final Document Structure

```
MASTER_SPEC.md
==============

PART 0 — System Contract
  - Mission statement
  - Authority boundaries
  - Non-goals

PART 1 — Goals and Non-Goals
  - What we are building
  - What we are explicitly NOT building

PART 2 — User Roles
  - Role definitions
  - Role permissions (reference to PART 6)

PART 3 — Canonical Execution Model
  - Execution flows
  - Operation ordering
  - Pre/post conditions

PART 4 — Data Models
  - Entities and fields
  - Types and constraints
  - Relationships

PART 5 — State Machines
  - States and transitions
  - Guards and side effects
  - Invalid transition handling

PART 6 — Permissions and Authority Boundaries
  - Role-based permissions
  - Resource access rules
  - Security model

PART 7 — API / Interface Contracts
  - Endpoints
  - Request/response schemas
  - Error responses
  - Rate limits

PART 8 — UI / UX Behavioral Rules
  - Component behavior
  - State-driven UI
  - Validation feedback

PART 9 — Storage and Persistence
  - Storage strategy
  - Data lifetime
  - Backup/recovery

PART 10 — Error Handling
  - Error definitions
  - Recovery strategies
  - User-facing messages

PART 11 — Observability
  - Logging strategy
  - Metrics and SLOs
  - Tracing and alerting

PART 12 — Invariants
  - System-wide invariants
  - Enforcement points
  - Violation responses

PART 13 — Hard Gates
  - Deployment blockers
  - Runtime gates
  - Violation responses

PART 14 — Conflict Resolution
  - Competing rule resolution
  - Priority scheme
  - Tie-breakers

PART 15 — Version / Phase Roadmap
  - Implementation phases
  - Version compatibility
  - Migration paths

PART 16 — Conformance Requirements
  - What "compliant" means
  - Test coverage requirements
  - Audit criteria

SCENARIOS.md
===========

[All scenarios: happy paths, kill tests, edge cases, etc.]

APPENDIX
========

- NORMALIZED_REQUIREMENTS.md (reference)
- RESEARCH_FINDINGS.md (reference)
- ADVERSARIAL_REVIEW.md (reference)
```

## Assembly Instructions

1. **Gather All Parts**: Read every PART file or section created by previous skills.
2. **Assemble MASTER_SPEC.md**: Combine all PARTs in order. Ensure cross-references work.
3. **Assemble SCENARIOS.md**: Combine all scenarios. Verify each has an ID, links to invariants, and clear oracle.
4. **Run Consistency Check**: Verify all REQ-IDs, INV-IDs, SCN-IDs are unique and referenced.
5. **Write Final Files**: Output `MASTER_SPEC.md` and `SCENARIOS.md` in the project root or `spec/` directory.

## Output

- `MASTER_SPEC.md` — The authoritative specification
- `SCENARIOS.md` — The exhaustive scenario sheet

**The spec is the contract. Assembly is final. Make it authoritative.**
