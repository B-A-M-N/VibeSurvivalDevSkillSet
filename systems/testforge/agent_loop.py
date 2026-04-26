"""TestForge Agent Loop.

Executes the TestForge workflow: takes IMPLEMENTATION_REPORT.md,
generates tests, runs them, validates coverage.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus,
)


# Phase sequence for TestForge
PHASES = [
    "01-test-strategy-planning",
    "02-unit-test-generation",
    "03-integration-test-generation",
    "04-kill-test-generation",
    "05-fuzz-target-generation",
    "06-coverage-validation",
    "07-test-execution",
    "08-coverage-report",
]


def enter_testforge(context: Optional[ForgeContext] = None) -> str:
    """Enter the TestForge workflow."""
    if context is None:
        context = ForgeContext(forge_name="testforge", phase=PHASES[0])

    # Define gates
    impl_gate = ForgeGate(
        name="implementation_ready",
        status=GateStatus.OPEN,
        required_artifacts=["IMPLEMENTATION_REPORT.md"],
        failure_action="block",
    )
    context.gates.append(impl_gate)

    impl_artifact = ForgeArtifact(
        name="IMPLEMENTATION_REPORT.md",
        path="IMPLEMENTATION_REPORT.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
        produced_by="codeforge",
    )
    context.add_artifact(impl_artifact)

    if not impl_artifact.exists():
        return "[TestForge] Waiting for IMPLEMENTATION_REPORT.md from CodeForge."

    return f"[TestForge] Entered. Implementation: {impl_artifact.path}"


def exit_testforge(context: Optional[ForgeContext] = None) -> str:
    """Exit the TestForge workflow."""
    test_report = ForgeArtifact(
        name="TEST_REPORT.md",
        path="TEST_REPORT.md",
        artifact_type=ArtifactType.OUTPUT,
        required=True,
        produced_by="testforge",
    )

    if not test_report.exists():
        return "[TestForge] WARNING: TEST_REPORT.md not found."

    return f"[TestForge] Exited. Tests complete: {test_report.path}"


def run_phase(phase_name: str, context: ForgeContext) -> ForgeResult:
    """Run a single TestForge phase."""
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
        produced_by="testforge",
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
