import json

from secrethandle.config import load_config
from secrethandle.experiments import run_synthetic_demo
from secrethandle.integrity import expected_canaries, find_canary_leaks


def test_outputs_declare_synthetic_and_do_not_serialize_canaries(tmp_path):
    config = load_config("configs/default.yaml")
    config["output"]["dir"] = str(tmp_path / "run")
    run_synthetic_demo(config)
    provenance = json.loads((tmp_path / "run" / "provenance.json").read_text(encoding="utf-8"))
    assert provenance["real_experiment"] is False
    assert provenance["paper_placeholder_numbers_used"] is False
    trials = (tmp_path / "run" / "trials.jsonl").read_text(encoding="utf-8")
    assert "123456" not in trials
    assert "secret\"" not in trials.lower()
    assert find_canary_leaks(tmp_path / "run", expected_canaries(config)) == []


def test_canary_leak_detector_flags_injected_secret(tmp_path):
    canaries = expected_canaries(load_config("configs/default.yaml"))
    leaked = sorted(canaries)[0]
    (tmp_path / "trials.jsonl").write_text(f'{{"value": "{leaked}"}}\n', encoding="utf-8")
    assert find_canary_leaks(tmp_path, canaries) == [("trials.jsonl", leaked)]
