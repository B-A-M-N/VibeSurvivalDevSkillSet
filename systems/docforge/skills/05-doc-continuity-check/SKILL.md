---
name: doc-continuity-check
description: Recheck docs on code change, update stale sections
trigger: docforge-overseer during phase 6
---

## Step-by-Step Instructions

1. **Detect Recent Changes**
   - Use `bash` to run `git log --oneline --since="7 days ago" --name-only | sort | uniq`
   - Use `bash` to run `git diff HEAD~10 --name-only | sort | uniq`
   - Identify which files changed recently (focus on source files, not tests/config)
   - For each changed file, note: what changed? (new function, modified signature, removed feature)

2. **Map Changes to Documentation**
   - For each changed source file:
     - Use `grep` to find related docs: `grep -rn "FunctionName\|ClassName" docs/`
     - Use `read_file` to read the related doc files
     - Check: does the doc still match the updated code?
     - Flag as stale if: signature changed but doc didn't, feature removed but doc still mentions it

3. **Check Docstring Staleness**
   - For changed functions/classes:
     - Use `read_file` to read the source file at the changed location
     - Extract the docstring (if any) and compare parameters vs actual signature
     - Flag: docstring mentions old parameter name, missing new parameter, wrong return type
     - Use `search_replace` to update stale docstrings

4. **Check API Reference Staleness**
   - For changed modules:
     - Use `read_file` to read `docs/api/<module>.md` (if exists)
     - Compare documented signatures vs actual code signatures
     - Flag: documented function doesn't exist anymore, signature mismatch, return type wrong
     - Use `search_replace` to update the API reference page

5. **Check Diagram Staleness**
   - Use `read_file` to read all files in `docs/diagrams/`
   - For each diagram, verify:
     - Do all components still exist in the codebase? (`grep -rn "ComponentName"`)
     - Are state transitions still accurate? (read state machine code)
     - Are data flows still correct? (trace through updated code)
   - Use `search_replace` to update stale diagram sections

6. **Generate STALENESS_REPORT.md**
   - Use `write_file` to create `docs/audit/STALENESS_REPORT.md`:
     ```markdown
     # Documentation Staleness Report
     ## Summary: N docs checked, M stale, P critical
     ## Stale Docstrings
     | File | Line | Issue | Severity |
     |------|------|-------|----------|
     | path | 42 | param X removed but doc mentions it | medium |
     ## Stale API Docs
     | Doc File | Issue | Severity |
     ## Stale Diagrams
     | Diagram | Component | Issue |
     ## Action Items
     1. Update docstring in path (effort: small)
     2. Rewrite API page for module (effort: large)
     ```
   - Classify severity: critical (wrong API docs causing user errors), medium (missing new params), low (typos)

7. **Auto-Update Quick Fixes**
   - For staleness items marked "effort: small" (single docstring update):
     - Use `read_file` to read the source file
     - Use `search_replace` to fix the docstring immediately
   - For larger items, add to `docs/audit/doc_tasks.json` for later delegation

8. **Update Continuity Log**
   - Use `bash` to append to `.docforge-continuity-log`:
     ```
     2026-04-25: Checked N files, found M stale docs, updated K
     ```
   - This allows tracking doc health over time and triggers recheck on significant changes
