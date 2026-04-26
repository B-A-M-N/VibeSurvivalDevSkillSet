---
name: constraint-enforcer
description: |
trigger: when constraints need validation
  Enforces hard boundaries and project invariants. Prevents out-of-scope 
  actions and unauthorized file modifications.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Grep
  - TaskCreate
---

# Constraint Enforcer

This skill protects project boundaries and ensures that all operations respect defined invariants. Constraints are absolute; violating them results in immediate halting.

## When to Use
- Before any destructive action (`rm`, `git reset`).
- Before modifying core configuration files (e.g., `package.json`, `pyproject.toml`).
- If you suspect a task is taking you "Out of Scope" (e.g., editing `.git/`).

## Core Invariants
1. **No Shadow Edits**: Never touch files in `.git/`, `node_modules/`, or `__pycache__/`.
2. **Persistence**: `invariants[]` in `.checkpoint.json` are binding. If a task conflicts, you must HALT.
3. **Least Privilege**: Only modify the specific files required for the current atomic step.

## Instructions
1. **Identify Boundaries**: Review the `invariants[]` list in `.checkpoint.json`.
2. **Validate Action**: Check if your next planned tool call targets a restricted path.
3. **Halt on Conflict**: If an action violates a constraint, stop immediately and report: "INVARIANT CONFLICT: [Reason]. Cannot proceed."

**When in doubt, DON'T. Ask first, act second.**
