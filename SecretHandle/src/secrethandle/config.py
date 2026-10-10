"""YAML configuration loading and validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping

import yaml


def load_config(path: str) -> Dict[str, Any]:
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"configuration not found: {config_path}")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("configuration root must be a mapping")
    validate_config(data)
    data["_config_path"] = str(config_path.resolve())
    data["_config_sha256"] = hashlib.sha256(config_path.read_bytes()).hexdigest()
    return data


def validate_config(config: Mapping[str, Any]) -> None:
    for key in ("run", "security", "data", "experiment", "output"):
        if key not in config or not isinstance(config[key], Mapping):
            raise ValueError(f"missing mapping: {key}")
    seed = config["run"].get("seed")
    if not isinstance(seed, int) or seed < 0:
        raise ValueError("run.seed must be a nonnegative integer")
    lambda_bits = config["security"].get("lambda_bits")
    if not isinstance(lambda_bits, int) or lambda_bits < 96 or lambda_bits % 8:
        raise ValueError("security.lambda_bits must be byte-aligned and at least 96")
    trials = config["experiment"].get("trials_per_attack")
    if not isinstance(trials, int) or trials <= 0:
        raise ValueError("experiment.trials_per_attack must be positive")
    mode = config["data"].get("mode")
    if mode not in {"synthetic", "real"}:
        raise ValueError("data.mode must be synthetic or real")
    if mode == "real" and not config["data"].get("root"):
        raise ValueError("data.root is required for real mode")


def public_config(config: Mapping[str, Any]) -> Dict[str, Any]:
    """Return config data safe for provenance; reject obvious credential fields."""

    forbidden = {"secret", "token", "api_key", "password", "credential"}

    def clean(value: Any, key: str = "") -> Any:
        if any(part in key.lower() for part in forbidden):
            return "[REDACTED]"
        if isinstance(value, Mapping):
            return {str(k): clean(v, str(k)) for k, v in value.items() if not str(k).startswith("_")}
        if isinstance(value, list):
            return [clean(v) for v in value]
        return value

    return clean(config)
