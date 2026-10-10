import pytest

from secrethandle.statistics import (
    bootstrap_interval,
    exact_mcnemar,
    paired_permutation_pvalue,
    wilson_interval,
)


def test_wilson_interval_contains_observed_rate():
    low, high = wilson_interval(0, 10)
    assert low == 0.0 and 0.0 < high < 1.0
    low, high = wilson_interval(5, 10)
    assert low < 0.5 < high


def test_bootstrap_is_seeded():
    first = bootstrap_interval([1, 2, 3, 4], repetitions=100, seed=4)
    second = bootstrap_interval([1, 2, 3, 4], repetitions=100, seed=4)
    assert first == second


def test_paired_tests_handle_ties_and_differences():
    assert exact_mcnemar([True, False], [True, False]) == 1.0
    value = paired_permutation_pvalue([1, 2, 3], [0, 1, 2], repetitions=100, seed=1)
    assert 0.0 < value <= 1.0
