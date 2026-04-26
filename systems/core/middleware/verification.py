"""Verification Middleware — implements MiddlewareInterface.

Intercepts tool calls and assistant messages in real time.
Forces evidence artifacts before file mutations.
Injects warnings when success is claimed without verification.

Uses tiered verification: read < lint < typecheck < test.
"""

from __future__ import annotations
from typing import Optional
import logging
import re

from systems.core.contract import (
    ForgeContext, ForgeResult, ForgeArtifact, ArtifactType,
)
from systems.core.middleware.interface import (
    MiddlewareInterface, MiddlewareResult,
)


logger = logging.getLogger(__name__)


# Tools that mutate files
MUTATION_TOOLS = {
    "write_file", "edit_file", "apply_patch",
    "search_replace", "Write", "Edit", "SearchReplace",
}

# Success claim patterns
SUCCESS_PATTERNS = [
    r'\bfixed\b', r'\bdone\b', r'\bworks\b', r'\bcompleted\b',
    r'\bresolved\b', r'\ball tests pass\b', r'\bsuccess\b',
]

# Verification tiers (higher = stronger evidence)
VERIFICATION_TIERS = {
    "read": {"level": 1, "label": "file read"},
    "grep": {"level": 1, "label": "code search"},
    "lint": {"level": 2, "label": "static analysis"},
    "typecheck": {"level": 3, "label": "type checking"},
    "test": {"level": 4, "label": "test execution"},
    "pytest": {"level": 4, "label": "test execution"},
    "jest": {"level": 4, "label": "test execution"},
    "go test": {"level": 4, "label": "test execution"},
    "cargo test": {"level": 4, "label": "test execution"},
    "benchmark": {"level": 4, "label": "performance test"},
    "perf": {"level": 4, "label": "performance test"},
}

# Minimum verification level required for each claim type
CLAIM_VERIFICATION_REQUIRED = {
    "fixed": 4,          # Bug fix → need tests
    "done": 2,            # Task done → need lint/typecheck
    "works": 4,           # Claim works → need tests
    "completed": 2,       # Completed → need lint/typecheck
    "resolved": 4,        # Issue resolved → need tests
    "all tests pass": 4, # Explicit test claim → need tests
    "success": 3,        # Success claim → need typecheck+
}


