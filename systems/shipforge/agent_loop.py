"""ShipForge Agent Loop.

Executes the ShipForge workflow: takes DOC_REPORT.md,
generates deployment configs, CI pipelines, checklists, and ships.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus,
)


# Phase sequence for ShipForge
PHASES = [
    "01-dockerfile-generation",
    "02-ci-pipeline-generation",
    "03-deployment-config-generation",
    "04-environment-parity-check",
    "05-security-hardening-check",
    "06-deployment-checklist-generation",
    "07-ship",
]


def enter_shipforge(context: Optional[ForgeContext] = None) -> str:
    """Enter the ShipForge workflow."""
    if context is None:
        context = ForgeContext(forge_name="shipforge", phase=PHASES[0])

    # Define gates
    doc_gate = ForgeGate(
        name="docs_ready",
        status=GateStatus.OPEN,
        required_artifacts=["DOC_REPORT.md"],
        failure_action="block",
    )
    context.gates.append(doc_gate)

    doc_report = ForgeArtifact(
        name="DOC_REPORT.md",
        path="DOC_REPORT.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
        produced_by="docforge",
    )
    context.add_artifact(doc_report)

    if not doc_report.exists():
        return "[ShipForge] Waiting for DOC_REPORT.md from DocForge."

    return f"[ShipForge] Entered. Doc report: {doc_report.path}"


def exit_shipforge(context: Optional[ForgeContext] = None) -> str:
    """Exit the ShipForge workflow."""
    deploy_report = ForgeArtifact(
        name="DEPLOY_REPORT.md",
        path="DEPLOY_REPORT.md",
        artifact_type=ArtifactType.OUTPUT,
        required=True,
        produced_by="shipforge",
    )

    if not deploy_report.exists():
        return "[ShipForge] WARNING: DEPLOY_REPORT.md not found."

    return f"[ShipForge] Exited. Deployment complete: {deploy_report.path}"


def run_phase(phase_name: str, context: ForgeContext) -> ForgeResult:
    """Run a single ShipForge phase."""
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
        produced_by="shipforge",
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
