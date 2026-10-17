"""Confidence intervals and paired analyses specified in Section 9.6."""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Sequence
from statistics import median


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Two-sided Wilson score interval for a binomial proportion."""

    if total <= 0 or successes < 0 or successes > total:
        raise ValueError("require 0 <= successes <= total and total > 0")
    phat = successes / total
    z2 = z * z
    denominator = 1.0 + z2 / total
    center = (phat + z2 / (2.0 * total)) / denominator
    radius = z * math.sqrt((phat * (1.0 - phat) + z2 / (4.0 * total)) / total) / denominator
    return max(0.0, center - radius), min(1.0, center + radius)


def percentile(values: Sequence[float], q: float) -> float:
    if not values or not 0.0 <= q <= 1.0:
        raise ValueError("nonempty values and q in [0, 1] required")
    ordered = sorted(float(v) for v in values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def bootstrap_interval(
    values: Sequence[float],
    statistic: Callable[[Sequence[float]], float] = median,
    confidence: float = 0.95,
    repetitions: int = 1000,
    seed: int = 0,
) -> tuple[float, float]:
    if not values or repetitions <= 0 or not 0.0 < confidence < 1.0:
        raise ValueError("valid values, repetitions, and confidence are required")
    rng = random.Random(seed)
    estimates = []
    values = list(map(float, values))
    for _ in range(repetitions):
        sample = [rng.choice(values) for _ in values]
        estimates.append(float(statistic(sample)))
    alpha = (1.0 - confidence) / 2.0
    return percentile(estimates, alpha), percentile(estimates, 1.0 - alpha)


def exact_mcnemar(left: Sequence[bool], right: Sequence[bool]) -> float:
    """Two-sided exact McNemar p-value using discordant pairs."""

    if len(left) != len(right) or not left:
        raise ValueError("paired nonempty sequences required")
    b = sum(bool(a) and not bool(c) for a, c in zip(left, right, strict=False))
    c = sum(not bool(a) and bool(c_) for a, c_ in zip(left, right, strict=False))
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2**n)
    return min(1.0, 2.0 * tail)


def paired_permutation_pvalue(
    left: Sequence[float], right: Sequence[float], repetitions: int = 5000, seed: int = 0
) -> float:
    if len(left) != len(right) or not left or repetitions <= 0:
        raise ValueError("paired nonempty sequences and positive repetitions required")
    differences = [float(a) - float(b) for a, b in zip(left, right, strict=False)]
    observed = abs(sum(differences) / len(differences))
    rng = random.Random(seed)
    extreme = 0
    for _ in range(repetitions):
        permuted = [d if rng.random() < 0.5 else -d for d in differences]
        if abs(sum(permuted) / len(permuted)) >= observed - 1e-15:
            extreme += 1
    return (extreme + 1) / (repetitions + 1)
