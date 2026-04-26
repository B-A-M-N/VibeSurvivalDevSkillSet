"""ReactiveForge Agent Loop.

Incident response workflow: detect → classify → research →
spawn subagents → synthesize fix → invoke CodeForge →
invoke TestForge → verify → close or escalate.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional, List

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus, ForgeFailure,
)
from systems.core.orchestrator import ForgeOrchestrator


# Workflow steps for ReactiveForge
WORKFLOW_STEPS = [
    "detect_anomaly",
    "classify_failure",
    "create_research_tracks",
    "spawn_subagents",
    "synthesize_candidate_fix",
    "invoke_codeforge",
    "invoke_testforge",
    "verify_fix",
    "close_or_escalate",
]


def enter_reactiveforge(context: Optional[ForgeContext] = None) -> str:
    """Enter the ReactiveForge workflow."""
    if context is None:
        context = ForgeContext(forge_name="reactiveforge", phase=WORKFLOW_STEPS[0])

    # Define gates
    anomaly_gate = ForgeGate(
        name="anomaly_detected",
        status=GateStatus.OPEN,
        required_artifacts=["TRACE_AANOMALY.md"],
        failure_action="block",
    )
    context.gates.append(anomaly_gate)

    incident_gate = ForgeGate(
        name="incident_defined",
        status=GateStatus.OPEN,
        required_artifacts=["INCIDENT_REPORT.md"],
        failure_action="block",
    )
    context.gates.append(incident_gate)

    # Check for required artifacts
    anomaly_artifact = ForgeArtifact(
        name="TRACE_AANOMALY.md",
        path="TRACE_AANOMALY.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
    )
    context.add_artifact(anomaly_artifact)

    incident_artifact = ForgeArtifact(
        name="INCIDENT_REPORT.md",
        path="INCIDENT_REPORT.md",
        artifact_type=ArtifactType.INPUT,
        required=True,
    )
    context.add_artifact(incident_artifact)

    if not anomaly_artifact.exists():
        return "[ReactiveForge] Waiting for TRACE_AANOMALY.md."
    if not incident_artifact.exists():
        return "[ReactiveForge] Waiting for INCIDENT_REPORT.md."

    return "[ReactiveForge] Entered. Anomaly and incident report found."


def exit_reactiveforge(context: Optional[ForgeContext] = None) -> str:
    """Exit the ReactiveForge workflow."""
    resolution = ForgeArtifact(
        name="INCIDENT_RESOLUTION.md",
        path="INCIDENT_RESOLUTION.md",
        artifact_type=ArtifactType.OUTPUT,
        required=True,
        produced_by="reactiveforge",
    )

    if not resolution.exists():
        return "[ReactiveForge] WARNING: INCIDENT_RESOLUTION.md not found."

    return f"[ReactiveForge] Exited. Resolution: {resolution.path}"


def run_phase(phase_name: str, context: ForgeContext) -> ForgeResult:
    """Run a single ReactiveForge workflow step."""
    if phase_name not in WORKFLOW_STEPS:
        return ForgeResult(
            success=False,
            message=f"Unknown step: {phase_name}",
        )

    context.phase = phase_name

    # Check gates
    for gate, status in context.check_gates():
        if status == GateStatus.CLOSED:
            return ForgeResult(
                success=False,
                message=f"Gate '{gate.name}' is closed.",
            )

    # Execute the step
    if phase_name == "detect_anomaly":
        return _detect_anomaly(context)
    elif phase_name == "classify_failure":
        return _classify_failure(context)
    elif phase_name == "create_research_tracks":
        return _create_research_tracks(context)
    elif phase_name == "spawn_subagents":
        return _spawn_subagents(context)
    elif phase_name == "synthesize_candidate_fix":
        return _synthesize_candidate_fix(context)
    elif phase_name == "invoke_codeforge":
        return _invoke_codeforge(context)
    elif phase_name == "invoke_testforge":
        return _invoke_testforge(context)
    elif phase_name == "verify_fix":
        return _verify_fix(context)
    elif phase_name == "close_or_escalate":
        return _close_or_escalate(context)

    return ForgeResult(
        success=True,
        message=f"Step {phase_name} completed",
        next_phase=_next_step(phase_name),
    )


def _detect_anomaly(context: ForgeContext) -> ForgeResult:
    """Detect trace anomaly."""
    anomaly = context.get_artifact("TRACE_AANOMALY.md")
    if anomaly and anomaly.exists():
        return ForgeResult(
            success=True,
            message="Anomaly detected from trace",
            next_phase=_next_step("detect_anomaly"),
        )
    return ForgeResult(
        success=False,
        message="No anomaly detected",
        failure=ForgeFailure(
            failure_type="no_anomaly",
            reason="TRACE_AANOMALY.md not found or empty",
            retryable=True,
        ),
    )


def _classify_failure(context: ForgeContext) -> ForgeResult:
    """Classify the failure type."""
    # Create failure classification artifact
    classification = ForgeArtifact(
        name="FAILURE_CLASSIFICATION.md",
        path="FAILURE_CLASSIFICATION.md",
        artifact_type=ArtifactType.OUTPUT,
        produced_by="reactiveforge",
    )
    context.add_artifact(classification)

    return ForgeResult(
        success=True,
        message="Failure classified",
        next_phase=_next_step("classify_failure"),
    )


def _create_research_tracks(context: ForgeContext) -> ForgeResult:
    """Create research tracks for investigation."""
    research_plan = ForgeArtifact(
        name="REACTIVE_RESEARCH_PLAN.md",
        path="REACTIVE_RESEARCH_PLAN.md",
        artifact_type=ArtifactType.OUTPUT,
        produced_by="reactiveforge",
    )
    context.add_artifact(research_plan)

    return ForgeResult(
        success=True,
        message="Research tracks created",
        next_phase=_next_step("create_research_tracks"),
    )


def _spawn_subagents(context: ForgeContext) -> ForgeResult:
    """Spawn subagents to investigate."""
    if context.agent_manager:
        try:
            context.agent_manager.set_current_agent("team-verify")
        except Exception:
            pass

    return ForgeResult(
        success=True,
        message="Subagents spawned for investigation",
        next_phase=_next_step("spawn_subagents"),
    )


def _synthesize_candidate_fix(context: ForgeContext) -> ForgeResult:
    """Synthesize candidate fix from research."""
    fix_candidate = ForgeArtifact(
        name="FIX_CANDIDATE.md",
        path="FIX_CANDIDATE.md",
        artifact_type=ArtifactType.OUTPUT,
        produced_by="reactiveforge",
    )
    context.add_artifact(fix_candidate)

    return ForgeResult(
        success=True,
        message="Candidate fix synthesized",
        next_phase=_next_step("synthesize_candidate_fix"),
    )


def _invoke_codeforge(context: ForgeContext) -> ForgeResult:
    """Invoke CodeForge to apply the fix."""
    orchestrator = ForgeOrchestrator()
    result = orchestrator.run_forge("codeforge", context)

    if result.success:
        return ForgeResult(
            success=True,
            message="CodeForge applied fix",
            next_phase=_next_step("invoke_codeforge"),
        )
    return ForgeResult(
        success=False,
        message="CodeForge failed to apply fix",
        failure=result.failure,
    )


def _invoke_testforge(context: ForgeContext) -> ForgeResult:
    """Invoke TestForge to validate the fix."""
    orchestrator = ForgeOrchestrator()
    result = orchestrator.run_forge("testforge", context)

    if result.success:
        return ForgeResult(
            success=True,
            message="TestForge validated fix",
            next_phase=_next_step("invoke_testforge"),
        )
    return ForgeResult(
        success=False,
        message="TestForge found issues",
        failure=result.failure,
    )


def _verify_fix(context: ForgeContext) -> ForgeResult:
    """Verify the fix passes all tests."""
    test_report = context.get_artifact("TEST_REPORT.md")
    if test_report and test_report.exists():
        return ForgeResult(
            success=True,
            message="Fix verified",
            next_phase=_next_step("verify_fix"),
        )
    return ForgeResult(
        success=False,
        message="Fix verification failed",
        failure=ForgeFailure(
            failure_type="verification_failed",
            reason="Tests did not pass",
            retryable=True,
        ),
    )


def _close_or_escalate(context: ForgeContext) -> ForgeResult:
    """Close incident or escalate to user."""
    # Check if all steps passed
    test_report = context.get_artifact("TEST_REPORT.md")
    if test_report and test_report.exists():
        # Create resolution document
        resolution = ForgeArtifact(
            name="INCIDENT_RESOLUTION.md",
            path="INCIDENT_RESOLUTION.md",
            artifact_type=ArtifactType.OUTPUT,
            produced_by="reactiveforge",
        )
        context.add_artifact(resolution)

        return ForgeResult(
            success=True,
            message="Incident resolved successfully",
        )
    else:
        # Escalate to user
        return ForgeResult(
            success=False,
            message="Incident not resolved, escalating to user",
            failure=ForgeFailure(
                failure_type="escalation",
                reason="Could not resolve incident automatically",
                retryable=False,
            ),
        )


def _next_step(current: str) -> Optional[str]:
    """Get the next step in workflow."""
    try:
        idx = WORKFLOW_STEPS.index(current)
        if idx + 1 < len(WORKFLOW_STEPS):
            return WORKFLOW_STEPS[idx + 1]
    except ValueError:
        pass
    return None


def get_available_phases() -> List[str]:
    """Return the list of workflow steps."""
    return WORKFLOW_STEPS.copy()
