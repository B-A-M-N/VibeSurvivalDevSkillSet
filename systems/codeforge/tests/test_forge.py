"""Tests for FORGE_NAME."""
import pytest
from pathlib import Path
from systems.core.contract import (
    ForgeContext, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus, ForgeResult
)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Import the Forge's agent_loop
from systems.FORGE_IMPORT.agent_loop import (
    enter_FUNC, exit_FUNC, run_phase, get_available_phases
)

FORGE = "FORGE_NAME"
SKILL_FILE = "SKILL.md"
AGENT_LOOP = "agent_loop.py"
MIDDLEWARE = "middleware.py"

class TestFORGE_NAMEFiles:
    """Test that required files exist."""

    def test_skill_md_exists(self):
        skill_md = Path(__file__).parent.parent / SKILL_FILE
        assert skill_md.exists(), f"{SKILL_FILE} not found"

    def test_agent_loop_exists(self):
        agent_loop = Path(__file__).parent.parent / AGENT_LOOP
        assert agent_loop.exists(), f"{AGENT_LOOP} not found"

    def test_middleware_exists(self):
        middleware = Path(__file__).parent.parent / MIDDLEWARE
        assert middleware.exists(), f"{MIDDLEWARE} not found"

    def test_readme_exists(self):
        readme = Path(__file__).parent.parent / "README.md"
        assert readme.exists(), "README.md not found"


class TestFORGE_NAMEAgentLoop:
    """Test the agent_loop functions."""

    def test_enter_returns_string(self):
        result = enter_FUNC()
        assert isinstance(result, str), "enter should return str"

    def test_exit_returns_string(self):
        result = exit_FUNC()
        assert isinstance(result, str), "exit should return str"

    def test_get_available_phases(self):
        phases = get_available_phases()
        assert isinstance(phases, list), "Should return a list"
        assert len(phases) > 0, "Should have at least one phase"

    def test_run_phase_valid(self):
        ctx = ForgeContext(forge_name=FORGE)
        phases = get_available_phases()
        if phases:
            result = run_phase(phases[0], ctx)
            assert isinstance(result, ForgeResult), "Should return ForgeResult"

    def test_run_phase_invalid(self):
        ctx = ForgeContext(forge_name=FORGE)
        result = run_phase("invalid-phase", ctx)
        assert isinstance(result, ForgeResult), "Should return ForgeResult"
        assert not result.success, "Invalid phase should fail"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
