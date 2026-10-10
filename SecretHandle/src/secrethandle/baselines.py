"""B0-B3 baseline interfaces from Section 9.4."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Optional, Sequence, Tuple

from .schemas import Artifact


@dataclass(frozen=True)
class BaselineResult:
    public_value: str
    delivered_value: Optional[str]
    bound_to_destination: bool
    artifacts: Tuple[Artifact, ...]
    applicable: bool = True
    note: str = ""


class Baseline(ABC):
    name: str

    @abstractmethod
    def run(self, secret: str, requested_target: str, authorized_target: str) -> BaselineResult:
        raise NotImplementedError


class UnprotectedBaseline(Baseline):
    """B0 synthetic-only baseline exposing and typing the raw value."""

    name = "B0_unprotected"

    def run(self, secret: str, requested_target: str, authorized_target: str) -> BaselineResult:
        return BaselineResult(
            public_value=secret,
            delivered_value=secret,
            bound_to_destination=False,
            artifacts=(Artifact("agent_prompt", f"value={secret}"),),
            note="synthetic-only unsafe baseline",
        )


class DetectedPlaceholderBaseline(Baseline):
    """B1 reference placeholder; not an implementation of an external paper repository."""

    name = "B1_detected_placeholder"

    def run(self, secret: str, requested_target: str, authorized_target: str) -> BaselineResult:
        placeholder = "<SENSITIVE:OTP>"
        return BaselineResult(
            public_value=placeholder,
            delivered_value=secret,
            bound_to_destination=False,
            artifacts=(Artifact("agent_prompt", placeholder), Artifact("action_echo", placeholder)),
            note="deterministic reference detector; no destination binding",
        )


class PlatformFlowBaseline(Baseline):
    """B2 placeholder for a manually provisioned Android platform-flow adapter."""

    name = "B2_platform_flow"

    def run(self, secret: str, requested_target: str, authorized_target: str) -> BaselineResult:
        return BaselineResult(
            public_value="",
            delivered_value=None,
            bound_to_destination=True,
            artifacts=(),
            applicable=False,
            note="requires Android Autofill/OTP Autofill/Credential Manager",
        )


class SecretHandleBaseline(Baseline):
    """B3 label used by the experiment runner; core behavior is in SecretHandleService."""

    name = "B3_secrethandle"

    def run(self, secret: str, requested_target: str, authorized_target: str) -> BaselineResult:
        raise RuntimeError("B3 must be run through the SecretHandle experiment harness")
