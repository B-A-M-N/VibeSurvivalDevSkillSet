---
name: code-quality
description: |
  Enforces code standards and best practices. Automatically validates syntax 
  and style before any file write or modification.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
---

# Code Quality

This skill ensures that all code modifications meet the project's quality standards. It automatically validates your changes against best practices and style guides.

## When to Use
- Before any `write_file` or `replace` operation.
- If you are unsure about the project's naming conventions or style.
- After a complex refactor to ensure no syntax errors were introduced.

## Quality Gates
1. **Syntax Check**: Run a non-interactive syntax check (e.g., `python3 -m py_compile`, `node -c`) before committing a write.
2. **Style Match**: Inspect surrounding code to match indentation (spaces vs. tabs) and naming conventions (snake_case vs. camelCase).
3. **No Secrets**: Verify that no API keys or credentials are included in the new code.

## Instructions
1. **Prepare Change**: Draft your code modification.
2. **Scan Context**: Read 10 lines above and below the target area to ensure style consistency.
3. **Validate**: Run a lint or syntax command via `bash`.
4. **Execute**: Proceed with the write only if validation passes.

**If you wouldn't accept it in a PR, don't write it.**
