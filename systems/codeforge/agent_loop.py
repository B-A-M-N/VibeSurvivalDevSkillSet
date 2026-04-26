"""CodeForge Agent Loop.

Executes the CodeForge workflow: takes MASTER_SPEC.md,
drives implementation, validates invariants, hands off to TestForge.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus,
)


# Phase sequence for CodeForge
PHASES = [
    "00-spec-ingest",
    "01-codebase-survey",
    "02-implementation-planning",
    "03-file-generation",
    "04-pattern-following",
    "05-invariant-checking",
    "06-integration",
    "07-handoff-verification",
]


def enter_codeforge(context: Optional[ForgeContext] = None) -> str:
    """Enter the CodeForge workflow.

    Sets up the context with required gates and artifacts.
    Validates that MASTER_SPEC.md exists.
    """
    if context is None:
        context = ForgeContext(forge_name="codeforge", phase=PHASES[0])

    # Define required artifacts
    spec_artifact = ForgeArtifact(
        name="MASTER_SPEC.md",
        path="MASTER_SPEC.md",
        artifact_type=ArtifactType.SPEC,
        required=True,
        produced_by="specforge",
    )
    context.add_artifact(spec_artifact)

    # Define gates
    spec_gate = ForgeGate(
        name="spec_present",
        status=GateStatus.OPEN,
        required_artifacts=["MASTER_SPEC.md"],
        failure_action="block",
    )
    context.gates.append(spec_gate)

    # Check initial gate
    if not spec_artifact.exists():
        return (f"[CodeForge] Waiting for MASTER_SPEC.md from SpecForge. "
                f"Place the file in the current directory.")

    return f"[CodeForge] Entered. Spec found: {spec_artifact.path}"


def exit_codeforge(context: Optional[ForgeContext] = None) -> str:
    """Exit the CodeForge workflow.

    Validates output artifacts and prepares handoff to TestForge.
    """
    implementation_report = ForgeArtifact(
        name="IMPLEMENTATION_REPORT.md",
        path="IMPLEMENTATION_REPORT.md",
        artifact_type=ArtifactType.OUTPUT,
        required=True,
        produced_by="codeforge",
    )

    if not implementation_report.exists():
        return (f"[CodeForge] WARNING: IMPLEMENTATION_REPORT.md not found. "
                f"Handoff to TestForge may fail.")

    return (f"[CodeForge] Exited. Implementation complete. "
            f"Handoff artifact: {implementation_report.path}")


def run_phase(phase_name: str, context: ForgeContext) -> ForgeResult:
    """Run a single CodeForge phase.

    Args:
        phase_name: The phase to run (e.g., "00-spec-ingest")
        context: The current ForgeContext

    Returns:
        ForgeResult with success/failure and produced artifacts
    """
    if phase_name not in PHASES:
        return ForgeResult(
            success=False,
            message=f"Unknown phase: {phase_name}",
            failure=None,
        )

    context.phase = phase_name

    # Check gates before running phase
    for gate, status in context.check_gates():
        if status == GateStatus.CLOSED:
            return ForgeResult(
                success=False,
                message=f"Gate '{gate.name}' is closed. Cannot run {phase_name}.",
                failure=None,
            )

    # Simulate phase execution (in real impl, would invoke the skill)
    phase_artifact = ForgeArtifact(
        name=f"{phase_name.upper()}_OUTPUT.md",
        path=f"{phase_name.upper()}_OUTPUT.md",
        artifact_type=ArtifactType.OUTPUT,
        produced_by="codeforge",
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
