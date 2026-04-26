---
name: specforge-21-adversarial-spec-review
description: |
  SpecForge — Adversarial Spec Review. Audits the spec and scenarios
  for contradictions, gaps, untestable rules, and implementation leakage.
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Bash
  - AskUserQuestion
---

# SpecForge: Adversarial Spec Review

**Role:** `adversarial-reviewer` — Phase7

## Mission

Tear the spec apart. Find contradictions, untestable rules, vague phrases, implementation leakage, missing failure cases, and gaps. Reject the spec if it's not ready.

## When to Use

- Phase7 of SpecForge (Adversarial Review)
- After MASTER_SPEC.md and SCENARIOS.md are complete
- Before final spec assembly

## Review Checklist

```
CONTRADICTIONS:
  [ ] Two rules that cannot both be true
  [ ] Requirement A says MUST, Requirement B says MUST NOT
  [ ] Conflicting authority boundaries
  [ ] State machine transitions that conflict

MISSING_AUTHORITY_BOUNDARIES:
  [ ] Role can "manage" something (too vague)
  [ ] Permission without conditions
  [ ] No violation response defined
  [ ] System actor authority undefined

UNTESTABLE_RULES:
  [ ] "User-friendly" (not testable)
  [ ] "Fast response" (no metric defined)
  [ ] "Intuitive UI" (not testable)
  [ ] "Reasonable timeout" (not quantified)

IMPLEMENTATION_LEAKAGE:
  [ ] Spec says "use Redis" (implementation choice, not requirement)
  [ ] Spec says "React frontend" (implementation choice)
  [ ] "Current code does X" treated as truth

VAGUE_PHRASES:
  [ ] "etc.", "and so on", "TBD", "TBC"
  [ ] "Appropriate", "reasonable", "as needed"
  [ ] "May", "might", "could" (use MUST/SHOULD)

MISSING_FAILURE_CASES:
  [ ] No kill test for critical invariant
  [ ] Happy path exists but no error path
  [ ] State transition has no failure branch

MISSING_INVARIANTS:
  [ ] Data model has no integrity invariants
  [ ] Permission model has no enforcement invariant
  [ ] No invariants for critical paths

MISSING_SCENARIO_COVERAGE:
  [ ] Requirement has no scenario
  [ ] Invariant has no kill test
  [ ] Error has no trigger scenario

UNSTATED_USER_DECISIONS:
  [ ] "Admin can do anything" — which admin? which actions?
  [ ] "Users can share" — what can they share? with whom?
```

## Instructions

1. **Read Master Spec**: Load MASTER_SPEC.md. Read every PART.
2. **Read Scenarios**: Load SCENARIOS.md. Check every scenario.
3. **Run Checklist**: Go through each item. Document findings.
4. **Reject if Critical**: If any critical item fails, reject the spec.
5. **Report Findings**: Write `ADVERSARIAL_REVIEW.md` with:
   - PASS / REJECT verdict
   - List of issues by severity (critical, major, minor)
   - Recommended fixes
6. **If REJECT**: Specify which agent must fix what.

## Output

`ADVERSARIAL_REVIEW.md` with PASS/REJECT verdict.

**If you can't break the spec, you're not trying hard enough.**
