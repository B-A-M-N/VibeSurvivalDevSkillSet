---
name: invariant-checking
description: Every file write checked against spec invariants before write_file allowed
trigger: need to validate code against spec invariants before committing changes
---

## Step-by-Step Instructions

### 1. Invariant Extraction
- Review MASTER_SPEC.md for all defined invariants
- Extract business rules and constraints
- Document cross-entity and cross-module invariants
- Note timing and sequencing requirements

### 2. Pre-Write Validation
- Check proposed changes against all relevant invariants
- Verify data structure constraints
- Validate API contract compliance
- Ensure state machine transitions are valid

### 3. Cross-Module Invariant Checking
- Verify invariants across module boundaries
- Check integration points for constraint compliance
- Validate data flow between components
- Ensure shared state consistency

### 4. Automated Validation
- Implement or use existing validation tools
- Create test cases for each invariant
- Run validation before and after changes
- Document validation results

### 5. Exception Handling
- Identify cases where invariants may be temporarily violated
- Document rollback or recovery procedures
- Plan for constraint relaxation if needed
- Prepare justification for any violations

### 6. Invariant Documentation
- Maintain updated invariant registry
- Document the impact of each invariant
- Note relationships between invariants
- Prepare invariant violation scenarios

### 7. Validation Reporting
- Generate detailed validation reports
- Document any near-violations or close calls
- Prepare recommendations for strengthening invariants
- Create invariant compliance metrics

### 8. Continuous Monitoring
- Set up ongoing invariant validation
- Monitor for invariant drift over time
- Alert on potential violations
- Prepare invariant update procedures