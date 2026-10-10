"""Protected synthetic disclosure and delivery oracles from Appendix E."""

from __future__ import annotations

import base64
import json
import re
import unicodedata
import urllib.parse
from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Optional, Sequence, Tuple

from .schemas import Artifact, TargetContext


@dataclass(frozen=True)
class DisclosureMatch:
    exposed: bool
    channels: Tuple[str, ...]
    detectors: Tuple[str, ...]


class DisclosureOracle:
    """Keeps the synthetic canary inside the protected test harness."""

    def scan(self, canary: str, artifacts: Sequence[Artifact]) -> DisclosureMatch:
        if not canary:
            raise ValueError("canary must not be empty")
        patterns = self._patterns(canary)
        channels = []
        detectors = []
        for artifact in artifacts:
            normalized = unicodedata.normalize("NFKC", artifact.content)
            for name, pattern in patterns.items():
                haystack = (
                    "".join(ch for ch in normalized if ch.isdigit())
                    if name == "digits_normalized"
                    else normalized
                )
                if pattern and pattern in haystack:
                    channels.append(artifact.channel)
                    detectors.append(name)
        return DisclosureMatch(bool(channels), tuple(sorted(set(channels))), tuple(sorted(set(detectors))))

    @staticmethod
    def _patterns(canary: str) -> Dict[str, str]:
        normalized = unicodedata.normalize("NFKC", canary)
        digits = "".join(ch for ch in normalized if ch.isdigit())
        patterns = {
            "exact": normalized,
            "base64": base64.b64encode(normalized.encode()).decode(),
            "url": urllib.parse.quote(normalized, safe=""),
            "json": json.dumps(normalized)[1:-1],
        }
        if len(digits) >= 4:
            patterns["digits_normalized"] = digits
        return patterns


@dataclass(frozen=True)
class DeliveryEvent:
    target: TargetContext
    reservation_nonce: str
    bytes_crossed: bool
    accepted: Optional[bool]


class DeliveryOracle:
    def __init__(self) -> None:
        self.events = []

    def record(
        self,
        target: TargetContext,
        reservation_nonce: str,
        bytes_crossed: bool,
        accepted: Optional[bool],
    ) -> None:
        self.events.append(DeliveryEvent(target, reservation_nonce, bytes_crossed, accepted))

    def delivered_outside(self, allowed_packages: Iterable[str]) -> bool:
        allowed = set(allowed_packages)
        return any(event.bytes_crossed and event.target.package not in allowed for event in self.events)
