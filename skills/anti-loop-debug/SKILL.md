---
name: anti-loop-debug
description: Analyzes repeating failure patterns and provides a way out of loops
trigger: when loop detection is needed
---

# Anti-Loop Debug

## Step-by-Step Instructions

1. **Detect Loops**
   - Monitor for repeating failure patterns
   - Track consecutive failures
   - Identify oscillation between actions

2. **Analyze Patterns**
   - Review error logs and stack traces
   - Identify root cause of repeated failures
   - Determine if failures are related

3. **Break the Loop**
   - Implement circuit breaker pattern
   - Add exponential backoff
   - Provide escape hatch for stuck states

4. **Output Results**
   - Log loop detection and resolution
   - Generate diagnostic report