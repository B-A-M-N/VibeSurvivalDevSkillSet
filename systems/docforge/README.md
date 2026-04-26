# DocForge — Automated Documentation Generation System

## Description
Generates and maintains docs, API references, docstrings, and architecture diagrams from code + spec. Rechecks on compaction or code change events.

## How It Maps to Mistral-Vibe Table
| Mistral-Vibe Component | DocForge Equivalent |
|------------------------|---------------------|
| Codebase Survey        | 00-codebase-doc-survey  |
| API Contract Analysis  | 01-api-reference-generation |
| Implementation Details | 02-inline-docstring-generation |
| Architecture           | 03-architecture-diagram-generation |
| Documentation Sync     | 04-readme-sync      |
| Continuity Assurance   | 05-doc-continuity-check |

## Architecture Flow
```
Code + Spec
    ↓
Survey (00-codebase-doc-survey)
    ↓
API Docs (01-api-reference-generation)
    ↓
Inline Docs (02-inline-docstring-generation)
    ↓
Architecture Diagrams (03-architecture-diagram-generation)
    ↓
README Sync (04-readme-sync)
    ↓
Recheck on Change (05-doc-continuity-check)
```

## Agents Table
| Agent | Role | Model | Max Turns |
|-------|------|-------|-----------|
| docforge-overseer | Orchestrator | hy3 | 50 |
| docforge-apidoc | API doc writer | devstral-2 | — |
| docforge-diagrams | Diagram generator | hy3 | 40 |

## Install Bash Commands
```bash
# Clone or navigate to the system
cd /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/systems/docforge

# Install dependencies (if any)
pip install -r requirements.txt 2>/dev/null || true

# Ensure agents directory exists
mkdir -p agents
mkdir -p prompts
mkdir -p docs
mkdir -p api
mkdir -p diagrams
```

## config.toml Snippet
```toml
[docforge]
output_dir = "docs"
api_output = "api"
diagram_output = "diagrams"
recheck_on_change = true
compaction_trigger = ["git:commit", "file:modify"]

[agents.docforge-overseer]
model = "hy3"
max_turns = 50

[agents.docforge-apidoc]
model = "devstral-2"
write_file = "always"

[agents.docforge-diagrams]
model = "hy3"
max_turns = 40
```

## Phases Table (6 Phases)
| Phase | Name | Agent | Description |
|-------|------|-------|-------------|
| 1 | Codebase Survey | Overseer | Survey existing docs, identify gaps vs code+spec |
| 2 | API Reference | apidoc | Generate API docs from signatures and spec contracts |
| 3 | Inline Docstrings | Overseer | Add/update docstrings on public interfaces |
| 4 | Architecture Diagrams | diagrams | Generate structure and flow diagrams |
| 5 | README Sync | Overseer | Sync README and docs with actual behavior |
| 6 | Continuity Check | Overseer | Recheck docs on change, update stale sections |

## Core Doctrine
1. **Code as Truth**: Source code is the primary source of truth; spec validates intent.
2. **Continuous Recheck**: Docs must be revalidated on every compaction or code change.
3. **Public-First**: Focus on public APIs and interfaces; internals are secondary.
4. **Diagram-Driven**: Architecture diagrams must reflect actual module dependencies.
5. **Zero-Stale**: No documentation section may be stale beyond one compaction cycle.

## Output Artifacts
- `docs/` — Main documentation site (markdown + generated HTML)
- `api/` — Auto-generated API references per module
- `diagrams/` — Architecture diagrams (mermaid, plantuml, svg)
- `README.md` — Project overview synced to current behavior
- `docs/continuity.log` — Timestamps of last recheck per module