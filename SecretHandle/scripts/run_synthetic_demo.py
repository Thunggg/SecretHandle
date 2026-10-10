#!/usr/bin/env python3
"""Run the deterministic synthetic smoke-test pipeline."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from secrethandle.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["synthetic-demo", *sys.argv[1:]]))
