# SpecForge — System Implementation

## Overview

SpecForge turns vague product intent into enforceable application contracts and scenario sheets. It coordinates 23 pipeline skill packages across 3 agents to transform intent into a complete specification with scenarios and kill tests.

## Agents

| Agent | TOML | Prompt | Role |
|-------|------|--------|------|
| `specforge-overseer` | `agents/specforge-overseer.toml` | `prompts/specforge-overseer.md` | Orchestrates full spec pipeline |
| `specforge-analyst` | `agents/specforge-analyst.toml` | `prompts/specforge-analyst.md` | Surveys existing docs/code and performs research |
| `specforge-architect` | `agents/specforge-architect.toml` | `prompts/specforge-architect.md` | Constructs specs, scenarios, and kill tests |

## Skill Packages

Each skill is a directory under `skills/` with `SKILL.md` as the entrypoint. These are pipeline-tier skills that execute sequentially to produce the master specification.

| # | Skill Package | Assigned Agent | Purpose |
|---|----------------|----------------|---------|
| 00 | `00-intake-goal-clarification` | overseer | Clarifies user intent and goals |
| 01 | `01-existing-document-review` | analyst | Reviews existing documentation |
| 02 | `02-implementation-survey` | analyst | Surveys current implementation |
| 03 | `03-intent-gap-analysis` | analyst + overseer | Finds gaps between intent and evidence |
| 04 | `04-research-plan-generation` | analyst + overseer | Plans targeted research |
| 05 | `05-targeted-domain-research` | analyst | Researches domain-specific patterns |
| 06 | `06-requirement-normalization` | architect | Normalizes requirements to canonical form |
| 07 | `07-authority-boundary-definition` | architect | Defines what the system can/cannot do |
| 08 | `08-data-model-specification` | architect | Specifies data models and schemas |
| 09 | `09-execution-flow-specification` | architect | Specifies execution flows |
| 10 | `10-state-machine-specification` | architect | Specifies state machines |
| 11 | `11-api-contract-specification` | architect | Specifies API contracts |
| 12 | `12-ui-behavior-specification` | architect | Specifies UI behavior |
| 13 | `13-security-permission-specification` | architect | Specifies security and permissions |
| 14 | `14-observability-specification` | architect | Specifies observability and logging |
| 15 | `15-error-handling-specification` | architect | Specifies error handling |
| 16 | `16-invariant-generation` | architect | Generates system invariants |
| 17 | `17-hard-gate-definition` | architect | Defines hard gates and constraints |
| 18 | `18-conflict-resolution-layer` | architect | Resolves conflicting requirements |
| 19 | `19-scenario-matrix-generation` | architect | Generates exhaustive scenarios |
| 20 | `20-kill-test-generation` | architect | Generates kill tests (failure cases) |
| 21 | `21-adversarial-spec-review` | overseer | Adversarial review of spec |
| 22 | `22-final-spec-assembly` | architect + overseer | Assembles final MASTER_SPEC |

## Agent Skill Mapping

```
specforge-overseer
├── 00-intake-goal-clarification
├── 03-intent-gap-analysis
├── 04-research-plan-generation
├── 21-adversarial-spec-review
└── 22-final-spec-assembly

specforge-analyst
├── 01-existing-document-review
├── 02-implementation-survey
├── 03-intent-gap-analysis
├── 04-research-plan-generation
└── 05-targeted-domain-research

specforge-architect
├── 06-requirement-normalization
├── 07-authority-boundary-definition
├── 08-data-model-specification
├── 09-execution-flow-specification
├── 10-state-machine-specification
├── 11-api-contract-specification
├── 12-ui-behavior-specification
├── 13-security-permission-specification
├── 14-observability-specification
├── 15-error-handling-specification
├── 16-invariant-generation
├── 17-hard-gate-definition
├── 18-conflict-resolution-layer
├── 19-scenario-matrix-generation
├── 20-kill-test-generation
└── 22-final-spec-assembly
```

