#!/usr/bin/env python3
"""Create labeled figures from runner-produced metrics CSV."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from secrethandle.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["plot", *sys.argv[1:]]))
