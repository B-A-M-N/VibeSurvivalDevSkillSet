"""
Runtime adapters — wrapper layer for control-plane integration.

These adapters wrap Vibe runtime objects (ToolManager, AgentLoop) at the
instance level so middleware can intercept calls without patching Vibe core.
"""

from .tool_manager_adapter import MiddlewareToolManager
from .agent_loop_adapter import MiddlewareAgentLoop
from .install import install_control_plane, wrap_tool_manager

__all__ = [
    "MiddlewareToolManager",
    "MiddlewareAgentLoop",
    "install_control_plane",
    "wrap_tool_manager",
]
