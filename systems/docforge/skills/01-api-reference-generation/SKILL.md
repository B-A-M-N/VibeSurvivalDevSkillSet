---
name: api-reference-generation
description: Generate API docs from code signatures and spec contracts
trigger: docforge-apidoc always
---

## Step-by-Step Instructions

1. **Read Task Assignment**
   - Use `read_file` to load `docs/audit/doc_tasks.json`
   - Filter for items with action: "create_api_page" or "update_api_page"
   - Read the corresponding source files with `read_file`

2. **Parse Signatures**
   - For each public function/class, extract: name, parameters (name/type/default), return type
   - Use `read_file` to read the full source file for context
   - Note any decorators, async modifiers, or special annotations
   - Identify which module/namespace each belongs to

3. **Cross-Reference Spec**
   - Use `read_file` to read relevant MASTER_SPEC.md sections
   - Validate: does the code signature match the spec contract?
   - Note any deviations with justification or flag as gap
   - Extract authentication, rate limiting, and error codes from spec

4. **Follow Existing Doc Patterns**
   - Use `grep` to find existing docstrings: `grep -A 10 '"""' path/to/file.py | head -20`
   - Identify format: Google style (`Args:`, `Returns:`, `Raises:`), NumPy, or reStructuredText
   - Note tone: technical, concise, friendly? Match exactly.
   - Note example patterns: how are code examples formatted?

5. **Generate API Reference Pages**
   - Use `write_file` to create `docs/api/<module>.md` for each module
   - Structure each page:
     ```markdown
     # <Module> API Reference
     ## <Function/Class Name> (signature)
     <one-line summary>
     ### Parameters
     | Name | Type | Default | Description |
     |------|------|---------|-------------|
     | param | str | "default" | description |
     ### Returns
     `<type>` — description
     ### Raises
     - `ExceptionType`: when it happens
     ### Example
     ```python
     result = module.function("arg")
     ```
   - Include authentication/rate limit info from spec if applicable

6. **Update Inline Docstrings**
   - Use `read_file` to read source file
   - Use `search_replace` to insert docstring after `def` or `class` line
   - Follow the exact format discovered in step 4
   - Include all parameters, return type, exceptions, and one example

7. **Generate API Index**
   - Use `write_file` to create `docs/api/INDEX.md`
   - Link to all API pages, organized by module
   - Include search tips and common patterns section
   - Cross-link related APIs

8. **Validate**
   - Use `read_file` to read each generated page
   - Verify: do all parameters match the actual signature?
   - Verify: do examples run without errors? (test with `bash` if feasible)
   - Check: are there broken internal links? (`[text](broken)`)
