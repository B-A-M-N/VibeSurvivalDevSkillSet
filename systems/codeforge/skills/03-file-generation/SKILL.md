---
name: file-generation
description: Generate new files based on spec, following existing patterns, with invariant guards
trigger: need to create new files while maintaining codebase consistency
---

## Step-by-Step Instructions

### 1. Pre-Generation Invariant Check
- Review all invariants from MASTER_SPEC.md
- Check existing code for relevant patterns
- Verify generation approach won't violate any constraints
- Prepare invariant validation checks

### 2. Template Selection
- Identify the most similar existing file or pattern
- Extract the template structure and conventions
- Note required imports, dependencies, and boilerplate
- Select appropriate file format and style

### 3. Content Generation
- Generate file content based on spec requirements
- Fill in spec-specific details and configurations
- Apply naming conventions from codebase survey
- Implement required interfaces and methods

### 4. Invariant Validation
- Run invariant checks against generated content
- Verify data structures match spec requirements
- Check API contracts and signatures
- Validate error handling and edge cases

### 5. Integration Compatibility
- Ensure new files integrate with existing modules
- Verify import paths and dependencies
- Check cross-module communication patterns
- Test compatibility with existing APIs

### 6. Pattern Alignment
- Compare generated code with existing patterns
- Adjust naming, formatting, and structure as needed
- Ensure consistency with codebase conventions
- Apply any framework-specific best practices

### 7. File Writing
- Write file only after all checks pass
- Use atomic file operations when possible
- Create backup or versioning if needed
- Log the generation event and parameters

### 8. Post-Generation Verification
- Verify file was written correctly
- Run automated tests if available
- Check file permissions and encoding
- Prepare for next phase validation