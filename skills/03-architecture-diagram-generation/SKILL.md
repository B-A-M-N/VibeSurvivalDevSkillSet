---
name: 03-architecture-diagram-generation
description: Generate architecture diagrams from code structure
trigger: docforge-diagrams always
---

## Step-by-Step Instructions

1. **Dependency Extraction**
   - Parse import statements across codebase
   - Build module dependency graph
   - Identify circular dependencies

2. **Graph Generation**
   - Create nodes for modules/classes
   - Draw edges for dependencies
   - Apply layout algorithms for clarity

3. **Flow Chart Creation**
   - Identify key workflows and processes
   - Map decision points and branches
   - Generate step-by-step flow representations

4. **State Machine Diagrams**
   - Identify stateful components
   - Map state transitions
   - Document trigger conditions

5. **Export Formats**
   - Generate Mermaid syntax
   - Create PlantUML definitions
   - Export SVG and DOT formats
   - Ensure diagram consistency