# TestForge — Spec-Driven Test Generation System
Takes MASTER_SPEC.md + SCENARIOS.md + implementation, generates comprehensive test suites

## How It Maps to Mistral-Vibe table (concept → component → file path)
| Concept                | Component               | File Path                                                    |
|------------------------|-------------------------|--------------------------------------------------------------|
| Master Specification   | spec_parser             | systems/testforge/spec/MASTER_SPEC.md                        |
| Scenario Definitions   | scenario_parser         | systems/testforge/spec/SCENARIOS.md                          |
| Unit Test Generation   | unit_generator          | skills/02-unit-test-generation/SKILL.md                      |
| Kill Test Generation   | kill_generator          | skills/03-kill-test-generation/SKILL.md                      |
| Integration Test Gen.  | integration_generator   | skills/04-integration-test-generation/SKILL.md               |
| Fuzz Target Generation | fuzz_generator          | skills/05-fuzz-target-generation/SKILL.md                    |
| Coverage Validation    | coverage_validator      | skills/06-coverage-validation/SKILL.md                       |

## Architecture Flow (ASCII diagram)
```
+--+       +--+       +--+
|  MASTER_SPEC.md   |       |  SCENARIOS.md     |       |  Implementation   |
+--+       +--+       +--+
          |                         |                         |
          v                         v                         v
  +--+
  |     testforge-                |       +--+
  |     overseer       <--+--+  |     |  Prompt:              |
  |     (plan/delegate)|       |  |  |     |  testforge-           |
  +--+       |  |  |     |  generator            |
                    |  |  +--+--+
                    |  v             +--+
                    |  +--+  |  Prompt:              |
                    +--| testforge-        |  |  testforge-           |
                       | generator        <--+  generator            |
                       +--+       +--+
                                    |
                                    v
                           +--+
                           |  testforge-        |
                           |  coverage          |
                           |  (gates/report)    |
                           +--+
                                    |
                                    v
                           +--+
                           |  Output Artifacts     |
                           +--+
```

## Agents
| Agent                  | Model       | Max Turns | Role                                              |
|------------------------|-------------|-----------|---------------------------------------------------|
| testforge-overseer     | hy3         | 60        | Orchestrator; plans matrix, delegates, gates      |
| testforge-generator    | devstral-2  | 80        | Test writer; unit, integration, kill, fuzz        |
| testforge-coverage     | hy3         | 40        | Coverage analyzer; validates against spec gates   |

## Install bash commands
```bash
cp -a systems/testforge/systems/testforge/...
```

## config.toml snippet
```toml
[agent_paths]
testforge = "systems/testforge/"

[enabled_agents]
testforge-overseer = true
testforge-generator = true
testforge-coverage = true

[enabled_skills]
00-spec-scenario-ingest = true
01-test-strategy-planning = true
02-unit-test-generation = true
03-kill-test-generation = true
04-integration-test-generation = true
05-fuzz-target-generation = true
06-coverage-validation = true
```

## Phases table (7 phases)
| Phase | Name                      | Agent                    | Skill ID               | Output                         |
|-------|---------------------------|--------------------------|------------------------|--------------------------------|
| 1     | Spec & Scenario Ingest    | testforge-overseer       | 00-spec-scenario-ingest| Parsed targets list            |
| 2     | Test Strategy Planning    | testforge-overseer       | 01-test-strategy-planning | Test matrix & priorities     |
| 3     | Unit Test Generation      | testforge-generator      | 02-unit-test-generation| Unit test files                |
| 4     | Kill Test Generation      | testforge-generator      | 03-kill-test-generation| Kill test files                |
| 5     | Integration Test Gen.     | testforge-generator      | 04-integration-test-generation | Integration test files    |
| 6     | Fuzz Target Generation    | testforge-generator      | 05-fuzz-target-generation | Fuzz target files            |
| 7     | Coverage Validation       | testforge-coverage       | 06-coverage-validation | Coverage report & gap list    |

## Core Doctrine
- Spec-driven: all tests derive from MASTER_SPEC.md requirements
- Scenario-backed: every SCENARIO becomes a kill test or edge case
- Coverage gates: no phase completes unless coverage thresholds are met
- Minimal redundancy: each test targets a unique contract/edge
- Fail-fast: hard gates stop the pipeline on first coverage miss

## Output Artifacts
- unit_tests/          — unit test files per module
- kill_tests/          — kill/edge-case tests from SCENARIOS.md
- integration_tests/   — cross-module & API integration tests
- fuzz_targets/        — seed inputs and harnesses for fuzzing
- coverage_report/     — HTML + JSON coverage report
- gaps.md              — uncovered spec requirements list
- test_manifest.json   — inventory of all generated tests