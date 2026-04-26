---
name: inline-docstring-generation
description: Add/update docstrings on all public interfaces
trigger: docforge-apidoc during phase 3
---

## Step-by-Step Instructions

1. **Identify Targets**
   - Use `read_file` to load `docs/audit/doc_tasks.json`
   - Filter for items with action: "add_docstring" or "update_docstring"
   - For each target, use `read_file` to read the source file
   - Confirm it's a public interface (not underscore-prefixed)

2. **Check Existing Pattern**
   - Use `grep` to find a nearby well-documented function: `grep -A 15 '"""' path/to/file.py | head -20`
   - Identify the exact format:
     - Google: `Args:`, `Returns:`, `Raises:` with indented descriptions
     - NumPy: `Parameters`, `Returns`, `Raises` with underlines
     - reStructuredText: `:param`, `:return:`, `:raises:`
   - Note indentation level (4 spaces? 8 spaces?)
   - Note blank line after summary? Before sections?

3. **Generate Docstring Content**
   - For each target function/class:
     - One-line summary: what it does, in imperative mood ("Fetch the user data")
     - Blank line
     - `Args:` section (if function has parameters):
       ```
       Args:
           param_name (type): Description of param.
       ```
     - `Returns:` section:
       ```
       Returns:
           type: Description of return value.
       ```
     - `Raises:` section (if function can raise exceptions):
       ```
       Raises:
           ExceptionType: When and why it's raised.
       ```
     - Example (only if behavior is non-obvious)

4. **Insert Docstring**
   - Use `read_file` to read the full source file
   - Find the line with `def function_name(` or `class ClassName(`
   - Use `search_replace` to insert the docstring after that line
   - Format: `"""\n<content>\n"""` with correct indentation (match surrounding code)
   - Verify indentation: docstring should align with function body (4 spaces in)

5. **Handle Special Cases**
   - Async functions: note `async` in summary if relevant
   - Decorated functions: document the wrapped function's interface
   - Property decorators: document as property, not method
   - Class methods: document class-level docstring + each public method

6. **Bulk Update for High Coverage**
   - For files with multiple undocumented public APIs:
     - Use `read_file` to read once
     - Use `search_replace` for each function, one at a time
     - Keep track: which functions done, which remain
   - Use `write_file` only if `search_replace` can't handle it (rare)

7. **Validate**
   - Use `read_file` to re-read the modified file
   - Verify: does every public function/class have a docstring?
   - Verify: do all parameter names in docstring match the actual signature?
   - Check: is the indentation consistent with the rest of the file?
   - Run a quick syntax check with `bash`: `python3 -m py_compile path/to/file.py`
