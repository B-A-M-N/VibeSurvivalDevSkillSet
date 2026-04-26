"""ResearchForge Runtime Integration.

Provides entrypoint/exitpoint hooks for ResearchForge pipeline execution.
ResearchForge uses the standard AgentLoop with subagent delegation —
no runtime mode switch needed since it runs as a normal multi-agent pipeline.
"""


def enter_researchforge():
    """
    Entrypoint for ResearchForge pipeline.
    Called when researchforge-overseer agent activates.
    No runtime switch needed — uses standard AgentLoop + task() delegation.
    """
    return {
        "mode": "researchforge",
        "agents": ["researchforge-overseer", "researchforge-evidence",
                   "researchforge-researcher", "researchforge-synthesizer"],
        "skills_path": "skills/researchforge",
    }


def exit_researchforge():
    """
    Exit point for ResearchForge pipeline.
    Called when pipeline completes or user cancels.
    """
    return {"status": "complete", "mode": "normal"}
