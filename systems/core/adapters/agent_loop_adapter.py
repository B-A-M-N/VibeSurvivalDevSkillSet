"""
MiddlewareAgentLoop — wraps Vibe's AgentLoop for turn-level control.

Instance-level adapter: no patching of vibe/core/agent_loop.py.
Wrap the agent loop to gain state injection and optional message-stream interception.
"""

import types


class MiddlewareAgentLoop:
    """
    Wraps a Vibe AgentLoop so middleware can inject state before each turn
    and (if act() yields events) intercept individual messages in the stream.
    """

    def __init__(self, base_agent_loop, middleware, context):
        self.base = base_agent_loop
        self.middleware = middleware
        self.context = context

        # Replace the inner tool_manager with our wrapped version
        self.base.tool_manager = MiddlewareToolManager(
            self.base.tool_manager,
            middleware,
            context,
        )

    def __getattr__(self, name):
        """Forward anything we don't override to the real AgentLoop."""
        return getattr(self.base, name)

    async def act(self, *args, **kwargs):
        """
        Intercept act(): inject state before the turn, then delegate to
        the base AgentLoop. If act() yields events, wrap them through
        middleware; otherwise return the result directly.
        """
        # --- Pre-turn state injection ---
        state = await self.middleware.run_hook(
            "inject_state",
            context=self.context,
        )

        if state.injection:
            self._inject_system_message(state.injection)

        # --- Check if base.act() returns an async generator or coroutine ---
        result = self.base.act(*args, **kwargs)

        if isinstance(result, types.AsyncGeneratorType):
            # Return a new async generator that intercepts each event
            return self._wrap_stream(result)

        # Coroutine: await and return directly (no per-event interception)
        return await result

    async def _wrap_stream(self, stream):
        """Wrap an async generator to intercept each event through middleware."""
        async for event in stream:
            decision = await self.middleware.run_hook(
                "on_message",
                context=self.context,
                message=event,
            )

            if decision.status == "block":
                continue

            if decision.injection:
                self._inject_system_message(decision.injection)

            yield event

    def _inject_system_message(self, text: str):
        """Inject a system message into the agent loop's message list."""
        if hasattr(self.base, "message_list"):
            self.base.message_list.add_system_message(text)
        elif hasattr(self.base, "messages"):
            self.base.messages.append({
                "role": "system",
                "content": text,
            })
        else:
            self.context.pending_injections.append(text)


# Import here to avoid circular import at module load time
from .tool_manager_adapter import MiddlewareToolManager  # noqa: E402
