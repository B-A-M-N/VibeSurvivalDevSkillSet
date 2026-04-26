"""Execution Tracing Middleware — implements MiddlewareInterface.

Captures commands run, files modified, decisions made in real time.
Analyzes traces and invokes agents to handle issues (MonitorForge).
"""

from __future__ import annotations
from typing import Optional
import logging
import json
import time
from pathlib import Path
from collections import defaultdict

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeGate,
)
from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult,
)


logger = logging.getLogger(__name__)


class TracingMiddleware(MiddlewareInterface):
    """Captures all execution events for observability and agent invocation."""

    priority: int = 50  # Runs first — observes everything

    def __init__(self, label: str = "TracingMiddleware",
                 trace_dir: Optional[Path] = None,
                 max_turn_duration: float = 60.0,
                 analysis_agent: str = "team-ops"):
        super().__init__(label=label)
        self.trace_dir = trace_dir or Path.home() / ".vibe" / "traces"
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.max_turn_duration = max_turn_duration
        self.analysis_agent = analysis_agent

        # Current turn being recorded (populated by hooks)
        self.current_turn: dict = {}
        self.turn_start_time: float = 0.0

        # Session-level trace (persisted)
        self.current_trace: dict = {
            "session_id": None,
            "turns": [],
            "commands": [],
            "files_modified": [],
            "decisions": [],
        }

        # Analysis state
        self._issue_detected = False
        self._issue_details: list[str] = []
        logger.info(
            "%s initialized, trace_dir=%s, analysis_agent=%s",
            label, self.trace_dir, analysis_agent,
        )

    # --- Phase boundary hooks ---

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """Start a new phase in the trace."""
        self.turn_start_time = time.time()
        self.current_turn = {
            "phase": context.phase,
            "start_time": self.turn_start_time,
            "commands": [],
            "files_modified": [],
            "tool_results": [],
            "decisions": [],
            "tool_calls": [],
        }

        # If previous analysis detected issues, inject warning
        if self._issue_detected and self.agent_manager:
            try:
                self.agent_manager.set_current_agent(self.analysis_agent)
                return MiddlewareResult.redirect(
                    self.analysis_agent,
                    f"[{self.label}] Trace analysis detected issues:\n"
                    f"{chr(10).join(self._issue_details)}\n"
                    f"Switching to {self.analysis_agent} to investigate."
                )
            except Exception as e:
                logger.error("%s: failed to invoke agent: %s", self.label, e)

        return MiddlewareResult.cont()

    def after_phase(
        self, context: ForgeContext, result: ForgeResult,
    ) -> MiddlewareResult:
        """Finalize phase trace, analyze for issues."""
        if self.current_turn:
            self.current_turn["end_time"] = time.time()
            self.current_turn["duration"] = (
                self.current_turn["end_time"] - self.current_turn["start_time"]
            )
            self.current_trace["turns"].append(self.current_turn)

            # Analyze for issues now that turn is complete
            self._analyze_trace()

            # Persist after each phase
            self._persist_trace()

            self.current_turn = {}

        return MiddlewareResult.cont()

    # --- Real-time hooks (populate the trace) ---

    def on_command(
        self, command: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Record shell commands as they happen."""
        if self.current_turn is not None:
            self.current_turn["commands"].append(command)
        self.current_trace["commands"].append(command)
        return MiddlewareResult.cont()

    def on_file_modified(
        self, path: str, operation: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Record file modifications as they happen."""
        if self.current_turn is not None:
            self.current_turn["files_modified"].append({
                "path": path,
                "operation": operation,
            })
        if path not in self.current_trace["files_modified"]:
            self.current_trace["files_modified"].append(path)
        return MiddlewareResult.cont()

    def on_tool_result(
        self, tool_name: str, args: dict, result: object, context: ForgeContext,
    ) -> MiddlewareResult:
        """Record tool results as they happen."""
        if self.current_turn is not None:
            self.current_turn["tool_results"].append({
                "tool": tool_name,
                "ok": not self._looks_failed(str(result)),
                "preview": str(result)[:500],
            })
        return MiddlewareResult.cont()

    def on_tool_call(
        self, tool_name: str, args: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Record tool calls."""
        if self.current_turn is not None:
            self.current_turn["tool_calls"].append({
                "tool": tool_name,
                "args_preview": str(args)[:200],
            })
        return MiddlewareResult.cont()

    def on_message(
        self, message: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Record assistant decisions from messages."""
        text = message.get("content", "")
        if text and self.current_turn is not None:
            # Only record substantive messages (not empty chunks)
            if len(text) > 10:
                self.current_turn["decisions"].append(
                    f"msg: {text[:100]}"
                )
        return MiddlewareResult.cont()

    def on_action(
        self, action: str, data: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Record agent actions."""
        if self.current_turn is not None:
            self.current_turn["decisions"].append(
                f"action: {action}"
            )
        self.current_trace["decisions"].append({
            "action": action,
            "data": data,
            "timestamp": time.time(),
        })
        return MiddlewareResult.cont()

    # --- Analysis ---

    def _analyze_trace(self) -> None:
        """Analyze the current trace for issues."""
        turns = self.current_trace["turns"]
        if not turns:
            return

        issues: list[str] = []

        # Check for high command count without file changes
        recent = turns[-3:] if len(turns) >= 3 else turns
        total_cmds = sum(len(t.get("commands", [])) for t in recent)
        total_files = sum(len(t.get("files_modified", [])) for t in recent)

        if total_cmds > 10 and total_files == 0:
            issues.append(
                f"High command count ({total_cmds}) "
                f"with no file changes in last {len(recent)} phases"
            )

        # Check for long-running phases
        for t in recent:
            dur = t.get("duration", 0)
            if dur > self.max_turn_duration:
                issues.append(
                    f"Long phase detected: "
                    f"{t.get('phase', '?')} took {dur:.1f}s"
                )

        # Check for repeated failed tool results
        if self.current_turn:
            failed = [
                r for r in self.current_turn.get("tool_results", [])
                if not r.get("ok", True)
            ]
            if len(failed) >= 3:
                issues.append(
                    f"{len(failed)} tool failures detected in current turn"
                )

        if issues:
            self._issue_detected = True
            self._issue_details = issues
            logger.warning(
                "%s: trace issues detected: %s", self.label, issues
            )
        else:
            self._issue_detected = False
            self._issue_details = []

    def _persist_trace(self) -> None:
        """Write the current trace to disk."""
        try:
            trace_file = self.trace_dir / f"trace_{int(time.time())}.json"
            with open(trace_file, "w") as f:
                json.dump(self.current_trace, f, indent=2, default=str)
        except Exception as e:
            logger.warning("%s: failed to persist trace: %s", self.label, e)

    def get_trace_summary(self) -> str:
        """Return a human-readable trace summary."""
        turns = self.current_trace["turns"]
        if not turns:
            return "No trace data yet."

        summary = [f"Trace Summary ({len(turns)} phases):"]
        for t in turns:
            dur = t.get("duration", 0)
            cmds = len(t.get("commands", []))
            files = len(t.get("files_modified", []))
            summary.append(
                f"  Phase {t.get('phase', '?')}: "
                f"{dur:.1f}s, {cmds} commands, {files} files modified"
            )

        summary.append(
            f"Total commands: {len(self.current_trace['commands'])}"
        )
        summary.append(
            f"Total files modified: "
            f"{len(self.current_trace['files_modified'])}"
        )
        return "\n".join(summary)

    def _looks_failed(self, result_str: str) -> bool:
        """Check if a tool result looks like a failure."""
        lower = result_str.lower()
        return any(
            w in lower for w in ("error", "failed", "exception", "traceback")
        )

    # --- Backward compat stubs ---

    def on_gate_failure(
        self, gate: ForgeGate, context: ForgeContext,
    ) -> MiddlewareResult:
        return MiddlewareResult.cont()

    def on_drift_detected(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        if self.current_turn:
            self.current_turn["decisions"].append(f"drift: {reason}")
        return MiddlewareResult.cont()

    def on_verification_failure(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        if self.current_turn:
            self.current_turn["decisions"].append(
                f"verification_failure: {reason}"
            )
        return MiddlewareResult.cont()

    def inject_state(self, context: ForgeContext) -> MiddlewareResult:
        summary = self.get_trace_summary()
        if summary and "No trace data" not in summary:
            return MiddlewareResult.inject(
                f"[{self.label}] Trace: {summary}"
            )
        return MiddlewareResult.cont()

    def emit_trace(self, event: str, data: dict) -> None:
        self._logger.debug("%s trace: %s %s", self.label, event, data)
