---
name: 00-codebase-doc-survey
description: Survey existing docs, identify gaps vs code+spec
trigger: docforge-overseer during phase 1
---

## Step-by-Step Instructions

1. **Index Source Files**
   - Scan all source directories for code files
   - Extract module paths and file structures
   - Build a code inventory database

2. **Extract Public Interfaces**
   - Identify all public classes, functions, methods
   - Parse signatures and type annotations
   - Document visibility modifiers

3. **Compare Against Documentation**
   - Check existing docs/ directory for coverage
   - Compare with spec requirements
   - Identify undocumented public APIs

4. **Gap Analysis**
   - Generate gap report: undocumented items
   - Prioritize by public API importance
   - Flag stale documentation sections

5. **Produce Survey Report**
   - Output JSON/Markdown survey results
   - Include coverage percentages per module
   - List gaps with file locations