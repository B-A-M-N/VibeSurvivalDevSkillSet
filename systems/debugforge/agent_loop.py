"""DebugForge Agent Loop.

Executes the DebugForge workflow: triages failures, isolates root cause,
generates fix options, applies fix, validates.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus,
)


# Phase sequence for DebugForge
PHASES = [
    "00-issue-intake",
    "01-reproduction",
    "02-bisection-isolation",
    "03-root-cause-analysis",
    "04-fix-option-generation",
    "05-fix-application",
    "06-validation",
]


def enter_debugforge(context: Optional[ForgeContext] = None) -> str:
    """Enter the DebugForge workflow."""
    if context is None:
        context = ForgeContext(forge_name="debugforge", phase=PHASES[0])

    # Define gates
    issue_gate = ForgeGate(
        name="issue_defined",
        status=GateStatus.OPEN,
        required_artifacts=["ISSUE.md", "FAILING_TESTS.md"],
        failure_action="block",
    )
    context.gates.append(issue_gate)

    issue_artifact = ForgeArtifact(
        name="ISSUE.md",
        path="ISSUE.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
    )
    context.add_artifact(issue_artifact)

    failing_tests = ForgeArtifact(
        name="FAILING_TESTS.md",
        path="FAILING_TESTS.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
    )
    context.add_artifact(failing_tests)

    if not issue_artifact.exists() or not failing_tests.exists():
        return "[DebugForge] Waiting for ISSUE.md and FAILING_TESTS.md."

    return f"[DebugForge] Entered. Issue: {issue_artifact.path}"


def exit_debugforge(context: Optional[ForgeContext] = None) -> str:
    """Exit the DebugForge workflow."""
    fix_report = ForgeArtifact(
        name="FIX_REPORT.md",
        path="FIX_REPORT.md",
        artifact_type=ArtifactType.OUTPUT,
        required=True,
        produced_by="debugforge",
    )

    if not fix_report.exists():
        return "[DebugForge] WARNING: FIX_REPORT.md not found."

    return f"[DebugForge] Exited. Fix complete: {fix_report.path}"


def run_phase(phase_name: str, context: ForgeContext) -> ForgeResult:
    """Run a single DebugForge phase."""
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
        produced_by="debugforge",
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
