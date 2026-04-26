"""SpecForge Middleware.

Implements the MiddlewareInterface for SpecForge.
SpecForge handles specification creation from goals.
"""

from __future__ import annotations
from typing import Optional
import logging

from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult, MiddlewareAction,
)
from systems.core.contract import ForgeContext, ForgeResult, ForgeGate

logger = logging.getLogger(__name__)


class SpecForgeMiddleware(MiddlewareInterface):
    """Middleware for SpecForge workflow."""

    def __init__(self, label: str = "SpecForgeMiddleware"):
        super().__init__(label=label)
        self.spec_phases = [
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

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """Check gates before phase starts."""
        for gate, status in context.check_gates():
            if status == ForgeGate.CLOSED:
                return MiddlewareResult.block(
                    f"[{self.label}] Gate '{gate.name}' is closed. "
                    f"Required artifacts: {gate.required_artifacts}"
                )
        return MiddlewareResult.cont()

    def after_phase(
        self, context: ForgeContext, result: ForgeResult
    ) -> MiddlewareResult:
        """After phase completes, check result."""
        if not result.success:
            return MiddlewareResult.block(
                f"[{self.label}] Phase failed: {result.message}"
            )
        return MiddlewareResult.cont()

    def on_gate_failure(
        self, gate: ForgeGate, context: ForgeContext
    ) -> MiddlewareResult:
        """Handle gate failure."""
        return MiddlewareResult.block(
            f"[{self.label}] Gate '{gate.name}' failed. "
            f"Required: {gate.required_artifacts}"
        )

    def on_drift_detected(
        self, context: ForgeContext, reason: str
    ) -> MiddlewareResult:
        """Handle drift detection."""
        return MiddlewareResult.inject(
            f"[{self.label}] Drift detected: {reason}. "
            f"Review spec strategy."
        )

    def on_verification_failure(
        self, context: ForgeContext, reason: str
    ) -> MiddlewareResult:
        """Handle verification failure."""
        return MiddlewareResult.block(
            f"[{self.label}] Verification failed: {reason}"
        )

    def inject_state(self, context: ForgeContext) -> MiddlewareResult:
        """Inject spec state."""
        completed = sum(
            1 for a in context.artifacts
            if a.artifact_type == "output" and a.exists()
        )
        return MiddlewareResult.inject(
            f"[{self.label}] Spec progress: {completed}/{len(self.spec_phases)} phases complete."
        )


def get_middleware_stack(agent_manager=None) -> list[MiddlewareInterface]:
    """Return the middleware stack for SpecForge."""
    stack = [
        SpecForgeMiddleware(),
    ]
    if agent_manager:
        for mw in stack:
            mw.set_agent_manager(agent_manager)
    return stack
