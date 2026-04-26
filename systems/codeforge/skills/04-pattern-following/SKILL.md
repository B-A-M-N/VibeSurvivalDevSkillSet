---
name: pattern-following
description: Detect and replicate existing code patterns, naming conventions, architecture style
---

## Steps to Detect and Apply Patterns

1. **Pattern Discovery**
   - Examine existing code files in the repository systematically
   - Identify recurring code structures and templates across modules
   - Document common class patterns, method signatures, and interfaces
   - Extract style conventions (indentation, spacing, line length, quotes)
   - Note file organization patterns (grouping, ordering, separation)

2. **Naming Convention Analysis**
   - Document class naming patterns (PascalCase for classes, snake_case for functions)
   - Extract method naming conventions and verb choices (get_, set_, create_, validate_)
   - Note variable naming styles (descriptive, context-specific)
   - Identify prefix/suffix patterns for special types (DTO, VO, Entity, Repository)

3. **Architecture Style Extraction**
   - Identify architectural patterns used (layered, hexagonal, modular)
   - Document dependency direction and coupling patterns (inversion of control)
   - Extract common design pattern implementations (Factory, Strategy, Observer)
   - Note interface and abstract class usage patterns

4. **Code Organization Patterns**
   - Document file structure conventions (group by feature vs. layer)
   - Extract import ordering and organization rules (standard library, third-party, local)
   - Identify common code blocks and their ordering (constants, imports, class definitions)
   - Note documentation and comment patterns (docstring format, section headers)

5. **Consistency Verification**
   - Verify pattern consistency across multiple files using grep/ack
   - Identify exceptions and their justifications (legacy code, special requirements)
   - Document pattern variations for different contexts (test vs. production)
   - Prepare pattern mapping for implementation reference

6. **Pattern Application Planning**
   - Map spec requirements to appropriate patterns from discovery
   - Plan how to apply patterns to new code (template-based generation)
   - Identify when to extend vs. replicate patterns (prefer extension for consistency)
   - Prepare for pattern-based code generation using write_file

7. **Implementation Guidelines**
   - Create pattern-based templates for new files (with invariant guards)
   - Document pattern-specific rules and constraints (naming, structure, dependencies)
   - Prepare examples of pattern application in context
   - Set up validation checks for pattern compliance (linters, custom scripts)

8. **Pattern Validation**
   - Verify new code follows documented patterns via automated checks
   - Check naming consistency across files systematically
   - Ensure architectural integrity is maintained (no circular dependencies)
   - Validate pattern adherence in integration testing

## Pattern Matching Examples

- **Class Names**: `UserService`, `PaymentProcessor`, `InventoryManager`
- **Method Names**: `calculateTotal()`, `validateInput()`, `fetchData()`
- **File Structure**: `src/modules/user/service.py`, `src/modules/payment/validator.py`
- **Imports Order**: `import os`, `from typing import List`, `from .models import User`