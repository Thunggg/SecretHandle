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


def _trial_config(attacks, conditions):
    return {
        "run": {"seed": 7, "name": "unit"},
        "security": {"lambda_bits": 128},
        "data": {"mode": "synthetic", "root": None},
        "experiment": {"trials_per_attack": 3, "attacks": attacks, "conditions": conditions},
        "output": {"dir": "outputs/unit"},
    }


def test_b3_read_exfil_never_exposes_raw_value():
    trials = generate_synthetic_trials(_trial_config(["read_exfil"], ["B3_secrethandle"]))
    assert trials and all(trial.exposure is False for trial in trials)


def test_b3_ambiguous_identity_fails_closed():
    trials = generate_synthetic_trials(_trial_config(["ambiguous_identity"], ["B3_secrethandle"]))
    assert all(trial.policy_rejected is True for trial in trials)
    assert all(trial.redirection_success is False for trial in trials)
    assert all(trial.identity_available is False for trial in trials)


def test_unprotected_baseline_read_exfil_exposes_and_ambiguity_redirects():
    trials = generate_synthetic_trials(
        _trial_config(["read_exfil", "ambiguous_identity"], ["B0_unprotected"])
    )
    read = [trial for trial in trials if trial.attack == "read_exfil"]
    ambiguous = [trial for trial in trials if trial.attack == "ambiguous_identity"]
    assert read and all(trial.exposure is True for trial in read)
    assert ambiguous and all(trial.redirection_success is True for trial in ambiguous)
    assert all(trial.identity_available is False for trial in ambiguous)
