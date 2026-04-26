---
name: 02-inline-docstring-generation
description: Add/update docstrings on all public interfaces
trigger: docforge-overseer during phase 3
---

## Step-by-Step Instructions

1. **Identify Public Interfaces**
   - Scan for public classes, methods, functions
   - Filter out private (underscore-prefixed) items
   - Build list of items needing docstrings

2. **Generate Docstring Templates**
   - Apply Google or NumPy docstring format
   - Include sections: Args, Returns, Raises, Examples
   - Extract type information from signatures

3. **Update Source Files**
   - Insert docstrings in appropriate locations
   - Preserve existing comments and logic
   - Maintain proper indentation and formatting

4. **Quality Checks**
   - Verify docstring syntax compliance
   - Ensure all parameters are documented
   - Check for proper type descriptions

5. **Validation**
   - Run docstring linters if available
   - Ensure consistency across codebase
   - Verify examples are syntactically correct