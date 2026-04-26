# ResearchForge — Deep Research System

Takes `PROBLEM_FRAME.md` (from SpecForge) and conducts deep research
to produce evidence-based solution options.

## Input Artifacts

- `PROBLEM_FRAME.md` — REQUIRED (produced by SpecForge)
- `EXISTING_SPEC.md` — Optional reference

## Output Artifacts

- `RESEARCH_PLAN.md` — research strategy and track definitions
- `EVIDENCE_*.md` — collected evidence files
- `SOLUTION_OPTIONS.md` — candidate solutions with pros/cons
- `FINAL_RESEARCH_PACKET.md` — complete research summary

## Phases (Skills)

| Phase | Skill | Description |
|-------|------|-------------|
| 1 | `researchforge-00-problem-intake` | Parse problem frame, extract research questions |
| 2 | `researchforge-01-context-map` | Map existing codebase context |
| 3 | `researchforge-02-evidence-collection` | Collect initial evidence |
| 4 | `researchforge-03-source-quality-check` | Validate source credibility |
| 5 | `researchforge-04-hypothesis-generation` | Generate candidate hypotheses |
| 6 | `researchforge-05-hypothesis-disconfirmation` | Try to disconfirm hypotheses |
| 7 | `researchforge-06-targeted-research-plan` | Plan deeper research tracks |
| 8 | `researchforge-07-official-docs-research` | Research official documentation |
| 9 | `researchforge-08-upstream-issue-research` | Check upstream issues/PRs |
| 10 | `researchforge-09-version-compatibility-research` | Check version compat |
| 11 | `researchforge-10-architecture-pattern-research` | Find similar patterns |
| 12 | `researchforge-11-risk-research` | Identify risks and mitigations |
| 13 | `researchforge-12-contradiction-hunt` | Find conflicting evidence |
| 14 | `researchforge-13-solution-option-synthesis` | Synthesize solution options |
| 15 | `researchforge-14-validation-plan-generation` | Plan how to validate |
| 16 | `researchforge-15-final-research-packet` | Package final research |
| 17 | `researchforge-16-adversarial-research-review` | Adversarial review |

## Gates

- `problem_defined` — PROBLEM_FRAME.md must exist
- `evidence_collected` — At least 3 evidence files must exist
- `research_complete` — FINAL_RESEARCH_PACKET.md must exist

## Handoff

On successful completion, hands off to **CodeForge** with:
- `FINAL_RESEARCH_PACKET.md`
- `SOLUTION_OPTIONS.md`

## Usage

```bash
python -c "from systems.core.orchestrator import ForgeOrchestrator; \
          from systems.core.contract import ForgeContext; \
          o = ForgeOrchestrator(); \
          ctx = ForgeContext(forge_name='researchforge'); \
          result = o.run_forge('researchforge', ctx)"
```
