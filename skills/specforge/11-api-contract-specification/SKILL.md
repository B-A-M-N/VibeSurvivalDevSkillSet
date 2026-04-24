---
name: specforge-11-api-contract-specification
description: |
  SpecForge — API Contract Specification. Defines endpoints, request/response
  schemas, auth requirements, rate limits, and error responses.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# SpecForge: API Contract Specification

**Role:** `spec-architect` — PART 7

## Mission

Define every API endpoint as a binding contract. Request schema, response schema, auth requirements, rate limits, and every error response. No "standard REST" hand-waving.

## When to Use

- Building PART 7 — API / Interface Contracts
- After data models and authority boundaries are defined
- When the system exposes APIs (HTTP, RPC, CLI, etc.)

## Endpoint Template

```
ENDPOINT: [method] [path]
DESCRIPTION: [what this does]

AUTH:
  required: true | false
  roles_allowed: [role list]
  token_type: [bearer | session | api_key | none]

REQUEST:
  headers:
    - name: [header]
      required: true | false
      type: [type]
  query_params:
    - name: [param]
      required: true | false
      type: [type]
  body_schema: [link to data model or inline definition]

RESPONSE:
  success:
    status: 200 | 201 | etc.
    body_schema: [model]
  errors:
    - status: 400
      condition: [when this happens]
      body: [error schema]
    - status: 401
      condition: [unauthenticated]
      body: [error schema]
    - status: 403
      condition: [unauthorized]
      body: [error schema]
    - status: 429
      condition: [rate limited]
      body: [error schema]

RATE_LIMIT:
  requests: [number]
  window: [seconds]
  exceeded_response: [429 with Retry-After header]

INVARIANTS:
  - [what must be true before/after this call]
```

## Instructions

1. **Read Requirements**: Find all API requirements in NORMALIZED_REQUIREMENTS.md.
2. **Define Every Endpoint**: No "CRUD endpoints for X" — list each one.
3. **Auth Per Endpoint**: Who can call this? With what token?
4. **Error Every Path**: 400, 401, 403, 404, 409, 422, 429, 500 — define when each fires.
5. **Rate Limits**: Define per-endpoint or globally.
6. **Write Output**: PART 7 section for `MASTER_SPEC.md`.

## Output

PART 7 section content for `MASTER_SPEC.md`.

**An API without defined error responses is not a contract. It is a wish.**
