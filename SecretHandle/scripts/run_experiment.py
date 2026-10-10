#!/usr/bin/env python3
"""Run a configured calibration/evaluation/ablation stage."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from secrethandle.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["experiment", *sys.argv[1:]]))
