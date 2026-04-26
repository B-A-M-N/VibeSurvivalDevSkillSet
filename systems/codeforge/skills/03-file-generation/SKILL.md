---
name: file-generation
description: Generate new files based on spec, following existing patterns, with invariant guards
---

## Steps to Generate Files Using write_file Tool

1. **Pre-Generation Invariant Check**
   - Review all invariants from MASTER_SPEC.md
   - Check existing code for relevant patterns
   - Verify generation approach won't violate any constraints
   - Prepare invariant validation checks

2. **Template Selection**
   - Identify the most similar existing file or pattern
   - Extract the template structure and conventions
   - Note required imports, dependencies, and boilerplate
   - Select appropriate file format and style

3. **Content Generation**
   - Generate file content based on spec requirements
   - Fill in spec-specific details and configurations
   - Apply naming conventions from codebase survey
   - Implement required interfaces and methods

4. **Invariant Validation**
   - Run invariant checks against generated content
   - Verify data structures match spec requirements
   - Check API contracts and signatures
   - Validate error handling and edge cases

5. **Integration Compatibility**
   - Ensure new files integrate with existing modules
   - Verify import paths and dependencies
   - Check cross-module communication patterns
   - Test compatibility with existing APIs

6. **Pattern Alignment**
   - Compare generated code with existing patterns
   - Adjust naming, formatting, and structure as needed
   - Ensure consistency with codebase conventions
   - Apply any framework-specific best practices

7. **File Writing with write_file Tool**
   - Prepare content with proper formatting and invariants
   - Use write_file tool with exact file paths
   - Ensure directory exists before writing (create parent dirs if needed)
   - Use atomic operations: write to temp then move if supported
   - Log the generation event and parameters
   - Verify write operation success

8. **Post-Generation Verification**
   - Verify file was written correctly via read
   - Run invariant checks on written content
   - Check file permissions and encoding (UTF-8)
   - Validate against spec contracts
   - Prepare for integration testing

## Invariant Guard Implementation

When using write_file, ensure each generated file includes:
- Invariant validation header comments
- Type checking for all inputs
- Boundary checks for data structures
- Consistency checks with MASTER_SPEC.md
- Error handling that preserves invariants
- Logging of invariant violations for debugging