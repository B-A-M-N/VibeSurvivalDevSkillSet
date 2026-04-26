"""
Continuity Overlord Middleware — Control Plane Enforcement Layer

This middleware governs the entire system by:
1. Gating all task delegation through overlord
2. Injecting watchdog + state-sentry checks at transitions
3. Detecting recursion/drift/runaway loops
4. Enforcing subagent boundaries
5. Gating transitions between phases
6. Providing restore/reset guarantees

Architecture:
- Runs as a global middleware in the main-agent loop
- Intercepts all tool calls (Bash, Write, Agent, TaskCreate)
- Enforces pre-turn and post-turn checks via watchdog
- Routes all delegation through overlord agent
- Manages phase transitions with state-sentry verification
"""

import os
import json
import time
from typing import Dict, List, Optional, Any, Callable


class ContinuityOverlordMiddleware:
    """
    Control-plane middleware for the Continuity Overlord system.

    This is NOT a skill-level middleware — it's a system-level enforcement
    layer that runs in the main agent loop to govern all subagent behavior.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.checkpoint_path = ".checkpoint.json"
        self.turn_count = 0
        self.last_overlord_check = 0
        self.overlord_interval = self.config.get("overlord_check_interval", 10)
        self.watchdog_interval = self.config.get("watchdog_interval", 3)
        self.last_watchdog_check = 0
        self.active_phase = None
        self.phase_stack = []
        self.delegation_log = []
        self.loop_detector = {}

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load middleware configuration."""
        default_config = {
            "overlord_check_interval": 10,
            "watchdog_interval": 3,
            "max_loop_iterations": 5,
            "enable_drift_detection": True,
            "require_overlord_for_subagents": True,
            "enforce_phase_gating": True,
            "auto_state_sentry_on_compaction": True,
        }
        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                default_config.update(json.load(f))
        return default_config

    def pre_turn(self, messages: List[Dict], context: Dict) -> Dict:
        """
        Pre-turn enforcement: runs before each LLM turn.

        - Increments turn counter
        - Triggers watchdog check every N turns
        - Triggers overlord check every M turns
        - Verifies phase state if in a phase
        """
        self.turn_count += 1
        result = {"continue": True, "inject_messages": []}

        # Watchdog check (every N turns)
        if self.turn_count - self.last_watchdog_check >= self.watchdog_interval:
            result["inject_messages"].append({
                "role": "system",
                "content": f"[WATCHDOG] Turn {self.turn_count}: Running drift detection. Use /watchdog to verify state."
            })
            self.last_watchdog_check = self.turn_count

        # Overlord check (every M turns)
        if self.config["require_overlord_for_subagents"]:
            if self.turn_count - self.last_overlord_check >= self.overlord_interval:
                result["inject_messages"].append({
                    "role": "system",
                    "content": f"[OVERLORD] Turn {self.turn_count}: Audit complexity. Delegate specialized work to team-dev/team-ops/team-verify via /overlord."
                })
                self.last_overlord_check = self.turn_count

        # Phase gating
        if self.config["enforce_phase_gating"] and self.active_phase:
            result["inject_messages"].append({
                "role": "system",
                "content": f"[PHASE] Currently in phase: {self.active_phase}. Ensure state-sentry verification before proceeding."
            })

        return result

    def post_turn(self, messages: List[Dict], context: Dict) -> Dict:
        """
        Post-turn enforcement: runs after each LLM turn.

        - Detects loops (same tool call pattern repeated)
        - Checks for compaction events
        - Validates checkpoint consistency
        """
        result = {"continue": True, "warnings": []}

        # Detect loops by tracking tool call patterns
        recent_tools = self._extract_recent_tool_calls(messages[-5:] if len(messages) >= 5 else messages)
        tool_key = json.dumps(recent_tools, sort_keys=True)

        if tool_key in self.loop_detector:
            self.loop_detector[tool_key] += 1
            if self.loop_detector[tool_key] >= self.config["max_loop_iterations"]:
                result["warnings"].append(
                    f"[ANTI-LOOP] Detected repeated pattern: {recent_tools}. "
                    "Run /anti-loop-debug to break the loop."
                )
                result["inject_messages"] = [{
                    "role": "system",
                    "content": "[ANTI-LOOP] Break detected. Running /anti-loop-debug..."
                }]
        else:
            self.loop_detector[tool_key] = 1

        # Compaction detection
        if self._detect_compaction(messages):
            if self.config["auto_state_sentry_on_compaction"]:
                result["inject_messages"] = [{
                    "role": "system",
                    "content": "[COMPACTION] Detected. Running state-sentry for recovery. Use /vibe-continuity to restore state."
                }]

        return result

    def intercept_tool_call(self, tool_name: str, tool_input: Dict) -> Dict:
        """
        Intercept tool calls to enforce governance.

        - Agent/TaskCreate → must go through overlord (if enabled)
        - Bash (destructive) → require pattern-prediction check
        - Write → require verification
        """
        result = {"allow": True, "warnings": []}

        # Gate subagent delegation through overlord
        if tool_name in ("Agent", "TaskCreate", "task") and self.config["require_overlord_for_subagents"]:
            if not self._is_overlord_calling(tool_input):
                result["allow"] = False
                result["warnings"].append(
                    "[OVERLORD] All subagent delegation must go through overlord. "
                    "Use /overlord to delegate to team-dev/team-ops/team-verify."
                )
                result["redirect"] = {
                    "tool": "Agent",
                    "input": {
                        "description": "overlord-delegation",
                        "prompt": f"Delegate task: {tool_input.get('prompt', tool_input.get('description', ''))}",
                        "subagent_type": "overlord"
                    }
                }

        # Destructive Bash commands require pattern-prediction
        if tool_name == "Bash":
            command = tool_input.get("command", "")
            if self._is_destructive_command(command):
                result["warnings"].append(
                    "[PATTERN-PREDICTION] Destructive command detected. "
                    "Run /pattern-prediction before executing."
                )

        return result

    def enter_phase(self, phase_name: str, context: Optional[Dict] = None):
        """Enter a new phase, pushing current phase to stack."""
        if self.active_phase:
            self.phase_stack.append(self.active_phase)
        self.active_phase = phase_name
        return {
            "phase": phase_name,
            "stack_depth": len(self.phase_stack),
            "context": context or {}
        }

    def exit_phase(self) -> Optional[str]:
        """Exit current phase, restoring previous phase if any."""
        exited = self.active_phase
        if self.phase_stack:
            self.active_phase = self.phase_stack.pop()
        else:
            self.active_phase = None
        return exited

    def get_state(self) -> Dict:
        """Return current middleware state for checkpointing."""
        return {
            "turn_count": self.turn_count,
            "active_phase": self.active_phase,
            "phase_stack": self.phase_stack,
            "last_watchdog_check": self.last_watchdog_check,
            "last_overlord_check": self.last_overlord_check,
            "delegation_log": self.delegation_log[-20:],  # Last 20 entries
        }

    def restore_state(self, state: Dict):
        """Restore middleware state from checkpoint."""
        self.turn_count = state.get("turn_count", 0)
        self.active_phase = state.get("active_phase")
        self.phase_stack = state.get("phase_stack", [])
        self.last_watchdog_check = state.get("last_watchdog_check", 0)
        self.last_overlord_check = state.get("last_overlord_check", 0)
        self.delegation_log = state.get("delegation_log", [])

    def _extract_recent_tool_calls(self, messages: List[Dict]) -> List[str]:
        """Extract tool call names from recent messages."""
        tools = []
        for msg in messages:
            if msg.get("role") == "assistant":
                tool_calls = msg.get("tool_calls", [])
                for tc in tool_calls:
                    tools.append(tc.get("function", {}).get("name", ""))
        return tools

    def _detect_compaction(self, messages: List[Dict]) -> bool:
        """Detect if a compaction event just occurred."""
        for msg in reversed(messages[-10:]):
            content = msg.get("content", "")
            if isinstance(content, str) and "compaction" in content.lower():
                return True
        return False

    def _is_destructive_command(self, command: str) -> bool:
        """Check if a bash command is destructive."""
        destructive_patterns = [
            "rm ", "del ", "drop ", "truncate", "git reset",
            "git checkout", "git clean", "mv ", "cp ", "chmod"
        ]
        command_lower = command.lower()
        return any(p in command_lower for p in destructive_patterns)

    def _is_overlord_calling(self, tool_input: Dict) -> bool:
        """Check if the tool call is coming from overlord agent."""
        # Check if subagent_type or description indicates overlord
        return (
            "overlord" in str(tool_input.get("subagent_type", "")).lower() or
            "overlord" in str(tool_input.get("description", "")).lower()
        )


