# DocForge — Implementation Details

## Overview
DocForge is an automated documentation generation and maintenance system that operates in six coordinated phases. It uses specialized agents to survey code, generate API documentation, create inline docstrings, produce architecture diagrams, sync README files, and continuously verify documentation freshness.

## Agent Responsibilities

### docforge-overseer (Orchestrator)
- Coordinates the six-phase workflow
- Gates progress on completeness checks
- Delegates tasks to specialized agents
- Maintains continuity state and logs

### docforge-apidoc (API Documentation Specialist)
- Parses source code for signatures and types
- Cross-references with spec contracts
- Generates Markdown API references
- Ensures parameter and return type accuracy

### docforge-diagrams (Architecture Visualizer)
- Extracts module and dependency graph
- Generates architecture diagrams
- Produces flow charts and state machines
- Outputs both mermaid and plantuml formats

## Workflow Details

### Phase 1: Codebase Survey (00-codebase-doc-survey)
1. Index all source files in the project
2. Compare existing docs against code + spec
3. Identify undocumented public APIs
4. Flag stale documentation sections
5. Produce a survey report

### Phase 2: API Reference Generation (01-api-reference-generation)
1. Parse function/method signatures
2. Extract type annotations
3. Cross-check with spec contracts
4. Generate Markdown API pages
5. Validate parameter/return descriptions

### Phase 3: Inline Docstring Generation (02-inline-docstring-generation)
1. Identify public classes/functions
2. Generate compliant docstrings (Google/NumPy format)
3. Update source files with new docstrings
4. Verify formatting standards

### Phase 4: Architecture Diagram Generation (03-architecture-diagram-generation)
1. Build dependency graph from imports
2. Generate module relationship diagrams
3. Create flow charts for key workflows
4. Export mermaid and plantuml files

### Phase 5: README Sync (04-readme-sync)
1. Extract key project facts from code
2. Update project overview sections
3. Sync API highlights with current state
4. Ensure examples reflect actual behavior

### Phase 6: Continuity Check (05-doc-continuity-check)
1. Monitor for code changes (git/compaction)
2. Revalidate affected documentation
3. Update stale sections automatically
4. Log all changes with timestamps

## Compaction & Change Detection
- Hooks into git:commit and file:modify events
- Triggers Phase 6 recheck on detected changes
- Maintains per-module continuity timestamps
- Supports incremental updates for efficiency

## State Management
- Continuity log stored at `docs/continuity.log`
- Agent state persisted between runs
- Checkpointing at each phase boundary
- Rollback capability on failure

## Configuration
- Central config.toml for agent settings
- Per-agent model and turn limits
- Output directory customization
- Trigger condition definitions