---
name: specforge-07-authority-boundary-definition
description: |
  SpecForge — Authority Boundary Definition. Defines what the system
  is authorized to do, what it must never do, and who holds each permission.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# SpecForge: Authority Boundary Definition

**Role:** `spec-architect` — PART 6

## Mission

Define the authority boundaries of the system. Who can do what, under what conditions, and what is explicitly forbidden. This is the security and permission backbone of the spec.

## When to Use

- Building PART 6 — Permissions and Authority Boundaries
- After normalized requirements are complete
- When user roles are defined

## Boundary Template

```
AUTHORITY: [system | role | user-type]
CAN:
  - [action] ON [resource] WHEN [condition]
  - [action] ON [resource] WHEN [condition]

CANNOT:
  - [action] ON [resource] (reason: [why])

BOUNDARY_ENFORCED_BY: [UI | API | DB | Policy]
VIOLATION_RESPONSE: [error | ignore | log | escalate]
```

## Instructions

1. **Read Requirements**: Load NORMALIZED_REQUIREMENTS.md. Extract all permission/role-related requirements.
2. **Define Roles**: List every user type/system actor. Define what each CAN and CANNOT do.
3. **Set Conditions**: Every permission has a condition (time, state, ownership, etc.).
4. **Define Violations**: What happens when authority is exceeded?
5. **Write Output**: Section for PART 6 of master spec.

## Hard Rule

> If a role can "manage" something, break it down. "Manage" is vague. Use: create, read, update, delete, approve, reject, archive.

## Output

PART 6 section content for `MASTER_SPEC.md`.

**Authority without boundaries is chaos. Define or drift.**
