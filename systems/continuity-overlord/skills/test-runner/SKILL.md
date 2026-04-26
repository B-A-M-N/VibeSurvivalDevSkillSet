---
name: test-runner
description: |
  Automates test discovery, execution, and analysis. Ensures all changes 
  are verified before being marked as complete.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Grep
  - TaskCreate
---

# Test Runner

This skill manages all testing operations. It ensures that code changes do not introduce regressions and that new features meet their functional requirements.

## When to Use
- After modifying any code file.
- Before committing changes via `git-integrator`.
- If you are stuck in a "Verification Loop" and need to isolate a failure.

## Test Discovery
1. **File Patterns**: Look for `test_*.py`, `*.test.js`, or files in `tests/` directories.
2. **Configuration**: Check `package.json` (scripts), `pytest.ini`, or `jest.config.js`.

## Instructions
1. **Discover**: Run `ls -R tests/` or `grep` for test decorators.
2. **Run Affected**: Execute only the tests relevant to the modified files (e.g., `pytest tests/test_auth.py`).
3. **Analyze Output**: If tests fail, read the full traceback to identify the root cause.
4. **Verify Coverage**: Ensure new code paths are exercised by at least one test case.

**If it's not tested, it's broken. If tests don't pass, it's not done.**
