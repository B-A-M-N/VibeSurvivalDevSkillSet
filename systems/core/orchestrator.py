"""Forge Orchestrator.

Runs Forge phases in order, passes artifacts between Forges,
enforces gates, calls middleware primitives, delegates to subagents,
and records traces.

Uses MiddlewarePipeline for universal hook dispatch.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
import time
import importlib

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus, ForgeFailure, ForgeHandoff,
)
from systems.core.registry import ForgeRegistry
from systems.core.middleware.interface import (
    MiddlewareResult, MiddlewareAction, MiddlewarePipeline,
)


logger = logging.getLogger(__name__)

# Singleton registry
_registry: Optional[ForgeRegistry] = None


def get_registry() -> ForgeRegistry:
    """Get or create the singleton registry."""
    global _registry
    if _registry is None:
        _registry = ForgeRegistry()
        _registry.discover()
    return _registry


class ForgeOrchestrator:
    """Orchestrates Forge execution with middleware and handoffs."""

    def __init__(self, agent_manager: Any = None, base_dir: Optional[Path] = None):
        self.agent_manager = agent_manager
        self.registry = ForgeRegistry(base_dir)
        self.registry.discover()
        self.middleware_stack: List[Any] = []
        self.pipeline: Optional[MiddlewarePipeline] = None
        self.trace_enabled = True
        logger.info(
            "ForgeOrchestrator initialized, %d forges found",
            len(self.registry.list_all()),
        )

    def set_agent_manager(self, agent_manager: Any) -> None:
        """Inject the agent manager."""
        self.agent_manager = agent_manager
        for mw in self.middleware_stack:
            if hasattr(mw, 'set_agent_manager'):
                mw.set_agent_manager(agent_manager)
        logger.info("Agent manager injected into orchestrator and middleware")

    def set_middleware_stack(self, stack: List[Any]) -> None:
        """Set the middleware stack and create the pipeline."""
        self.middleware_stack = stack
        self.pipeline = MiddlewarePipeline(stack)
        for mw in self.middleware_stack:
            if self.agent_manager and hasattr(mw, 'set_agent_manager'):
                mw.set_agent_manager(self.agent_manager)
        logger.info(
            "Middleware pipeline set with %d primitives", len(stack),
        )

    def run_forge(
        self, forge_name: str, context: Optional[ForgeContext] = None,
    ) -> ForgeResult:
        """Run a single Forge workflow.

        Executes the Forge's phases with middleware hooks,
        enforces gates, and produces output artifacts.
        """
        forge_info = self.registry.get(forge_name)
        if forge_info is None:
            return ForgeResult(
                success=False,
                message=f"Forge not found: {forge_name}",
                failure=ForgeFailure(
                    failure_type="not_found",
                    reason=f"Forge {forge_name} is not installed",
                    retryable=False,
                ),
            )

        if not forge_info.valid:
            return ForgeResult(
                success=False,
                message=f"Forge {forge_name} is invalid. Missing: {forge_info.missing}",
                failure=ForgeFailure(
                    failure_type="invalid_forge",
                    reason=f"Missing files: {forge_info.missing}",
                    retryable=False,
                ),
            )

        if context is None:
            context = ForgeContext(forge_name=forge_name)
        else:
            context.forge_name = forge_name

        logger.info("Starting Forge: %s", forge_name)

        # Load middleware stack from Forge's middleware.py
        self._load_middleware(forge_name)

        # Load agent_loop for phase execution
        agent_loop = self._load_agent_loop(forge_name)
        if agent_loop is None:
            return ForgeResult(
                success=False,
                message=f"Could not load agent_loop.py for {forge_name}",
                failure=ForgeFailure(
                    failure_type="import_error",
                    reason=f"agent_loop.py not loadable",
                    retryable=False,
                ),
            )

        # Run enter hook
        enter_fn = getattr(agent_loop, f"enter_{forge_name}", None)
        if enter_fn:
            try:
                enter_result = enter_fn(context)
                logger.info("Enter %s: %s", forge_name, enter_result)
            except Exception as e:
                logger.warning("Could not run enter hook for %s: %s", forge_name, e)

        # Get available phases
        get_phases_fn = getattr(agent_loop, "get_available_phases", None)
        if get_phases_fn:
            phases = get_phases_fn()
        else:
            phases = []

        # Run phases
        result = self._execute_phases(context, phases, agent_loop)

        # Run exit hook
        exit_fn = getattr(agent_loop, f"exit_{forge_name}", None)
        if exit_fn:
            try:
                exit_result = exit_fn(context)
                logger.info("Exit %s: %s", forge_name, exit_result)
            except Exception as e:
                logger.warning("Could not run exit hook for %s: %s", forge_name, e)

        logger.info("Completed Forge: %s (success=%s)", forge_name, result.success)
        return result

    def run_chain(
        self, chain: List[str], initial_context: Optional[ForgeContext] = None,
    ) -> List[ForgeResult]:
        """Run a chain of Forges, passing artifacts between them.

        Chain: SpecForge → ResearchForge → CodeForge → TestForge → DocForge → ShipForge
        """
        results: List[ForgeResult] = []
        ctx = initial_context or ForgeContext()

        for i, forge_name in enumerate(chain):
            logger.info("Chain step %d/%d: %s", i + 1, len(chain), forge_name)

            result = self.run_forge(forge_name, ctx)
            results.append(result)

            if not result.success:
                logger.error("Chain broken at %s: %s", forge_name, result.message)
                break

            # Pass artifacts to next context
            ctx.artifacts.extend(result.artifacts_produced)

            # Handoff validation
            if i + 1 < len(chain):
                target = chain[i + 1]
                handoff = ForgeHandoff(
                    source_forge=forge_name,
                    target_forge=target,
                    artifacts=result.artifacts_produced,
                    validation_required=True,
                )
                valid, errors = handoff.validate()
                if not valid:
                    logger.error("Handoff %s->%s invalid: %s",
                                forge_name, target, errors)
                    results.append(ForgeResult(
                        success=False,
                        message=f"Handoff validation failed: {errors}",
                        failure=ForgeFailure(
                            failure_type="handoff_failed",
                            reason=f"Cannot handoff {forge_name}->{target}: {errors}",
                            retryable=False,
                        ),
                    ))
                    break

        return results

    # --- Middleware hook dispatch (used by mistral-vibe runtime) ---

    async def run_tool_with_hooks(
        self, tool_name: str, args: dict, context: ForgeContext,
        execute_fn: Any,
    ) -> dict:
        """Execute a tool with middleware hooks.

        Call this from the mistral-vibe tool execution path.

        Flow:
        1. context.record_tool_call(tool_name, args)
        2. pipeline.on_tool_call()
        3. If blocked/modified -> return early
        4. Execute tool
        5. context.record_tool_result(tool_name, result)
        6. pipeline.on_tool_result()
        7. Return result
        """
        if self.pipeline is None:
            # No middleware — execute directly
            return await execute_fn(tool_name, args)

        # Record the tool call
        context.record_tool_call(tool_name, args)
        context.increment_phase_steps()

        # --- BEFORE: on_tool_call hook ---
        result = await self.pipeline.run_hook(
            "on_tool_call",
            context,
            tool_name=tool_name,
            args=args,
        )

        if result.status == "block":
            return result.to_tool_denial()

        if result.status == "modify" and result.modified_args:
            args = result.modified_args

        if result.status == "require_user":
            return result.to_tool_denial()

        # --- Execute the tool ---
        tool_result = await execute_fn(tool_name, args)

        # Record the result
        context.record_tool_result(tool_name, tool_result)

        # --- AFTER: on_tool_result hook ---
        result2 = await self.pipeline.run_hook(
            "on_tool_result",
            context,
            tool_name=tool_name,
            args=args,
            result=tool_result,
        )

        if result2.injection:
            # The injection will be added to the message list by the caller
            pass

        return {
            "result": tool_result,
            "injection": result2.injection if result2.injection else None,
        }

    async def inject_state_before_turn(
        self, context: ForgeContext,
    ) -> str:
        """Collect state injections from all middleware.

        Call this before each model turn in the mistral-vibe runtime.
        Returns combined injection string, or empty string.
        """
        if self.pipeline is None:
            return ""

        result = await self.pipeline.run_hook(
            "inject_state", context,
        )

        if result.injection:
            return result.injection
        return ""

    async def on_message(self, message: dict, context: ForgeContext) -> str:
        """Process a message through middleware.

        Call this for each message from the LLM stream.
        Returns injection string if middleware wants to inject, else empty.
        """
        if self.pipeline is None:
            return ""

        result = await self.pipeline.run_hook(
            "on_message", context, message=message,
        )

        if result.injection:
            return result.injection
        return ""

    async def on_command(self, command: str, context: ForgeContext) -> str:
        """Process a shell command through middleware.

        Call this from the Bash tool execution path.
        Returns injection string if middleware wants to inject, else empty.
        """
        if self.pipeline is None:
            return ""

        result = await self.pipeline.run_hook(
            "on_command", context, command=command,
        )

        if result.status == "block":
            return f"[BLOCKED: {result.message}]"
        if result.injection:
            return result.injection
        return ""

    async def on_file_modified(
        self, path: str, operation: str, context: ForgeContext,
    ) -> str:
        """Process a file modification through middleware.

        Call this when a file is written or edited.
        Returns injection string if middleware wants to inject, else empty.
        """
        if self.pipeline is None:
            return ""

        result = await self.pipeline.run_hook(
            "on_file_modified", context, path=path, operation=operation,
        )

        if result.status == "block":
            return f"[BLOCKED: {result.message}]"
        if result.injection:
            return result.injection
        return ""

    async def on_action(
        self, action: str, data: dict, context: ForgeContext,
    ) -> str:
        """Process an agent action through middleware."""
        if self.pipeline is None:
            return ""

        result = await self.pipeline.run_hook(
            "on_action", context, action=action, data=data,
        )

        if result.injection:
            return result.injection
        return ""

    # --- Internal phase execution ---

    def _execute_phases(
        self, context: ForgeContext, phases: List[str],
        agent_loop: Any,
    ) -> ForgeResult:
        """Execute phases with middleware hooks."""
        run_phase_fn = getattr(agent_loop, "run_phase", None)

        if not run_phase_fn or not phases:
            # No phases to run
            return ForgeResult(
                success=True,
                message=f"No phases to execute for {context.forge_name}",
            )

        for phase_name in phases:
            context.phase = phase_name
            logger.info("Executing phase: %s", phase_name)

            # Run before_phase middleware (via pipeline)
            if self.pipeline:
                pre = self.pipeline.run_hook_sync(
                    "before_phase", context,
                )
                if pre.status in ("block", "redirect", "require_user"):
                    return ForgeResult(
                        success=False,
                        message=pre.message or "Blocked by middleware",
                        failure=ForgeFailure(
                            failure_type="middleware_block",
                            reason=pre.message,
                            retryable=True,
                            escalation_agent=pre.agent_to_switch,
                        ),
                    )

            # Execute the phase
            try:
                phase_result = run_phase_fn(phase_name, context)
                if not isinstance(phase_result, ForgeResult):
                    phase_result = ForgeResult(
                        success=True,
                        message=f"Phase {phase_name} completed",
                    )
            except Exception as e:
                logger.error("Phase %s failed: %s", phase_name, e)
                phase_result = ForgeResult(
                    success=False,
                    message=f"Phase {phase_name} failed: {e}",
                )

            # Run after_phase middleware (via pipeline)
            if self.pipeline:
                post = self.pipeline.run_hook_sync(
                    "after_phase", context, phase_result=phase_result,
                )
                if post.status == "block":
                    return ForgeResult(
                        success=False,
                        message=post.message or "Blocked by middleware",
                    )

            # Check if phase failed
            if not phase_result.success:
                return phase_result

            # Record trace
            if self.trace_enabled:
                context.add_trace("phase_complete", {
                    "forge": context.forge_name,
                    "phase": phase_name,
                    "success": phase_result.success,
                })

        return ForgeResult(
            success=True,
            message=f"All phases completed for {context.forge_name}",
            artifacts_produced=context.artifacts,
        )

    def _load_middleware(self, forge_name: str) -> None:
        """Load middleware stack from Forge's middleware.py."""
        try:
            # Import the forge's middleware module
            module_name = f"systems.{forge_name}.middleware"
            mw_module = importlib.import_module(module_name)

            if hasattr(mw_module, "get_middleware_stack"):
                stack = mw_module.get_middleware_stack(
                    agent_manager=self.agent_manager,
                )
                self.set_middleware_stack(stack)
                logger.info(
                    "Loaded middleware stack for %s: %d primitives",
                    forge_name, len(stack),
                )
        except Exception as e:
            logger.warning("Could not load middleware for %s: %s", forge_name, e)

    def _load_agent_loop(self, forge_name: str) -> Any:
        """Load the Forge's agent_loop module."""
        try:
            module_name = f"systems.{forge_name}.agent_loop"
            return importlib.import_module(module_name)
        except Exception as e:
            logger.warning("Could not load agent_loop for %s: %s", forge_name, e)
            return None

    def validate_chain(self, chain: List[str]) -> tuple[bool, List[str]]:
        """Validate that a chain of Forges can be executed."""
        valid, handoffs = self.registry.get_handoff_chain(chain)
        errors: List[str] = []
        for handoff in handoffs:
            h_valid, h_errors = handoff.validate()
            if not h_valid:
                errors.extend(h_errors)
        return len(errors) == 0, errors


def run_forge_chain(
    chain: List[str], initial_context: Optional[ForgeContext] = None,
) -> List[ForgeResult]:
    """Convenience function to run a Forge chain."""
    orchestrator = ForgeOrchestrator()
    return orchestrator.run_chain(chain, initial_context)


if __name__ == "__main__":
    """CLI entry point to run a Forge or chain."""
    import sys
    from systems.core.contract import ForgeContext

    if len(sys.argv) < 2:
        print("Usage: python -m systems.core.orchestrator <forge_name> [forge2] [forge3] ...")
        print("Available Forges:", get_registry().list_valid())
        sys.exit(1)

    chain = sys.argv[1:]
    orchestrator = ForgeOrchestrator()
    ctx = ForgeContext()
    results = orchestrator.run_chain(chain, ctx)

    for i, (forge, result) in enumerate(zip(chain, results)):
        status = "OK" if result.success else "FAILED"
        print(f"{i+1}. {forge}: {status} - {result.message}")
        if not result.success and result.failure:
            print(f"   Failure: {result.failure.reason}")
