---
name: codebase-doc-survey
description: Survey existing docs, identify gaps vs code+spec
trigger: docforge-overseer during phase 1
---

## Step-by-Step Instructions

1. **Scan Repository Structure**
   - Use `bash` to run `find . -name "*.py" -o -name "*.js" -o -name "*.ts" | head -50`
   - Use `bash` to run `ls -la` on each major directory
   - Build a directory tree with `tree -L 3` or equivalent
   - Identify main language, framework, and build system

2. **Extract Public Interfaces**
   - Use `grep` to find all `def `, `class `, `export `, `public ` declarations
   - Use `read_file` to read key source files and extract signatures
   - Parse function/method signatures with parameter names and types
   - Build a table: `| Module | Function/Class | Parameters | Return Type |`

3. **Inventory Existing Docs**
   - Use `read_file` to read README.md, all files in docs/, and inline docstrings
   - Use `grep` to find all docstring locations: `grep -rn '"""' --include="*.py" | head -30`
   - Build coverage map: which public APIs have docs, which don't
   - Note doc style: Google, NumPy, or reStructuredText

4. **Compare Against MASTER_SPEC.md**
   - Use `read_file` to read MASTER_SPEC.md sections on APIs and components
   - For each spec requirement, check: is it implemented? Is it documented?
   - Flag: spec says X but docs say Y (conflict)
   - Flag: spec defines it but neither code nor docs exist (not implemented)

5. **Gap Analysis**
   - Classify gaps by severity:
     - **Critical**: Public API with no docs at all
     - **High**: Docs exist but don't match code behavior
     - **Medium**: Missing examples or edge case documentation
     - **Low**: Typos or formatting issues
   - Build gap table: `| API | Status | Severity | File | Action Needed |`

6. **Generate DOC_GAP_REPORT.md**
   - Use `write_file` to create `docs/audit/DOC_GAP_REPORT.md`
   - Include: Executive summary, Coverage percentage, Critical/High/Medium/Low gap tables
   - Include: Recommended priorities with effort estimates (small/medium/large)
   - Include: Spec compliance section (what's documented vs spec)

7. **Output Registration**
   - Create `docs/audit/doc_tasks.json` with all gaps as task items:
     ```json
     [{"id": "gap-001", "severity": "critical", "file": "path", "action": "add_docstring", "effort": "small"}]
     ```
   - Use `write_file` to save the task list for downstream agents
