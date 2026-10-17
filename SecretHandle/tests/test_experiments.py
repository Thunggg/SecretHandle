import json
from pathlib import Path

from secrethandle.config import load_config
from secrethandle.experiments import (
    generate_synthetic_trials,
    run_killer_experiment,
    run_synthetic_demo,
)


def config_for(tmp_path):
    config = load_config("configs/default.yaml")
    config["output"]["dir"] = str(tmp_path / "out")
    return config


def test_reference_experiment_and_killer_conditions(tmp_path):
    config = config_for(tmp_path)
    trials = generate_synthetic_trials(config)
    assert trials and all(trial.synthetic for trial in trials)
    killer = run_killer_experiment(config)
    assert killer["passed"] and killer["synthetic_only"]


def test_outputs_are_generated_and_labeled(tmp_path):
    config = config_for(tmp_path)
    result = run_synthetic_demo(config)
    output = Path(result["output_dir"])
    assert {"trials.jsonl", "summary.json", "provenance.json", "metrics.csv"}.issubset(
        path.name for path in output.iterdir()
    )
    provenance = json.loads((output / "provenance.json").read_text())
    assert not provenance["real_experiment"]
    assert "not a paper result" in provenance["label"]


def test_fixed_seed_produces_identical_semantic_trials(tmp_path):
    first = config_for(tmp_path / "a")
    second = config_for(tmp_path / "b")
    a = [t.to_dict() for t in generate_synthetic_trials(first)]
    b = [t.to_dict() for t in generate_synthetic_trials(second)]
    assert a == b
