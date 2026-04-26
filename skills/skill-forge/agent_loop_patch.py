"""
Patch for /path/to/vibe/vibe/core/agent_loop.py

Adds skill-forge runtime mode switching:
- Detects /skill-forge invocation
- Saves current agent loop + middleware
- Loads SkillForgeMiddleware + switches to skill-forge agent
- Restores previous state on exit

APPLY:
    python3 /path/to/agent_loop_patch.py
"""
from pathlib import Path
import sys

AGENT_LOOP_PATH = Path("/path/to/vibe/vibe/core/agent_loop.py")
PATCH_MARKER = "# --- SKILL-FORGE PATCH START ---"


def apply_patch():
    if not AGENT_LOOP_PATH.exists():
        print(f"ERROR: {AGENT_LOOP_PATH} not found")
        return False

    content = AGENT_LOOP_PATH.read_text()

    if PATCH_MARKER in content:
        print("Patch already applied.")
        return True

    # 1. Add imports after existing imports
    import_insert = """
import sys
from pathlib import Path
try:
    from vibe.core.skills.manager import SkillManager
except ImportError:
    SkillManager = None
"""
    # Find last import line
    lines = content.split('\n')
    last_import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('from ') or line.startswith('import '):
            last_import_idx = i
    lines.insert(last_import_idx + 1, import_insert.rstrip())
    content = '\n'.join(lines)

    # 2. Add state variables to __init__ (after _teleport_service)
    state_vars = """
        # Skill-forge state
        self._skill_forge_state: dict = {}
        self._skill_forge_middleware = None
"""
    content = content.replace(
        'self._teleport_service: TeleportService | None = None',
        'self._teleport_service: TeleportService | None = None' + state_vars
    )

    # 3. Add methods before _setup_middleware
    new_methods = """
    # --- SKILL-FORGE PATCH START ---

    def _enter_skill_forge(self) -> None:
        \"\"\"Enter skill-forge mode: save state, load custom middleware.\"\"\"
        import sys
        from pathlib import Path

        try:
            skill_info = self.skill_manager.get_skill('skill-forge')
            if not skill_info or not skill_info.skill_dir:
                print("[SkillForge] Could not find skill-forge skill.")
                return
        except Exception as e:
            print(f"[SkillForge] Error: {e}")
            return

        skill_forge_dir = Path(skill_info.skill_dir)

        # Save state
        current_agent = getattr(self.agent_manager, 'current_agent', None)
        current_agent_name = getattr(current_agent, 'name', 'unknown') if current_agent else 'unknown'

        self._skill_forge_state = {
            'middlewares': list(self.middleware_pipeline._middlewares),
            'agent_name': self.agent_manager.active_profile.name,
            'middleware_label': f"pre-forge-mw-{current_agent_name}",
            'agent_loop_label': f"pre-forge-loop-{current_agent_name}",
        }

        # Clear middleware
        self.middleware_pipeline._middlewares.clear()

        # Add skill-forge to sys.path
        if str(skill_forge_dir) not in sys.path:
            sys.path.insert(0, str(skill_forge_dir))

        # Load SkillForgeMiddleware
        try:
            from middleware import SkillForgeMiddleware
            self._skill_forge_middleware = SkillForgeMiddleware()
            self._skill_forge_middleware.stash_state(
                pipeline=self.middleware_pipeline,
                agent_manager=self.agent_manager,
                middleware_label=self._skill_forge_state['middleware_label'],
                agent_loop_label=self._skill_forge_state['agent_loop_label'],
            )
            self.middleware_pipeline.add(self._skill_forge_middleware)
            print("[SkillForge] Loaded SkillForgeMiddleware.")
        except Exception as e:
            print(f"[SkillForge] Failed to load middleware: {e}")
            self._skill_forge_middleware = None

        # Switch to skill-forge agent
        try:
            self.agent_manager.switch_profile('skill-forge')
            system_prompt = get_universal_system_prompt(
                self.tool_manager, self.config, self.skill_manager, self.agent_manager
            )
            self.messages.update_system_prompt(system_prompt)
            print("[SkillForge] Switched to skill-forge agent loop.")
        except Exception as e:
            print(f"[SkillForge] Failed to switch agent: {e}")

        print(
            f"[SkillForge] Saved middleware (label: {self._skill_forge_state['middleware_label']}) "
            f"and agent loop (label: {self._skill_forge_state['agent_loop_label']}). "
            f"Entered Skill Forge mode."
        )

    def _exit_skill_forge(self, apply_user_work: bool = True) -> None:
        \"\"\"Exit skill-forge mode: restore previous state.\"\"\"
        import sys
        from pathlib import Path

        if not self._skill_forge_state:
            print("[SkillForge] Not in skill-forge mode.")
            return

        if apply_user_work:
            print("[SkillForge] Applying work, then restoring previous state.")
        else:
            print("[SkillForge] Discarding work, restoring previous state.")

        # Remove SkillForgeMiddleware
        if self._skill_forge_middleware:
            self.middleware_pipeline._middlewares = [
                m for m in self.middleware_pipeline._middlewares
                if m is not self._skill_forge_middleware
            ]

        # Restore middleware
        saved_middlewares = self._skill_forge_state.get('middlewares', [])
        self.middleware_pipeline._middlewares.extend(saved_middlewares)
        print(f"[SkillForge] Restored {len(saved_middlewares)} middlewares.")

        # Restore agent loop
        saved_agent_name = self._skill_forge_state.get('agent_name')
        if saved_agent_name:
            try:
                self.agent_manager.switch_profile(saved_agent_name)
                system_prompt = get_universal_system_prompt(
                    self.tool_manager, self.config, self.skill_manager, self.agent_manager
                )
                self.messages.update_system_prompt(system_prompt)
                print(f"[SkillForge] Restored agent loop: {saved_agent_name}")
            except Exception as e:
                print(f"[SkillForge] Failed to restore agent: {e}")

        # Clean sys.path
        try:
            skill_info = self.skill_manager.get_skill('skill-forge')
            if skill_info and skill_info.skill_dir:
                skill_dir_str = str(Path(skill_info.skill_dir))
                if skill_dir_str in sys.path:
                    sys.path.remove(skill_dir_str)
        except Exception:
            pass

        # Cleanup
        self._skill_forge_state = {}
        self._skill_forge_middleware = None
        print("[SkillForge] Exited Skill Forge mode. Previous state restored.")

    def _check_skill_forge(self, user_msg: str) -> bool:
        \"\"\"Check if user message invokes /skill-forge. Returns True if invoked.\"\"\"
        stripped = user_msg.strip()
        if stripped.startswith('/skill-forge') or stripped == '/skill-forge':
            self._enter_skill_forge()
            return True
        return False

    # --- SKILL-FORGE PATCH END ---
"""

    content = content.replace(
        '    def _setup_middleware(self) -> None:',
        new_methods + '\n    def _setup_middleware(self) -> None:'
    )

    # 4. Patch _conversation_loop to check for /skill-forge
    check_code = """
        # Check for skill-forge invocation
        if self._check_skill_forge(user_msg):
            pass  # Skill-forge mode is now active
        else:
    """
    content = content.replace(
        '        user_message = LLMMessage(',
        check_code + '        user_message = LLMMessage('
    )

    # Write patched file
    backup = AGENT_LOOP_PATH.with_suffix('.py.bak')
    AGENT_LOOP_PATH.rename(backup)
    AGENT_LOOP_PATH.write_text(content)

    print(f"Patched: {AGENT_LOOP_PATH}")
    print(f"Backup: {backup}")
    return True


if __name__ == '__main__':
    apply_patch()
