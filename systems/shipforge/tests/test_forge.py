"""Tests for ShipForge."""

import pytest
from pathlib import Path
from systems.core.contract import (
    ForgeContext, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus, ForgeResult
)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from systems.shipforge.agent_loop import (
    enter_shipforge, exit_shipforge, run_phase, get_available_phases
)


class TestShipForgeFiles:
    """Test that required files exist."""

    def test_skill_md_exists(self):
        skill_md = Path(__file__).parent.parent / "SKILL.md"
        assert skill_md.exists(), "SKILL.md not found"

    def test_agent_loop_exists(self):
        agent_loop = Path(__file__).parent.parent / "agent_loop.py"
        assert agent_loop.exists(), "agent_loop.py not found"

    def test_middleware_exists(self):
        middleware = Path(__file__).parent.parent / "middleware.py"
        assert middleware.exists(), "middleware.py not found"


class TestShipForgeAgentLoop:
    """Test the agent_loop functions."""

    def test_enter_returns_string(self):
        result = enter_shipforge()
        assert isinstance(result, str), "enter_shipforge should return str"

    def test_exit_returns_string(self):
        result = exit_shipforge()
        assert isinstance(result, str), "exit_shipforge should return str"

    def test_get_available_phases(self):
        phases = get_available_phases()
        assert isinstance(phases, list), "Should return a list"
        assert len(phases) > 0, "Should have at least one phase"

    def test_run_phase_valid(self):
        ctx = ForgeContext(forge_name="shipforge")
        phases = get_available_phases()
        if phases:
            result = run_phase(phases[0], ctx)
            assert isinstance(result, ForgeResult), "Should return ForgeResult"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
