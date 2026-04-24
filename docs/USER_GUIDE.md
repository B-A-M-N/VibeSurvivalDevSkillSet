# User Guide: Interacting with the Framework

## 1. The TUI Sidebar (Shift+Tab)
When you press **Shift+Tab**, the list you see is the **Agent Team**.

*   **Do Not Switch Agents**: Unless you want to interview a subagent, stay on the **Main Agent**. The framework is designed for the Main Agent to lead.
*   **Plan Mode (Green)**: Keep this on for high-precision work. The "Task Decomposer" skill will provide detailed checklists for you to review before they run.

## 2. Reading the "Task" Logs
Since subagents don't chat with you, their output is hidden in the `task()` tool results.

1.  Look for a tool call named `task` in the step log.
2.  Expand it to see the report.
3.  **OK**: Everything is normal.
4.  **DRIFT**: The agent was caught doing something it shouldn't. You will see a "Correction" block in the main chat shortly after.

## 3. Mandatory Slash Commands
You can manually trigger the framework's power-tools at any time:

| Command | Usage |
|---------|-------|
| `/vibe-continuity` | Use this if the agent seems "lost" or after a long break. |
| `/behavior-audit` | Use this if the agent starts being repetitive or "chatty". |
| `/anti-loop-debug` | Use this if you see the same error message appearing multiple times. |
| `/task-decomposer` | Use this before starting a very complex multi-file task. |

## 4. Protecting your Shift+Tab
The most common issue with Vibe TUI is the **Shift+Tab** keybind being hijacked by Vim keybindings.
*   The framework's `config.toml` explicitly sets `vim_keybindings = false`.
*   If your navigation stops working, verify this setting in `~/.vibe/config.toml`.

---

**Status**: 📗 **GUIDE COMPLETE**
