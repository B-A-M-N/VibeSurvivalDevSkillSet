"""ResearchForge Agent Loop.

Executes the ResearchForge workflow: deep research, evidence collection,
hypothesis generation, and synthesis.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus,
)


# Phase sequence for ResearchForge
PHASES = [
    "00-problem-intake",
    "01-context-map",
    "02-evidence-collection",
    "03-source-quality-check",
    "04-hypothesis-generation",
    "05-hypothesis-disconfirmation",
    "06-targeted-research-plan",
    "07-official-docs-research",
    "08-upstream-issue-research",
    "09-version-compatibility-research",
    "10-architecture-pattern-research",
    "11-risk-research",
    "12-contradiction-hunt",
    "13-solution-option-synthesis",
    "14-validation-plan-generation",
    "15-final-research-packet",
    "16-adversarial-research-review",
]


def enter_researchforge(context: Optional[ForgeContext] = None) -> str:
    """Enter the ResearchForge workflow."""
    if context is None:
        context = ForgeContext(forge_name="researchforge", phase=PHASES[0])

    # Define gates
    initial_gate = ForgeGate(
        name="problem_defined",
        status=GateStatus.OPEN,
        required_artifacts=["PROBLEM_FRAME.md"],
        failure_action="block",
    )
    context.gates.append(initial_gate)

    problem_artifact = ForgeArtifact(
        name="PROBLEM_FRAME.md",
        path="PROBLEM_FRAME.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
        produced_by="specforge",
    )
    context.add_artifact(problem_artifact)

    if not problem_artifact.exists():
        return f"[ResearchForge] Waiting for PROBLEM_FRAME.md from SpecForge."

    return f"[ResearchForge] Entered. Problem frame found: {problem_artifact.path}"


def exit_researchforge(context: Optional[ForgeContext] = None) -> str:
    """Exit the ResearchForge workflow."""
    final_packet = ForgeArtifact(
        name="FINAL_RESEARCH_PACKET.md",
        path="FINAL_RESEARCH_PACKET.md",
        artifact_type=ArtifactType.OUTPUT,
        required=True,
        produced_by="researchforge",
    )

    if not final_packet.exists():
        return f"[ResearchForge] WARNING: FINAL_RESEARCH_PACKET.md not found."

    return f"[ResearchForge] Exited. Research complete: {final_packet.path}"


def run_phase(phase_name: str, context: ForgeContext) -> ForgeResult:
    """Run a single ResearchForge phase."""
    if phase_name not in PHASES:
        return ForgeResult(
            success=False,
            message=f"Unknown phase: {phase_name}",
        )

    context.phase = phase_name

    # Check gates
    for gate, status in context.check_gates():
        if status == GateStatus.CLOSED:
            return ForgeResult(
                success=False,
                message=f"Gate '{gate.name}' is closed.",
            )

    # Simulate phase execution
    phase_artifact = ForgeArtifact(
        name=f"{phase_name.upper()}_OUTPUT.md",
        path=f"{phase_name.upper()}_OUTPUT.md",
        artifact_type=ArtifactType.OUTPUT,
        produced_by="researchforge",
    )
    context.add_artifact(phase_artifact)

    return ForgeResult(
        success=True,
        message=f"Phase {phase_name} completed",
        next_phase=_next_phase(phase_name),
    )


def _next_phase(current: str) -> Optional[str]:
    """Get the next phase in sequence."""
    try:
        idx = PHASES.index(current)
        if idx + 1 < len(PHASES):
            return PHASES[idx + 1]
    except ValueError:
        pass
    return None


def get_available_phases() -> list[str]:
    """Return the list of available phases."""
    return PHASES.copy()
