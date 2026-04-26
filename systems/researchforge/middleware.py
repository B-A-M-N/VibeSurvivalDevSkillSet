"""ResearchForge Middleware.

Implements the MiddlewareInterface for ResearchForge.
ResearchForge handles deep research workflows.
"""

from __future__ import annotations
from typing import Optional
import logging

from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult, MiddlewareAction,
)
from systems.core.contract import ForgeContext, ForgeResult, ForgeGate

logger = logging.getLogger(__name__)


class ResearchForgeMiddleware(MiddlewareInterface):
    """Middleware for ResearchForge workflow."""

    def __init__(self, label: str = "ResearchForgeMiddleware"):
        super().__init__(label=label)
        self.research_phases = [
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

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """Check gates before phase starts."""
        # Check all gates
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
            f"Review research strategy."
        )

    def on_verification_failure(
        self, context: ForgeContext, reason: str
    ) -> MiddlewareResult:
        """Handle verification failure."""
        return MiddlewareResult.block(
            f"[{self.label}] Verification failed: {reason}"
        )

    def inject_state(self, context: ForgeContext) -> MiddlewareResult:
        """Inject research state."""
        # Count completed phases
        completed = sum(
            1 for a in context.artifacts
            if a.artifact_type == "output" and a.exists()
        )
        return MiddlewareResult.inject(
            f"[{self.label}] Research progress: {completed}/{len(self.research_phases)} phases complete."
        )


def get_middleware_stack(agent_manager=None) -> list[MiddlewareInterface]:
    """Return the middleware stack for ResearchForge."""
    stack = [
        ResearchForgeMiddleware(),
    ]
    if agent_manager:
        for mw in stack:
            mw.set_agent_manager(agent_manager)
    return stack
