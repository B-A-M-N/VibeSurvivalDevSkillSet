---
name: architecture-diagram-generation
description: Generate architecture diagrams from code structure
trigger: docforge-diagrams always
---

## Step-by-Step Instructions

1. **Build Dependency Graph**
   - Use `bash` to run `grep -rn "import " --include="*.py" | head -50`
   - Use `bash` to run `grep -rn "from .* import" --include="*.py" | head -50`
   - Parse: which modules import which other modules
   - Build node list: all major components/modules
   - Build edge list: dependency relationships between them

2. **Identify Component Layers**
   - Use `read_file` to read main entry point and key files
   - Classify components into layers:
     - **Presentation**: UI, API endpoints, controllers
     - **Business Logic**: services, use cases, domain models
     - **Data Layer**: repositories, models, database access
   - Note external dependencies: databases, APIs, message queues

3. **Generate Component Diagram (ASCII)**
   - Use `write_file` to create `docs/diagrams/components.md`
   - ASCII format:
     ```
                    ┌─────────────┐
                    │   API Layer  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Business Logic │
                    └──────┬──────┘
                  ┌─────┴─────┐
                  │ Data Layer  │
                  └─────────────┘
     ```
   - Label each component within its layer box
   - Draw arrows for dependencies (─→ for sync, ⇢ for async)

4. **Generate State Machine Diagrams**
   - Use `grep` to find state machine code: `grep -rn "state\|transition" --include="*.py" | head -20`
   - Use `read_file` to read state machine implementations
   - For each state machine, create `docs/diagrams/state-<name>.md`:
     ```
     [Initial State] ──→ [State 1] ──→ [State 2]
                      │              │
                      └─(event)─→ [State 3]
     ```
   - Label transitions with event names and guard conditions

5. **Generate Flow Charts**
   - Use `read_file` to read key workflow implementations
   - For each workflow (signup, checkout, etc.), create `docs/diagrams/flow-<name>.md`:
     ```
     [Start] → (Decision: check X?) → [Action A]
                         │
                         └─(no)→ [Action B] → [End]
     ```
   - Use (Diamond) for decisions, [Box] for actions, [Start/End] for terminals

6. **Generate Data Flow Diagrams**
   - Trace data from input to output through the system
   - Create `docs/diagrams/dataflow-<name>.md`:
     ```
     [Input] → [Validate] → [Transform] → [Store] → [Output]
     ```
   - Note data formats at each step (JSON, protobuf, etc.)
   - Note transformations applied at each step

7. **Generate Mermaid Alternatives**
   - For each diagram, also provide Mermaid syntax (renders on GitHub):
     ```mermaid
     graph TD
         A[API Layer] --> B[Business Logic]
         B --> C[Data Layer]
     ```
   - Use `write_file` to include both ASCII and Mermaid in each diagram file

8. **Update README with Diagram Links**
   - Use `read_file` to read current README.md
   - Use `search_replace` to add a `## Architecture Diagrams` section
   - Link to each diagram: `[Component Diagram](docs/diagrams/components.md)`
   - Embed one key diagram directly in README if it's small enough

9. **Validate**
   - Use `read_file` to check each diagram file
   - Verify: do all components match the actual codebase?
   - Verify: are state transitions accurate vs the code?
   - Check: can someone new understand the architecture from these diagrams?
