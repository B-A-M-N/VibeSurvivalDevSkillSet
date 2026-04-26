---
name: git-integrator
description: |
trigger: on git events or scheduled
  Manages Git operations intelligently. Handles commits, branches, 
  and conflict resolution based on the task objective.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Git Integrator

This skill manages all Git operations intelligently. It ensures that version control is integrated into every change and helps maintain a clean repository history.

## When to Use
- After completing a task step to commit changes.
- Before starting a new feature to create a branch.
- If you encounter merge conflicts during a pull.

## Commit Guidelines
1. **Atomic Commits**: Group related changes into a single commit.
2. **Standard Format**: Use `type(scope): subject` (e.g., `feat(auth): add JWT validation`).
3. **Imperative Mood**: Use "Add feature", not "Added feature".

## Instructions
1. **Check Status**: Run `git status` to see modified files.
2. **Review Diff**: Use `git diff` to verify the changes match the intent.
3. **Stage & Commit**: Use `git add` and `git commit -m "[message]"`.
4. **Branching**: If starting a new objective, use `git checkout -b [type]/[description]`.

**Every change deserves a commit. Every commit deserves a good message.**
