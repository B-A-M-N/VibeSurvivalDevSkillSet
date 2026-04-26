# Bisection Isolation Skill

name: 02-bisection-isolation
description: Isolate root cause via bisection-like search of recent changes
trigger: when needing to identify which change introduced a bug

## Step-by-Step Instructions

### 1. Gather Git History
- List recent commits with `git log --oneline`
- Identify time range when bug was introduced
- Get full commit messages and diffs
- Create timeline of changes

### 2. Create Bisection Strategy
- Identify midpoint commit
- Test bug at midpoint
- Narrow search range based on result
- Repeat until isolating single commit

### 3. Execute Bisection
```bash
# Start bisection
git bisect start
git bisect bad HEAD  # Current state is bad
git bisect good <known-good-commit>  # Last known good state

# For each bisection step
git checkout <midpoint-commit>
# Run tests to verify if bug exists
# Mark as good or bad
git bisect good  # Bug not present
git bisect bad   # Bug still present

# Complete bisection
git bisect log
git bisect reset
```

### 4. Analyze Isolated Change
- Examine the specific commit
- Review code diff in detail
- Identify changed variables and logic
- Check for side effects

### 5. Document Search Path
```markdown
## Bisection Log

| Step | Commit | Hash | Status | Notes |
|------|--------|------|--------|-------|
| 1 | Initial bad | abc123 | bad | Bug present |
| 2 | Midpoint | def456 | good | Bug absent |
| 3 | Quarter | ghi789 | bad | Bug present |
...

**Root Cause**: Commit <hash> - <description>
**Impact**: <scope of changes>
```

## Tools
- `git bisect` - Binary search through commits
- `git log` - View commit history
- `git diff` - Examine changes
- Bash scripting - Automate testing

## Best Practices
- Test quickly at each step
- Automate when possible
- Document decisions
- Verify isolation with multiple tests

## Common Pitfalls
- Not enough known good commits
- Non-deterministic bugs
- Large commits with multiple changes
- Environment-dependent issues