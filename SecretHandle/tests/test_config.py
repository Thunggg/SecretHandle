from pathlib import Path

import pytest
import yaml

from secrethandle.config import load_config, validate_config


def test_synthetic_config_loads():
    config = load_config("configs/synthetic_demo.yaml")
    assert config["data"]["mode"] == "synthetic"
    assert len(config["_config_sha256"]) == 64


def test_real_config_requires_root():
    config = yaml.safe_load(Path("configs/default.yaml").read_text())
    config["data"] = {"mode": "real", "root": None}
    with pytest.raises(ValueError):
        validate_config(config)
