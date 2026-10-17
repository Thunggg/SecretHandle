"""Generate labeled plots only from result CSV files produced by the runner."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .io import read_metrics_csv

SYNTHETIC_LABEL = "Synthetic smoke-test output, not a paper result"


def make_plots(input_csv: str, output_dir: str) -> list[str]:
    rows = read_metrics_csv(input_csv)
    if not rows:
        raise ValueError("metrics CSV is empty")
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    conditions = sorted({row["condition"] for row in rows})
    selected = ["exposure_E", "redirection_R", "utility_U", "post_entry_leakage_L"]
    generated = []
    for metric in selected:
        values = []
        available = []
        for condition in conditions:
            match = next((row for row in rows if row["condition"] == condition and row["metric"] == metric), None)
            is_available = match is not None and match["value"] not in {"", "None"}
            available.append(is_available)
            values.append(float(match["value"]) if is_available and match is not None else 0.0)
        fig, axis = plt.subplots(figsize=(8, 4.5))
        bars = axis.bar(
            conditions,
            values,
            color=["#2f6b9a" if item else "#eef0f2" for item in available],
            edgecolor=["#2f6b9a" if item else "#5f6770" for item in available],
            hatch=["" if item else "//" for item in available],
        )
        for bar, value, is_available in zip(bars, values, available, strict=False):
            label = f"{value:.2f}" if is_available else "N/A"
            axis.text(
                bar.get_x() + bar.get_width() / 2,
                min(0.96, value + 0.03) if is_available else 0.03,
                label,
                ha="center",
                va="bottom",
                fontsize=9,
            )
        axis.set_ylim(0, 1)
        axis.set_ylabel(metric)
        axis.set_title(SYNTHETIC_LABEL)
        axis.tick_params(axis="x", rotation=20)
        fig.tight_layout()
        path = destination / f"{metric}.png"
        fig.savefig(path, dpi=180)
        plt.close(fig)
        generated.append(str(path))
    (destination / "README.txt").write_text(
        SYNTHETIC_LABEL + "\nPlots are generated from metrics.csv; they are not paper results.\n",
        encoding="utf-8",
    )
    return generated
