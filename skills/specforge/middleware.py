"""SpecForge Middleware.

Uses reusable middleware primitives from systems.core.middleware:
- GatingMiddleware: phase ordering (intake → research → spec → scenarios → review → assembly)
- VerificationMiddleware: requires evidence artifacts before claiming done
"""

from __future__ import annotations
from systems.core.middleware.gating import GatingMiddleware
from systems.core.middleware.verification import VerificationMiddleware

# Phase map: skill prefix -> phase number
SPEC_PHASE_MAP = {
    '00-intake': 0,
    '01-existing': 1, '02-implementation': 1,
    '03-gap': 2,
    '04-research': 3, '05-targeted': 3,
    '06-requirement': 4, '07-authority': 4, '08-data': 4,
    '09-execution': 4, '10-state': 4, '11-api': 4, '12-ui': 4,
    '13-security': 4, '14-observability': 4, '15-error': 4,
    '16-invariant': 4, '17-hard-gate': 4, '18-conflict': 4,
    '19-scenario': 5, '20-kill': 5,
    '21-adversarial': 6,
    '22-final': 7,
}

SPEC_PHASE_NAMES = [
    "Intake", "Evidence Review", "Gap Analysis", "Targeted Research",
    "Spec Construction", "Scenario Generation", "Adversarial Review", "Final Assembly"
]


def get_middleware_stack(agent_manager=None):
    """Return the middleware stack for SpecForge."""
    gating = GatingMiddleware(label="SpecForge", require_confirmation=False, agent_manager=agent_manager)
    gating.enable_phase_gating(SPEC_PHASE_MAP, SPEC_PHASE_NAMES)

    verification = VerificationMiddleware(label="SpecForge", agent_manager=agent_manager)

    return [gating, verification]
