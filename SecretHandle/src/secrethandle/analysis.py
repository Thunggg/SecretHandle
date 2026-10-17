"""Post-hoc analysis of raw secret-free trials.

Produces paired comparisons (B0 vs B3) where applicable and device-blocked/
exclusion reporting as required by the prospective analysis plan (Section 9.6).
"""
from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .io import atomic_write_json, atomic_write_jsonl
from .schemas import TrialOutcome
from .statistics import exact_mcnemar, paired_permutation_pvalue

DICHOTOMOUS_METRICS = [
    "exposure",
    "redirection_success",
    "utility_success",
    "post_entry_leakage",
    "forgery_acceptance",
    "replay_acceptance",
    "policy_rejected",
    "false_rejection",
    "identity_available",
]


def _load_trials(path: Path) -> list[TrialOutcome]:
    trials: list[TrialOutcome] = []
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            trials.append(TrialOutcome(**data))
    if not trials:
        raise ValueError(f"no trials found in {path}")
    return trials


def _group_by(trials: Iterable[TrialOutcome], key: str) -> dict[str, list[TrialOutcome]]:
    grouped: dict[str, list[TrialOutcome]] = {}
    for trial in trials:
        val = getattr(trial, key)
        grouped.setdefault(str(val), []).append(trial)
    return grouped


def _paired_comparisons(trials: list[TrialOutcome]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    by_attack = _group_by(trials, "attack")
    for attack, subset in by_attack.items():
        b0 = [t for t in subset if t.condition == "B0_unprotected" and t.applicable]
        b3 = [t for t in subset if t.condition == "B3_secrethandle" and t.applicable]
        b0.sort(key=lambda x: x.trial_id)
        b3.sort(key=lambda x: x.trial_id)
        n = min(len(b0), len(b3))
        for metric in DICHOTOMOUS_METRICS:
            left_vals: list[bool] = []
            right_vals: list[bool] = []
            for i in range(n):
                lval = getattr(b0[i], metric)
                rval = getattr(b3[i], metric)
                if lval is None or rval is None:
                    continue
                left_vals.append(bool(lval))
                right_vals.append(bool(rval))
            if len(left_vals) < 1:
                continue
            p_mcnemar = exact_mcnemar(left_vals, right_vals)
            results.append(
                {
                    "comparison": "B0_unprotected_vs_B3_secrethandle",
                    "attack": attack,
                    "metric": metric,
                    "n_pairs": len(left_vals),
                    "p_mcnemar_exact": p_mcnemar,
                    "paired_permutation_pvalue": None,
                }
            )
        b0_lat = [float(t.latency_ms) for t in b0 if t.latency_ms is not None]
        b3_lat = [float(t.latency_ms) for t in b3 if t.latency_ms is not None]
        if len(b0_lat) == len(b3_lat) and b0_lat:
            p_perm = paired_permutation_pvalue(b0_lat, b3_lat, repetitions=1000, seed=0)
            results.append(
                {
                    "comparison": "B0_unprotected_vs_B3_secrethandle",
                    "attack": attack,
                    "metric": "latency_ms",
                    "n_pairs": len(b0_lat),
                    "p_mcnemar_exact": None,
                    "paired_permutation_pvalue": p_perm,
                }
            )
    return results


def _exclusions(trials: list[TrialOutcome]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for trial in trials:
        if not trial.applicable:
            reason = str(trial.metadata.get("exclusion_reason", "not_applicable"))
            counts[reason] = counts.get(reason, 0) + 1
    return counts


def _write_paired_csv(output_dir: Path, paired: list[dict[str, Any]]) -> None:
    tables_dir = output_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "comparison",
        "attack",
        "metric",
        "n_pairs",
        "p_mcnemar_exact",
        "paired_permutation_pvalue",
    ]
    path = tables_dir / "paired_comparisons.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in paired:
            writer.writerow({k: row.get(k) for k in fieldnames})


def _write_exclusions_csv(output_dir: Path, exclusions: dict[str, int]) -> None:
    tables_dir = output_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    path = tables_dir / "exclusions.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["exclusion_reason", "count"])
        for reason in sorted(exclusions):
            writer.writerow([reason, exclusions[reason]])


def analyze_trials_from_file(trials_file: Path, output_dir: Path) -> dict[str, Any]:
    trials = _load_trials(trials_file)
    output_dir.mkdir(parents=True, exist_ok=True)
    paired = _paired_comparisons(trials)
    exclusions = _exclusions(trials)
    atomic_write_json(output_dir / "paired_comparisons.json", paired)
    atomic_write_json(output_dir / "exclusions.json", exclusions)
    atomic_write_jsonl(output_dir / "paired_comparisons.jsonl", (r for r in paired))
    _write_paired_csv(output_dir, paired)
    _write_exclusions_csv(output_dir, exclusions)
    return {
        "output_dir": str(output_dir),
        "n_trials": len(trials),
        "n_paired_comparisons": len(paired),
        "device_blocked_exclusions": exclusions,
    }


def analyze_trials_from_dir(trials_dir: Path, output_dir: Path) -> dict[str, Any]:
    return analyze_trials_from_file(trials_dir / "trials.jsonl", output_dir)
