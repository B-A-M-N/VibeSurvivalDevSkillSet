"""SpecForge Agent Loop.

Executes the SpecForge workflow: takes a goal, surveys existing docs,
identifies gaps, and produces MASTER_SPEC.md.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus,
)


# Phase sequence for SpecForge
PHASES = [
    "00-intake-goal-clarification",
    "01-existing-document-review",
    "02-implementation-survey",
    "03-intent-gap-analysis",
    "04-research-plan-generation",
    "05-architecture-exploration",
    "06-spec-template-selection",
    "07-spec-draft-generation",
    "08-cross-team-review-simulation",
    "09-constraint-injection",
    "10-edge-case-generation",
    "11-acceptance-criteria-definition",
    "12-spec-review-checklist",
    "13-spec-validation-and-refinement",
    "14-final-spec-packaging",
    "15-spec-handoff-preparation",
]


def enter_specforge(context: Optional[ForgeContext] = None) -> str:
    """Enter the SpecForge workflow."""
    if context is None:
        context = ForgeContext(forge_name="specforge", phase=PHASES[0])

    # Define gates
    initial_gate = ForgeGate(
        name="goal_defined",
        status=GateStatus.OPEN,
        required_artifacts=["GOAL.md"],
        failure_action="block",
    )
    context.gates.append(initial_gate)

    goal_artifact = ForgeArtifact(
        name="GOAL.md",
        path="GOAL.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
    )
    context.add_artifact(goal_artifact)

    if not goal_artifact.exists():
        return f"[SpecForge] Waiting for GOAL.md."

    return f"[SpecForge] Entered. Goal found: {goal_artifact.path}"


def exit_specforge(context: Optional[ForgeContext] = None) -> str:
    """Exit the SpecForge workflow."""
    master_spec = ForgeArtifact(
        name="MASTER_SPEC.md",
        path="MASTER_SPEC.md",
        artifact_type=ArtifactType.SPEC,
        required=True,
        produced_by="specforge",
    )

    if not master_spec.exists():
        return f"[SpecForge] WARNING: MASTER_SPEC.md not found."

    return f"[SpecForge] Exited. Spec complete: {master_spec.path}"


def run_phase(phase_name: str, context: ForgeContext) -> ForgeResult:
    """Run a single SpecForge phase."""
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
        produced_by="specforge",
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
