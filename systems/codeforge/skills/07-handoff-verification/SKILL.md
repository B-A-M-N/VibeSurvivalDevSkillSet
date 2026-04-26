---
name: handoff-verification
description: Final spec compliance check, produce IMPLEMENTATION_REPORT.md and handoff to TestForge
---

## Steps to Verify Implementation and Handoff to TestForge

1. **Final Spec Compliance Check**
   - Review MASTER_SPEC.md in entirety with traceability matrix
   - Verify all requirements are implemented (100% coverage)
   - Check for any missed spec sections or edge cases
   - Document any spec deviations with business justifications and risk assessments
   - Create compliance checklist with status (Pass/Fail/Pending)

2. **Comprehensive Invariant Verification**
   - Run all invariant checks across entire codebase using validation middleware
   - Verify zero invariant violations exist in production code
   - Document any near-violations or close calls with root cause analysis
   - Prepare justification documentation for any accepted risks (with stakeholder approval)
   - Generate invariant compliance report with metrics

3. **Implementation Report Generation**
   - Create IMPLEMENTATION_REPORT.md containing:
     - Executive summary with scope, timeline, and deliverables
     - Spec compliance status per requirement (traceability matrix)
     - Invariant verification results with evidence
     - Known issues, limitations, and technical debt
     - Recommendations for future work and enhancements
     - Supporting documentation references (links to specs, test results)
   - Include code quality metrics (test coverage, complexity, linting)
   - Prepare stakeholder review materials

4. **Quality Assurance & Testing**
   - Run comprehensive test suite (unit, integration, contract, end-to-end)
   - Verify all integration tests pass with production-like data
   - Check performance benchmarks against spec requirements
   - Validate error handling, edge cases, and failure scenarios
   - Conduct security and compliance audits

5. **Documentation Review**
   - Verify all code is documented with clear comments and docstrings
   - Check API documentation completeness (OpenAPI/Swagger if applicable)
   - Ensure examples, usage patterns, and migration guides are clear
   - Prepare user and developer documentation for release

6. **TestForge Handoff Preparation**
   - Package all implementation artifacts (code, configs, schemas)
   - Prepare comprehensive handoff documentation (runbooks, deployment guides)
   - Document deployment, configuration, and environment setup requirements
   - Provide TestForge team with context, decisions, and known limitations
   - Establish communication channels for handoff questions

7. **Final Verification & Sign-off**
   - Conduct final review with all stakeholders (product, engineering, QA)
   - Verify TestForge acceptance criteria are fully met
   - Prepare for deployment or additional testing cycles
   - Document handoff completion with sign-off records
   - Establish post-handoff monitoring and support plan

8. **Handoff Execution & Transition**
   - Transfer ownership to TestForge team formally
   - Provide ongoing support during transition period (defined SLA)
   - Document any handoff issues, blockers, or unexpected behaviors
   - Prepare for post-handoff monitoring and feedback incorporation
   - Archive project artifacts and lessons learned

## Implementation Report Structure

# IMPLEMENTATION_REPORT.md

## 1. Executive Summary
- Project scope and objectives
- Timeline and delivery status
- Key achievements and milestones

## 2. Spec Compliance Matrix
- Requirements traceability (ID → status → evidence)
- Coverage percentage by module
- Gap analysis and remediation plan

## 3. Invariant Verification Results
- Compliance metrics (pass/fail counts)
- Violation details (if any) with remediation
- Validation logs and evidence

## 4. Technical Findings
- Architecture decisions and alternatives considered
- Performance test results
- Security and compliance status

## 5. Known Issues & Limitations
- Documented bugs and workarounds
- Technical debt and future improvements
- Dependencies and constraints

## 6. Recommendations
- Short-term fixes for immediate issues
- Long-term architectural improvements
- Testing and monitoring enhancements