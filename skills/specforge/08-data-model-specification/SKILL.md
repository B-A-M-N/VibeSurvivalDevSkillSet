---
name: specforge-08-data-model-specification
description: |
  SpecForge — Data Model Specification. Defines canonical data models,
  types, relationships, constraints, and persistence rules.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# SpecForge: Data Model Specification

**Role:** `spec-architect` — PART 4

## Mission

Define the canonical data models. Every field, type, constraint, relationship, and persistence rule. No "TBD" types. No vague "object" definitions.

## When to Use

- Building PART 4 — Data Models
- After requirements and authority boundaries are defined
- When storage strategy is being decided

## Model Template

```
MODEL: [EntityName]
DESCRIPTION: [what this represents]

FIELDS:
  - name: [field_name]
    type: [primitive | reference | enum]
    required: true | false
    constraints: [unique, min, max, pattern, etc.]
    default: [value or NULL]
    source: [requirement ID or research finding]

RELATIONSHIPS:
  - to: [OtherEntity]
    type: one-to-one | one-to-many | many-to-many
    via: [foreign key or join table]
    constraint: [cascade, restrict, set null]

PERSISTENCE:
  storage: [database | file | cache | session]
  lifetime: [permanent | session | TTL]
  indexing: [fields that must be indexed]
```

## Instructions

1. **Read Requirements**: Extract all data-related requirements from NORMALIZED_REQUIREMENTS.md.
2. **Define Entities**: One model per entity. No "User + all their data" — break it down.
3. **Type Everything**: String, Int, Boolean, Enum, Reference. No "any" or "object".
4. **Constrain**: Every field has constraints (required, unique, range, pattern).
5. **Relationship Map**: How entities connect. Cardinality must be explicit.
6. **Write Output**: PART 4 section for `MASTER_SPEC.md`.

## Output

PART 4 section content for `MASTER_SPEC.md`.

**Data models are the skeleton. Make them unbreakable.**
