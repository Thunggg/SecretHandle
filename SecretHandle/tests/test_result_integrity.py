import json

from secrethandle.config import load_config
from secrethandle.experiments import run_synthetic_demo


def test_outputs_declare_synthetic_and_do_not_serialize_canaries(tmp_path):
    config = load_config("configs/default.yaml")
    config["output"]["dir"] = str(tmp_path / "run")
    run_synthetic_demo(config)
    provenance = json.loads((tmp_path / "run" / "provenance.json").read_text())
    assert provenance["real_experiment"] is False
    assert provenance["paper_placeholder_numbers_used"] is False
    trials = (tmp_path / "run" / "trials.jsonl").read_text()
    assert "123456" not in trials
    assert "secret\"" not in trials.lower()