class VerificationMiddleware(MiddlewareInterface):
    """Requires evidence artifacts after tool execution."""

    priority: int = 350  # Runs after drift, before gating

    def __init__(self, label: str = "VerificationMiddleware",
                 verification_agent: str = "team-verify"):
        super().__init__(label=label)
        self.verification_agent = verification_agent
        self._verification_failed = False
        self._failure_reason = ""
        # Track read files for evidence linking
        self._recent_reads: list[str] = []  # Recent files read
        logger.info(
            "%s initialized (verification_agent=%s)", label, verification_agent
        )

    # --- Phase boundary hooks (backward compat) ---

    def before_phase(self, context: ForgeContext) -> MiddlewareResult:
        """Block if previous phase wrote files without producing evidence."""
        if context.verification_events:
            last = context.verification_events[-1]
            if not last.get("verified", True):
                return MiddlewareResult.block(
                    f"[{self.label}] {last.get('reason', 'Verification failed')}"
                )
        return MiddlewareResult.cont()

    def after_phase(
        self, context: ForgeContext, result: ForgeResult,
    ) -> MiddlewareResult:
        """Reset flags after phase completes."""
        self._verification_failed = False
        self._failure_reason = ""
        return MiddlewareResult.cont()

    # --- Real-time hooks (the control plane) ---

    def on_tool_call(
        self, tool_name: str, args: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Intercept tool calls BEFORE execution.

        Block file mutations that lack:
        1. Recent evidence (read the file first)
        2. Proper verification tier for the claim being made
        """
        if not self._is_mutation_tool(tool_name):
            # Track read operations for evidence linking
            if tool_name.lower() in ("read", "read_file", "Read"):
                path = self._get_file_path(args)
                if path and path not in self._recent_reads:
                    self._recent_reads.append(path)
                    if len(self._recent_reads) > 10:
                        self._recent_reads.pop(0)
            return MiddlewareResult.cont()

        path = self._get_file_path(args)
        if not path:
            return MiddlewareResult.cont()

        # Rule: need evidence (read the file) before writing
        if not self._has_evidence_for_write(context, path):
            self._verification_failed = True
            self._failure_reason = f"File mutation without evidence: {path}"
            context.add_verification_event({
                "type": "blocked_mutation",
                "path": path,
                "reason": "no evidence or read before write",
            })
            return MiddlewareResult.block(
                f"[{self.label}] Refusing file modification: "
                f"no recent evidence/read supports changing {path}."
            )

        return MiddlewareResult.cont()

    def on_message(
        self, message: dict, context: ForgeContext,
    ) -> MiddlewareResult:
        """Intercept assistant messages.

        Inject warning if success is claimed without proper verification tier.
        """
        text = message.get("content", "")
        if not text:
            return MiddlewareResult.cont()

        # Check for success claims
        for pattern in SUCCESS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                # Determine required verification level
                claim_type = self._get_claim_type(text)
                required_level = CLAIM_VERIFICATION_REQUIRED.get(claim_type, 2)

                if not self._has_verification_at_level(context, required_level):
                    context.add_verification_event({
                        "type": "success_without_verification",
                        "text_review": text[:100],
                        "claim_type": claim_type,
                        "required_level": required_level,
                    })
                    return MiddlewareResult.inject(
                        f"[{self.label}] You are making a '{claim_type}' claim "
                        f"without proper verification.\n"
                        f"Required: verification level {required_level} "
                        f"({self._level_label(required_level)}).\n"
                        f"Run or cite verification before claiming completion."
                    )

        # Check for "all tests pass" without recent test command
        if re.search(r'\ball tests pass\b', text, re.IGNORECASE):
            if not self._has_recent_test_run(context):
                return MiddlewareResult.inject(
                    f"[{self.label}] You claim 'all tests pass' but "
                    f"no recent test command was detected.\n"
                    f"Run tests first, then claim."
                )

        return MiddlewareResult.cont()

    def on_tool_result(
        self, tool_name: str, args: dict, result: object, context: ForgeContext,
    ) -> MiddlewareResult:
        """Check tool results for verification failures."""
        if tool_name in ("bash", "run_shell", "shell"):
            result_str = str(result).lower()
            if "failed" in result_str or "error" in result_str:
                # Bash command failed — record for drift detection
                context.add_verification_event({
                    "type": "bash_failure",
                    "command": args.get("command", ""),
                    "result_review": str(result)[:200],
                })
        return MiddlewareResult.cont()

    def on_file_modified(
        self, path: str, operation: str, context: ForgeContext,
    ) -> MiddlewareResult:
        """Record file modification for verification tracking."""
        context.add_verification_event({
            "type": "file_modified",
            "path": path,
            "operation": operation,
        })
        return MiddlewareResult.cont()

    # --- Backward compat ---

    def on_verification_failure(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        """Called when verification fails (backward compat)."""
        self._verification_failed = True
        self._failure_reason = reason
        if self.agent_manager:
            try:
                self.agent_manager.set_current_agent(self.verification_agent)
                return MiddlewareResult.redirect(
                    self.verification_agent,
                    f"[{self.label}] Verification failed: {reason}"
                )
            except Exception as e:
                logger.error("%s: failed to invoke agent: %s", self.label, e)
        return MiddlewareResult.block(
            f"[{self.label}] Verification failed: {reason}"
        )

    # --- Helpers ---

    def _get_claim_type(self, text: str) -> str:
        """Determine which claim type was made."""
        text_lower = text.lower()
        for claim_type in CLAIM_VERIFICATION_REQUIRED:
            if claim_type in text_lower:
                return claim_type
        return "success"

    def _level_label(self, level: int) -> str:
        """Get label for a verification level."""
        for info in VERIFICATION_TIERS.values():
            if info["level"] == level:
                return info["label"]
        return f"level {level}"

    def _has_verification_at_level(self, context: ForgeContext, required_level: int) -> bool:
        """Check if verification was done at the required level or higher."""

        # Check trace events for verification commands
        for event in context.trace_events[-15:]:
            if event.get("type") == "command":
                cmd = event.get("command", "").lower()
                for v_name, v_info in VERIFICATION_TIERS.items():
                    if v_name in cmd and v_info["level"] >= required_level:
                        return True

        # Check verification events
        for event in context.verification_events[-10:]:
            if event.get("type") == "bash_failure":
                continue  # Failed commands don't count
            if event.get("verified_level", 0) >= required_level:
                return True

        # Check for evidence artifacts
        for art in context.artifacts:
            if art.artifact_type == ArtifactType.EVIDENCE and art.exists():
                return True

        return False

    def _has_evidence_for_write(self, context: ForgeContext, path: str) -> bool:
        """Check if there's evidence before writing to path.

        Evidence = file was read recently OR evidence artifact exists.
        """

        # Rule 1: file was read recently (evidence linking)
        if path in self._recent_reads:
            return True

        # Rule 2: evidence artifact exists
        for art in context.artifacts:
            if art.artifact_type == ArtifactType.EVIDENCE and art.exists():
                # Check if artifact references this path
                try:
                    from pathlib import Path
                    content = Path(art.path).read_text()[:500]
                    if path in content:
                        return True
                except Exception:
                    pass

        # Rule 3: recent read of any file (general evidence)
        if self._recent_reads:
            return True

        return False

    def _has_recent_test_run(self, context: ForgeContext) -> bool:
        """Check if a test command was run recently."""
        for event in context.trace_events[-10:]:
            if event.get("type") == "command":
                cmd = event.get("command", "").lower()
                if any(re.search(p, cmd) for p in (
                    r'\btest\b', r'\bpytest\b', r'\bjest\b',
                    r'\bgo test\b', r'\bcargo test\b',
                )):
                    return True
        return False

    def _is_mutation_tool(self, tool_name: str) -> bool:
        """Check if a tool mutates files."""
        return tool_name.lower() in (t.lower() for t in MUTATION_TOOLS)

    def _get_file_path(self, args: dict) -> str:
        """Extract file path from tool arguments."""
        return (
            args.get("file_path", "")
            or args.get("path", "")
            or args.get("target_file", "")
            or args.get("dest", "")
        )

    # --- Backward compat (gate/drift/verification failures) ---

    def on_gate_failure(
        self, gate: ForgeGate, context: ForgeContext,
    ) -> MiddlewareResult:
        """Called when a gate check fails (backward compat)."""
        return MiddlewareResult.block(
            f"[{self.label}] Gate '{gate.name}' is closed. "
            f"Required artifacts missing."
        )

    def on_drift_detected(
        self, context: ForgeContext, reason: str,
    ) -> MiddlewareResult:
        """Called when drift/loop is detected (backward compat)."""
        return MiddlewareResult.cont()

    def emit_trace(self, event: str, data: dict) -> None:
        self._logger.debug("%s trace: %s %s", self.label, event, data)
