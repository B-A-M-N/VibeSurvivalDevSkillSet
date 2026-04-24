---
name: specforge-14-observability-specification
description: |
  SpecForge — Observability Specification. Defines what gets logged,
  what metrics are collected, tracing strategy, and alerting thresholds.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
---

# SpecForge: Observability Specification

**Role:** `spec-architect` — PART 11

## Mission

Define the observability contract. What logs, what metrics, what traces, and what triggers alerts. The system must be diagnosable without guessing.

## When to Use

- Building PART 11 — Observability
- After API contracts and execution flows are defined
- When the system needs monitoring, debugging, or performance tracking

## Observability Template

```
LOGGING:
  structured: true | false
  format: [JSON | text | key=value]
  levels:
    - ERROR: [when to use]
    - WARN: [when to use]
    - INFO: [when to use]
    - DEBUG: [when to use, disabled in prod]

  required_fields_per_log:
    - timestamp
    - trace_id
    - user_id (if applicable)
    - [custom fields]

  events_always_logged:
    - [API request start/end]
    - [state transitions]
    - [permission denials]
    - [errors with stack traces]

METRICS:
  - name: [metric_name]
    type: [counter | gauge | histogram]
    description: [what this measures]
    labels: [dimensions]
    collection_interval: [seconds]

  SLOs:
    - metric: [error_rate | latency_p99]
      threshold: [value]
      window: [duration]

TRACING:
  strategy: [OpenTelemetry | vendor | custom]
  sampled_rate: [percentage]
  propagated_via: [headers | context]

ALERTING:
  - condition: [metric + threshold]
    severity: [critical | warning | info]
    notification: [where alert goes]
    cooldown: [minimum time between alerts]

HEALTH_CHECKS:
  - endpoint: /health | [custom]
    checks: [DB connectivity | external API | disk space]
    failure_action: [return 503 | restart | log only]
```

## Instructions

1. **Read Requirements**: Find observability requirements in NORMALIZED_REQUIREMENTS.md.
2. **Define Logs**: Structured format, required fields, events that always log.
3. **Define Metrics**: Counters, gauges, histograms — with SLOs.
4. **Define Tracing**: How requests are traced across services.
5. **Define Alerts**: What triggers alerts, with severity and cooldown.
6. **Write Output**: PART 11 section for `MASTER_SPEC.md`.

## Output

PART 11 section content for `MASTER_SPEC.md`.

**"It probably logged something" is not observability. Define what, where, and why.**
