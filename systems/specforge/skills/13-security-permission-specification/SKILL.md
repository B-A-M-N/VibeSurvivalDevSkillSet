---
name: specforge-13-security-permission-specification
description: |
  SpecForge — Security & Permission Specification. Defines authentication,
  authorization, secrets handling, injection defenses, and audit logging.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# SpecForge: Security & Permission Specification

**Role:** `spec-architect` — PART 6 (extended)

## Mission

Define the complete security model. Authentication mechanisms, authorization checks, secrets handling, injection defenses, and what gets audited. Every permission check is explicit.

## When to Use

- Building PART 6 — Permissions and Authority Boundaries (security subsection)
- After user roles and data models are defined
- When the system handles sensitive data or privileged operations

## Security Template

```
AUTHENTICATION:
  method: [session | JWT | OAuth2 | API_key | mTLS]
  token_lifetime: [duration]
  refresh_policy: [how/when tokens refresh]
  credential_storage: [hashed | encrypted | never_stored]

AUTHORIZATION:
  model: [RBAC | ABAC | ACL]
  permission_check_enforcement_point: [API middleware | UI | DB | all]
  default_deny: true | false

SECRETS:
  - type: [API key | password | token | cert]
    storage: [env var | vault | encrypted DB field]
    rotation: [manual | automatic | never]
    access_logged: true | false

INJECTION_DEFENSES:
  - vector: [SQLi | XSS | CSRF | SSTI | command injection]
    defense: [parameterized queries | output encoding | CSRF tokens | etc.]
    enforcement_point: [ORM | template engine | middleware]

AUDIT_LOG:
  events_logged:
    - [login | logout | permission change | data access | data modify]
  fields_per_event: [timestamp | user | action | resource | outcome]
  retention: [duration]
  tamper_resistance: [append-only | signed | hash-chain]

VULNERABILITY_HARD_GATES:
  - [condition that MUST fail deployment if true]
```

## Instructions

1. **Read Authority Boundaries**: PART 6 draft from `07-authority-boundary-definition`.
2. **Define Auth**: How do users prove who they are? How do tokens work?
3. **Permission Checks**: Every protected operation lists WHERE the check happens.
4. **Secrets**: What secrets exist? How are they stored? Who accesses them?
5. **Defense in Depth**: Map each injection vector to its defense.
6. **Audit**: What must be logged for forensic use?
7. **Write Output**: Security subsection for PART 6 in `MASTER_SPEC.md`.

## Output

Security subsection for PART 6 in `MASTER_SPEC.md`.

**Security by vibes is insecurity. Define every check.**
