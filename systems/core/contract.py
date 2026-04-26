"""Forge Runtime Contracts.

Shared types for the Forge runtime system.
Every Forge consumes/produces explicit artifacts and hands off via contracts.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List, Tuple, Any


class ArtifactType(Enum):
    """Type of artifact produced/consumed by a Forge."""
    INPUT = "input"
    OUTPUT = "output"
    EVIDENCE = "evidence"
    SPEC = "spec"
    RESEARCH = "research"
    CODE = "code"
    TEST = "test"
    DOC = "doc"
    DEPLOY = "deploy"
    TRACE = "trace"


class GateStatus(Enum):
    """Status of a gate check."""
    OPEN = "open"
    CLOSED = "closed"
    WARNING = "warning"


@dataclass
class ForgeArtifact:
    """An artifact produced or consumed by a Forge.

    Attributes:
        name: Human-readable name (e.g., "FINAL_SPEC.md")
        path: File path relative to working directory
        artifact_type: Whether this is input, output, evidence, etc.
        required: Whether the Forge requires this to start
        produced_by: Which Forge produces this
        validated: Whether the artifact has passed validation
    """
    name: str
    path: str
    artifact_type: ArtifactType = ArtifactType.OUTPUT
    required: bool = False
    produced_by: Optional[str] = None
    validated: bool = False

    def exists(self) -> bool:
        """Check if the artifact file exists on disk."""
        return Path(self.path).exists()

    def validate(self) -> bool:
        """Validate the artifact (existence + non-empty)."""
        p = Path(self.path)
        if not p.exists():
            return False
        if p.is_file() and p.stat().st_size == 0:
            return False
        self.validated = True
        return True


@dataclass
class ForgeGate:
    """A gate condition that must pass before phase advancement.

    Attributes:
        name: Gate identifier (e.g., "evidence_present")
        status: Current gate status
        check_fn: Optional callable for custom checks
    """
    name: str
    status: GateStatus = GateStatus.OPEN
    required_artifacts: List[str] = field(default_factory=list)  # artifact names
    failure_action: str = "block"  # "block", "escalate", "warn"

    def check(self, context: "ForgeContext") -> GateStatus:
        """Evaluate the gate against the current context."""
        for art_name in self.required_artifacts:
            art = context.get_artifact(art_name)
            if art is None or not art.exists():
                self.status = GateStatus.CLOSED
                return self.status

        self.status = GateStatus.OPEN
        return self.status

    def is_open(self) -> bool:
        return self.status == GateStatus.OPEN

    def is_closed(self) -> bool:
        return self.status == GateStatus.CLOSED


@dataclass
class ForgeResult:
    """Outcome of a Forge phase or entire Forge execution.

    Attributes:
        success: Whether the phase/forge completed successfully
        artifacts_produced: Artifacts produced by this phase/forge
        next_phase: Optional next phase name (for phase-based forges)
        message: Human-readable result message
        failure: Optional failure details if success=False
    """
    success: bool = True
    artifacts_produced: List[ForgeArtifact] = field(default_factory=list)
    next_phase: Optional[str] = None
    message: str = ""
    failure: Optional["ForgeFailure"] = None

    def add_artifact(self, artifact: ForgeArtifact) -> None:
        self.artifacts_produced.append(artifact)

    def get_artifact(self, name: str) -> Optional[ForgeArtifact]:
        for a in self.artifacts_produced:
            if a.name == name:
                return a
        return None


@dataclass
class ForgeHandoff:
    """Contract for handing off between two Forges.

    Attributes:
        source_forge: Name of the producing Forge
        target_forge: Name of the consuming Forge
        artifacts: Artifacts to transfer
        validation_required: Whether target must validate before starting
    """
    source_forge: str
    target_forge: str
    artifacts: List[ForgeArtifact] = field(default_factory=list)
    validation_required: bool = True

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the handoff is possible."""
        errors: List[str] = []
        for art in self.artifacts:
            if not art.exists():
                errors.append(f"Artifact {art.name} does not exist at {art.path}")
            elif not art.validate():
                errors.append(f"Artifact {art.name} failed validation")
        return len(errors) == 0, errors


@dataclass
class ForgeFailure:
    """Describes a Forge failure mode.

    Attributes:
        failure_type: Category of failure
        reason: Human-readable explanation
        retryable: Whether the operation can be retried
        escalation_agent: Agent to invoke for recovery
        escalated: Whether escalation already happened
    """
    failure_type: str = "unknown"
    reason: str = ""
    retryable: bool = True
    escalation_agent: Optional[str] = None
    escalated: bool = False

    def escalate(self, agent_manager: Any = None) -> bool:
        """Invoke the escalation agent."""
        if self.escalated:
            return False
        if self.escalation_agent and agent_manager:
            try:
                agent_manager.set_current_agent(self.escalation_agent)
                self.escalated = True
                return True
            except Exception:
                pass
        return False


