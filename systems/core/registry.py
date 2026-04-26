"""Forge Registry.

Discovers installed Forges, validates required files, and exposes available workflows.
Prevents broken Forge activation.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional, List, Dict
import logging
import re

from systems.core.contract import (
    ForgeContext, ForgeHandoff, ForgeArtifact, ArtifactType,
)

logger = logging.getLogger(__name__)

# Base directories for Forges
SYSTEMS_DIR = Path(__file__).parent.parent  # systems/
SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"

# Required files per Forge
# Can be at Forge root level OR in subdirectories (prompts/, agents/, tests/)
REQUIRED_FILES = {
    "SKILL.md": ("Skill definition (user-invocable entry point)", True),
    "agent_loop.py": ("Runtime integration (enter/exit hooks)", True),
    "middleware.py": ("Middleware stack (get_middleware_stack())", True),
    "README.md": ("Documentation for the Forge", True),
    "prompt.md": ("System prompt for the Forge agent", False),  # Optional at root (can be in prompts/)
    "agent.toml": ("Agent configuration (TOML)", False),  # Optional at root (can be in agents/)
    "tests/test_forge.py": ("Tests for the Forge", True),
}

# Forge names that are valid (handoff chain)
VALID_FORGE_NAMES = [
    "specforge",
    "researchforge",
    "codeforge",
    "testforge",
    "debugforge",
    "docforge",
    "shipforge",
]


class ForgeInfo:
    """Information about an installed Forge."""

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.valid = False
        self.missing: List[str] = []
        self.artifacts: List[ForgeArtifact] = []
        self.dependencies: List[str] = []  # Forges this depends on

    def __repr__(self):
        status = "VALID" if self.valid else "INVALID"
        return f"ForgeInfo({self.name}, {status}, missing={self.missing})"


class ForgeRegistry:
    """Discovers and validates installed Forges."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir
        self.systems_dir = base_dir if base_dir else SYSTEMS_DIR
        self.skills_dir = SKILLS_DIR
        self._forges: Dict[str, ForgeInfo] = {}
        logger.info("ForgeRegistry initialized, systems_dir=%s, skills_dir=%s",
                    self.systems_dir, self.skills_dir)

    def discover(self) -> Dict[str, ForgeInfo]:
        """Discover all installed Forges.

        Scans systems/ directory for Forge directories.
        A valid Forge has middleware.py and/or agent_loop.py at its root.
        Returns dict of {forge_name: ForgeInfo}.
        """
        self._forges.clear()

        # Scan base_dir (defaults to systems/)
        scan_dir = self.base_dir if self.base_dir else self.systems_dir
        if scan_dir.exists():
            for d in scan_dir.iterdir():
                if not d.is_dir():
                    continue
                # Skip non-Forge directories
                if d.name in ("core", "skill-forge", "continuity-overlord"):
                    continue
                # Check if this looks like a Forge
                if self._is_forge_dir(d):
                    info = self._validate_forge(d.name, d)
                    self._forges[d.name] = info

        logger.info("Discovered %d Forges, %d valid",
                    len(self._forges), sum(1 for f in self._forges.values() if f.valid))
        return self._forges

    def _is_forge_dir(self, path: Path) -> bool:
        """Check if a directory looks like a Forge."""
        # Has middleware.py or agent_loop.py at root level
        if (path / "middleware.py").exists():
            return True
        if (path / "agent_loop.py").exists():
            return True
        # Has a skills/ subdirectory with SKILL.md files (pipeline Forge)
        if (path / "skills").exists():
            skills_dir = path / "skills"
            if any((skills_dir / d / "SKILL.md").exists() for d in skills_dir.iterdir() if d.is_dir()):
                return True
        return False

    def _validate_forge(self, name: str, path: Path) -> ForgeInfo:
        """Validate a single Forge against required files."""
        info = ForgeInfo(name, path)

        # Check required files
        for req_file, (description, required) in REQUIRED_FILES.items():
            fp = path / req_file
            if not fp.exists():
                # For optional files, check subdirectories
                if req_file == "prompt.md":
                    # Check prompts/ directory for any .md file
                    prompts_dir = path / "prompts"
                    if prompts_dir.exists() and any(prompts_dir.glob("*.md")):
                        continue  # Found prompt in subdirectory
                elif req_file == "agent.toml":
                    # Check agents/ directory for any .toml file
                    agents_dir = path / "agents"
                    if agents_dir.exists() and any(agents_dir.glob("*.toml")):
                        continue  # Found agent config in subdirectory
                # File not found
                if required:
                    info.missing.append(req_file)
                    logger.warning("Forge %s missing: %s (%s)",
                                  name, req_file, description)

        # Check that either top-level SKILL.md exists OR skills/ subdirectory exists
        has_skill_md = (path / "SKILL.md").exists()
        skills_dir = path / "skills"
        has_skills_dir = (skills_dir.exists() and
                         any((skills_dir / d / "SKILL.md").exists()
                             for d in skills_dir.iterdir() if d.is_dir()))
        if not has_skill_md and not has_skills_dir:
            info.missing.append("SKILL.md or skills/ (with SKILL.md files)")

        info.valid = len(info.missing) == 0

        # Load known artifacts if SKILL.md exists
        skill_md = path / "SKILL.md"
        if skill_md.exists():
            info.artifacts = self._extract_artifacts(skill_md)

        # Determine dependencies based on handoff chain
        info.dependencies = self._get_dependencies(name)

        return info

    def _extract_artifacts(self, skill_md: Path) -> List[ForgeArtifact]:
        """Extract artifact references from SKILL.md."""
        artifacts: List[ForgeArtifact] = []
        try:
            content = skill_md.read_text()
            # Look for artifact references like OUTPUT.md, INPUT.md, etc.
            patterns = [
                r'([A-Z_][A-Z_]*\.md)',  # PROBLEM_FRAME.md, RESEARCH_PLAN.md, etc.
                r'artifact[s]?[:\s]+([A-Za-z_/]+\.md)',
            ]
            found = set()
            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    name = match.group(1)
                    if name not in found:
                        found.add(name)
                        artifacts.append(ForgeArtifact(
                            name=name,
                            path=name,
                            artifact_type=ArtifactType.OUTPUT,
                        ))
        except Exception as e:
            logger.error("Failed to extract artifacts from %s: %s", skill_md, e)
        return artifacts

    def _get_dependencies(self, forge_name: str) -> List[str]:
        """Get the Forges that this Forge depends on (from handoff chain)."""
        # Define the handoff chain
        chain = VALID_FORGE_NAMES
        try:
            idx = chain.index(forge_name)
            if idx > 0:
                return [chain[idx - 1]]
        except ValueError:
            pass
        return []

    def get(self, forge_name: str) -> Optional[ForgeInfo]:
        """Get a specific Forge by name."""
        if not self._forges:
            self.discover()
        return self._forges.get(forge_name)

    def validate(self, forge_name: str) -> List[str]:
        """Returns list of missing required files for a Forge."""
        info = self.get(forge_name)
        if info is None:
            return ["Forge not found: " + forge_name]
        return info.missing.copy()

    def get_handoff_chain(self, chain: List[str]) -> tuple[bool, List[ForgeHandoff]]:
        """Validate a chain of Forges can hand off to each other.

        Returns (valid, handoffs) where handoffs is the list of ForgeHandoff objects.
        """
        if not self._forges:
            self.discover()

        errors: List[str] = []
        handoffs: List[ForgeHandoff] = []

        for i, source in enumerate(chain):
            if source not in self._forges:
                errors.append(f"Forge not found: {source}")
                continue

            if not self._forges[source].valid:
                errors.append(
                    f"Forge {source} is invalid, missing: {self._forges[source].missing}"
                )

            # Check handoff to next Forge in chain
            if i + 1 < len(chain):
                target = chain[i + 1]
                if target not in self._forges:
                    errors.append(f"Next forge in chain not found: {target}")
                    continue

                source_artifacts = self._forges[source].artifacts
                handoff = ForgeHandoff(
                    source_forge=source,
                    target_forge=target,
                    artifacts=source_artifacts,
                    validation_required=True,
                )
                valid, handoff_errors = handoff.validate()
                if not valid:
                    errors.extend(handoff_errors)
                else:
                    handoffs.append(handoff)

        return len(errors) == 0, handoffs

    def list_valid(self) -> List[str]:
        """List names of valid Forges."""
        if not self._forges:
            self.discover()
        return [name for name, info in self._forges.items() if info.valid]

    def list_all(self) -> List[str]:
        """List all discovered Forge names."""
        if not self._forges:
            self.discover()
        return list(self._forges.keys())

    def validate_all(self) -> Dict[str, List[str]]:
        """Validate all discovered Forges. Returns {forge_name: missing_files}."""
        if not self._forges:
            self.discover()
        return {name: info.missing for name, info in self._forges.items()}


def validate_forge_cli() -> int:
    """CLI entry point to validate all Forges. Returns 0 if all valid."""
    registry = ForgeRegistry()
    registry.discover()
    all_valid = True
    for name, missing in registry.validate_all().items():
        if missing:
            print(f"FAIL: {name} - missing: {missing}")
            all_valid = False
        else:
            print(f"OK: {name}")
    return 0 if all_valid else 1


if __name__ == "__main__":
    import sys
    sys.exit(validate_forge_cli())
