---
name: codebase-survey
description: Survey existing codebase, map files to spec sections, identify integration points and patterns
---

## Steps to Survey Codebase

1. **Repository Overview**
   - List all files and directories in the codebase
   - Identify the main programming language and frameworks
   - Document the project structure and build system
   - Note any existing documentation or README files

2. **Code Organization Analysis**
   - Map directory structure to functional areas
   - Identify core modules and their responsibilities
   - Document package/module dependencies
   - Note any layered architecture (presentation, business, data layers)

3. **Pattern Identification**
   - Extract coding patterns from existing files
   - Document naming conventions (classes, functions, variables)
   - Identify architectural patterns (MVC, MVP, MVVM, etc.)
   - Note common design patterns used (singleton, factory, repository, etc.)

4. **API and Integration Points**
   - Document all existing APIs and their usage
   - Identify integration points with external systems
   - Note authentication and authorization mechanisms
   - Document data flow between components

5. **File Type Mapping**
   - Map file extensions to their purposes
   - Identify configuration files and their formats
   - Document test files and testing patterns
   - Note any generated files or artifacts

6. **Dependency Analysis**
   - Extract import statements and dependencies
   - Document external libraries and frameworks
   - Note version constraints and compatibility requirements
   - Identify circular dependencies or potential issues

7. **Cross-Reference with Spec**
   - Map existing code to spec sections
   - Identify implemented vs missing features
   - Document gaps between current state and requirements
   - Note areas requiring modification or extension

8. **Pattern Extraction for Implementation**
   - Document reusable patterns for new implementation
   - Extract code templates and boilerplate
   - Note best practices from existing code
   - Prepare pattern library for implementer agent

## Output: CODEBASE_MAP.md

The output `CODEBASE_MAP.md` should contain:
- Directory structure visualization
- Module dependency graph
- API endpoint inventory with spec section mappings
- Pattern catalog with code examples
- Integration point matrix
- File type registry
- Dependency tree
- Spec compliance gap analysis