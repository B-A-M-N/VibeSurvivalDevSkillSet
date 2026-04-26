---
name: 05-doc-continuity-check
description: Recheck docs on code change, update stale sections
trigger: docforge-overseer during phase 6
---

## Step-by-Step Instructions

1. **Change Detection**
   - Monitor git commits and file modifications
   - Identify affected modules and components
   - Trigger recheck on compaction events

2. **Stale Section Identification**
   - Compare continuity log timestamps
   - Flag documentation older than threshold
   - Identify modules with recent code changes

3. **Targeted Recheck**
   - Revalidate affected API references
   - Update stale docstrings and comments
   - Regenerate impacted diagrams

4. **Incremental Updates**
   - Apply minimal necessary changes
   - Preserve valid existing documentation
   - Batch related updates efficiently

5. **Logging & Reporting**
   - Record all changes with timestamps
   - Generate continuity reports
   - Track documentation freshness metrics