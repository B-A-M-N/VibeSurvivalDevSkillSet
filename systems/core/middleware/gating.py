"""Gating Middleware — implements MiddlewareInterface.

Hard-gates turns until user confirms or a condition is met.
Can invoke a gating agent when gates are stuck.
Consumes on_tool_call() hook for phase/tool rules.
"""

from __future__ import annotations
from typing import Optional
import logging

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ForgeGate,
)
from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult,
)


logger = logging.getLogger(__name__)


# Phase -> allowed tools (simplified). Tools not listed are allowed in all phases.
PHASE_TOOL_RULES = {
    "research": {
        "allow": {"read_file", "Read", "Grep", "Bash", "search_replace", "SearchReplace"},
        "block": {"write_file", "Write", "edit_file", "apply_patch"},
        "require_evidence_for": [],
    },
    "spec": {
        "allow": {"read_file", "Read", "Grep", "write_file", "Write"},
        "block": {"edit_file", "apply_patch"},
        "require_evidence_for": ["write_file", "Write"],
    },
    "implementation": {
        "allow": {"write_file", "Write", "edit_file", "Read", "Grep", "Bash"},
        "block": {},
        "require_evidence_for": ["write_file", "Write", "edit_file"],
    },
    "verification": {
        "allow": {"bash", "Bash", "read_file", "Read", "Grep"},
        "block": {"write_file", "Write", "edit_file", "apply_patch"},
        "require_evidence_for": [],
    },
}

# Tools that always require user confirmation
USER_CONFIRM_TOOLS = {
    "apply_patch", "ApplyPatch",
    "delete_file", "DeleteFile",
}


