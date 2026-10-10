"""Principal-specific structured observation redaction (Algorithm 3)."""

from __future__ import annotations

import threading
from typing import Dict, Iterable, Optional

from .schemas import Observation, ObservationItem, RedactionObligation, SecretType


_DEFAULT_MASKS = {
    SecretType.OTP: "[OTP PROTECTED]",
    SecretType.CREDENTIAL: "[CREDENTIAL PROTECTED]",
    SecretType.IDENTIFIER: "[IDENTIFIER PROTECTED]",
    SecretType.CLIPBOARD: "[CLIPBOARD VALUE PROTECTED]",
    SecretType.PAYMENT: "[PAYMENT VALUE PROTECTED]",
}


class ObservationRedactor:
    def __init__(self) -> None:
        self._obligations: Dict[str, RedactionObligation] = {}
        self._lock = threading.RLock()

    def register(
        self, target_token_id: str, handle_id: str, secret_type: SecretType, now: float
    ) -> RedactionObligation:
        obligation = RedactionObligation(
            target_token_id=target_token_id,
            handle_id=handle_id,
            secret_type=secret_type,
            created_at=now,
            mask=_DEFAULT_MASKS[secret_type],
        )
        with self._lock:
            self._obligations[target_token_id] = obligation
        return obligation

    def clear(self, target_token_id: str) -> bool:
        with self._lock:
            return self._obligations.pop(target_token_id, None) is not None

    def redact(self, observation: Observation) -> Observation:
        """Implement Equation (4) and Algorithm 3 for structured synthetic observations."""

        with self._lock:
            obligations = dict(self._obligations)
        output = []
        suppress_frame = observation.frame_suppressed
        for item in observation.items:
            obligation = obligations.get(item.target_token_id or "")
            if obligation is None:
                output.append(item)
                continue
            if not item.stable_identity:
                suppress_frame = True
                output.append(
                    ObservationItem(
                        channel=item.channel,
                        text="[WINDOW SUPPRESSED]",
                        target_token_id=item.target_token_id,
                        stable_identity=False,
                        window_id=item.window_id,
                    )
                )
            else:
                output.append(
                    ObservationItem(
                        channel=item.channel,
                        text=obligation.mask,
                        target_token_id=item.target_token_id,
                        stable_identity=True,
                        window_id=item.window_id,
                    )
                )
        return Observation(tuple(output), suppress_frame)

    def active_count(self) -> int:
        with self._lock:
            return len(self._obligations)
