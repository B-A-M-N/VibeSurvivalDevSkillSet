# Fix Application Skill

name: 06-fix-application
description: Apply chosen fix, verify it works, update tests
trigger: when fix is validated against scenarios

## Step-by-Step Instructions

### 1. Prepare Fix Application
- Review fix implementation plan
- Backup current state (git commit)
- Prepare test environment
- Ensure rollback capability

### 2. Apply Fix
- Implement the chosen fix option
- Make minimal necessary changes
- Follow code quality standards
- Update related code if needed

### 3. Run Comprehensive Tests
- Execute unit tests
- Run integration tests
- Perform regression testing
- Validate scenario coverage

### 4. Update Tests
- Add tests for the fix
- Update existing tests if affected
- Ensure test coverage
- Document test changes

### 5. Verify and Document
```bash
# Apply fix
git apply fix.patch
# Or make changes manually

# Run tests
pytest tests/ -v
# Or use custom test runner

# Verify results
echo "Exit code: $?"

# Document
cat > fix_application.md << 'EOF'
## Fix Application

### Fix Applied
[Description of fix]

### Changes Made
- File 1: [changes]
- File 2: [changes]

### Tests Updated
- Test 1: [updated]
- Test 2: [updated]

### Verification Results
- All tests pass: ✓
- Scenarios validated: [list]
- Performance: [metrics]

### Rollback Plan
[How to revert if needed]
EOF
```

## Application Methods

### Direct Code Changes
- Edit source files directly
- Update function implementations
- Modify logic as needed

### Configuration Changes
- Update config files
- Change environment variables
- Adjust parameters

### Test Updates
- Add new test cases
- Update existing tests
- Fix flaky tests
- Improve test coverage

## Verification Checklist
- [ ] Fix applied correctly
- [ ] All tests pass
- [ ] No regressions introduced
- [ ] Performance acceptable
- [ ] Backward compatible
- [ ] Documentation updated
- [ ] Tests updated

## Rollback Strategy
1. Keep git history
2. Create backup before applying
3. Document rollback steps
4. Test rollback process
5. Verify rollback works

## Best Practices
- Make atomic changes when possible
- Test incrementally
- Document everything
- Keep fixes minimal
- Verify thoroughly