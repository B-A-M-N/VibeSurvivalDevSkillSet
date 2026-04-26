---
name: context-guardian
description: |
trigger: before major code changes
  Optimizes context usage to prevent token waste and premature compaction.
  Enforces a "Grep-First" reading strategy.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Context Guardian

This skill enforces context efficiency. Every file read or tool result in the context window must earn its place. Wasteful or exploratory reads are forbidden.

## When to Use
- Before reading a file to find a specific function or bug.
- If you are approaching the context compaction threshold (e.g., > 180,000 tokens).
- If you find yourself reading more than 3 files in a single turn.

## The Grep-First Principle
"Never read a whole file just to find a specific part. Grep first, then read the delta."

## Instructions
1. **Locate with Grep**: Use `grep -n` to find the exact line numbers of your target pattern.
2. **Targeted Read**: Use `read_file` with `start_line` and `end_line` parameters to read only the necessary context (±20 lines around the match).
3. **Chunk Large Files**: For files > 64KB, read only the header (lines 1-50) and the specific sections identified via grep.
4. **Discard successful output**: Do not keep large, successful tool outputs in context if they don't provide necessary information for the next step.

**Every token must fight for its life.**
