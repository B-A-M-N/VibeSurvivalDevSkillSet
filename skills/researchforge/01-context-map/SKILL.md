---
name: researchforge-01-context-map
description: |
  ResearchForge — Context Map. Identifies all components, systems,
  and dependencies relevant to the problem space.
user-invocable: false
allowed-tools:
  - read_file
  - grep
  - bash
  - task
---

# ResearchForge: Context Map

**Role:** `research-overseer` — Phase1 (context)

## Mission

Map the context around the problem. What components, systems, dependencies, and external services touch this issue? No research in isolation — understand the neighborhood first.

## When to Use

- After PROBLEM_FRAME.md is complete
- Before collecting evidence
- When the problem touches multiple systems

## Context Map Template

```
CONTEXT_MAP.md
==============

PROBLEM_SCOPE:
  primary_component: [main component where issue manifests]
  affected_systems: [list of systems that are affected or implicated]

COMPONENT_MAP:
  - name: [component/service]
    type: [internal | external | dependency | infrastructure]
    version: [if known]
    role: [what it does in relation to the problem]
    health: [known good | suspected bad | unknown]

DEPENDENCY_GRAPH:
  - from: [component A]
    to: [component B]
    type: [sync call | async | event | shared DB | file system]
    critical: true | false

EXTERNAL_SERVICES:
  - name: [service name]
    type: [API | database | message queue | auth provider]
    status_endpoint: [how to check if it's up]
    known_issues: [link to status page or known problems]

ENVIRONMENT:
  runtime: [OS, container, bare metal]
  versions: [language, framework, critical dependency versions]
  config_files: [paths to relevant configs]
  network: [behind firewall, public, VPN, etc.]
```

## Instructions

1. **Read Problem Frame**: Load PROBLEM_FRAME.md to understand scope.
2. **Map Components**: List every component mentioned in affected_components.
3. **Trace Dependencies**: What does each component call? What calls it?
4. **Identify External**: APIs, databases, queues, auth providers — anything outside the codebase.
5. **Note Environment**: OS, versions, configs, network topology.
6. **Write Output**: `CONTEXT_MAP.md`.

## Output

`CONTEXT_MAP.md` — the system context for the research.

**Research without context is guessing. Map the neighborhood.**
