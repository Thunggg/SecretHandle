import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "secrethandle.cli", "--help"],
        env={**os.environ, "PYTHONPATH": "src"}, text=True, capture_output=True, check=True,
    )
    assert "synthetic-demo" in result.stdout


def test_cli_synthetic_demo(tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text(
        Path("configs/default.yaml").read_text().replace("outputs/default", str(tmp_path / "out")),
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "scripts/run_synthetic_demo.py", "--config", str(config)],
        text=True, capture_output=True, check=True,
    )
    payload = json.loads(result.stdout)
    assert "not a paper result" in payload["label"]
    assert (tmp_path / "out" / "metrics.csv").is_file()
