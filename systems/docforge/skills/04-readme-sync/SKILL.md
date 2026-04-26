---
name: readme-sync
description: Sync README and docs with actual code behavior
trigger: docforge-overseer during phase 5
---

## Step-by-Step Instructions

1. **Read Current README**
   - Use `read_file` to read README.md completely
   - Identify all sections: Overview, Installation, Usage, API, Examples, etc.
   - Extract all code examples, commands, and expected outputs
   - Extract all API references and links to docs

2. **Verify Code Examples**
   - For each code example in README:
     - Copy the example code
     - Use `bash` to run it (if it's a shell command) or `python3 -c "code"` (if it's Python)
     - Compare actual output vs README's expected output
     - Flag mismatches: `Example at line X: expected Y, got Z`
   - For API examples: use `read_file` to verify the function signature matches

3. **Verify Feature Claims**
   - For each feature listed in README Overview or Features section:
     - Use `grep` to find the feature in the codebase
     - Use `read_file` to verify it's actually implemented
     - Flag: "Feature X listed but not found in codebase" (stale)
     - Flag: "Feature X implemented but not listed in README" (gap)

4. **Check Links and References**
   - Use `grep` to find all links in README: `grep -n "](http" README.md`
   - For internal links `[text](docs/...)`: verify the file exists with `read_file`
   - For external links: note them for manual checking
   - Flag broken links: `[text](broken-path)` → needs fixing

5. **Check Version Information**
   - Use `bash` to check current version: `grep -rn "version\|VERSION" --include="*.py" | head -5`
   - Compare with README's version claims
   - Update if mismatch using `search_replace`

6. **Update Stale Sections**
   - For each stale section identified:
     - Use `read_file` to read current README.md
     - Use `search_replace` to update the specific section
     - Examples: replace old output with actual output
     - Features: add missing or remove non-existent
     - API: update signatures to match current code
   - Keep the existing tone and formatting style exactly

7. **Update Diagram Links**
   - Use `read_file` to check if new diagrams were created by docforge-diagrams
   - If `docs/diagrams/` exists, use `search_replace` to add diagram section to README:
     ```markdown
     ## Architecture Diagrams
     - [Component Overview](docs/diagrams/components.md)
     - [State Machines](docs/diagrams/state-....md)
     ```

8. **Add New API Highlights (if needed)**
   - Use `read_file` to check if new APIs were documented in docs/api/
   - Use `search_replace` to update README's API section with new links
   - Keep format consistent with existing API entries

9. **Final Validation**
   - Use `read_file` to re-read the updated README.md
   - Verify all `search_replace` operations succeeded (no duplicate or corrupted sections)
   - Run a quick Markdown render check: `bash -c "cat README.md | head -50"` to spot obvious issues
   - Ensure the README matches the current state of the codebase
