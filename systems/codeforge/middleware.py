"""CodeForge Middleware — Invariant enforcement during implementation.

Runs as a custom middleware in the CodeForge agent loop.
Injects invariant checks before file writes and gates phase transitions.
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

import json
import logging

logger = logging.getLogger(__name__)


class CodeForgeMiddleware(ConversationMiddleware):
    """Enforces invariants and gates phase transitions during CodeForge execution."""

    def __init__(self) -> None:
        self.active_phase: str | None = None
        self.phase_stack: list[str] = []
        self.write_count: int = 0
        self.last_invariant_check: int = 0
        self.invariant_interval: int = 3  # check every N writes

    async def before_turn(self, context: ConversationContext) -> MiddlewareResult:
        """Run before each LLM turn. Inject invariant reminders and phase context."""
        messages_to_inject: list[str] = []

        # Inject current phase context
        if self.active_phase:
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>Currently in CodeForge phase: {self.active_phase}. "
                f"All file writes will be checked against spec invariants.</{VIBE_WARNING_TAG}>"
            )

        # Check for recent file writes and update counter
        recent_writes = self._count_recent_writes(context.messages)
        if recent_writes > 0:
            self.write_count += recent_writes

        # Periodic invariant reminder
        if self.write_count - self.last_invariant_check >= self.invariant_interval:
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>Reminder: You have written {self.write_count} files this session. "
                f"Ensure every write complies with MASTER_SPEC.md invariants.</{VIBE_WARNING_TAG}>"
            )
            self.last_invariant_check = self.write_count

        if messages_to_inject:
            return MiddlewareResult(
                action=MiddlewareAction.INJECT_MESSAGE,
                message="\n\n".join(messages_to_inject),
            )

        return MiddlewareResult()

    def enter_phase(self, phase_name: str, context: dict | None = None) -> None:
        """Enter a new CodeForge phase."""
        if self.active_phase:
            self.phase_stack.append(self.active_phase)
        self.active_phase = phase_name
        logger.info("CodeForge entered phase: %s (stack depth: %d)", phase_name, len(self.phase_stack))

    def exit_phase(self) -> str | None:
        """Exit current phase, restore previous if any."""
        exited = self.active_phase
        if self.phase_stack:
            self.active_phase = self.phase_stack.pop()
            logger.info("CodeForge exited phase: %s, restored: %s", exited, self.active_phase)
        else:
            self.active_phase = None
            logger.info("CodeForge exited phase: %s (no previous phase)", exited)
        return exited

    def get_state(self) -> dict:
        """Return current middleware state for checkpointing."""
        return {
            "active_phase": self.active_phase,
            "phase_stack": self.phase_stack.copy(),
            "write_count": self.write_count,
            "last_invariant_check": self.last_invariant_check,
        }

    def restore_state(self, state: dict) -> None:
        """Restore middleware state from checkpoint."""
        self.active_phase = state.get("active_phase")
        self.phase_stack = state.get("phase_stack", [])
        self.write_count = state.get("write_count", 0)
        self.last_invariant_check = state.get("last_invariant_check", 0)
        logger.info("CodeForge middleware state restored: phase=%s", self.active_phase)

    def _count_recent_writes(self, messages) -> int:
        """Count file write tool calls in recent messages."""
        count = 0
        for msg in messages[-10:]:
            if getattr(msg, 'role', None) == 'assistant':
                tool_calls = getattr(msg, 'tool_calls', [])
                for tc in tool_calls:
                    if getattr(tc, 'function', {}).get('name', '') in ('write_file', 'search_replace', 'Edit'):
                        count += 1
        return count

    def reset(self, reset_reason: ResetReason = ResetReason.STOP) -> None:
        """Reset middleware state."""
        self.active_phase = None
        self.phase_stack = []
        self.write_count = 0
        self.last_invariant_check = 0
        logger.info("CodeForge middleware reset due to: %s", reset_reason)
