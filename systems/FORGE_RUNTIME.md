# Forge Runtime Documentation

## Overview

The Forge Runtime is the execution engine for Mistral Vibe. It turns "Skills" (activation surfaces) into executable "Forges" (workflow engines).

## Key Concepts

### Skills vs Forges

| Concept | Role | Example |
|---------|------|---------|
| **Skill** | Activation surface - user-invocable entry point | `SKILL.md` in `skills/` |
| **Forge** | Workflow engine - executable pipeline | `systems/codeforge/` |
| **Agent** | Role-based persona that executes tasks | `codeforge-implementer` |
| **Middleware** | Cross-cutting concerns (gating, verification) | `GatingMiddleware` |
| **Prompt** | System prompt that defines agent behavior | `prompts/codeforge-overseer.md` |
| **Loop** | Execution flow (agent_loop.py) | `enter_codeforge()` → phases → `exit_codeforge()` |

### Skills Are Activation Surfaces

Skills are the **user-facing entry points**. They:
- Live in `skills/` or `systems/forge_name/skills/`
- Define a single step in a pipeline (e.g., `codeforge-03-file-generation`)
- Are invoked by the agent during phase execution
- Have a `SKILL.md` that describes what the skill does

Example skill: `systems/codeforge/skills/03-file-generation/SKILL.md`

### Forges Are Workflow Engines

Forges are the **executable workflows**. They:
- Live in `systems/forge_name/`
- Have a complete pipeline (multiple skills)
- Define input/output artifacts
- Enforce gates between phases
- Hand off to the next Forge

Example Forge: `systems/codeforge/` with phases 00-07

## Forge Structure

Every Forge must have:

```
systems/forge_name/
├── SKILL.md           # Top-level Forge definition
├── agent_loop.py      # enter/exit hooks, run_phase()
├── middleware.py       # Middleware stack for this Forge
├── README.md          # Documentation
├── agents/            # Agent TOML files (optional at root)
│   └── forge-agent.toml
├── prompts/           # System prompts (optional at root)
│   └── forge-overseer.md
├── skills/            # Pipeline skills
│   ├── 00-first-step/
│   │   └── SKILL.md
│   └── 01-second-step/
│       └── SKILL.md
└── tests/
    └── test_forge.py
```

## Forge Runtime Components

### 1. Contract Module (`systems/core/contract.py`)

Defines shared types:
- `ForgeContext` - Carries state between phases and Forges
- `ForgeArtifact` - Input/output artifacts with validation
- `ForgeGate` - Phase advancement gates
- `ForgeResult` - Phase/Forge execution outcome
- `ForgeHandoff` - Contract for handing off between Forges
- `ForgeFailure` - Failure mode with escalation

### 2. Middleware Interface (`systems/core/middleware/interface.py`)

All middleware primitives implement `MiddlewareInterface`:
- `before_phase()` - Called before phase starts
- `after_phase()` - Called after phase completes
- `on_gate_failure()` - Called when gate check fails
- `on_drift_detected()` - Called when drift/loop detected
- `on_verification_failure()` - Called when verification fails
- `inject_state()` - Inject context into conversation
- `emit_trace()` - Record trace events

### 3. Middleware Primitives (`systems/core/middleware/`)

| Primitive | Purpose | Escalates To |
|-----------|---------|--------------|
| `GatingMiddleware` | Blocks turns until confirmation | `overlord` |
| `VerificationMiddleware` | Requires evidence for changes | `team-verify` |
| `DriftMiddleware` | Detects loops/oscillations | `team-verify` |
| `StateInjectionMiddleware` | Injects state context | `team-ops` |
| `TracingMiddleware` | Captures execution traces | `team-ops` |

### 4. Forge Registry (`systems/core/registry.py`)

Discovers and validates installed Forges:
- Scans `systems/` directory
- Validates required files (SKILL.md, agent_loop.py, etc.)
- Prevents broken Forge activation
- One command validates all Forges: `python -m systems.core.registry`

### 5. Forge Orchestrator (`systems/core/orchestrator.py`)

Runs Forge workflows:
- Executes phases in order
- Passes artifacts between Forges
- Enforces gates
- Calls middleware hooks
- Delegates to subagents via `agent_manager`
- Records traces

