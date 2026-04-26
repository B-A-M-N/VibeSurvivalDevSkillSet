"""ResearchForge Middleware.

Uses reusable middleware primitives from systems.core.middleware:
- GatingMiddleware: phase ordering (problem → evidence → hypotheses → research → synthesis)
- VerificationMiddleware: requires evidence artifacts
- DriftMiddleware: detects repeated research without progress
"""

from __future__ import annotations
from systems.core.middleware.gating import GatingMiddleware
from systems.core.middleware.verification import VerificationMiddleware
from systems.core.middleware.drift import DriftMiddleware

# Phase map: skill prefix -> phase number
RESEARCH_PHASE_MAP = {
    '00-problem': 0, '01-context': 0,
    '02-evidence': 1, '03-source': 1,
    '04-hypothesis': 2, '05-hypothesis-dis': 2,
    '06-targeted': 3, '07-official': 3, '08-upstream': 3,
    '09-version': 3, '10-architecture': 3, '11-risk': 3,
    '12-contradiction': 4,
    '13-solution': 5,
    '14-validation': 6,
    '15-final': 7,
    '16-adversarial': 8,
}

RESEARCH_PHASE_NAMES = [
    "Frame Problem", "Evidence Ledger", "Hypotheses", "Targeted Research",
    "Contradiction Hunt", "Solution Options", "Validation Plan",
    "Final Packet", "Adversarial Review"
]


def get_middleware_stack(agent_manager=None):
    """Return the middleware stack for ResearchForge."""
    gating = GatingMiddleware(label="ResearchForge", require_confirmation=False, agent_manager=agent_manager)
    gating.enable_phase_gating(RESEARCH_PHASE_MAP, RESEARCH_PHASE_NAMES)

    verification = VerificationMiddleware(label="ResearchForge", agent_manager=agent_manager)
    drift = DriftMiddleware(label="ResearchForge", max_repeats=3, max_oscillations=2, agent_manager=agent_manager)

    return [gating, verification, drift]
