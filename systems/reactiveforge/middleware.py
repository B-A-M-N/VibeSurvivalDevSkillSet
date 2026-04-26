"""ReactiveForge Middleware.

Implements the MiddlewareInterface for ReactiveForge.
Handles incident response workflow.
"""

from __future__ import annotations
from typing import Optional
import logging

from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult, MiddlewareAction,
)
from systems.core.contract import ForgeContext, ForgeResult, ForgeGate

logger = logging.getLogger(__name__)


class ReactiveForgeMiddleware(MiddlewareInterface):
    """Middleware for ReactiveForge workflow."""

    def __init__(self, label: str = "ReactiveForgeMiddleware"):
        super().__init__(label=label)
        self.anomaly_types = ["bug", "performance", "security", "deployment"]

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """Check gates before step starts."""
        for gate, status in context.check_gates():
            if status == ForgeGate.CLOSED:
                return MiddlewareResult.block(
                    f"[{self.label}] Gate '{gate.name}' is closed. "
                    f"Required artifacts: {gate.required_artifacts}"
                )

        # Check trace for anomalies
        if context.trace_events:
            recent = context.trace_events[-5:]
            for event in recent:
                if "error" in str(event).lower() or "fail" in str(event).lower():
                    return MiddlewareResult.inject(
                        f"[{self.label}] Anomaly detected in trace. "
                        f"Reviewing incident..."
                    )

        return MiddlewareResult.cont()

    def after_phase(
        self, context: ForgeContext, result: ForgeResult
    ) -> MiddlewareResult:
        """After step completes, check result."""
        if not result.success:
            return MiddlewareResult.block(
                f"[{self.label}] Step failed: {result.message}"
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
            f"Review incident response strategy."
        )

    def on_verification_failure(
        self, context: ForgeContext, reason: str
    ) -> MiddlewareResult:
        """Handle verification failure."""
        return MiddlewareResult.block(
            f"[{self.label}] Verification failed: {reason}"
        )

    def inject_state(self, context: ForgeContext) -> MiddlewareResult:
        """Inject incident state."""
        artifacts = [a.name for a in context.artifacts if a.exists()]
        return MiddlewareResult.inject(
            f"[{self.label}] Incident state: {len(artifacts)} artifacts present. "
            f"Current phase: {context.phase}"
        )

    def emit_trace(self, event: str, data: dict) -> None:
        """Record trace event."""
        if hasattr(self, 'agent_manager') and self.agent_manager:
            ctx = ForgeContext()
            ctx.set_agent_manager(self.agent_manager)
            ctx.add_trace(event, data)


def get_middleware_stack(agent_manager=None) -> list[MiddlewareInterface]:
    """Return the middleware stack for ReactiveForge."""
    stack = [
        ReactiveForgeMiddleware(),
    ]
    if agent_manager:
        for mw in stack:
            mw.set_agent_manager(agent_manager)
    return stack
