"""ShipForge Middleware — Deployment readiness gating and environment parity.

Runs as a custom middleware in the ShipForge agent loop.
Ensures all security checks pass and environment parity is verified before deploy.
"""

from __future__ import annotations

from vibe.core.middleware import (
    ConversationContext,
    MiddlewareResult,
    MiddlewareAction,
    ResetReason,
    ConversationMiddleware,
)
from vibe.core.utils import VIBE_WARNING_TAG

import logging

logger = logging.getLogger(__name__)


class ShipForgeMiddleware(ConversationMiddleware):
    """Gates deployment readiness: security, parity, and checklist completion."""

    def __init__(self) -> None:
        self.active_phase: str | None = None
        self.security_checks_passed: bool = False
        self.parity_verified: bool = False
        self.checklist_complete: bool = False
        self.dockerfile_generated: bool = False
        self.ci_pipeline_generated: bool = False
        self.deployment_configs_generated: bool = False
        self.parity_issues: list[str] = []

    async def before_turn(self, context: ConversationContext) -> MiddlewareResult:
        """Run before each LLM turn. Gate deployment and inject readiness status."""
        messages_to_inject: list[str] = []

        if self.active_phase:
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>ShipForge phase: {self.active_phase}. "
                f"Security: {self.security_checks_passed}, "
                f"Parity: {self.parity_verified}, "
                f"Checklist: {self.checklist_complete}.</{VIBE_WARNING_TAG}>"
            )

        # Check recent deployment writes
        self._check_recent_deployment_writes(context.messages)

        # Gate: cannot deploy without passing all checks
        if self.active_phase == "deploy" or self.active_phase == "ship":
            blockers = []
            if not self.security_checks_passed:
                blockers.append("security hardening check not passed")
            if not self.parity_verified:
                blockers.append(f"environment parity not verified ({len(self.parity_issues)} issues)")
            if not self.checklist_complete:
                blockers.append("deployment checklist not complete")
            if not self.dockerfile_generated:
                blockers.append("Dockerfile not generated")
            if not self.ci_pipeline_generated:
                blockers.append("CI pipeline not generated")
            if not self.deployment_configs_generated:
                blockers.append("deployment configs not generated")

            if blockers:
                messages_to_inject.append(
                    f"<{VIBE_WARNING_TAG}>Cannot deploy. Blockers:\n- " +
                    "\n- ".join(blockers) +
                    f"\nComplete all prerequisites first.</{VIBE_WARNING_TAG}>"
                )
                return MiddlewareResult(
                    action=MiddlewareAction.INJECT_MESSAGE,
                    message="\n\n".join(messages_to_inject),
                )

        if messages_to_inject:
            return MiddlewareResult(
                action=MiddlewareAction.INJECT_MESSAGE,
                message="\n\n".join(messages_to_inject),
            )

        return MiddlewareResult()

    def _check_recent_deployment_writes(self, messages) -> None:
        """Check recent writes for deployment artifacts."""
        for msg in messages[-10:]:
            if getattr(msg, 'role', None) == 'assistant':
                for tc in getattr(msg, 'tool_calls', []):
                    if getattr(tc, 'function', {}).get('name', '') == 'write_file':
                        args = getattr(tc, 'function', {}).get('arguments', {})
                        file_path = args.get('file_path', '')
                        if 'dockerfile' in str(file_path).lower():
                            self.dockerfile_generated = True
                        if 'ci' in str(file_path).lower() or 'github' in str(file_path).lower():
                            self.ci_pipeline_generated = True
                        if 'k8s' in str(file_path).lower() or 'docker-compose' in str(file_path).lower():
                            self.deployment_configs_generated = True

    def set_phase(self, phase: str) -> None:
        """Set the current ShipForge phase."""
        self.active_phase = phase
        logger.info("ShipForge phase set to: %s", phase)

    def mark_security_passed(self) -> None:
        """Mark security hardening check as passed."""
        self.security_checks_passed = True
        logger.info("ShipForge: security checks passed")

    def mark_parity_verified(self) -> None:
        """Mark environment parity as verified."""
        self.parity_verified = True
        self.parity_issues = []
        logger.info("ShipForge: environment parity verified")

    def add_parity_issue(self, issue: str) -> None:
        """Record an environment parity issue."""
        self.parity_issues.append(issue)
        self.parity_verified = False
        logger.info("ShipForge: parity issue: %s", issue)

    def mark_checklist_complete(self) -> None:
        """Mark deployment checklist as complete."""
        self.checklist_complete = True
        logger.info("ShipForge: deployment checklist complete")

    def get_state(self) -> dict:
        """Return current middleware state."""
        return {
            "active_phase": self.active_phase,
            "security_checks_passed": self.security_checks_passed,
            "parity_verified": self.parity_verified,
            "checklist_complete": self.checklist_complete,
            "dockerfile_generated": self.dockerfile_generated,
            "ci_pipeline_generated": self.ci_pipeline_generated,
            "deployment_configs_generated": self.deployment_configs_generated,
            "parity_issues": self.parity_issues.copy(),
        }

    def restore_state(self, state: dict) -> None:
        """Restore middleware state from checkpoint."""
        self.active_phase = state.get("active_phase")
        self.security_checks_passed = state.get("security_checks_passed", False)
        self.parity_verified = state.get("parity_verified", False)
        self.checklist_complete = state.get("checklist_complete", False)
        self.dockerfile_generated = state.get("dockerfile_generated", False)
        self.ci_pipeline_generated = state.get("ci_pipeline_generated", False)
        self.deployment_configs_generated = state.get("deployment_configs_generated", False)
        self.parity_issues = state.get("parity_issues", [])
        logger.info("ShipForge middleware state restored: phase=%s", self.active_phase)

    def reset(self, reset_reason: ResetReason = ResetReason.STOP) -> None:
        """Reset middleware state."""
        self.active_phase = None
        self.security_checks_passed = False
        self.parity_verified = False
        self.checklist_complete = False
        self.dockerfile_generated = False
        self.ci_pipeline_generated = False
        self.deployment_configs_generated = False
        self.parity_issues = []
        logger.info("ShipForge middleware reset due to: %s", reset_reason)
