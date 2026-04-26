"""Drift / Loop Detection Middleware — implements MiddlewareInterface.

Detects repeated actions, no-op changes, oscillations.
Consumes on_command() and on_file_modified() hooks
to intercept shell commands and file edits in real time.

Uses contextual gating: test loops, iterative fixes, and
error signature changes are NOT drift.
"""

from __future__ import annotations
from typing import Optional
import logging
import hashlib
import re
from collections import Counter

from systems.core.contract import ForgeContext, ForgeResult
from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult,
)


logger = logging.getLogger(__name__)


class DriftMiddleware(MiddlewareInterface):
    """Detects agent drift and invokes corrective agents.

    Consumes on_command() and on_file_modified() hooks
    to catch drift as it happens.

    Drift = lack of progress, NOT repetition alone.
    """

    priority: int = 300  # Runs after tracing, before gating

    def __init__(self, label: str = "DriftMiddleware",
                 max_repeats: int = 3,
                 max_oscillations: int = 2,
                 max_tool_calls_no_progress: int = 15,
                 max_test_loop: int = 8,  # Allow more repeats during test loops
                 corrective_agent: str = "team-verify"):
        super().__init__(label=label)
        self.max_repeats = max_repeats
        self.max_oscillations = max_oscillations
        self.max_tool_calls_no_progress = max_tool_calls_no_progress
        self.max_test_loop = max_test_loop
        self.corrective_agent = corrective_agent

        # In-memory tracking (reset on restart — acceptable for session scope)
        self._command_counts: Counter = Counter()
        self._command_error_signatures: dict[str, str] = {}  # cmd -> last error signature
        self._edit_history: dict[str, list[str]] = {}  # path -> list of hashes
        self._file_fix_window: dict[str, float] = {}  # path -> timestamp of first recent edit
        self._drift_detected = False
        self._drift_reason = ""
        logger.info(
            "%s initialized (max_repeats=%d, max_oscillations=%d, "
            "max_test_loop=%d, corrective=%s)",
            label, max_repeats, max_oscillations, max_test_loop, corrective_agent,
        )

    def _is_test_command(self, command: str) -> bool:
        """Check if command is a test/validation command."""
        cmd_lower = command.lower()
        return any(
            re.search(p, cmd_lower)
            for p in (
                r'\btest\b', r'\bpytest\b', r'\bjest\b', r'\bgo test\b',
                r'\bcargo test\b', r'\bbenchmark\b', r'\bperf\b',
                r'\bab ', r'\bwrk ', r'\bsiege ',
                r'\bmake check\b', r'\bnpm test\b', r'\blint\b',
                r'\btypecheck\b', r'\bvalidate\b',
            )
        )

    def _get_error_signature(self, result_str: str) -> Optional[str]:
        """Extract a signature from an error result (for change detection)."""
        # Use first 200 chars of error, normalized
        normalized = re.sub(r'\s+', ' ', result_str[:200]).strip()
        return normalized or None

    def _is_file_being_fixed(self, path: str, context: ForgeContext) -> bool:
        """Check if file is in an active fix/refactor window."""
        now = __import__("time").time()
        if path in self._file_fix_window:
            # 5-minute window for iterative fixes
            if now - self._file_fix_window[path] < 300:
                return True
        # Check if there's a recent test run for this file
        for event in context.trace_events[-10:]:
            if event.get("type") == "command":
                cmd = event.get("command", "").lower()
                if "test" in cmd or "lint" in cmd or "typecheck" in cmd:
                    if now - event.get("timestamp", 0) < 120:  # Within 2 minutes
                        return True
        return False

    # --- Phase boundary hooks (backward compat) ---

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """If drift was detected in a prior hook, invoke corrective agent."""
        if self._drift_detected:
            reason = self._drift_reason
            logger.warning("%s: drift detected - %s", self.label, reason)
            if self.agent_manager:
                try:
                    self.agent_manager.set_current_agent(self.corrective_agent)
                    return MiddlewareResult.redirect(
                        self.corrective_agent,
                        f"[{self.label}] DRIFT DETECTED: {reason}\n"
                        f"Switching to {self.corrective_agent} to fix the loop."
                    )
                except Exception as e:
                    logger.error("%s: failed to invoke agent: %s", self.label, e)
            return MiddlewareResult.inject(
                f"[{self.label}] DRIFT DETECTED: {reason}\n"
                f"Change strategy. Review what failed."
            )
        return MiddlewareResult.cont()

    def after_phase(
        self, context: ForgeContext, result: ForgeResult,
    ) -> MiddlewareResult:
        """Reset drift flag after phase completes."""
        self._drift_detected = False
        self._drift_reason = ""
        return MiddlewareResult.cont()

    # --- Real-time hooks (the control plane) ---

    def on_command(
        self, command: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Intercept shell commands. Detect drift with contextual gating.

        Drift rule: same command 3 times in recent history → drift.
        EXCEPT: test commands get max_test_loop repeats.
        Drift rule: bash failure repeated with same command → drift.
        EXCEPT: error signature changed = progress, not drift.
        """
        context.record_command(command)

        is_test = self._is_test_command(command)

        # Track command (with higher threshold for test loops)
        self._command_counts[command] += 1
        current_count = self._command_counts[command]
        threshold = self.max_test_loop if is_test else self.max_repeats

        if current_count >= threshold:
            return self._trigger_drift(
                context,
                f"Command repeated {current_count} times: {command[:80]} "
                f"(threshold={threshold}, test_loop={is_test})"
            )

        # Rule: too many tool calls without artifact progress
        if len(context.recent_tool_calls) > self.max_tool_calls_no_progress:
            if not self._has_recent_artifact_progress(context):
                return self._trigger_drift(
                    context,
                    f"More than {self.max_tool_calls_no_progress} tool calls "
                    f"without artifact progress"
                )

        return MiddlewareResult.cont()

    def on_tool_result(
        self, tool_name: str, args: dict, result: object, context: ForgeContext,
    ) -> MiddlewareResult:
        """Check for repeated bash failures with error signature tracking."""
        if tool_name in ("bash", "run_shell", "shell"):
            result_str = str(result).lower()
            if "error" in result_str or "failed" in result_str or "exit code" in result_str:
                cmd = args.get("command", "")
                error_sig = self._get_error_signature(str(result))

                # If error signature changed, this is progress, not drift
                last_sig = self._command_error_signatures.get(cmd)
                if last_sig and error_sig and last_sig != error_sig:
                    # Error changed = progress, reset counter
                    self._command_counts[cmd] = 0
                    self._command_error_signatures[cmd] = error_sig
                    return MiddlewareResult.cont()

                # Error signature same = potential drift
                if error_sig:
                    self._command_error_signatures[cmd] = error_sig

                # Check if this failed command was already tried
                recent = context.recent_commands[-5:] if len(context.recent_commands) >= 5 else context.recent_commands
                if cmd in recent:
                    count = recent.count(cmd)
                    if count >= 2:
                        return self._trigger_drift(
                            context,
                            f"Bash command failed twice with same error signature: {cmd[:80]}"
                        )
        return MiddlewareResult.cont()

    def on_file_modified(
        self, path: str, operation: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Intercept file writes/edits. Detect edit churn with contextual gating.

        Drift rule: same file edited 4 times without progress → drift.
        EXCEPT: file is in active fix window (5 min) = allowed.
        EXCEPT: recent test run for file = allowed churn.
        """
        context.record_file_modified(path)

        # Check if file is in active fix/refactor window
        if self._is_file_being_fixed(path, context):
            # Update fix window timestamp
            self._file_fix_window[path] = __import__("time").time()
            return MiddlewareResult.cont()

        # Track edit history with content hashing
        content_hash = self._hash_file(path)
        if not content_hash:
            return MiddlewareResult.cont()

        if path not in self._edit_history:
            self._edit_history[path] = []

        history = self._edit_history[path]
        if content_hash in history:
            # Same content written again — oscillation (not progress)
            return self._trigger_drift(
                context,
                f"Repeating same edit to {path}"
            )

        history.append(content_hash)
        if len(history) > self.max_oscillations:
            history.pop(0)

        # Rule: oscillation pattern (A-B-A)
        if len(history) >= 3:
            if history[-1] == history[-3] and history[-1] != history[-2]:
                return self._trigger_drift(
                    context,
                    f"Oscillating edits on {path}: edit pattern detected"
                )

        # Rule: same file edited N times without progress
        if len(history) >= 4:
            if not self._has_recent_artifact_progress(context):
                return self._trigger_drift(
                    context,
                    f"File {path} edited {len(history)} times "
                    f"without artifact progress"
                )

        return MiddlewareResult.cont()

    # --- Drift trigger ---

    def _trigger_drift(self, context: ForgeContext, reason: str) -> MiddlewareResult:
        """Set drift state and return appropriate result."""
        self._drift_detected = True
        self._drift_reason = reason
        logger.warning("%s: drift detected: %s", self.label, reason)

        context.add_drift_event({
            "reason": reason,
            "timestamp": __import__("time").time(),
        })

        # Return inject for real-time hook (orchestrator handles it)
        return MiddlewareResult.inject(
            f"[{self.label}] DRIFT DETECTED: {reason}\n"
            f"Stop normal execution.\n"
            f"Summarize:\n"
            f"1. What you attempted\n"
            f"2. What failed\n"
            f"3. What evidence you have\n"
            f"4. New corrected plan\n"
            f"Do not repeat the previous command unchanged."
        )

    def on_drift_detected(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        """Called when drift/loop is detected (backward compat)."""
        return self._trigger_drift(context, reason)

    # --- Helpers ---

    def _hash_file(self, path: str) -> Optional[str]:
        """Get MD5 hash of a file's content."""
        try:
            from pathlib import Path
            content = Path(path).read_bytes()
            return hashlib.md5(content).hexdigest()[:8]
        except Exception:
            return None

    def _has_recent_artifact_progress(self, context: ForgeContext) -> bool:
        """Check if any artifact was produced recently."""
        for art in context.artifacts:
            if art.exists() and getattr(art, 'produced_by', None):
                return True
        # Also check trace events for recent successful tool results
        for event in context.trace_events[-10:]:
            if event.get("type") == "tool_result" and event.get("ok", True):
                return True
        return False

    # --- Backward compat stubs ---

    def on_gate_failure(
        self, gate: ForgeGate, context: ForgeContext,
    ) -> MiddlewareResult:
        return MiddlewareResult.cont()

    def emit_trace(self, event: str, data: dict) -> None:
        self._logger.debug("%s trace: %s %s", self.label, event, data)