## Execution Flow

### Phase 1: Intake
```
specforge-overseer
  → 00-intake-goal-clarification: Clarify intent and goals
  → Output: INTENT_LEDGER.md
```

### Phase 2: Evidence Review
```
specforge-overseer
  → task(agent="specforge-analyst", ...)
    → 01-existing-document-review: Review docs
    → 02-implementation-survey: Survey codebase
  → Output: IMPLEMENTATION_EVIDENCE_MAP.md
```

### Phase 3: Gap Analysis
```
specforge-overseer
  → 03-intent-gap-analysis: Compare intent vs evidence
  → Output: SPEC_GAP_REPORT.md
```

### Phase 4: Targeted Research
```
specforge-overseer
  → task(agent="specforge-analyst", ...)
    → 04-research-plan-generation: Plan research
    → 05-targeted-domain-research: Research domain patterns
  → Output: RESEARCH_FINDINGS.md
```

### Phase 5: Spec Construction
```
specforge-overseer
  → task(agent="specforge-architect", ...)
    → 06-requirement-normalization
    → 07-authority-boundary-definition
    → 08-data-model-specification
    → 09-execution-flow-specification
    → 10-state-machine-specification
    → 11-api-contract-specification
    → 12-ui-behavior-specification
    → 13-security-permission-specification
    → 14-observability-specification
    → 15-error-handling-specification
    → 16-invariant-generation
    → 17-hard-gate-definition
    → 18-conflict-resolution-layer
  → Output: MASTER_SPEC.md (16 PARTs)
```

### Phase 6: Scenario Generation
```
specforge-overseer
  → task(agent="specforge-architect", ...)
    → 19-scenario-matrix-generation: Happy paths, edge cases
    → 20-kill-test-generation: Failure cases, permission violations
  → Output: SCENARIOS.md
```

### Phase 7: Adversarial Review
```
specforge-overseer
  → 21-adversarial-spec-review: Challenge assumptions
  → REJECT if spec is weak
  → Output: ADVERSARIAL_REVIEW.md
```

### Phase 8: Final Assembly
```
specforge-overseer
  → 22-final-spec-assembly: Combine all parts
  → Output: Final MASTER_SPEC.md + SCENARIOS.md
```

## Output Artifacts

| Artifact | Purpose |
|----------|---------|
| `INTENT_LEDGER.md` | Clarified user intent and goals |
| `IMPLEMENTATION_EVIDENCE_MAP.md` | Existing docs and code survey |
| `SPEC_GAP_REPORT.md` | Gaps between intent and evidence |
| `RESEARCH_FINDINGS.md` | Domain research results |
| `MASTER_SPEC.md` | 16 PARTs: contract, goals, roles, data models, state machines, API, UI, security, observability, invariants, hard gates, conflict resolution, conformance |
| `SCENARIOS.md` | Exhaustive scenarios: kill tests, happy paths, edge cases, permission failures, API violations |
| `ADVERSARIAL_REVIEW.md` | Challenge results and verdict |

## MASTER_SPEC.md Structure (16 PARTs)

```
PART 1:  Contract & Scope
PART 2:  Goals & Non-Goals
PART 3:  Roles & Actors
PART 4:  Data Models & Schemas
PART 5:  State Machines
PART 6:  API Contracts
PART 7:  UI Behavior
PART 8:  Security & Permissions
PART 9:  Observability & Logging
PART 10: Error Handling
PART 11: Invariants
PART 12: Hard Gates
PART 13: Conflict Resolution
PART 14: Conformance Criteria
PART 15: Scenario Matrix (reference)
PART 16: Kill Test Suite (reference)
```

## Core Doctrine

```
Intent is normative.           (user intent drives everything)
Research is advisory.           (findings inform, don't dictate)
Implementation is evidence.       (existing code is descriptive, not truth)
The spec is authoritative.        (only after adversarial review)
```
