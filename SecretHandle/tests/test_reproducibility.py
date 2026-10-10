import json
from pathlib import Path

from secrethandle.config import load_config
from secrethandle.experiments import run_synthetic_demo


def semantic_trials(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()]


def test_repeated_runs_have_identical_trials(tmp_path):
    first = load_config("configs/default.yaml")
    second = load_config("configs/default.yaml")
    first["output"]["dir"] = str(tmp_path / "first")
    second["output"]["dir"] = str(tmp_path / "second")
    run_synthetic_demo(first)
    run_synthetic_demo(second)
    assert semantic_trials(tmp_path / "first" / "trials.jsonl") == semantic_trials(
        tmp_path / "second" / "trials.jsonl"
    )
