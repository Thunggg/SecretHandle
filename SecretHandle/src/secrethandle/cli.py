"""Command-line interface for synthetic and externally provisioned workflows."""

from __future__ import annotations

import argparse
import json
import logging
from collections.abc import Sequence
from pathlib import Path

from .config import load_config
from .experiments import run_ablation, run_killer_experiment, run_synthetic_demo
from .plotting import make_plots


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="secrethandle",
        description="SecretHandle reference model and reproducible synthetic harness",
    )
    parser.add_argument("--verbose", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("synthetic-demo", help="run labeled synthetic smoke tests")
    demo.add_argument("--config", required=True)

    experiment = subparsers.add_parser("experiment", help="run a configured stage")
    experiment.add_argument("--config", required=True)
    experiment.add_argument(
        "--stage", required=True, choices=["evaluate", "ablation", "killer"]
    )

    plot = subparsers.add_parser("plot", help="plot a generated metrics CSV")
    plot.add_argument("--input", required=True)
    plot.add_argument("--output", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    if args.command == "synthetic-demo":
        result = run_synthetic_demo(load_config(args.config))
    elif args.command == "experiment":
        config = load_config(args.config)
        if args.stage == "evaluate":
            if config["data"]["mode"] != "synthetic":
                parser.error("real mode requires external adapters and manually provisioned data")
            result = run_synthetic_demo(config)
        elif args.stage == "ablation":
            result = run_ablation(config)
            output = Path(str(config["output"]["dir"])) / "ablation_manifest.json"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        else:
            result = run_killer_experiment(config)
    else:
        generated = make_plots(args.input, args.output)
        result = {"generated": generated}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
