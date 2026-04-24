# **Subagent Orchestration: Supportive Assistance Protocol**
# Version: 3.0.0 (Optimized for Mistral Vibe 2.0)

---

## **THE SHIFT: FROM POLICING TO PARTNERSHIP**

In the old system, the Observer was a supervisor that punished deviation. In this version, the Observer is a **Research Assistant** that helps the Main Agent maintain continuity.

---

## **SUPPORTIVE ARCHITECTURE**

```
┌─────────────────────────────────────────────────────────────────┐
│                            MAIN AGENT                               │
│  The "Architect": Makes decisions and executes the .todo.         │
│  Perspective: High-level reasoning and implementation.            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ Reads hints at session start
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CONTINUATION OBSERVER                         │
│  The "Researcher": Background state verification.                  │
│  Job: Finds what the Architect might have missed (drift/typos).    │
│  Writes: .observer-hints.json (Helpful context, not commands).     │
└─────────────────────────────────────────────────────────────────┘
```

---

## **HINT-BASED ORCHESTRATION**

Instead of forcing skills, the Observer provides **Contextual Hints**:

| **Condition** | **Supportive Hint** | **Observer Action** |
|---------------|---------------------|---------------------|
| Repeated failure | "Target [file] has failed 3 times. Possible permission issue detected." | Search for permission/path errors. |
| Context Compaction | "Context was recently compacted. Here is a summary of the last 3 critical decisions." | Synthesize key context from history. |
| Dependency Gap | "You're editing [file_A] but [file_B] imports it. You might need to check B." | Use `grep` to find stale imports. |
| Stale Progress | "The current todo item hasn't moved in 5 turns. Consider splitting the task." | Suggest a more atomic breakdown. |

---

## **HINT PACKET FORMAT**

Observer writes `.observer-hints.json` to assist the Main Agent:

```json
{
  "schema_version": "3.0.0",
  "generated_at": "2026-04-20T14:30:00Z",
  "insights": {
    "continuity_score": 88,
    "last_verified_state": "All modified files match checkpoint hashes.",
    "potential_drift": null
  },
  "recommendations": [
    {
      "type": "context",
      "message": "Note: src/auth.py was modified in turn 5 to add JWT support.",
      "relevance": "high"
    },
    {
      "type": "strategy",
      "message": "The current step is large. Consider verifying the config load before implementing the logic.",
      "relevance": "medium"
    }
  ],
  "technical_data": {
    "missing_dependencies": ["PyJWT"],
    "stale_imports": ["src/old_auth.py"]
  }
}
```

---

## **PROTOCOL: THE ASSISTANT'S LOOP**

### Observer (Subagent)
1. **Poll Checkpoint**: Understand what the Architect is doing.
2. **Passive Verification**: Use `ls`, `grep`, and `read_file` to confirm the Architect's "Save Point" is accurate.
3. **Drift Detection**: If the code deviates from the checkpoint, **record the discrepancy as a hint**, do not force a halt.
4. **Update Hints**: Write `.observer-hints.json`.

### Main Agent (Architect)
1. **On Startup**: Read `.observer-hints.json`.
2. **Acknowledge**: Briefly note the hints: *"Observer hints loaded: noted potential drift in auth.py."*
3. **Decide**: Use the hints to improve the current action.
4. **Execute**: Continue with the `.todo`.

---

## **BENEFITS OF THIS MODEL**

- **No Paralysis**: The Main Agent is always in control.
- **Lower Cognitive Load**: The Main Agent doesn't have to verify *everything*—it can trust the Observer to flag inconsistencies in the background.
- **Improved Accuracy**: Two sets of "eyes" on the codebase, but only one set of "hands" (the Main Agent) on the keyboard.
- **Natural Communication**: Allows the model to use its full reasoning capacity while the subagent handles the boring metadata/state tracking.