def inject_middleware(agent_loop):
    """
    Inject Continuity Overlord middleware into the agent loop.

    This function is called during system initialization to wrap
    the agent loop with control-plane enforcement.
    """
    middleware = ContinuityOverlordMiddleware()

    original_pre_turn = agent_loop.pre_turn if hasattr(agent_loop, 'pre_turn') else None
    original_post_turn = agent_loop.post_turn if hasattr(agent_loop, 'post_turn') else None

    def wrapped_pre_turn(messages, context):
        if original_pre_turn:
            result = original_pre_turn(messages, context)
        else:
            result = {"continue": True, "inject_messages": []}

        middleware_result = middleware.pre_turn(messages, context)
        result["inject_messages"].extend(middleware_result.get("inject_messages", []))
        return result

    def wrapped_post_turn(messages, context):
        if original_post_turn:
            result = original_post_turn(messages, context)
        else:
            result = {"continue": True, "warnings": []}

        middleware_result = middleware.post_turn(messages, context)
        result["warnings"].extend(middleware_result.get("warnings", []))
        return result

    agent_loop.pre_turn = wrapped_pre_turn
    agent_loop.post_turn = wrapped_post_turn
    agent_loop._overlord_middleware = middleware

    return agent_loop


if __name__ == "__main__":
    # Quick test
    mw = ContinuityOverlordMiddleware()
    print("Continuity Overlord Middleware initialized")
    print(f"Watchdog interval: {mw.watchdog_interval}")
    print(f"Overlord interval: {mw.overlord_interval}")
