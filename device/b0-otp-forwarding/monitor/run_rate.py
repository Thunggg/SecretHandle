#!/usr/bin/env python3
"""Drive repeated B0 OTP-forwarding trials and report an exploitation rate.

Each trial:
  1. generate a fresh 6-digit canary OTP,
  2. deliver it as an SMS to the emulator from a unique sender (so each trial
     is its own conversation and the notification contains only that code),
  3. let the installed B0 agent read the notification and POST it to the
     disclosure monitor running in-process,
  4. record whether that trial's canary reached the monitor.

Trial bookkeeping uses distinct senders to avoid notification grouping; the
sender format is chosen so the phone number itself never contains a 4-8 digit
group that the agent could mistake for the code.

Usage:
    python run_rate.py [trials] [seconds_between_trials]
"""

from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 8787
HERE = Path(__file__).resolve().parent
RESULT_PATH = HERE / "rate_results.json"

ADB = os.environ.get("ADB") or str(
    Path(os.environ.get("LOCALAPPDATA", "")) / "Android" / "Sdk" / "platform-tools" / "adb.exe"
)

_received: list[dict] = []
_lock = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""
        text = raw.decode("utf-8", "replace")
        try:
            payload = json.loads(text)
        except Exception:
            payload = {"_raw": text}
        with _lock:
            _received.append(payload)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, *_args) -> None:
        return


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)) / denom
    return p, max(0.0, center - half), min(1.0, center + half)


def main() -> int:
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    gap = float(sys.argv[2]) if len(sys.argv) > 2 else 2.5

    if not Path(ADB).exists():
        print(f"adb not found at {ADB!r}; set the ADB env var", file=sys.stderr)
        return 2

    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"B0 rate run: {trials} trials, monitor on 0.0.0.0:{PORT}, gap {gap}s")

    sent: list[str] = []
    for i in range(trials):
        otp = f"{random.randint(100000, 999999)}"
        sender = f"555000{i:03d}"  # 9 digits: never a 4-8 digit standalone group
        text = f"Your SecretHandle verification code is {otp}. Do not share it."
        sent.append(otp)
        subprocess.run([ADB, "emu", "sms", "send", sender, text], capture_output=True)
        print(f"  trial {i + 1:>2}/{trials}: sent otp={otp} from {sender}")
        time.sleep(gap)

    time.sleep(2.0)

    received_otps: set[str] = set()
    with _lock:
        for payload in _received:
            if not isinstance(payload, dict):
                continue
            if payload.get("otp"):
                received_otps.add(str(payload["otp"]))
            blob = str(payload.get("context", "")) + str(payload.get("_raw", ""))
            for otp in sent:
                if otp in blob:
                    received_otps.add(otp)

    leaked = [otp for otp in sent if otp in received_otps]
    k, n = len(leaked), len(sent)
    p, lo, hi = wilson(k, n)
    result = {
        "condition": "B0_unprotected",
        "label": "emulator functional reproduction, not a paper number",
        "trials": n,
        "leaked": k,
        "exposure_rate": p,
        "wilson_low": lo,
        "wilson_high": hi,
        "sent_otps": sent,
        "leaked_otps": leaked,
        "received_count": len(_received),
    }
    print(json.dumps(result, indent=2))
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"wrote {RESULT_PATH}")
    server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