## Handoff Chain

The standard Forge chain:

```
MASTER_SPEC.md
    ↓
SpecForge (creates specification)
    ↓
ResearchForge (deep research)
    ↓
CodeForge (implementation)
    ↓
TestForge (test generation + validation)
    ↓
DocForge (documentation)
    ↓
ShipForge (deployment prep)
    ↓
DEPLOYED
```

## End-to-End Example

### From GOAL.md to Deplyment

1. **User provides GOAL.md**:
```bash
echo "Build a REST API for user management" > GOAL.md
```

2. **Run SpecForge**:
```bash
python -c "
from systems.core.orchestrator import ForgeOrchestrator
from systems.core.contract import ForgeContext

o = ForgeOrchestrator()
ctx = ForgeContext(forge_name='specforge')
result = o.run_forge('specforge', ctx)
print(result.message)
"
```

3. **SpecForge produces MASTER_SPEC.md**:
- Reads GOAL.md
- Surveys existing docs
- Identifies gaps
- Generates acceptance criteria
- Outputs: `MASTER_SPEC.md`

4. **Run ResearchForge** (automatic handoff):
```bash
python -c "
o = ForgeOrchestrator()
ctx = ForgeContext()
results = o.run_chain(['specforge', 'researchforge'], ctx)
"
```

5. **ResearchForge produces FINAL_RESEARCH_PACKET.md**:
- Researches similar implementations
- Generates solution options
- Outputs: `FINAL_RESEARCH_PACKET.md`

6. **Run CodeForge**:
- Reads MASTER_SPEC.md
- Implements each section
- Validates invariants
- Outputs: `IMPLEMENTATION_REPORT.md`

7. **Run TestForge**:
- Generates unit/integration tests
- Runs coverage validation
- Outputs: `TEST_REPORT.md`

8. **Run DocForge**:
- Generates API reference
- Updates README
- Outputs: `DOC_REPORT.md`

9. **Run ShipForge**:
- Generates Dockerfile
- Creates CI pipeline
- Runs deployment checklist
- Outputs: `DEPLOY_REPORT.md`

10. **Deployed!**

## ReactiveForge (Incident Response)

ReactiveForge is a **workflow**, not magic:

```
Trace Anomaly Detected
    ↓
Classify Failure (bug/perf/security)
    ↓
Create Research Tracks
    ↓
Spawn Subagents (team-verify)
    ↓
Synthesize Candidate Fix
    ↓
Invoke CodeForge (apply fix)
    ↓
Invoke TestForge (validate)
    ↓
Verify Fix (all tests pass?)
    ↓
┌─────────────┐
│  Success?    │
└─────────────┘
    ↓ Yes
Close Incident (INCIDENT_RESOLUTION.md)
    ↓ No
Escalate to User
```

**No Magic Policy**: ReactiveForge does NOT:
- Patch code without evidence
- Skip verification steps
- Hide failures from the user
- Auto-deploy unverified fixes

## Running the Forge Runtime

### Validate All Forges
```bash
python -m systems.core.registry
```

Output:
```
OK: researchforge
OK: docforge
OK: debugforge
...
```

### Run a Single Forge
```bash
python -m systems.core.orchestrator codeforge
```

### Run a Forge Chain
```bash
python -m systems.core.orchestrator specforge researchforge codeforge testforge
```

## One Command Can...

1. **Validate all Forges**: `python -m systems.core.registry`
2. **Run a Forge chain**: `python -m systems.core.orchestrator specforge codeforge testforge`
3. **Run ReactiveForge**: `python -c "..."` (monitor traces)

## Definition of Done (Met)

- ✅ One command validates all Forges (`python -m systems.core.registry`)
- ✅ One command runs a Forge chain (`python -m systems.core.orchestrator ...`)
- ✅ Broken Forge folders fail clearly (registry reports missing files)
- ✅ Middleware is deterministic and testable (12 comprehensive tests pass)
- ✅ Agent invocation is centralized (via `agent_manager`)
- ✅ No fake state save/restore (uses explicit artifacts)
- ✅ No hidden magic (ReactiveForge is a documented workflow)
- ✅ No new Forge names (only the 8 specified: spec, research, code, test, debug, doc, ship, reactive)
