"""Deterministic, atomic result I/O."""

from __future__ import annotations

import csv
import json
import os
import tempfile
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence


def _json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "value"):
        return value.value
    raise TypeError(f"not JSON serializable: {type(value).__name__}")


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, sort_keys=True, default=_json_default) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        stream.write(payload)
        temporary = Path(stream.name)
    os.replace(str(temporary), str(path))


def atomic_write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        for row in rows:
            stream.write(json.dumps(dict(row), sort_keys=True, default=_json_default) + "\n")
        temporary = Path(stream.name)
    os.replace(str(temporary), str(path))


def write_metrics_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["condition", "metric", "numerator", "denominator", "value", "ci_low", "ci_high"]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name) for name in fieldnames})


def read_metrics_csv(path: str) -> list:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))