@dataclass
class ForgeContext:
    """Carries state between Forge phases and across Forge handoffs.

    Attributes:
        forge_name: Current Forge being executed
        phase: Current phase name/number
        artifacts: All known artifacts (input + produced)
        gates: Gate checks for phase advancement
        agent_manager: Injected at runtime for agent invocation
        metadata: Arbitrary key-value for Forge-specific state
        current_tool_calls: Tool calls in the current turn
        recent_tool_calls: Recent tool calls across turns (full history)
        recent_commands: Recent shell commands for drift detection
        files_modified: Files modified in this session
        current_phase_steps: Step counter within current phase
        verification_events: Recorded verification events
        drift_events: Recorded drift events
        action_events: Recorded action events
        trace_events: Trace events for observability
    """
    forge_name: str = ""
    phase: str = ""
    artifacts: List[ForgeArtifact] = field(default_factory=list)
    gates: List[ForgeGate] = field(default_factory=list)
    agent_manager: Any = None  # Injected at runtime, type: AgentManager
    metadata: dict = field(default_factory=dict)
    trace_events: List[dict] = field(default_factory=list)
    # --- Runtime tracking fields (populated by middleware hooks) ---
    current_tool_calls: List[dict] = field(default_factory=list)
    recent_tool_calls: List[dict] = field(default_factory=list)
    recent_commands: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    current_phase_steps: int = 0
    verification_events: List[dict] = field(default_factory=list)
    drift_events: List[dict] = field(default_factory=list)
    action_events: List[dict] = field(default_factory=list)

    def add_artifact(self, artifact: ForgeArtifact) -> None:
        """Register an artifact in the context."""
        for i, a in enumerate(self.artifacts):
            if a.name == artifact.name:
                self.artifacts[i] = artifact
                return
        self.artifacts.append(artifact)

    def get_artifact(self, name: str) -> Optional[ForgeArtifact]:
        """Find an artifact by name."""
        for a in self.artifacts:
            if a.name == name:
                return a
        return None

    def check_gates(self) -> List[Tuple[ForgeGate, GateStatus]]:
        """Check all gates. Returns list of (gate, status)."""
        results: List[Tuple[ForgeGate, GateStatus]] = []
        for gate in self.gates:
            status = gate.check(self)
            results.append((gate, status))
        return results

    def all_gates_open(self) -> bool:
        """Check if all gates are open."""
        return all(gate.is_open() for gate, _ in self.check_gates())

    def add_trace(self, event: str, data: dict) -> None:
        """Record a trace event."""
        import time
        self.trace_events.append({
            "event": event,
            "data": data,
            "timestamp": time.time(),
            "forge": self.forge_name,
            "phase": self.phase,
        })

    def set_agent_manager(self, agent_manager: Any) -> None:
        """Inject the agent manager (called by orchestrator)."""
        self.agent_manager = agent_manager

    # --- Runtime tracking helpers (populated by middleware hooks) ---

    def record_tool_call(self, tool_name: str, args: dict) -> None:
        """Record a tool call in the current turn and recent history."""
        event = {"tool": tool_name, "args": args}
        self.current_tool_calls.append(event)
        self.recent_tool_calls.append(event)

    def record_tool_result(self, tool_name: str, result: object) -> None:
        """Record a tool result in trace events."""
        self.trace_events.append({
            "type": "tool_result",
            "tool": tool_name,
            "result_preview": str(result)[:1000],
        })

    def record_command(self, command: str) -> None:
        """Record a shell command for drift detection and tracing."""
        self.recent_commands.append(command)
        self.trace_events.append({"type": "command", "command": command})

    def record_file_modified(self, path: str) -> None:
        """Record a file modification for churn detection and tracing."""
        if path not in self.files_modified:
            self.files_modified.append(path)
        self.trace_events.append({"type": "file_modified", "path": path})

    def increment_phase_steps(self) -> int:
        """Increment and return the current phase step counter."""
        self.current_phase_steps += 1
        return self.current_phase_steps

    def add_verification_event(self, event: dict) -> None:
        """Record a verification event."""
        self.verification_events.append(event)

    def add_drift_event(self, event: dict) -> None:
        """Record a drift detection event."""
        self.drift_events.append(event)

    def add_action_event(self, event: dict) -> None:
        """Record an agent action event."""
        self.action_events.append(event)
