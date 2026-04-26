---
name: invariant-checking
description: Every file write checked against spec invariants before write_file allowed
---

## Steps to Enforce Invariants with write_file

1. **Invariant Extraction**
   - Review MASTER_SPEC.md for all defined invariants (business rules, constraints)
   - Extract cross-entity and cross-module invariants
   - Document timing and sequencing requirements
   - Create invariant registry with unique IDs (INV-001, INV-002, etc.)

2. **Pre-Write Validation Middleware**
   - Implement validation layer that intercepts all write_file calls
   - Check proposed changes against ALL relevant invariants before allowing write
   - Verify data structure constraints (types, ranges, required fields)
   - Validate API contract compliance (endpoints, schemas, contracts)
   - Ensure state machine transitions are valid (current state + transition → valid next state)

3. **Cross-Module Invariant Checking**
   - Verify invariants across module boundaries (shared state, APIs)
   - Check integration points for constraint compliance
   - Validate data flow between components (input/output schemas)
   - Ensure shared state consistency (no race conditions, stale data)

4. **Automated Validation Implementation**
   - Create invariant validation functions for each rule type
   - Implement unit tests for each invariant (positive and negative cases)
   - Run validation before write_file execution (pre-check)
   - Run validation after write_file execution (post-check)
   - Log validation results with file paths and invariant IDs

5. **Exception Handling Strategy**
   - Define temporary violation scenarios (migration windows, emergency patches)
   - Document rollback procedures to restore invariant compliance
   - Plan constraint relaxation only with explicit approval and audit trail
   - Prepare justification documentation for any permitted violations

6. **Invariant Documentation & Tracking**
   - Maintain updated invariant registry with status (active, deprecated, violated)
   - Document impact of each invariant (severity, affected modules)
   - Track invariant relationships and dependencies
   - Prepare invariant violation scenarios for testing

7. **Validation Reporting**
   - Generate invariant compliance reports after each write operation
   - Document any near-violations or close calls with root cause
   - Prepare recommendations for strengthening weak invariants
   - Create metrics dashboard (compliance rate, violation trends)

8. **Continuous Monitoring & Alerts**
   - Set up automated invariant validation on every file write
   - Monitor for invariant drift over time (historical analysis)
   - Configure alerts for potential violations (blocking, warning levels)
   - Prepare invariant update procedures for spec changes

## Invariant Validation Example

For each write_file operation:
```
Pre-write checks:
- INV-001: balance >= 0 → validate new balance calculation
- INV-002: email unique → check against all existing records
- INV-003: API schema compliance → validate request/response format
- INV-004: state transition valid → verify current_state + action → next_state

Post-write verification:
- Re-run all invariants against updated data
- Verify no cross-module violations introduced
- Confirm integration points remain functional
```

## write_file Integration

The write_file tool must be wrapped with invariant validation:
1. Capture proposed changes
2. Run pre-write validation suite
3. If all invariants pass → execute write_file
4. If violations detected → reject write, log error, suggest fixes
5. Post-write validation and reporting