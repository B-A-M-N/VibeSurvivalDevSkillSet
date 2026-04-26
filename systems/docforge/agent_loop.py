"""DocForge Agent Loop.

Executes the DocForge workflow: takes code/test artifacts,
generates documentation, API refs, README sync, etc.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus,
)


# Phase sequence for DocForge
PHASES = [
    "01-api-reference-generation",
    "02-inline-docstring-generation",
    "03-architecture-diagram-generation",
    "04-readme-sync",
    "05-doc-continuity-check",
]


def enter_docforge(context: Optional[ForgeContext] = None) -> str:
    """Enter the DocForge workflow."""
    if context is None:
        context = ForgeContext(forge_name="docforge", phase=PHASES[0])

    # Define gates
    code_gate = ForgeGate(
        name="code_ready",
        status=GateStatus.OPEN,
        required_artifacts=["TEST_REPORT.md"],
        failure_action="block",
    )
    context.gates.append(code_gate)

    test_report = ForgeArtifact(
        name="TEST_REPORT.md",
        path="TEST_REPORT.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
        produced_by="testforge",
    )
    context.add_artifact(test_report)

    if not test_report.exists():
        return "[DocForge] Waiting for TEST_REPORT.md from TestForge."

    return f"[DocForge] Entered. Test report: {test_report.path}"


def exit_docforge(context: Optional[ForgeContext] = None) -> str:
    """Exit the DocForge workflow."""
    doc_report = ForgeArtifact(
        name="DOC_REPORT.md",
        path="DOC_REPORT.md",
        artifact_type=ArtifactType.OUTPUT,
        required=True,
        produced_by="docforge",
    )

    if not doc_report.exists():
        return "[DocForge] WARNING: DOC_REPORT.md not found."

    return f"[DocForge] Exited. Docs complete: {doc_report.path}"


def run_phase(phase_name: str, context: ForgeContext) -> ForgeResult:
    """Run a single DocForge phase."""
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
        produced_by="docforge",
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
