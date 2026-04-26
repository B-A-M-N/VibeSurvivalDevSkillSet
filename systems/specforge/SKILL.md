# SpecForge — Specification Creation System

Takes a `GOAL.md` and produces `MASTER_SPEC.md` with full
acceptance criteria, edge cases, and constraints.

## Input Artifacts

- `GOAL.md` — REQUIRED (user-provided or from issue)

## Output Artifacts

- `MASTER_SPEC.md` — complete specification
- `ACCEPTANCE_CRITERIA.md` — testable acceptance criteria
- `EDGE_CASES.md` — edge cases and error scenarios

## Phases (Skills)

| Phase | Skill | Description |
|-------|------|-------------|
| 1 | `specforge-00-intake-goal-clarification` | Clarify goal, extract requirements |
| 2 | `specforge-01-existing-document-review` | Review existing documentation |
| 3 | `specforge-02-implementation-survey` | Survey existing implementation |
| 4 | `specforge-03-intent-gap-analysis` | Identify gaps between intent and reality |
| 5 | `specforge-04-research-plan-generation` | Plan research for unknowns |
| 6 | `specforge-05-architecture-exploration` | Explore architecture options |
| 7 | `specforge-06-spec-template-selection` | Select appropriate spec template |
| 8 | `specforge-07-spec-draft-generation` | Generate spec draft |
| 9 | `specforge-08-cross-team-review-simulation` | Simulate cross-team review |
| 10 | `specforge-09-constraint-injection` | Inject constraints and invariants |
| 11 | `specforge-10-edge-case-generation` | Generate edge cases |
| 12 | `specforge-11-acceptance-criteria-definition` | Define acceptance criteria |
| 13 | `specforge-12-spec-review-checklist` | Run spec review checklist |
| 14 | `specforge-13-spec-validation-and-refinement` | Validate and refine spec |
| 15 | `specforge-14-final-spec-packaging` | Package final spec |
| 16 | `specforge-15-spec-handoff-preparation` | Prepare for handoff |

## Gates

- `goal_defined` — GOAL.md must exist
- `spec_complete` — MASTER_SPEC.md must exist

## Handoff

On successful completion, hands off to **ResearchForge** with:
- `MASTER_SPEC.md`

## Usage

```bash
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='specforge'); \
          result = o.run_forge('specforge', ctx)"
```
