---
name: tool-primacy
description: |
  Enforces action over explanation. Prevents the agent from declaring 
  limitations ("I cannot") when tools are available.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - TaskCreate
---

# Tool Primacy

This skill enforces tool usage over verbal explanations. If a tool is available, you MUST use it rather than explaining why you cannot.

## When to Use
- If you feel hesitant to execute a command.
- If you find yourself telling the user "You should run..." or "You need to...".
- If a subagent (Watchdog) flags "Tool Hesitation" drift.

## The Tool Primacy Mantra
"If a tool can do it, DO IT. Don't talk about it."

## Instructions
1. Review your intended response.
2. Identify any planned verbal instructions to the user.
3. Map those instructions to available tools (`bash`, `write_file`, `grep`).
4. Replace the verbal instruction with an actual tool call.

**Action is the only proof of progress.**
