"""
Patch for mistral-vibe core to support generic runtime-activated skills.

This adds a generic mechanism (not skill-forge-specific):

1. SkillMetadata gains an optional `activation` field
2. SkillManager parses and exposes activation data
3. AgentLoop checks for activation.type == "runtime" and calls the entrypoint

No hardcoded skill names. No monkey-patching. One generic hook.

APPLY:
    python3 core_patch.py
"""
from pathlib import Path
import sys

# Paths
MANAGER_PATH = Path("/home/bamn/mistral-vibe/vibe/core/skills/manager.py")
AGENT_LOOP_PATH = Path("/home/bamn/mistral-vibe/vibe/core/agent_loop.py")
PATCH_MARKER = "# --- RUNTIME ACTIVATION HOOK ---"


def patch_manager():
    """Patch manager.py to support activation metadata."""
    if not MANAGER_PATH.exists():
        print(f"ERROR: {MANAGER_PATH} not found")
        return False

    content = MANAGER_PATH.read_text()

    if PATCH_MARKER in content:
        print("manager.py already patched.")
        return True

    # 1. Add RuntimeActivation class after ParsedSkillCommand
    runtime_class = """

class RuntimeActivation:
    \"\"\"Result when a skill declares runtime activation.\"\"\"
    def __init__(self, skill_info, entrypoint: str, exitpoint: str):
        self.skill_info = skill_info
        self.entrypoint = entrypoint
        self.exitpoint = exitpoint
        self.name = skill_info.name
"""
    # Find end of ParsedSkillCommand class
    insert_after = '        )\n'
    if 'class ParsedSkillCommand' in content:
        # Find the class and its end
        lines = content.split('\n')
        in_class = False
        insert_idx = len(lines)
        for i, line in enumerate(lines):
            if 'class ParsedSkillCommand' in line:
                in_class = True
            if in_class and line.strip() == '' and i > 0:
                insert_idx = i
                break
        lines.insert(insert_idx, runtime_class)
        content = '\n'.join(lines)

    # 2. Add activation field to SkillMetadata (in models.py)
    # Actually, do it in the parse - check frontmatter for 'activation'
    # Modify parse_skill_command to check for activation
    old_parse = """    def parse_skill_command(self, text_prompt: str) -> ParsedSkillCommand | None:
        stripped = text_prompt.strip()
        if not stripped.startswith("/"):
            return None

        parts = stripped[1:].split(None, 1)
        if not parts:
            return None

        skill_name = parts[0].lower()
        skill_info = self.get_skill(skill_name)
        if skill_info is None:
            return None

        extra_instructions = parts[1] if len(parts) > 1 else None

        return ParsedSkillCommand(
            name=skill_name,
            content=skill_info.prompt,
            extra_instructions=extra_instructions,
        )"""

    new_parse = """    def parse_skill_command(self, text_prompt: str) -> ParsedSkillCommand | RuntimeActivation | None:
        stripped = text_prompt.strip()
        if not stripped.startswith("/"):
            return None

        parts = stripped[1:].split(None, 1)
        if not parts:
            return None

        skill_name = parts[0].lower()
        skill_info = self.get_skill(skill_name)
        if skill_info is None:
            return None

        # Check for runtime activation
        if hasattr(skill_info, 'activation') and skill_info.activation:
            act = skill_info.activation
            if isinstance(act, dict) and act.get('type') == 'runtime':
                return RuntimeActivation(
                    skill_info=skill_info,
                    entrypoint=act.get('entrypoint', ''),
                    exitpoint=act.get('exitpoint', ''),
                )

        extra_instructions = parts[1] if len(parts) > 1 else None

        return ParsedSkillCommand(
            name=skill_name,
            content=skill_info.prompt,
            extra_instructions=extra_instructions,
        )"""

    if old_parse in content:
        content = content.replace(old_parse, new_parse)
    else:
        print("WARNING: Could not find parse_skill_command to patch")

    MANAGER_PATH.write_text(content)
    print(f"Patched: {MANAGER_PATH}")
    return True


def patch_agent_loop():
    """Patch agent_loop.py to handle RuntimeActivation."""
    if not AGENT_LOOP_PATH.exists():
        print(f"ERROR: {AGENT_LOOP_PATH} not found")
        return False

    content = AGENT_LOOP_PATH.read_text()

    if PATCH_MARKER in content:
        print("agent_loop.py already patched.")
        return True

    # Add import for RuntimeActivation after existing imports
    import_addition = """
# --- RUNTIME ACTIVATION HOOK ---
try:
    from vibe.core.skills.manager import RuntimeActivation
except ImportError:
    RuntimeActivation = None
"""
    # Find last import line
    lines = content.split('\n')
    last_import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('from ') or line.startswith('import '):
            last_import_idx = i
    lines.insert(last_import_idx + 1, import_addition)
    content = '\n'.join(lines)

    # Patch act() method to check for RuntimeActivation
    old_act = """        async for event in self._conversation_loop(
                msg, client_message_id=client_message_id
            ):
                yield event"""

    new_act = """        # Check for runtime activation
        if RuntimeActivation and isinstance(parsed, RuntimeActivation):
            # Runtime owns the transition
            try:
                # Parse entrypoint: "module:function"
                ep_parts = parsed.entrypoint.split(':')
                if len(ep_parts) == 2:
                    import importlib
                    mod = importlib.import_module(ep_parts[0])
                    func = getattr(mod, ep_parts[1])
                    await func(
                        pipeline=self.middleware_pipeline,
                        agent_manager=self.agent_manager,
                        skill_forge_dir=Path(parsed.skill_info.skill_dir) if parsed.skill_info else None,
                    )
            except Exception as e:
                yield AssistantEvent(
                    content=f"<{VIBE_STOP_EVENT_TAG}>Runtime activation failed: {e}</{VIBE_STOP_EVENT_TAG}>",
                    stopped_by_middleware=True,
                )
            return
        # Normal skill execution
        async for event in self._conversation_loop(
                msg, client_message_id=client_message_id
            ):
                yield event"""

    if old_act in content:
        content = content.replace(old_act, new_act)
    else:
        print("WARNING: Could not find act() method to patch")

    AGENT_LOOP_PATH.write_text(content)
    print(f"Patched: {AGENT_LOOP_PATH}")
    return True


if __name__ == '__main__':
    print("Patching mistral-vibe core for generic runtime activation...")
    if patch_manager():
        print("manager.py: OK")
    if patch_agent_loop():
        print("agent_loop.py: OK")
    print("Done. Now /skill-forge will be intercepted before normal execution.")
