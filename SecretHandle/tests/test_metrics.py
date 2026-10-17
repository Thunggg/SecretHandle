import pytest

from secrethandle.metrics import (
    aggregate_trial_metrics,
    deterministic_view_difference,
    exposure_rate,
)
from secrethandle.schemas import TrialOutcome


def trial(**overrides):
    data = {
        "trial_id": "t", "condition": "B3", "attack": "benign", "applicable": True,
        "exposure": False, "redirection_success": None, "utility_success": True,
        "post_entry_leakage": False, "forgery_acceptance": None, "replay_acceptance": None,
        "latency_ms": 1.0,
    }
    data.update(overrides)
    return TrialOutcome(**data)


def test_equation_8_and_empty_guard():
    assert exposure_rate([False, True, False]) == pytest.approx(1 / 3)
    with pytest.raises(ValueError):
        exposure_rate([])


def test_metric_aggregation_has_explicit_denominators():
    summary = aggregate_trial_metrics([trial(), trial(trial_id="t2", exposure=True)])
    exposure = next(metric for metric in summary.metrics if metric.name == "exposure_E")
    assert (exposure.numerator, exposure.denominator, exposure.value) == (1, 2, 0.5)
    redirect = next(metric for metric in summary.metrics if metric.name == "redirection_R")
    assert redirect.value is None and redirect.denominator == 0


def test_view_difference_diagnostic():
    assert deterministic_view_difference(["a", "b"], ["a", "c"]) == 0.5
