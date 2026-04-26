"""State Injection Middleware — implements MiddlewareInterface.

Injects last known state into the conversation so the agent
doesn't "forget" mid-run.

Surgical injection: only last failure, current phase,
2-3 recent actions, active constraints.
"""

from __future__ import annotations
from typing import Optional
import logging
import json
from pathlib import Path

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate,
)
from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult,
)


logger = logging.getLogger(__name__)


class StateInjectionMiddleware(MiddlewareInterface):
    """Injects state context before each model turn."""

    priority: int = 10  # Runs first — injects state before observation

    def __init__(self, label: str = "StateInjectionMiddleware",
                 state_dir: Optional[Path] = None,
                 max_injection_length: int = 500,  # Keep it short
                 state_agent: str = "team-ops"):
        super().__init__(label=label)
        self.state_dir = state_dir or Path.home() / ".vibe" / "state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.max_injection_length = max_injection_length
        self.state_agent = state_agent

        # State files to summarize (surgical — only most relevant)
        self.state_files = [
            "PROBLEM_FRAME.md",
            "RESEARCH_PLAN.md",
            "FINAL_RESEARCH_PACKET.md",
            ".checkpoint.json",
        ]

        # Tracking
        self.last_injection_turn = -1
        self._stale_detected = False
        self._stale_details: list[str] = []
        logger.info(
            "%s initialized, state_dir=%s, max_len=%d, state_agent=%s",
            label, self.state_dir, max_injection_length, state_agent,
        )

    # --- Phase boundary hooks ---

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """Inject state summary, or invoke state agent if stale."""
        if context.phase == self.last_injection_turn:
            return MiddlewareResult.cont()  # Already injected this phase

        # Check for stale state
        self._check_stale_state(context)
        if self._stale_detected:
            if self.agent_manager:
                try:
                    self.agent_manager.set_current_agent(self.state_agent)
                    return MiddlewareResult.redirect(
                        self.state_agent,
                        f"[{self.label}] Stale state detected:\n"
                        f"{chr(10).join(self._stale_details)}\n"
                        f"Switching to {self.state_agent} to fix."
                    )
                except Exception as e:
                    logger.error("%s: failed to invoke agent: %s", self.label, e)

            return MiddlewareResult.inject(
                f"[{self.label}] Stale state:\n"
                f"{chr(10).join(self._stale_details)}"
            )

        # Inject state summary
        state_summary = self._build_state_summary(context)
        if not state_summary:
            return MiddlewareResult.cont()

        self.last_injection_turn = context.phase

        return MiddlewareResult.inject(
            f"[{self.label}] State Summary:\n{state_summary}"
        )

    def after_phase(
        self, context: ForgeContext, result: ForgeResult,
    ) -> MiddlewareResult:
        """Persist any state updates after phase."""
        return MiddlewareResult.cont()

    # --- Real-time hooks ---

    def on_command(
        self, command: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Track commands for state staleness detection."""
        return MiddlewareResult.cont()

    def on_file_modified(
        self, path: str, operation: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Track file modifications for state tracking."""
        return MiddlewareResult.cont()

    def on_tool_result(
        self, tool_name: str, args: dict, result: object, context: ForgeContext,
    ) -> MiddlewareResult:
        """Track tool results for state updates."""
        return MiddlewareResult.cont()

    def inject_state(self, context: ForgeContext) -> MiddlewareResult:
        """Inject state summary (called by orchestrator before model turns).

        Surgical injection: only last failure, current phase,
        2-3 recent actions, active constraints.
        """
        parts: list[str] = []

        # 1. Current phase (always show)
        if context.phase:
            parts.append(f"Phase: {context.phase}")

        # 2. Last failure (from drift or verification events)
        last_failure = self._get_last_failure(context)
        if last_failure:
            parts.append(f"Last failure:\n  {last_failure}")

        # 3. 2-3 recent actions (from trace_events)
        recent_actions = self._get_recent_actions(context, count=3)
        if recent_actions:
            parts.append(f"Recent actions:\n{recent_actions}")

        # 4. Active constraints (from phase/gates)
        constraints = self._get_active_constraints(context)
        if constraints:
            parts.append(f"Active constraints:\n{constraints}")

        # 5. Phase steps counter
        if context.current_phase_steps > 0:
            parts.append(f"Phase steps: {context.current_phase_steps}")

        if not parts:
            return MiddlewareResult.cont()

        summary = "\n".join(parts)

        # Truncate if too long
        if len(summary) > self.max_injection_length:
            summary = summary[:self.max_injection_length] + "...[truncated]"

        return MiddlewareResult.inject(
            f"[{self.label}] Current Runtime State:\n{summary}"
        )

    # --- Surgical state builders ---

    def _get_last_failure(self, context: ForgeContext) -> str:
        """Get the last failure from drift/verification events."""
        # Check drift events (most recent first)
        for event in reversed(context.drift_events[-5:]):
            reason = event.get("reason", "")
            if reason:
                return f"Drift: {reason[:100]}"

        # Check verification events
        for event in reversed(context.verification_events[-5:]):
            if event.get("type") == "success_without_verification":
                return f"Premature success claim: {event.get('text_review', '')[:100]}"
            if event.get("type") == "bash_failure":
                return f"Bash failure: {event.get('command', '')[:100]}"

        # Check trace events for failures
        for event in reversed(context.trace_events[-10:]):
            if event.get("type") == "tool_result":
                if not event.get("ok", True):
                    return f"Tool failure: {event.get('tool', '')} - {event.get('preview', '')[:80]}"

        return ""

    def _get_recent_actions(self, context: ForgeContext, count: int = 3) -> str:
        """Get 2-3 recent actions from trace events."""
        actions: list[str] = []
        seen_commands: set[str] = set()

        for event in reversed(context.trace_events[-10:]):
            if len(actions) >= count:
                break

            if event.get("type") == "command":
                cmd = event.get("command", "")
                # Skip duplicate commands
                if cmd not in seen_commands:
                    seen_commands.add(cmd)
                    actions.append(f"  {cmd[:80]}")
            elif event.get("type") == "file_modified":
                path = event.get("path", "")
                if path not in seen_commands:
                    seen_commands.add(path)
                    actions.append(f"  Edited: {path}")

        return "\n".join(reversed(actions))

    def _get_active_constraints(self, context: ForgeContext) -> str:
        """Get active constraints from gates and phase."""
        constraints: list[str] = []

        # Open gates
        for gate in context.gates:
            if gate.is_open():
                constraints.append(f"  Gate '{gate.name}' is OPEN")
            else:
                constraints.append(f"  Gate '{gate.name}' is CLOSED")

        # Phase-specific constraints
        if context.phase:
            phase_lower = context.phase.lower()
            if "research" in phase_lower:
                constraints.append("  Research phase: read-only, no writes")
            elif "spec" in phase_lower:
                constraints.append("  Spec phase: docs/artifacts only")
            elif "implementation" in phase_lower:
                constraints.append("  Implementation: edits allowed, need evidence")
            elif "verification" in phase_lower:
                constraints.append("  Verification: tests only, no new features")

        return "\n".join(constraints)

    # --- State building (backward compat, more verbose) ---

    def _build_state_summary(self, context: ForgeContext) -> str:
        """Build a concise state summary (phase boundary version)."""
        parts: list[str] = []

        # Check state files in state_dir (surgical read)
        for fname in self.state_files:
            f = self.state_dir / fname
            if f.exists() and f.is_file():
                try:
                    content = f.read_text()[:200]  # Shorter than before
                    parts.append(f"[{fname}]: {content}")
                except Exception:
                    pass

        # Checkpoint (brief)
        checkpoint_file = self.state_dir / ".checkpoint.json"
        if checkpoint_file.exists():
            try:
                data = json.loads(checkpoint_file.read_text())
                phase = data.get("phase", "unknown")
                steps = data.get("completed_steps", [])
                parts.append(
                    f"[checkpoint]: phase={phase}, "
                    f"steps={len(steps)}"
                )
            except Exception:
                pass

        return "\n".join(parts) if parts else ""

    def _check_stale_state(self, context: ForgeContext) -> None:
        """Check if state is stale."""
        self._stale_detected = False
        self._stale_details = []

        # Check checkpoint for stale state
        checkpoint_art = context.get_artifact(".checkpoint.json")
        if checkpoint_art and checkpoint_art.exists():
            try:
                data = json.loads(Path(checkpoint_art.path).read_text())
                phase = data.get("phase", "")
                steps = data.get("completed_steps", [])

                if phase in ("EXECUTING", "BLOCKED") and len(steps) > 5:
                    # Check if the same step has been repeated
                    recent = steps[-3:] if len(steps) >= 3 else steps
                    if len(set(recent)) < len(recent):
                        self._stale_detected = True
                        self._stale_details.append(
                            f"Phase {phase} with {len(steps)} steps, "
                            f"recent steps show no progress: {recent}"
                        )
                        logger.warning(
                            "%s: stale state detected: %s",
                            self.label, self._stale_details,
                        )
                        return
            except Exception:
                pass

        # Check if recent tool calls show no progress
        if len(context.recent_tool_calls) > 10:
            # Check if the same tools are being called repeatedly
            recent_tools = [t.get("tool") for t in context.recent_tool_calls[-10:]]
            if len(set(recent_tools)) == 1:
                self._stale_detected = True
                self._stale_details.append(
                    f"Last 10 tool calls are all '{recent_tools[0]}'"
                )

    # --- Backward compat stubs ---

    def on_gate_failure(
        self, gate: ForgeGate, context: ForgeContext,
    ) -> MiddlewareResult:
        return MiddlewareResult.cont()

    def on_drift_detected(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        return MiddlewareResult.cont()

    def on_verification_failure(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        return MiddlewareResult.cont()

    def emit_trace(self, event: str, data: dict) -> None:
        self._logger.debug("%s trace: %s %s", self.label, event, data)
