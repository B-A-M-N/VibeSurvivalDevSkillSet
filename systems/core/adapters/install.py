"""
Install helper — one-liner factory to wrap an AgentLoop with the control plane.

Usage:
    from systems.core.adapters.install import install_control_plane

    agent_loop = install_control_plane(
        agent_loop=base_agent_loop,
        middleware=my_middleware_pipeline,
        context=my_forge_context,
    )
"""


def install_control_plane(agent_loop, middleware, context):
    """
    Wrap an existing Vibe AgentLoop with the full control-plane adapter stack.

    Returns a MiddlewareAgentLoop that:
      - wraps tool_manager for tool/command/file interception
      - injects state before each turn
      - optionally intercepts message stream events

    The original agent_loop is NOT modified — a wrapped instance is returned.
    """
    from .agent_loop_adapter import MiddlewareAgentLoop

    return MiddlewareAgentLoop(
        base_agent_loop=agent_loop,
        middleware=middleware,
        context=context,
    )


def wrap_tool_manager(agent_loop, middleware, context):
    """
    Lightweight install: only wrap ToolManager, no AgentLoop wrapper.

    This is the minimum viable adapter — gives you tool/command/file
    interception without turn-level or stream interception.
    """
    from .tool_manager_adapter import MiddlewareToolManager

    agent_loop.tool_manager = MiddlewareToolManager(
        agent_loop.tool_manager,
        middleware,
        context,
    )
    return agent_loop
