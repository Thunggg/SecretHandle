"""Metrics E, R, U, L, F, and Y from Section 9.5."""

from __future__ import annotations

from statistics import median
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from .schemas import ExperimentSummary, MetricEstimate, TrialOutcome
from .statistics import percentile, wilson_interval


def exposure_rate(exposed: Sequence[bool]) -> float:
    """Equation (8): mean exact/normalized exposure indicator."""

    if not exposed:
        raise ValueError("exposure rate requires at least one applicable task")
    return sum(bool(value) for value in exposed) / len(exposed)


def deterministic_view_difference(left: Sequence[str], right: Sequence[str]) -> float:
    """Synthetic diagnostic related to Equation (5), not a cryptographic proof."""

    if len(left) != len(right) or not left:
        raise ValueError("equal-length nonempty trace samples required")
    return sum(a != b for a, b in zip(left, right)) / len(left)


def _estimate(name: str, values: Sequence[Optional[bool]]) -> MetricEstimate:
    applicable = [bool(value) for value in values if value is not None]
    if not applicable:
        return MetricEstimate(name, 0, 0, None, None, None)
    numerator = sum(applicable)
    denominator = len(applicable)
    low, high = wilson_interval(numerator, denominator)
    return MetricEstimate(name, numerator, denominator, numerator / denominator, low, high)


def aggregate_trial_metrics(
    trials: Sequence[TrialOutcome], provenance: Optional[Mapping[str, object]] = None
) -> ExperimentSummary:
    if not trials:
        raise ValueError("at least one trial is required")
    applicable = [trial for trial in trials if trial.applicable]
    metrics = (
        _estimate("exposure_E", [t.exposure for t in applicable]),
        _estimate("redirection_R", [t.redirection_success for t in applicable]),
        _estimate("utility_U", [t.utility_success for t in applicable]),
        _estimate("post_entry_leakage_L", [t.post_entry_leakage for t in applicable]),
        _estimate("forgery_acceptance_F", [t.forgery_acceptance for t in applicable]),
        _estimate("replay_acceptance_Y", [t.replay_acceptance for t in applicable]),
        _estimate("policy_rejection", [t.policy_rejected for t in applicable]),
        _estimate("false_rejection", [t.false_rejection for t in applicable]),
        _estimate("identity_available", [t.identity_available for t in applicable]),
    )
    latencies = [t.latency_ms for t in applicable if t.latency_ms is not None]
    latency = {
        "count": len(latencies),
        "median_ms": None if not latencies else median(latencies),
        "p95_ms": None if not latencies else percentile(latencies, 0.95),
    }
    exclusions: Dict[str, int] = {}
    for trial in trials:
        if not trial.applicable:
            reason = str(trial.metadata.get("exclusion_reason", "not_applicable"))
            exclusions[reason] = exclusions.get(reason, 0) + 1
    conditions = sorted({trial.condition for trial in trials})
    return ExperimentSummary(
        label="synthetic smoke-test output, not a paper result",
        metrics=metrics,
        latency=latency,
        exclusions=exclusions,
        provenance=dict(provenance or {}, conditions=conditions),
    )
