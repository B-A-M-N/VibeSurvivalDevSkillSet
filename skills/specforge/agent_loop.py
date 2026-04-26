"""SpecForge Runtime Integration.

Provides entrypoint/exitpoint hooks for SpecForge pipeline execution.
SpecForge uses the standard AgentLoop with subagent delegation —
no runtime mode switch needed since it runs as a normal multi-agent pipeline.
"""


def enter_specforge():
    """
    Entrypoint for SpecForge pipeline.
    Called when specforge-overseer agent activates.
    No runtime switch needed — uses standard AgentLoop + task() delegation.
    """
    return {
        "mode": "specforge",
        "agents": ["specforge-overseer", "specforge-analyst", "specforge-architect"],
        "skills_path": "skills/specforge",
    }


def exit_specforge():
    """
    Exit point for SpecForge pipeline.
    Called when pipeline completes or user cancels.
    """
    return {"status": "complete", "mode": "normal"}
