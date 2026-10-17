#!/usr/bin/env python3
"""One-command offline canary-leak smoke check for the synthetic pipeline.

Runs the deterministic synthetic runner for a configuration, reconstructs every
canary it could have minted, and verifies that none of them appears in any
generated artifact. It also asserts the provenance flags that mark the output
as synthetic. Exits non-zero on any leak or provenance violation.

This never touches the network, a dataset, a model, an Android device, or a
credential, so it is safe to run in CI and in isolation.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from secrethandle.config import load_config
from secrethandle.experiments import run_synthetic_demo
from secrethandle.integrity import expected_canaries, find_canary_leaks


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="smoke-check",
        description="Offline, isolated canary-leak smoke check for synthetic outputs.",
    )
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument(
        "--output",
        default=None,
        help="output directory (default: the config's output.dir)",
    )
    args = parser.parse_args(argv)

    config = load_config(args.config)
    if args.output:
        config["output"]["dir"] = args.output
    output_dir = Path(str(config["output"]["dir"]))

    result = run_synthetic_demo(config)

    provenance = json.loads((output_dir / "provenance.json").read_text(encoding="utf-8"))
    flags_ok = (
        provenance.get("real_experiment") is False
        and provenance.get("paper_placeholder_numbers_used") is False
        and provenance.get("label") == "synthetic smoke-test output, not a paper result"
    )

    canaries = expected_canaries(config)
    leaks = find_canary_leaks(output_dir, canaries)

    report = {
        "config": args.config,
        "output_dir": str(output_dir),
        "trial_count": result["trial_count"],
        "canaries_checked": len(canaries),
        "provenance_flags_ok": flags_ok,
        "leaks": leaks,
        "status": "pass" if (flags_ok and not leaks) else "fail",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if (flags_ok and not leaks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
