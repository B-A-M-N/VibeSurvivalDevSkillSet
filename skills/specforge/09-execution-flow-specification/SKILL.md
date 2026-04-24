---
name: specforge-09-execution-flow-specification
description: |
  SpecForge — Execution Flow Specification. Defines canonical execution model,
  operation ordering, and control flow with deterministic rules.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# SpecForge: Execution Flow Specification

**Role:** `spec-architect` — PART 3

## Mission

Define the canonical execution model. What happens when, in what order, with what prerequisites, and what are the deterministic rules governing flow.

## When to Use

- Building PART 3 — Canonical Execution Model
- After data models and authority boundaries are defined
- Before state machines (which are a subset of execution flow)

## Flow Template

```
FLOW: [FlowName]
TRIGGER: [what starts this flow]
PREREQUISITES:
  - [condition 1]
  - [condition 2]

STEPS:
  1. [action] -> [next step | END]
     precondition: [must be true]
     postcondition: [becomes true]
     failure_path: [where to go on failure]

  2. [action] -> [next step | END]
     ...

INVARIANTS_MAINTAINED:
  - [invariant that must hold during this flow]

CONCURRENT_OPERATIONS:
  - [operations that can happen in parallel during this flow]
```

## Instructions

1. **Read Requirements**: Find all workflow/process requirements in NORMALIZED_REQUIREMENTS.md.
2. **Map Flows**: One FLOW block per distinct operation sequence.
3. **Define Steps**: Each step is atomic. One verb, one target.
4. **Pre/Post Conditions**: Every step has them. No exceptions.
5. **Failure Paths**: Where does execution go on failure? Must be explicit.
6. **Write Output**: PART 3 section for `MASTER_SPEC.md`.

## Output

PART 3 section content for `MASTER_SPEC.md`.

**Execution without defined flow is guessing. Specify or fail.**
