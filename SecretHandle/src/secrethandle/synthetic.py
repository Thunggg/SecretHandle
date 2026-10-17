"""Deterministic synthetic canaries and target contexts for smoke tests."""

from __future__ import annotations

import hashlib
import random

from .schemas import SecretType, TargetContext, TargetToken


class SeededIdentifierSource:
    def __init__(self, seed: int, lambda_bits: int = 128) -> None:
        self._rng = random.Random(seed)
        self._bits = lambda_bits

    def __call__(self) -> str:
        return f"{self._rng.getrandbits(self._bits):0{self._bits // 4}x}"


def synthetic_key(seed: int) -> bytes:
    return hashlib.sha256(f"secrethandle-synthetic-key:{seed}".encode()).digest()


def canary(seed: int, secret_type: SecretType = SecretType.OTP) -> str:
    rng = random.Random(seed)
    if secret_type is SecretType.OTP:
        return f"{rng.randrange(0, 1_000_000):06d}"
    return f"SH-{secret_type.value.upper()}-{rng.getrandbits(48):012x}"


def target_tokens(now: float = 1000.0) -> tuple[TargetToken, TargetToken, TargetToken]:
    legitimate = TargetToken(
        "node-good",
        TargetContext("com.example.bank", "https://bank.example", "otp", "otp-field", 1, "win-bank"),
        now + 600,
    )
    attacker = TargetToken(
        "node-attacker",
        TargetContext("com.attacker.app", None, "otp", "steal-field", 1, "win-attacker"),
        now + 600,
    )
    stale = TargetToken(
        "node-stale",
        TargetContext("com.example.bank", "https://bank.example", "otp", "otp-field", 0, "win-bank"),
        now - 1,
    )
    return legitimate, attacker, stale
