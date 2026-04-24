# Continuity Framework: Technical Architecture

## 1. The RPC Worker Model
Mistral Vibe does not support multi-agent chat rooms or background daemons. To overcome this, this framework implements an **RPC (Remote Procedure Call) Worker Model**.

*   **Main Agent (Architect)**: The only agent with user-facing output.
*   **Subagents (Workers)**: Isolated logic units spawned via the `task()` tool.
*   **Bridge**: The Architect provides "Context Injections" in the task string to sync the subagent's mental model.

## 2. Shared-State Persistence
Because subagents have isolated memory, the filesystem acts as the **Global State Layer**.

| File | Purpose |
|------|---------|
| `.checkpoint.json` | The Ground Truth. Records completed steps and current intent. |
| `.todo` | The Execution Queue. Forces atomicity. |
| `~/.vibe/prompts/` | Persistent logic that survives Vibe's `AutoCompactMiddleware`. |

## 3. The Control Loop
Every turn in the Architect's reasoning is governed by a **Pre-Action Audit**:

1.  **Observe**: Read `.checkpoint.json`.
2.  **Verify**: Call `state-sentry` if resuming or compacted.
3.  **Audit**: Call `watchdog` to detect behavioral drift.
4.  **Act**: Execute the tool call verified by the audit.
5.  **Record**: Update the checkpoint.

## 4. Subagent Isolation Constraints
Subagents are strictly non-interactive:
*   They **cannot** ask the user questions.
*   They **cannot** see the Main Agent's conversation history.
*   They **must** return plain text to the `task()` tool result.

This isolation is why the **Architect Prompt** is the most critical component—it is the only entity that can synthesize the worker reports into a coherent project path.
