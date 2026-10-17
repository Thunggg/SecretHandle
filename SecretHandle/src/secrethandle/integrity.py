"""Canary-leak detection for generated synthetic artifacts.

The synthetic runner mints deterministic canaries from a configured seed. This
module reconstructs the exact set of canaries a run could have produced and
scans the generated artifacts for any of them, so a smoke check can prove the
pipeline never serializes a secret value into an output file.

The scan is deliberately offline: it reads only local files and uses no
network, dataset, model, device, or credential.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .synthetic import canary

DEFAULT_ATTACKS = ("benign", "redirect", "forgery", "replay", "reread", "expired")
TOKEN = re.compile(r"(?<!\d)\d{6}(?!\d)|SH-[A-Z]+-[0-9a-f]{12}")


def expected_canaries(config: Mapping[str, Any]) -> set[str]:
    """Every canary value the synthetic runner could mint for ``config``."""

    base_seed = int(config["run"]["seed"])
    count = int(config["experiment"]["trials_per_attack"])
    attacks = list(config["experiment"].get("attacks", DEFAULT_ATTACKS))
    return {
        canary(base_seed + offset + 1000 * index)
        for index in range(len(attacks))
        for offset in range(count)
    }


def find_canary_leaks(directory: Path, canaries: set[str]) -> list[tuple[str, str]]:
    """Return ``(relative_path, token)`` pairs where a canary leaked into output."""

    leaks: list[tuple[str, str]] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in TOKEN.findall(text):
            if token in canaries:
                leaks.append((str(path.relative_to(directory)), token))
    return leaks
