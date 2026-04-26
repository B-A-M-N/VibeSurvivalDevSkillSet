# ResearchForge System

Solves complex issues through disciplined research. Produces a grounded research packet. No code changes.

## What's Included

| Type | Files | Count |
|------|-------|-------|
| Skills | `skills/researchforge/00-*` through `16-*` | 17 skills |
| Agents | `agents/researchforge/overseer.toml`, `evidence.toml`, `researcher.toml`, `synthesizer.toml` | 4 agents |
| Prompts | `prompts/researchforge-overseer.md`, `evidence.md`, `researcher.md`, `synthesizer.md` | 4 prompts |

## Architecture

```
Problem → ResearchForge Overseer (researchforge-overseer)
  ├── Phase1: Frame Problem (skill 00-problem-intake + 01-context-map)
  │     → Output: PROBLEM_FRAME.md, CONTEXT_MAP.md
  ├── Phase2: Evidence Ledger (delegate to researchforge-evidence)
  │     → Output: EVIDENCE_LEDGER.md, SOURCE_QUALITY_REPORT.md
  ├── Phase3: Hypotheses (delegate to researchforge-evidence)
  │     → Output: HYPOTHESIS_MATRIX.md, DISCONFIRMATION_REPORT.md
  ├── Phase4: Targeted Research (delegate to researchforge-researcher)
  │     → Output: RESEARCH_PLAN.md, RESEARCH_FINDINGS.md
  ├── Phase5: Contradiction Hunt (delegate to researchforge-evidence)
  │     → Output: CONTRADICTION_REPORT.md
  ├── Phase6: Solution Options (delegate to researchforge-synthesizer)
  │     → Output: SOLUTION_OPTIONS.md, VALIDATION_PLAN.md
  ├── Phase7: Validation Plan (researchforge-synthesizer)
  │     → Output: VALIDATION_PLAN.md
  └── Phase8: Final Packet + Adversarial Review
        → Output: FINAL_RESEARCH_PACKET.md, RESEARCH_REVIEW.md
```

## Execution Graph

```
Problem → AgentLoop.act("researchforge-00-problem-intake")
         ↓
    MiddlewarePipeline: inject Orient context (OS, git, tools available)
         ↓
    LLM: generates PROBLEM_FRAME.md (structured output)
         ↓
    Subagent spawn: researchforge-evidence (evidence + hypotheses)
         ↓
    Subagent spawn: researchforge-researcher (official docs, upstream issues)
         ↓
    Subagent spawn: researchforge-synthesizer (solution options + validation)
         ↓
    Adversarial review: REJECT if evidence weak
         ↓
    Final packet: FINAL_RESEARCH_PACKET.md
```

## Install

```bash
mkdir -p ~/.vibe/skills ~/.vibe/agents ~/.vibe/prompts
cp -r skills/researchforge/* ~/.vibe/skills/
cp -r agents/researchforge/* ~/.vibe/agents/
cp prompts/researchforge-*.md ~/.vibe/prompts/
```

Enable in `~/.vibe/config.toml`:
```toml
agent_paths = ["agents", "agents/specforge", "agents/researchforge"]
enabled_agents = [
  "specforge-overseer", "specforge-analyst", "specforge-architect",
  "researchforge-overseer", "researchforge-evidence",
  "researchforge-researcher", "researchforge-synthesizer",
]
enabled_skills = [
  # ResearchForge (17 skills)
  "researchforge-00-problem-intake",
  # ... through 16-adversarial-research-review
]
```

## Phases

1. **Frame Problem** — clarify the real problem (`00-problem-intake`, `01-context-map`)
2. **Evidence Ledger** — collect and classify evidence (`02-evidence-collection`, `03-source-quality-check`)
3. **Hypotheses** — generate and disconfirm hypotheses (`04-hypothesis-generation`, `05-hypothesis-disconfirmation`)
4. **Targeted Research** — docs, issues, versions, patterns, risks (`06-targeted-research-plan` through `11-risk-research`)
5. **Contradiction Hunt** — find weaknesses in evidence (`12-contradiction-hunt`)
6. **Solution Options** — synthesize min 2 options (`13-solution-option-synthesis`)
7. **Validation Plan** — define proof (`14-validation-plan-generation`)
8. **Final Packet** — assemble research packet (`15-final-research-packet`)
9. **Adversarial Review** — reject if evidence weak (`16-adversarial-research-review`)

## Output Artifacts

- `FINAL_RESEARCH_PACKET.md` — Problem Frame, Context Map, Evidence Ledger, Hypothesis Matrix, Research Findings, Contradiction Report, Solution Options, Validation Plan, Confidence Assessment
- `RESEARCH_REVIEW.md` — PASS/REJECT verdict with audit details

## Core Doctrine

```
Problem first.               (PROBLEM_FRAME.md must be coherent)
Evidence second.             (collect before hypothesizing)
Hypotheses third.            (every hypothesis needs disconfirmation criteria)
Recommendations last.         (no recommendation without evidence)
No implementation.            (research only, no code changes)
```
