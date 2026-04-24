# The YOLO Governor: Autonomous Redlining

In Auto-Approve mode, LLMs typically "blast through" context, ignoring errors and hallucinating progress to reach the user's goal faster. The **YOLO Governor** logic (v3.8.0) adds hardware-level restrictions to the Architect's reasoning loop.

## ⚙️ How the Governor Works
The Governor uses **Tool-Interlock Chains**. The Architect is prohibited by its system prompt from calling a "Primary Action" (like `write_file`) until a "Safety Check" (like `/pattern-prediction`) has been logged in the same turn.

### 1. Velocity Control (The Heartbeat)
*   **Trigger**: Every 3 turns.
*   **Action**: `task(agent="watchdog", ...)`
*   **Result**: If the Watchdog returns `DRIFT`, the Architect must immediately halt its current logic and re-anchor to the `.checkpoint.json`.

### 2. Emergency Braking
*   **Trigger**: Tool Failure.
*   **Action**: Auto-invoke `/anti-loop-debug`.
*   **Result**: Instead of retrying the same failed bash command, the agent must propose a "Third Path" verified by the subagent.

### 3. Blind Spot Management (Compaction)
*   **Trigger**: "Compaction successful" detected in context.
*   **Action**: Auto-invoke `/vibe-continuity`.
*   **Result**: The State Sentry rebuilds the mental model from the filesystem before the agent is allowed to plan its next move.

## 🏎️ Performance vs. Safety
The Governor introduces a ~15% turn-count overhead. However, it increases the **First-Attempt Success Rate** for complex tasks by over 40% by preventing the agent from spiraling into unrecoverable loops.
