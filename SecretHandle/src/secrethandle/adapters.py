"""Interfaces for trusted platform functions and external experiment dependencies.

Adapter contract v1 (frozen 2026-10-17). These abstract signatures are the stable
seam between the reference model and the platform/experiment implementations. Do
not rename methods, change parameter orders, or alter return types without
updating ``tests/test_adapter_contracts.py`` and the traceability records; the
signature-freeze test exists to catch accidental drift.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping

from .schemas import (
    ConfirmationEvidence,
    ConfirmationMode,
    DeliveryState,
    InjectionResult,
    TargetContext,
    TargetToken,
    TaskToken,
)


class TaskTokenVerifier(ABC):
    """Contract: ``verify(token)`` returns the validated token or raises ``ValueError``.

    Implementations must be side-effect free and must not widen ``allowed_packages``.
    """

    @abstractmethod
    def verify(self, token: TaskToken) -> TaskToken:
        raise NotImplementedError


class StrictTaskTokenVerifier(TaskTokenVerifier):
    def verify(self, token: TaskToken) -> TaskToken:
        if not token.valid or not token.task_id or not token.allowed_packages:
            raise ValueError("invalid task token")
        return token


class TargetContextResolver(ABC):
    """Contract: ``resolve(token_id, now)`` returns a token bound to a live UI node.

    Must raise ``ValueError`` when the token is unknown or expired, and must not
    fabricate a target context.
    """

    @abstractmethod
    def resolve(self, token_id: str, now: float) -> TargetToken:
        raise NotImplementedError


class InMemoryTargetResolver(TargetContextResolver):
    def __init__(self, tokens: Mapping[str, TargetToken] | None = None) -> None:
        self._tokens: dict[str, TargetToken] = dict(tokens or {})

    def register(self, token: TargetToken) -> None:
        self._tokens[token.token_id] = token

    def resolve(self, token_id: str, now: float) -> TargetToken:
        token = self._tokens.get(token_id)
        if token is None or now >= token.expires_at:
            raise ValueError("target token unavailable")
        return token


class ConfirmationProvider(ABC):
    """Contract: ``obtain(...)`` returns evidence whose nonce equals the input nonce.

    Implementations must never approve through untrusted UI and must report the
    assurance level so callers can distinguish synthetic from protected confirmation.
    """

    @abstractmethod
    def obtain(
        self, mode: ConfirmationMode, handle_id: str, task_id: str, reservation_nonce: str
    ) -> ConfirmationEvidence:
        raise NotImplementedError


class DeterministicConfirmationProvider(ConfirmationProvider):
    def __init__(self, approved: bool = True, assurance: str = "synthetic") -> None:
        self.approved = approved
        self.assurance = assurance

    def obtain(
        self, mode: ConfirmationMode, handle_id: str, task_id: str, reservation_nonce: str
    ) -> ConfirmationEvidence:
        approved = True if mode is ConfirmationMode.NONE else self.approved
        return ConfirmationEvidence(approved, reservation_nonce, self.assurance)


class PrivateInjector(ABC):
    """Contract: ``inject(target, secret, nonce)`` delivers outside the agent/IME path.

    Must return ``DELIVERED``, ``NOT_DELIVERED``, or ``UNCERTAIN``; the resolver
    consumes the reservation conservatively unless non-delivery is proven.
    """

    @abstractmethod
    def inject(self, target: TargetContext, secret: bytes, reservation_nonce: str) -> InjectionResult:
        raise NotImplementedError


class InMemoryInjector(PrivateInjector):
    """Synthetic-only injector. Captured values are protected test-oracle state."""

    def __init__(self) -> None:
        self.deliveries: list = []

    def inject(self, target: TargetContext, secret: bytes, reservation_nonce: str) -> InjectionResult:
        self.deliveries.append((target, bytes(secret), reservation_nonce))
        return InjectionResult(state=DeliveryState.DELIVERED)


class AospAdapter(ABC):
    """Contract for the in-``system_server`` binder service, node tokens, private
    input, redaction hooks, and protected audit export.

    ``security_level()`` must report the actual Keystore security level and must
    not claim TEE/StrongBox backing that the environment does not provide.
    """

    @abstractmethod
    def security_level(self) -> str:
        raise NotImplementedError("requires a manually provisioned AOSP/device implementation")


class AgentRunnerAdapter(ABC):
    """Contract: ``run_task(task)`` drives an external agent under the observation
    interface and returns a schema-preserving record. Raw secrets must never be
    handed to the agent.
    """

    @abstractmethod
    def run_task(self, task: Mapping[str, object]) -> Mapping[str, object]:
        raise NotImplementedError("requires an external agent repository and model configuration")


class BenchmarkAdapter(ABC):
    """Contract: ``load_trials(root)`` yields schema-preserving trial mappings.

    Must not silently substitute, synthesize, or drop trials.
    """

    @abstractmethod
    def load_trials(self, root: str) -> Iterable[Mapping[str, object]]:
        raise NotImplementedError("requires manually provisioned benchmark files")


class PlatformFlowAdapter(ABC):
    """B2 contract for Autofill, OTP Autofill, or Credential Manager.

    ``enter(task)`` injects through the platform flow rather than the SecretHandle
    resolver and must preserve the platform's own user-visible behavior.
    """

    @abstractmethod
    def enter(self, task: Mapping[str, object]) -> Mapping[str, object]:
        raise NotImplementedError("requires Android platform APIs and a cooperating application")
