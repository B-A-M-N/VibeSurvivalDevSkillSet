"""DocForge Middleware — Documentation coverage tracking and staleness detection.

Runs as a custom middleware in the DocForge agent loop.
Tracks doc coverage against code+spec and detects stale documentation.
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
import time

logger = logging.getLogger(__name__)


class DocForgeMiddleware(ConversationMiddleware):
    """Tracks documentation coverage and detects stale docs."""

    def __init__(self) -> None:
        self.active_phase: str | None = None
        self.docs_generated: int = 0
        self.docs_updated: int = 0
        self.stale_docs: list[str] = []
        self.coverage_map: dict[str, list[str]] = {}  # code_file -> [doc_files]
        self.last_staleness_check: float = 0.0
        self.staleness_interval: float = 300.0  # check every 5 minutes

    async def before_turn(self, context: ConversationContext) -> MiddlewareResult:
        """Run before each LLM turn. Inject coverage status and staleness warnings."""
        messages_to_inject: list[str] = []
        now = time.time()

        if self.active_phase:
            messages_to_inject.append(
                f"<{VIBE_WARNING_TAG}>DocForge phase: {self.active_phase}. "
                f"Docs generated: {self.docs_generated}, updated: {self.docs_updated}, "
                f"stale: {len(self.stale_docs)}.</{VIBE_WARNING_TAG}>"
            )

        # Track doc writes
        gen, upd = self._count_recent_doc_writes(context.messages)
        if gen > 0 or upd > 0:
            self.docs_generated += gen
            self.docs_updated += upd

        # Periodic staleness check reminder
        if now - self.last_staleness_check >= self.staleness_interval:
            if self.stale_docs:
                messages_to_inject.append(
                    f"<{VIBE_WARNING_TAG}>Stale docs detected: {len(self.stale_docs)} docs may be out of date. "
                    f"Run /docforge-05-doc-continuity-check to update.</{VIBE_WARNING_TAG}>"
                )
            self.last_staleness_check = now

        if messages_to_inject:
            return MiddlewareResult(
                action=MiddlewareAction.INJECT_MESSAGE,
                message="\n\n".join(messages_to_inject),
            )

        return MiddlewareResult()

    def _count_recent_doc_writes(self, messages) -> tuple[int, int]:
        """Count doc-related writes in recent messages."""
        generated = 0
        updated = 0
        for msg in messages[-10:]:
            if getattr(msg, 'role', None) == 'assistant':
                for tc in getattr(msg, 'tool_calls', []):
                    if getattr(tc, 'function', {}).get('name', '') in ('write_file', 'search_replace', 'Edit'):
                        args = getattr(tc, 'function', {}).get('arguments', {})
                        file_path = args.get('file_path', args.get('path', ''))
                        content = args.get('content', '')
                        if 'doc' in str(file_path).lower() or str(file_path).endswith('.md'):
                            if 'generate' in str(content).lower() or 'new' in str(content).lower():
                                generated += 1
                            elif 'update' in str(content).lower():
                                updated += 1
        return generated, updated

    def register_coverage(self, code_file: str, doc_files: list[str]) -> None:
        """Register that a code file has corresponding documentation."""
        self.coverage_map[code_file] = doc_files
        logger.info("DocForge: mapped %s -> %s", code_file, doc_files)

    def mark_stale(self, doc_file: str) -> None:
        """Mark a documentation file as stale."""
        if doc_file not in self.stale_docs:
            self.stale_docs.append(doc_file)
            logger.info("DocForge: marked stale: %s", doc_file)

    def set_phase(self, phase: str) -> None:
        """Set the current DocForge phase."""
        self.active_phase = phase
        logger.info("DocForge phase set to: %s", phase)

    def get_state(self) -> dict:
        """Return current middleware state."""
        return {
            "active_phase": self.active_phase,
            "docs_generated": self.docs_generated,
            "docs_updated": self.docs_updated,
            "stale_docs": self.stale_docs.copy(),
            "coverage_map": self.coverage_map.copy(),
            "last_staleness_check": self.last_staleness_check,
        }

    def restore_state(self, state: dict) -> None:
        """Restore middleware state from checkpoint."""
        self.active_phase = state.get("active_phase")
        self.docs_generated = state.get("docs_generated", 0)
        self.docs_updated = state.get("docs_updated", 0)
        self.stale_docs = state.get("stale_docs", [])
        self.coverage_map = state.get("coverage_map", {})
        self.last_staleness_check = state.get("last_staleness_check", 0.0)
        logger.info("DocForge middleware state restored: phase=%s", self.active_phase)

    def reset(self, reset_reason: ResetReason = ResetReason.STOP) -> None:
        """Reset middleware state."""
        self.active_phase = None
        self.docs_generated = 0
        self.docs_updated = 0
        self.stale_docs = []
        self.coverage_map = {}
        self.last_staleness_check = 0.0
        logger.info("DocForge middleware reset due to: %s", reset_reason)
