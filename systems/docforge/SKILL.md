# DocForge — Documentation Generation System

Takes code and test artifacts, generates API references,
inline docs, architecture diagrams, and README sync.

## Input Artifacts

- `TEST_REPORT.md` — REQUIRED (produced by TestForge)
- `IMPLEMENTATION_REPORT.md` — Optional (context from CodeForge)

## Output Artifacts

- `DOC_REPORT.md` — documentation report
- `API_REFERENCE.md` — API reference docs
- `ARCHITECTURE_DIAGRAM.md` — architecture diagrams
- Updated `README.md`

## Phases (Skills)

| Phase | Skill | Description |
|-------|------|-------------|
| 1 | `docforge-01-api-reference-generation` | Generate API reference |
| 2 | `docforge-02-inline-docstring-generation` | Add inline docstrings |
| 3 | `docforge-03-architecture-diagram-generation` | Generate architecture diagrams |
| 4 | `docforge-04-readme-sync` | Sync README with implementation |
| 5 | `docforge-05-doc-continuity-check` | Verify doc consistency |

## Gates

- `tests_ready` — TEST_REPORT.md must exist
- `docs_complete` — DOC_REPORT.md must exist

## Handoff

On successful completion, hands off to **ShipForge** with:
- `DOC_REPORT.md`

## Usage

```bash
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='docforge'); \
          result = o.run_forge('docforge', ctx)"
```
