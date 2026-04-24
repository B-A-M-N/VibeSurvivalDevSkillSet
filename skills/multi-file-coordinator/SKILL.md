---
name: multi-file-coordinator
description: |
  Coordinates complex changes spanning multiple files. Manages cross-file 
  dependencies and ensures consistency after batch modifications.
user-invocable: true
allowed-tools:
  - read_file
  - write_file
  - grep
  - bash
  - todo
---

# Multi-File Coordinator

This skill manages operations that span multiple files (e.g., refactoring a shared function name). It ensures that all references are updated simultaneously and that the system remains in a consistent state.

## When to Use
- When a change in one file requires corresponding changes in 2+ other files.
- During a large-scale refactor or "Search & Replace" task.
- If you find yourself losing track of which files have been updated in a multi-step plan.

## Coordination Rules
1. **Dependency Mapping**: Identify all files that import or reference the target symbol BEFORE making the first change.
2. **Atomic Commits**: Group all related file changes into a single logical step in `.todo`.
3. **Consistency Check**: After the batch update, use `grep` to verify no references to the old pattern remain in the entire codebase.

## Instructions
1. **Identify Targets**: Use `grep -r` to find all occurrences of the pattern across the project.
2. **Execute Batch**: Modify each file sequentially, verifying each write as you go.
3. **Global Verify**: Run a project-wide grep to ensure total coverage.
4. **Functional Test**: Run tests to confirm cross-file logic is still intact.

**One change, multiple files, zero inconsistencies.**