class GatingMiddleware(MiddlewareInterface):
    """Blocks turns until explicit user confirmation or phase advancement."""

    priority: int = 400  # Runs last — enforces after observation

    def __init__(self, label: str = "GatingMiddleware",
                 require_confirmation: bool = False,
                 gating_agent: str = "overlord"):
        super().__init__(label=label)
        self.require_confirmation = require_confirmation
        self.gating_agent = gating_agent
        self.user_confirmed = False
        self.current_phase = 0
        self.phase_gating_enabled = False
        self.phase_map: dict[str, int] = {}  # skill_name_prefix -> phase_number
        self.phase_names: list[str] = []
        logger.info(
            "%s initialized (confirmation=%s, phase_gating=%s, agent=%s)",
            label, require_confirmation, self.phase_gating_enabled, gating_agent,
        )

    def enable_phase_gating(self, phase_map: dict, phase_names: list[str]) -> None:
        """Configure phase-based gating. Call before entering pipeline."""
        self.phase_gating_enabled = True
        self.phase_map = phase_map
        self.phase_names = phase_names
        logger.info("Phase gating enabled with %d phases", len(phase_names))

    def set_agent_manager(self, agent_manager) -> None:
        """Inject the agent manager (called by orchestrator setup)."""
        self.agent_manager = agent_manager
        logger.info("%s: agent_manager injected", self.label)

    # --- Phase boundary hooks ---

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """Block if waiting for confirmation or invalid phase skip."""
        if self.require_confirmation and not self.user_confirmed:
            logger.info("%s: waiting for user confirmation", self.label)
            return MiddlewareResult.block(
                f"[{self.label}] Waiting for your input to proceed."
            )

        if self.phase_gating_enabled:
            current_skill = self._get_current_skill(context)
            expected_phase = self._skill_to_phase(current_skill)
            if expected_phase > self.current_phase + 1:
                name = (
                    self.phase_names[expected_phase]
                    if expected_phase < len(self.phase_names)
                    else str(expected_phase)
                )
                prev = (
                    self.phase_names[self.current_phase]
                    if self.current_phase < len(self.phase_names)
                    else str(self.current_phase)
                )
                logger.warning(
                    "%s: phase skip %s -> %s", self.label, self.current_phase, expected_phase
                )
                # Invoke gating agent to resolve the stuck state
                if self.agent_manager:
                    try:
                        logger.info(
                            "%s: invoking %s to resolve gate",
                            self.label, self.gating_agent
                        )
                        self.agent_manager.set_current_agent(self.gating_agent)
                    except Exception as e:
                        logger.error("%s: failed to invoke agent: %s", self.label, e)
                return MiddlewareResult.block(
                    f"[{self.label}] Cannot skip to {name}. "
                    f"Complete {prev} first. Overlord summoned."
                )

        self.user_confirmed = False
        return MiddlewareResult.cont()

    def after_phase(
        self, context: ForgeContext, result: ForgeResult,
    ) -> MiddlewareResult:
        """Update phase state after phase completes."""
        if self.phase_gating_enabled:
            current_skill = self._get_current_skill(context)
            new_phase = self._skill_to_phase(current_skill)
            if new_phase > self.current_phase:
                logger.info(
                    "%s: phase advanced %s -> %s",
                    self.label, self.current_phase, new_phase
                )
                self.current_phase = new_phase
        return MiddlewareResult.cont()

    # --- Real-time hooks (the control plane) ---

    def on_tool_call(
        self, tool_name: str, args: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Intercept tool calls BEFORE execution.

        Check phase/tool rules and user confirmation requirements.
        """
        tool_lower = tool_name.lower()

        # Rule 1: always require user confirmation for certain tools
        if any(t.lower() == tool_lower for t in USER_CONFIRM_TOOLS):
            return MiddlewareResult.require_user(
                f"[{self.label}] User confirmation required for {tool_name}."
            )

        # Rule 2: phase/tool rules
        phase_rules = self._get_phase_rules(context.phase)
        if phase_rules:
            # Check if tool is explicitly blocked in this phase
            blocked = phase_rules.get("block", set())
            if any(t.lower() == tool_lower for t in blocked):
                return MiddlewareResult.block(
                    f"[{self.label}] Tool {tool_name} is not allowed "
                    f"in phase '{context.phase}'."
                )

            # Check if tool requires evidence in this phase
            require_evidence = phase_rules.get("require_evidence_for", [])
            if any(t.lower() == tool_lower for t in require_evidence):
                if not self._has_recent_evidence(context):
                    return MiddlewareResult.block(
                        f"[{self.label}] Tool {tool_name} requires "
                        f"recent evidence before use in phase '{context.phase}'."
                    )

        return MiddlewareResult.cont()

    def on_message(
        self, message: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Check messages for gate violations."""
        # Could check for premature success claims, etc.
        return MiddlewareResult.cont()

    # --- Backward compat ---

    def on_gate_failure(
        self, gate: ForgeGate, context: ForgeContext,
    ) -> MiddlewareResult:
        """Called when a gate check fails (backward compat)."""
        return MiddlewareResult.block(
            f"[{self.label}] Gate '{gate.name}' is closed. "
            f"Required artifacts missing."
        )

    def on_drift_detected(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        """Called when drift/loop is detected."""
        return MiddlewareResult.inject(
            f"[{self.label}] DRIFT DETECTED: {reason}\n"
            f"Change strategy. Review what failed."
        )

    def on_verification_failure(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        """Called when verification fails."""
        return MiddlewareResult.block(
            f"[{self.label}] Verification failed: {reason}"
        )

    def inject_state(self, context: ForgeContext) -> MiddlewareResult:
        """Inject state context."""
        return MiddlewareResult.cont()

    def emit_trace(self, event: str, data: dict) -> None:
        """Record a trace event."""
        logger.debug("%s trace: %s %s", self.label, event, data)

    def confirm(self) -> None:
        """Call when user confirms the current step."""
        self.user_confirmed = True
        logger.info("%s: step confirmed by user", self.label)

    # --- Helpers ---

    def _get_current_skill(self, context: ForgeContext) -> Optional[str]:
        """Extract current skill name from context artifacts."""
        for art in reversed(context.artifacts):
            if art.name and ('/' in art.name or 'forge' in art.name.lower()):
                return art.name
        # Also check recent tool calls
        if context.recent_tool_calls:
            last = context.recent_tool_calls[-1]
            if 'skill' in last.get('args', {}):
                return last['args']['skill']
        return None

    def _skill_to_phase(self, skill_name: Optional[str]) -> int:
        """Map skill name to phase number."""
        if not skill_name:
            return 0
        if not self.phase_map:
            return 0
        for prefix, phase in self.phase_map.items():
            if prefix in skill_name.lower():
                return phase
        return self.current_phase

    def _get_phase_rules(self, phase: str) -> Optional[dict]:
        """Get tool rules for a phase."""
        phase_lower = phase.lower()
        for key, rules in PHASE_TOOL_RULES.items():
            if key in phase_lower:
                return rules
        return None

    def _has_recent_evidence(self, context: ForgeContext) -> bool:
        """Check if there's recent evidence in the context."""
        for art in context.artifacts:
            if art.artifact_type == "evidence" and art.exists():
                return True
        for event in context.trace_events[-5:]:
            if event.get("type") == "command":
                cmd = event.get("command", "").lower()
                if any(v in cmd for v in ("test", "lint", "typecheck")):
                    return True
        return False
