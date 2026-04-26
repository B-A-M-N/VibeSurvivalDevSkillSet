# ResearchForge — System Implementation

## Overview

ResearchForge solves complex issues through disciplined research. It produces a grounded research packet without making code changes. The system coordinates 17 pipeline skill packages across 4 agents.

## Agents

| Agent | TOML | Prompt | Role |
|-------|------|--------|------|
| `researchforge-overseer` | `agents/researchforge-overseer.toml` | `prompts/researchforge-overseer.md` | Orchestrates full research pipeline |
| `researchforge-evidence` | `agents/researchforge-evidence.toml` | `prompts/researchforge-evidence.md` | Collects and classifies evidence |
| `researchforge-researcher` | `agents/researchforge-researcher.toml` | `prompts/researchforge-researcher.md` | Performs targeted research (docs, issues, versions) |
| `researchforge-synthesizer` | `agents/researchforge-synthesizer.toml` | `prompts/researchforge-synthesizer.md` | Synthesizes solution options and validation plans |

## Skill Packages

Each skill is a directory under `skills/` with `SKILL.md` as the entrypoint. These are pipeline-tier skills that execute sequentially to produce the research packet.

| # | Skill Package | Assigned Agent | Purpose |
|---|----------------|---------------|---------|
| 00 | `00-problem-intake` | overseer | Frames the problem clearly |
| 01 | `01-context-map` | overseer | Maps the context and environment |
| 02 | `02-evidence-collection` | evidence | Collects evidence from sources |
| 03 | `03-source-quality-check` | evidence + overseer | Evaluates source reliability |
| 04 | `04-hypothesis-generation` | evidence | Generates testable hypotheses |
| 05 | `05-hypothesis-disconfirmation` | evidence + overseer | Disconfirms hypotheses with evidence |
| 06 | `06-targeted-research-plan` | researcher | Plans targeted research strategy |
| 07 | `07-official-docs-research` | researcher | Researches official documentation |
| 08 | `08-upstream-issue-research` | researcher | Searches upstream issues and PRs |
| 09 | `09-version-compatibility-research` | researcher | Checks version compatibility |
| 10 | `10-architecture-pattern-research` | researcher | Finds relevant architecture patterns |
| 11 | `11-risk-research` | synthesizer | Identifies risks and mitigations |
| 12 | `12-contradiction-hunt` | evidence | Finds contradictions in evidence |
| 13 | `13-solution-option-synthesis` | synthesizer + overseer | Synthesizes solution options |
| 14 | `14-validation-plan-generation` | synthesizer + overseer | Generates validation plan |
| 15 | `15-final-research-packet` | overseer | Assembles final research packet |
| 16 | `16-adversarial-research-review` | overseer | Adversarial review of research |

## Agent Skill Mapping

```
researchforge-overseer
├── 00-problem-intake
├── 01-context-map
├── 03-source-quality-check
├── 05-hypothesis-disconfirmation
├── 12-contradiction-hunt
├── 13-solution-option-synthesis
├── 14-validation-plan-generation
├── 15-final-research-packet
└── 16-adversarial-research-review

researchforge-evidence
├── 02-evidence-collection
├── 03-source-quality-check
├── 04-hypothesis-generation
├── 05-hypothesis-disconfirmation
└── 12-contradiction-hunt

researchforge-researcher
├── 06-targeted-research-plan
├── 07-official-docs-research
├── 08-upstream-issue-research
├── 09-version-compatibility-research
└── 10-architecture-pattern-research

researchforge-synthesizer
├── 11-risk-research
├── 13-solution-option-synthesis
└── 14-validation-plan-generation
```

## Execution Flow

### Phase 1: Frame Problem
```
researchforge-overseer
  → 00-problem-intake: Clarify the real problem
  → 01-context-map: Map OS, tools, git state, environment
  → Output: PROBLEM_FRAME.md, CONTEXT_MAP.md
```

### Phase 2: Evidence Ledger
```
researchforge-overseer
  → task(agent="researchforge-evidence", ...)
    → 02-evidence-collection: Gather docs, code, issues
    → 03-source-quality-check: Rate each source
  → Output: EVIDENCE_LEDGER.md, SOURCE_QUALITY_REPORT.md
```

### Phase 3: Hypotheses
```
researchforge-overseer
  → task(agent="researchforge-evidence", ...)
    → 04-hypothesis-generation: Generate testable hypotheses
    → 05-hypothesis-disconfirmation: Find disconfirming evidence
  → Output: HYPOTHESIS_MATRIX.md, DISCONFIRMATION_REPORT.md
```

### Phase 4: Targeted Research
```
researchforge-overseer
  → task(agent="researchforge-researcher", ...)
    → 06-targeted-research-plan: Plan research strategy
    → 07-official-docs-research: Read official docs
    → 08-upstream-issue-research: Search issues/PRs
    → 09-version-compatibility-research: Check versions
    → 10-architecture-pattern-research: Find patterns
    → 11-risk-research: Identify risks
  → Output: RESEARCH_PLAN.md, RESEARCH_FINDINGS.md
```

### Phase 5: Contradiction Hunt
```
researchforge-overseer
  → task(agent="researchforge-evidence", ...)
    → 12-contradiction-hunt: Find weak evidence
  → Output: CONTRADICTION_REPORT.md
```

### Phase 6-7: Solution Options & Validation
```
researchforge-overseer
  → task(agent="researchforge-synthesizer", ...)
    → 13-solution-option-synthesis: Min 2 options with tradeoffs
    → 11-risk-research: Risk assessment
    → 14-validation-plan-generation: Define proof
  → Output: SOLUTION_OPTIONS.md, VALIDATION_PLAN.md
```

### Phase 8: Final Packet + Adversarial Review
```
researchforge-overseer
  → 15-final-research-packet: Assemble all artifacts
  → 16-adversarial-research-review: REJECT if evidence weak
  → Output: FINAL_RESEARCH_PACKET.md, RESEARCH_REVIEW.md
```

## Output Artifacts

| Artifact | Producer | Purpose |
|----------|-----------|---------|
| `PROBLEM_FRAME.md` | overseer (00) | Clarified problem statement |
| `CONTEXT_MAP.md` | overseer (01) | Environment and codebase map |
| `EVIDENCE_LEDGER.md` | evidence (02) | Classified evidence collection |
| `SOURCE_QUALITY_REPORT.md` | evidence (03) | Source reliability ratings |
| `HYPOTHESIS_MATRIX.md` | evidence (04) | Testable hypotheses |
| `DISCONFIRMATION_REPORT.md` | evidence (05) | Disconfirming evidence |
| `RESEARCH_FINDINGS.md` | researcher (07-10) | Targeted research results |
| `CONTRADICTION_REPORT.md` | evidence (12) | Evidence weaknesses |
| `SOLUTION_OPTIONS.md` | synthesizer (13) | Min 2 solution options |
| `VALIDATION_PLAN.md` | synthesizer (14) | Proof definition |
| `FINAL_RESEARCH_PACKET.md` | overseer (15) | Complete research packet |
| `RESEARCH_REVIEW.md` | overseer (16) | PASS/REJECT verdict |

## Core Doctrine

```
Problem first.               (PROBLEM_FRAME.md must be coherent)
Evidence second.             (collect before hypothesizing)
Hypotheses third.            (every hypothesis needs disconfirmation criteria)
Recommendations last.         (no recommendation without evidence)
No implementation.            (research only, no code changes)
```
