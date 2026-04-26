"""Middleware Primitive Interface.

All middleware primitives must implement MiddlewareInterface.
This replaces the ad-hoc dict returns with typed MiddlewareResult.

Extended with event/tool/action hooks so middleware can intercept
the real runtime stream, not just phase boundaries.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum
import inspect

from systems.core.contract import (
    ForgeContext,
    ForgeResult,
    ForgeGate,
    GateStatus,
)


class MiddlewareAction(Enum):
    """What the middleware wants the runtime to do."""
    CONTINUE = "continue"      # Proceed normally
    BLOCK = "block"            # Stop and return message
    INJECT = "inject"           # Inject a message into the conversation
    REDIRECT = "redirect"       # Change the current agent
    REQUIRE_USER = "require_user"  # Ask user for confirmation
    MODIFY = "modify"           # Modify tool args before execution


@dataclass
class MiddlewareResult:
    """Typed return value from middleware methods.

    Replaces raw dicts like {"block": True, "message": "..."}.

    Status values:
    - continue: proceed normally
    - block: stop execution, show message
    - inject: inject a message into the conversation
    - redirect: switch to a different agent
    - require_user: ask user for approval
    - modify: sanitize/modify tool arguments
    """

    status: str = "continue"  # Literal["continue","block","inject","redirect","require_user","modify"]
    message: str = ""           # Used for block/require_user messages
    injection: str = ""          # Used for inject status
    agent_to_switch: Optional[str] = None  # Used with redirect
    modified_args: Optional[dict] = None  # Used with modify
    metadata: dict = field(default_factory=dict)

    # Backward compatibility
    @property
    def action(self) -> MiddlewareAction:
        """Map status string to MiddlewareAction enum."""
        try:
            return MiddlewareAction(self.status)
        except ValueError:
            return MiddlewareAction.CONTINUE

    @property
    def blocked(self) -> bool:
        return self.status == "block"

    @property
    def injection_needed(self) -> bool:
        return self.status == "inject" and bool(self.injection)

    @classmethod
    def cont(cls) -> "MiddlewareResult":
        """Continue normally."""
        return cls(status="continue")

    @classmethod
    def block(cls, msg: str) -> "MiddlewareResult":
        """Block execution with a message."""
        return cls(status="block", message=msg)

    @classmethod
    def inject(cls, msg: str) -> "MiddlewareResult":
        """Inject a message into the conversation."""
        return cls(status="inject", injection=msg)

    @classmethod
    def redirect(cls, agent_name: str, msg: str = "") -> "MiddlewareResult":
        """Switch to a different agent."""
        return cls(
            status="redirect",
            agent_to_switch=agent_name,
            message=msg,
        )

    @classmethod
    def require_user(cls, msg: str) -> "MiddlewareResult":
        """Require user confirmation before proceeding."""
        return cls(status="require_user", message=msg)

    @classmethod
    def modify(cls, args: dict) -> "MiddlewareResult":
        """Modify tool arguments before execution."""
        return cls(status="modify", modified_args=args)

    def to_tool_denial(self) -> dict:
        """Convert to a tool-denial response for the tool execution path."""
        if self.status == "block":
            return {"error": self.message or "Operation blocked by middleware"}
        if self.status == "require_user":
            return {"error": self.message or "User confirmation required"}
        if self.status == "modify" and self.modified_args:
            return {"modified_args": self.modified_args}
        return {"error": "Operation denied by middleware"}


class MiddlewareInterface:
    """Base interface that all middleware primitives must implement.

    Hooks:
    - before_phase: called before a Forge phase starts
    - after_phase: called after a Forge phase completes
    - on_message: called for each message chunk from the LLM stream
    - on_tool_call: called BEFORE a tool executes
    - on_tool_result: called AFTER a tool executes
    - on_action: called for agent actions (subagent spawn, etc.)
    - on_command: called for shell commands (Bash tool)
    - on_file_modified: called for file writes/edits
    - on_gate_failure: called when a gate check fails
    - on_drift_detected: called when drift/loop is detected
    - on_verification_failure: called when verification fails
    - inject_state: called to inject state context before model turns
    - emit_trace: called to record trace events
    """

    # Priority: lower runs first. Override in subclasses.
    priority: int = 100

    def __init__(self, label: str = "MiddlewareInterface"):
        self.label = label
        self.agent_manager = None
        self._logger = __import__("logging").getLogger(__name__)

    def set_agent_manager(self, agent_manager: Any) -> None:
        """Inject the agent manager (called by orchestrator setup)."""
        self.agent_manager = agent_manager
        self._logger.info("%s: agent_manager injected", self.label)

    # --- Phase boundary hooks ---

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """Called before a Forge phase starts.

        Return MiddlewareResult:
        - continue: proceed normally
        - block: stop execution, show message
        - inject: inject a message, then continue
        - redirect: change agent, then continue
        """
        return MiddlewareResult.cont()

    def after_phase(
        self, context: ForgeContext, result: ForgeResult,
    ) -> MiddlewareResult:
        """Called after a Forge phase completes.

        Update phase state, check results, potentially block or switch agents.
        """
        return MiddlewareResult.cont()

    # --- Event/tool/action hooks (the control plane) ---

    def on_message(self, message: dict, context: ForgeContext) -> MiddlewareResult:
        """Called for each message from the LLM stream.

        message dict typically has keys like 'role', 'content', 'tool_calls', etc.
        Use this to intercept assistant messages, tool-call proposals, etc.
        """
        return MiddlewareResult.cont()

    def on_tool_call(
        self, tool_name: str, args: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Called BEFORE a tool executes.

        Can block the tool, modify its args, or require user confirmation.
        - block: tool is not executed, agent gets error message
        - modify: tool executes with modified_args instead of original args
        - require_user: tool execution paused pending user approval
        """
        return MiddlewareResult.cont()

    def on_tool_result(
        self, tool_name: str, args: dict, result: object, context: ForgeContext,
    ) -> MiddlewareResult:
        """Called AFTER a tool executes.

        result is the raw tool return value.
        Can inject warnings, trigger drift detection, etc.
        """
        return MiddlewareResult.cont()

    def on_action(
        self, action: str, data: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Called for agent actions (subagent spawn, handoff, etc.)."""
        return MiddlewareResult.cont()

    def on_command(
        self, command: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Called for shell commands (Bash tool).

        Use this for drift detection on repeated commands,
        verification of test commands, etc.
        """
        return MiddlewareResult.cont()

    def on_file_modified(
        self, path: str, operation: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Called when a file is written or edited.

        operation is the tool name that caused the modification.
        Use this for edit-churn detection, evidence-before-write checks, etc.
        """
        return MiddlewareResult.cont()

    # --- Feedback/state hooks ---

    def on_gate_failure(
        self, gate: ForgeGate, context: ForgeContext,
    ) -> MiddlewareResult:
        """Called when a gate check fails.

        Default: block with gate reason.
        Override in subclasses for custom behavior.
        """
        return MiddlewareResult.block(
            f"[{self.label}] Gate '{gate.name}' is closed. "
            f"Required artifacts missing."
        )

    def on_drift_detected(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        """Called when drift/loop is detected.

        Default: inject warning and suggest strategy change.
        Override in subclasses for custom behavior (e.g., switch to team-verify).
        """
        return MiddlewareResult.inject(
            f"[{self.label}] DRIFT DETECTED: {reason}\n"
            f"Change strategy. Review what failed."
        )

    def on_verification_failure(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        """Called when verification fails (no evidence found).

        Default: block with reason.
        Override in subclasses for custom behavior (e.g., switch to team-verify).
        """
        return MiddlewareResult.block(
            f"[{self.label}] Verification failed: {reason}"
        )

    def inject_state(self, context: ForgeContext) -> MiddlewareResult:
        """Called to inject state context before model turns.

        Default: return state summary from context artifacts.
        """
        summary_parts = []
        for art in context.artifacts:
            if art.exists():
                summary_parts.append(f"[{art.name}]: exists at {art.path}")
        if summary_parts:
            return MiddlewareResult.inject(
                f"[{self.label}] State Summary:\n" + "\n".join(summary_parts)
            )
        return MiddlewareResult.cont()

    def emit_trace(self, event: str, data: dict) -> None:
        """Record a trace event.

        Called by the orchestrator after tool execution or phase transitions.
        Base implementation logs the event; override for custom behavior.
        """
        self._logger.debug("%s trace: %s %s", self.label, event, data)

# ---------------------------------------------------------------------------
# MiddlewarePipeline — universal hook runner
# ---------------------------------------------------------------------------

class MiddlewarePipeline:
    """Universal hook runner for middleware.

    Instead of every caller manually iterating middleware,
    use one pipeline object with a single run_hook() method.

    Features:
    - Middleware sorted by priority (lower runs first).
    - Multi-result resolution: block > redirect > require_user > modify > inject > continue.
    - Injection dedup: same injection text skipped within a single hook run.
    - Injection limit: max 2 distinct injections per hook run.
    """

    def __init__(self, middleware: list):
        # Sort by priority (lower runs first)
        self.middleware = sorted(middleware, key=lambda mw: mw.priority)
        self._logger = __import__("logging").getLogger(__name__)
        self._last_injections: set[str] = set()  # For dedup across runs

    def _resolve_results(self, results: list[MiddlewareResult]) -> MiddlewareResult:
        """Resolve multiple terminal results.

        Priority: block > redirect > require_user > modify > inject > continue.
        """
        if not results:
            return MiddlewareResult.cont()

        # Count statuses
        blocks = [r for r in results if r.status == "block"]
        redirects = [r for r in results if r.status == "redirect"]
        require_users = [r for r in results if r.status == "require_user"]
        modifies = [r for r in results if r.status == "modify"]
        injections = [r for r in results if r.status == "inject"]

        # Highest priority status wins
        if blocks:
            # Return the highest-priority block (first in sorted order)
            return blocks[0]

        if redirects:
            return redirects[0]

        if require_users:
            return require_users[0]

        if modifies:
            return modifies[0]

        # Combine unique injections (max 2)
        if injections:
            seen: set[str] = set()
            unique: list[str] = []
            for r in injections:
                text = r.injection or ""
                if text and text not in seen:
                    seen.add(text)
                    unique.append(text)
                    if len(unique) >= 2:  # Limit injections
                        break
            if unique:
                return MiddlewareResult.inject("\n\n".join(unique))

        return MiddlewareResult.cont()

    async def run_hook(
        self, hook_name: str, context: ForgeContext, *args, **kwargs
    ) -> MiddlewareResult:
        """Run a named hook across all middleware.

        Returns resolved result based on priority rules.
        """
        results: list[MiddlewareResult] = []
        seen_injections: set[str] = set()

        for mw in self.middleware:
            hook = getattr(mw, hook_name, None)
            if not hook:
                continue

            # Support both sync and async hooks
            result = hook(*args, context=context, **kwargs)

            if inspect.isawaitable(result):
                result = await result

            # Terminal statuses: collect for resolution
            if result.status in ("block", "redirect", "require_user", "modify"):
                self._logger.debug(
                    "Pipeline: %s.%s -> %s (from %s, priority=%d)",
                    mw.label, hook_name, result.status, mw.label, mw.priority,
                )
                results.append(result)
                # Continue collecting — we need to resolve conflicts
                continue

            # Collect injections (with dedup)
            if result.status == "inject" and result.injection:
                injection_text = result.injection
                # Skip if recently injected (within last 5 minutes)
                if injection_text in self._last_injections:
                    self._logger.debug(
                        "Pipeline: skipping duplicate injection from %s", mw.label,
                    )
                    continue
                if injection_text not in seen_injections:
                    seen_injections.add(injection_text)
                    results.append(result)

        # Resolve multi-results
        resolved = self._resolve_results(results)

        # Track injections for dedup
        if resolved.status == "inject" and resolved.injection:
            self._last_injections.add(resolved.injection)
            # Keep only recent injections (avoid unbounded growth)
            if len(self._last_injections) > 20:
                self._last_injections.clear()

        return resolved

    def run_hook_sync(
        self, hook_name: str, context: ForgeContext, *args, **kwargs
    ) -> MiddlewareResult:
        """Synchronous version of run_hook for non-async contexts."""
        results: list[MiddlewareResult] = []
        seen_injections: set[str] = set()

        for mw in self.middleware:
            hook = getattr(mw, hook_name, None)
            if not hook:
                continue

            result = hook(*args, context=context, **kwargs)

            if result.status in ("block", "redirect", "require_user", "modify"):
                results.append(result)
                continue

            if result.status == "inject" and result.injection:
                injection_text = result.injection
                if injection_text not in seen_injections:
                    seen_injections.add(injection_text)
                    results.append(result)

        return self._resolve_results(results)
