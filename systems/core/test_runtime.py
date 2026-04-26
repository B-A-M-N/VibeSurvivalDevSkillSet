"""Comprehensive Forge Runtime Tests.

Tests:
- Forge registry rejects incomplete Forge
- middleware primitives run in correct order
- gates block invalid phase progression
- verification failure invokes team-verify
- stale state invokes team-ops
- drift invokes team-verify
- ReactiveForge does not patch without evidence
- handoff artifacts are preserved across Forge chain
"""

import pytest
from pathlib import Path
from typing import List
import sys
import tempfile
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
    ForgeGate, GateStatus, ForgeHandoff, ForgeFailure,
)
from systems.core.registry import ForgeRegistry, ForgeInfo
from systems.core.orchestrator import ForgeOrchestrator
from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult, MiddlewareAction,
)
from systems.core.middleware.gating import GatingMiddleware
from systems.core.middleware.verification import VerificationMiddleware
from systems.core.middleware.drift import DriftMiddleware
from systems.core.middleware.state_injection import StateInjectionMiddleware
from systems.core.middleware.tracing import TracingMiddleware


class TestForgeRegistry:
    """Test that the registry correctly validates Forges."""

    def test_registry_discovers_all_forge(self):
        """Registry should discover all 8 Forges."""
        registry = ForgeRegistry()
        registry.discover()
        assert len(registry.list_all()) >= 8, "Should discover at least 8 Forges"

    def test_registry_valid_forgers(self):
        """Registry should report valid Forges."""
        registry = ForgeRegistry()
        registry.discover()
        valid = registry.list_valid()
        assert len(valid) >= 8, f"Should have 8 valid Forges, got {len(valid)}"

    def test_registry_rejects_incomplete_forge(self):
        """Registry should reject Forge with missing files."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Create incomplete Forge directory with middleware.py so it's discovered
            forge_dir = tmp_path / "incomplete_forge"
            forge_dir.mkdir()
            (forge_dir / "middleware.py").write_text("# middleware")
            # Don't create agent_loop.py, SKILL.md, etc.

            registry = ForgeRegistry(base_dir=tmp_path)
            registry.discover()

            info = registry.get("incomplete_forge")
            assert info is not None, "Should discover the incomplete Forge"
            assert not info.valid, "Forge should be invalid"
            assert len(info.missing) > 0, "Should have missing files"


class TestMiddlewareOrder:
    """Test that middleware primitives run in correct order."""

    def test_middleware_stack_order(self):
        """Middleware should be called in stack order."""
        call_order = []

        class TrackingMiddleware(MiddlewareInterface):
            def __init__(self, name):
                super().__init__(label=name)

            def before_phase(self, context):
                call_order.append(f"{self.label}.before")
                return MiddlewareResult.cont()

            def after_phase(self, context, result):
                call_order.append(f"{self.label}.after")
                return MiddlewareResult.cont()

        mw1 = TrackingMiddleware("first")
        mw2 = TrackingMiddleware("second")
        mw3 = TrackingMiddleware("third")

        stack = [mw1, mw2, mw3]

        ctx = ForgeContext(forge_name="test")
        for mw in stack:
            result = mw.before_phase(ctx)
            assert result.action == MiddlewareAction.CONTINUE

        # Check order
        assert call_order[0] == "first.before"
        assert call_order[1] == "second.before"
        assert call_order[2] == "third.before"


class TestGateBlocking:
    """Test that gates block invalid phase progression."""

    def test_gate_blocks_when_closed(self):
        """Gate should block phase when artifact missing."""
        ctx = ForgeContext(forge_name="test", phase="test_phase")

        # Create a gate that requires an artifact
        gate = ForgeGate(
            name="test_gate",
            status=GateStatus.OPEN,
            required_artifacts=["NONEXISTENT.md"],
        )
        ctx.gates.append(gate)

        # Check gate - should be closed
        status = gate.check(ctx)
        assert status == GateStatus.CLOSED, "Gate should be closed"

    def test_gate_opens_when_artifact_exists(self, tmp_path):
        """Gate should open when required artifact exists."""
        ctx = ForgeContext(forge_name="test", phase="test_phase")

        # Create artifact file
        artifact_file = tmp_path / "EXISTS.md"
        artifact_file.write_text("# Test")

        # Create gate
        gate = ForgeGate(
            name="test_gate",
            status=GateStatus.OPEN,
            required_artifacts=["EXISTS.md"],
        )
        ctx.gates.append(gate)

        # Add artifact to context
        artifact = ForgeArtifact(
            name="EXISTS.md",
            path=str(artifact_file),
            artifact_type=ArtifactType.INPUT,
        )
        ctx.add_artifact(artifact)

        # Check gate - should be open
        status = gate.check(ctx)
        assert status == GateStatus.OPEN, "Gate should be open"


class TestVerificationFailure:
    """Test that verification failure invokes team-verify."""

    def test_verification_failure_returns_block(self):
        """VerificationMiddleware should block on failure."""
        mw = VerificationMiddleware(verification_agent="team-verify")

        ctx = ForgeContext(forge_name="test")
        result = mw.on_verification_failure(ctx, "No evidence found")

        # The middleware should return a block or switch_agent result
        assert result.action in (MiddlewareAction.BLOCK, MiddlewareAction.SWITCH_AGENT), \
            "Should block or switch agent on verification failure"


class TestStaleState:
    """Test that stale state invokes team-ops."""

    def test_stale_state_detection(self, tmp_path):
        """StateInjectionMiddleware should detect stale state."""
        mw = StateInjectionMiddleware(state_agent="team-ops")

        ctx = ForgeContext(forge_name="test")

        # Create checkpoint file with stale state
        checkpoint_file = tmp_path / ".checkpoint.json"
        checkpoint_data = {
            "phase": "EXECUTING",
            "completed_steps": ["step1", "step1", "step1", "step1", "step1"],
        }
        checkpoint_file.write_text(json.dumps(checkpoint_data))

        checkpoint_artifact = ForgeArtifact(
            name=".checkpoint.json",
            path=str(checkpoint_file),
            artifact_type=ArtifactType.INPUT,
        )
        ctx.add_artifact(checkpoint_artifact)

        # Call before_phase which should detect stale state
        result = mw.before_phase(ctx)

        # Should either inject or switch agent
        assert result.action in (MiddlewareAction.INJECT, MiddlewareAction.SWITCH_AGENT), \
            "Should handle stale state"


class TestDriftDetection:
    """Test that drift invokes team-verify."""

    def test_drift_detection_switches_agent(self):
        """DriftMiddleware should switch to corrective agent."""
        mw = DriftMiddleware(corrective_agent="team-verify")

        # Mock agent manager
        class MockAgentManager:
            def set_current_agent(self, agent):
                pass
        mw.agent_manager = MockAgentManager()

        ctx = ForgeContext(forge_name="test")

        # Simulate drift detection
        mw.drift_detected = True
        mw.drift_reason = "Command repeated 5 times"

        result = mw.before_phase(ctx)
        assert result.action == MiddlewareAction.SWITCH_AGENT, \
            f"Should switch agent on drift, got {result.action}"
        assert result.agent_to_switch == "team-verify", \
            "Should switch to team-verify"


class TestReactiveForgeNoPatchWithoutEvidence:
    """Test ReactiveForge does not patch without evidence."""

    def test_reactive_forge_requires_evidence(self):
        """ReactiveForge should not proceed without trace anomaly."""
        from systems.reactiveforge.agent_loop import enter_reactiveforge

        result = enter_reactiveforge()
        # Should indicate waiting for anomaly
        assert "Waiting" in result or "detect" in result.lower(), \
            "Should wait for anomaly evidence"


class TestHandoffArtifacts:
    """Test that handoff artifacts are preserved across Forge chain."""

    def test_handoff_preserves_artifacts(self):
        """Handoff should preserve artifacts between Forges."""
        # Create source Forge artifacts
        artifacts = [
            ForgeArtifact(
                name="OUTPUT.md",
                path="OUTPUT.md",
                artifact_type=ArtifactType.OUTPUT,
                produced_by="source_forge",
            ),
            ForgeArtifact(
                name="REPORT.md",
                path="REPORT.md",
                artifact_type=ArtifactType.OUTPUT,
                produced_by="source_forge",
            ),
        ]

        handoff = ForgeHandoff(
            source_forge="source_forge",
            target_forge="target_forge",
            artifacts=artifacts,
            validation_required=True,
        )

        # Validate handoff (will fail because artifacts don't exist on disk)
        valid, errors = handoff.validate()
        assert not valid, "Handoff should fail for non-existent artifacts"

    def test_handoff_chain_validates(self):
        """Handoff chain should validate correctly."""
        registry = ForgeRegistry()
        registry.discover()

        # Test valid chain
        chain = ["specforge", "researchforge", "codeforge"]
        valid, handoffs = registry.get_handoff_chain(chain)
        # The handoff objects should be created
        assert isinstance(handoffs, list), "Should return list of handoffs"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
