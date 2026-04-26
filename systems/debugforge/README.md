# DebugForge — Structured Bug Squashing System

## Description
Reproduces bugs, isolates root cause, generates fix options, validates against scenario matrix

## How It Maps to Mistral-Vibe Table
| Phase | Mistral-Vibe Mapping |
|-------|---------------------|
| Issue Intake | Parse and classify severity |
| Reproduction | Create minimal reproduction case |
| Bisection Isolation | Narrow down root cause via changes |
| Fix Options | Generate and evaluate fix strategies |
| Scenario Validation | Validate against SCENARIOS.md and MASTER_SPEC.md |
| Fix Application | Apply fix and verify |
| Verification | Confirm resolution and update tests |

## Architecture Flow
```
Issue → reproduce → isolate → fix options → validate → verify
    ↓        ↓          ↓           ↓            ↓         ↓
[report] [script]  [bisection]  [generation] [matrix] [execution]
```

## Agents Table
| Agent | Role | Model |
|-------|------|-------|
| debugforge-overseer | Orchestrator, manages bug lifecycle | opus |
| debugforge-reproducer | Bug reproducer, creates minimal test case | devstral-2 |
| debugforge-fixer | Fix generator, creates fix options | hy3 |

## Install Bash Commands
```bash
# Create directory structure
mkdir -p /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/systems/debugforge/{agents,prompts}
mkdir -p /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/skills/00-issue-intake
mkdir -p /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/skills/01-reproduction
mkdir -p /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/skills/02-bisection-isolation
mkdir -p /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/skills/03-root-cause-analysis
mkdir -p /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/skills/04-fix-option-generation
mkdir -p /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/skills/05-scenario-validation
mkdir -p /home/bamn/Mistral-Vibe-Survival-Dev-Skill-Set/skills/06-fix-application

# Install required tools
pip install toml
```

## config.toml Snippet
```toml
[debugforge]
overseer_model = "opus"
reproducer_model = "devstral-2"
fixer_model = "hy3"
max_turns_overseer = 60
max_turns_reproducer = 40
max_turns_fixer = 50
scenarios_file = "SCENARIOS.md"
spec_file = "MASTER_SPEC.md"
```

## Phases Table (7 Phases)
| Phase | Name | Description |
|-------|------|-------------|
| 00 | Issue Intake | Parse issue report, extract repro steps, classify severity |
| 01 | Reproduction | Reproduce bug reliably, create minimal reproduction case |
| 02 | Bisection Isolation | Isolate root cause via bisection-like search of recent changes |
| 03 | Root Cause Analysis | Deep analysis of root cause, gather evidence |
| 04 | Fix Option Generation | Generate minimum 2 fix options with tradeoff analysis |
| 05 | Scenario Validation | Validate each fix option against SCENARIOS.md and MASTER_SPEC.md |
| 06 | Fix Application | Apply chosen fix, verify it works, update tests |

## Core Doctrine
1. **Reproducibility First**: Every bug must be reproducible before analysis
2. **Minimal Case**: Reduce test cases to the smallest failing scenario
3. **Bisection Search**: Use binary search approach to isolate root cause
4. **Multiple Options**: Generate at least 2 fix options for evaluation
5. **Scenario Validation**: All fixes must pass scenario matrix validation
6. **Evidence-Based**: Root cause must be backed by concrete evidence
7. **Test-Driven Fix**: Fixes must be validated through test updates

## Output Artifacts
- `bug_report.md` - Parsed issue with repro steps
- `reproduction_case.py` - Minimal reproduction script
- `bisection_log.md` - Search path and root cause isolation
- `root_cause_analysis.md` - Evidence-backed root cause
- `fix_options.md` - Multiple fix strategies with tradeoffs
- `validation_matrix.md` - Scenario validation results
- `fix_application.md` - Applied fix and verification results
- `scenario_matrix.md` - Cross-reference of fixes vs scenarios