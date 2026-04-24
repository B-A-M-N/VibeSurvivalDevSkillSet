---
name: specforge-15-error-handling-specification
description: |
  SpecForge — Error Handling Specification. Defines error types,
  recovery strategies, user-facing messages, and retry/backoff policies.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# SpecForge: Error Handling Specification

**Role:** `spec-architect` — PART 10

## Mission

Define every error: what causes it, what the system does, what the user sees, and how to recover. No "handle errors gracefully" — define each one.

## When to Use

- Building PART 10 — Error Handling
- After API contracts and execution flows are defined
- When the system can fail in detectable ways

## Error Template

```
ERROR: [ERROR_CODE or name]
CATEGORY: [validation | auth | permission | not_found | conflict | rate_limit | internal | external | timeout]

TRIGGERED_WHEN:
  - [exact condition 1]
  - [exact condition 2]

SYSTEM_RESPONSE:
  log_level: [ERROR | WARN | INFO]
  http_status: [400 | 401 | 403 | 404 | 409 | 422 | 429 | 500]
  retry_allowed: true | false
  retry_strategy: [immediate | backoff | none]
  max_retries: [number]
  backoff_policy: [exponential | linear | fixed]
  circuit_breaker: true | false

USER_FACING_MESSAGE:
  summary: [one-line message]
  detail: [what the user can do about it]
  action_button: [retry | contact_support | go_back | none]

RECOVERY:
  automatic: [what system tries to fix]
  manual: [what user must do]
  escalation: [who to notify if recovery fails]

DEGRADED_MODE:
  fallback_behavior: [what happens if this error is non-critical]
```

## Instructions

1. **Read API Contracts**: Every error response in PART 7 needs a full definition here.
2. **Define by Category**: Validation, auth, permission, not_found, conflict, etc.
3. **System Response**: Log level, HTTP status, retry policy, circuit breaker.
4. **User Message**: Exact text shown. No "An error occurred" — be specific.
5. **Recovery Path**: Automatic retry? Manual action? Escalation?
6. **Write Output**: PART 10 section for `MASTER_SPEC.md`.

## Output

PART 10 section content for `MASTER_SPEC.md`.

**"Handle errors" is not a spec. Name them, define them, recover from them.**
