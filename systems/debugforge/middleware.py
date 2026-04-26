"""DebugForge Middleware — Bug lifecycle gating and fix validation.

Runs as a custom middleware in the DebugForge agent loop.
Ensures reproduction before fixing, validates fixes against SCENARIOS.md.
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


class DebugForgeMiddleware(ConversationMiddleware):
    """Enforces structured bug squashing: reproduce → isolate → fix → validate."""

    def __init__(self) -> None:
        self.active_phase: str | None = None
        self.bug_reproduced: bool = False
        self.root_cause_found: bool = False
        self.fix_options: list[str] = []
        self.current_fix: str | None = None
        self.scenarios_validated: list[str] = []
        self.required_phases: list[str] = [
            "issue-intake",
            "reproduction",
            "isolation",
            "root-cause",
            "fix-options",
            "scenario-validation",
            "fix-application",
        ]

    async def before_turn(self, context: ConversationContext) -> MiddlewareResult:
        """Run before each LLM turn. Gate phases and inject reminders."""
        messages_to_inject: list[str] = []

        if self.active_phase:
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>DebugForge phase: {self.active_phase}. "
                f"Reproduced: {self.bug_reproduced}, "
                f"Root cause found: {self.root_cause_found}, "
                f"Fix options: {len(self.fix_options)}.</{VIBE_WARNING_TAG}>"
            )

        # Check recent writes for phase tracking
        self._check_recent_writes(context.messages)

        # Phase gating: cannot skip to fix without reproduction
        if self.active_phase in ("root-cause", "fix-options", "fix-application") and not self.bug_reproduced:
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>Cannot proceed to {self.active_phase}: "
                f"bug must be reproduced first. Run /debugforge-01-reproduction.</{VIBE_WARNING_TAG}>"
            )
            return MiddlewareResult(
                action=MiddlewareAction.INJECT_MESSAGE,
                message="\n\n".join(messages_to_inject),
            )

        # Phase gating: cannot apply fix without scenario validation
        if self.active_phase == "fix-application" and not self.scenarios_validated:
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>Cannot apply fix: "
                f"must validate against SCENARIOS.md first.</{VIBE_WARNING_TAG}>"
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

    def _check_recent_writes(self, messages) -> None:
        """Check recent writes for phase tracking."""
        for msg in messages[-10:]:
            if getattr(msg, 'role', None) == 'assistant':
                for tc in getattr(msg, 'tool_calls', []):
                    if getattr(tc, 'function', {}).get('name', '') == 'write_file':
                        args = getattr(tc, 'function', {}).get('arguments', {})
                        file_path = args.get('file_path', '')
                        if 'REPRODUCTION' in str(file_path).upper():
                            self.bug_reproduced = True
                        if 'FIX' in str(file_path).upper():
                            self.current_fix = str(file_path)

    def set_phase(self, phase: str) -> None:
        """Set the current DebugForge phase."""
        if phase not in self.required_phases:
            logger.warning("Unknown DebugForge phase: %s", phase)
        self.active_phase = phase
        logger.info("DebugForge phase set to: %s", phase)

    def mark_reproduced(self) -> None:
        """Mark bug as successfully reproduced."""
        self.bug_reproduced = True
        logger.info("DebugForge: bug reproduction confirmed")

    def mark_root_cause_found(self) -> None:
        """Mark root cause as identified."""
        self.root_cause_found = True
        logger.info("DebugForge: root cause found")

    def add_fix_option(self, description: str) -> None:
        """Add a fix option."""
        self.fix_options.append(description)
        logger.info("DebugForge: added fix option (%d total)", len(self.fix_options))

    def mark_scenario_validated(self, scenario_name: str) -> None:
        """Mark a scenario as validated against the fix."""
        if scenario_name not in self.scenarios_validated:
            self.scenarios_validated.append(scenario_name)
            logger.info("DebugForge: validated scenario '%s' (%d total)", scenario_name, len(self.scenarios_validated))

    def get_state(self) -> dict:
        """Return current middleware state."""
        return {
            "active_phase": self.active_phase,
            "bug_reproduced": self.bug_reproduced,
            "root_cause_found": self.root_cause_found,
            "fix_options": self.fix_options.copy(),
            "current_fix": self.current_fix,
            "scenarios_validated": self.scenarios_validated,
        }

    def restore_state(self, state: dict) -> None:
        """Restore middleware state from checkpoint."""
        self.active_phase = state.get("active_phase")
        self.bug_reproduced = state.get("bug_reproduced", False)
        self.root_cause_found = state.get("root_cause_found", False)
        self.fix_options = state.get("fix_options", [])
        self.current_fix = state.get("current_fix")
        self.scenarios_validated = state.get("scenarios_validated", [])
        logger.info("DebugForge middleware state restored: phase=%s", self.active_phase)

    def reset(self, reset_reason: ResetReason = ResetReason.STOP) -> None:
        """Reset middleware state."""
        self.active_phase = None
        self.bug_reproduced = False
        self.root_cause_found = False
        self.fix_options = []
        self.current_fix = None
        self.scenarios_validated = []
        logger.info("DebugForge middleware reset due to: %s", reset_reason)
