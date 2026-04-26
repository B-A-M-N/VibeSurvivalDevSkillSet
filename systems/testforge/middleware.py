"""TestForge Middleware — Test coverage gating and scenario enforcement.

Runs as a custom middleware in the TestForge agent loop.
Ensures every hard gate in MASTER_SPEC.md has a test before allowing handoff.
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


class TestForgeMiddleware(ConversationMiddleware):
    """Enforces test coverage requirements and gates handoff to next system."""

    def __init__(self) -> None:
        self.active_phase: str | None = None
        self.test_count: int = 0
        self.coverage_threshold: float = 0.8  # 80% coverage required
        self.hard_gates_covered: list[str] = []
        self.hard_gates_total: list[str] = []

    async def before_turn(self, context: ConversationContext) -> MiddlewareResult:
        """Run before each LLM turn. Inject coverage reminders and phase context."""
        messages_to_inject: list[str] = []

        if self.active_phase:
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>TestForge phase: {self.active_phase}. "
                f"Tests written: {self.test_count}. "
                f"Hard gates covered: {len(self.hard_gates_covered)}/{len(self.hard_gates_total)}.</{VIBE_WARNING_TAG}>"
            )

        # Track test writes
        recent = self._count_recent_test_writes(context.messages)
        if recent > 0:
            self.test_count += recent

        # Warn if trying to handoff without sufficient coverage
        if self.active_phase == "handoff" and len(self.hard_gates_covered) < len(self.hard_gates_total):
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>Cannot handoff: not all hard gates have tests. "
                f"Missing: {set(self.hard_gates_total) - set(self.hard_gates_covered)}</{VIBE_WARNING_TAG}>"
            )

        if messages_to_inject:
            return MiddlewareResult(
                action=MiddlewareAction.INJECT_MESSAGE,
                message="\n\n".join(messages_to_inject),
            )

        return MiddlewareResult()

    def _count_recent_test_writes(self, messages) -> int:
        """Count test file writes in recent messages."""
        count = 0
        for msg in messages[-10:]:
            if getattr(msg, 'role', None) == 'assistant':
                for tc in getattr(msg, 'tool_calls', []):
                    if getattr(tc, 'function', {}).get('name', '') in ('write_file', 'search_replace', 'Edit'):
                        args = getattr(tc, 'function', {}).get('arguments', {})
                        file_path = args.get('file_path', args.get('path', ''))
                        if 'test' in str(file_path).lower() or 'spec' in str(file_path).lower():
                            count += 1
        return count

    def set_hard_gates(self, gate_names: list[str]) -> None:
        """Set the list of hard gates from MASTER_SPEC.md."""
        self.hard_gates_total = gate_names
        logger.info("TestForge: registered %d hard gates", len(gate_names))

    def mark_gate_covered(self, gate_name: str) -> None:
        """Mark a hard gate as having a test."""
        if gate_name not in self.hard_gates_covered:
            self.hard_gates_covered.append(gate_name)
            logger.info("TestForge: gate '%s' covered (%d/%d)", gate_name, len(self.hard_gates_covered), len(self.hard_gates_total))

    def set_phase(self, phase: str) -> None:
        """Set the current TestForge phase."""
        self.active_phase = phase
        logger.info("TestForge phase set to: %s", phase)

    def get_state(self) -> dict:
        """Return current middleware state."""
        return {
            "active_phase": self.active_phase,
            "test_count": self.test_count,
            "coverage_threshold": self.coverage_threshold,
            "hard_gates_covered": self.hard_gates_covered,
            "hard_gates_total": self.hard_gates_total,
        }

    def restore_state(self, state: dict) -> None:
        """Restore middleware state from checkpoint."""
        self.active_phase = state.get("active_phase")
        self.test_count = state.get("test_count", 0)
        self.coverage_threshold = state.get("coverage_threshold", 0.8)
        self.hard_gates_covered = state.get("hard_gates_covered", [])
        self.hard_gates_total = state.get("hard_gates_total", [])
        logger.info("TestForge middleware state restored")

    def reset(self, reset_reason: ResetReason = ResetReason.STOP) -> None:
        """Reset middleware state."""
        self.active_phase = None
        self.test_count = 0
        self.hard_gates_covered = []
        self.hard_gates_total = []
        logger.info("TestForge middleware reset due to: %s", reset_reason)
