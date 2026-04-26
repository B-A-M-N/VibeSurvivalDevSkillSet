---
name: 01-api-reference-generation
description: Generate API docs from code signatures and spec contracts
trigger: docforge-apidoc always
---

## Step-by-Step Instructions

1. **Parse Signatures**
   - Extract function/method signatures from source
   - Capture parameter names, types, and defaults
   - Identify return types and type hints

2. **Spec Contract Validation**
   - Cross-reference with API specification documents
   - Validate parameter contracts and constraints
   - Ensure spec compliance

3. **Generate API Pages**
   - Create Markdown files per module/namespace
   - Document all public endpoints
   - Include parameter tables and return values

4. **Type Documentation**
   - Document complex types and interfaces
   - Generate type usage examples
   - Cross-link related API sections

5. **Validation & Formatting**
   - Verify all parameters are documented
   - Ensure consistent formatting across pages
   - Generate index and navigation