"""Interfaces for trusted platform functions and external experiment dependencies."""

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
    @abstractmethod
    def verify(self, token: TaskToken) -> TaskToken:
        raise NotImplementedError


class StrictTaskTokenVerifier(TaskTokenVerifier):
    def verify(self, token: TaskToken) -> TaskToken:
        if not token.valid or not token.task_id or not token.allowed_packages:
            raise ValueError("invalid task token")
        return token


class TargetContextResolver(ABC):
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
    """Stub contract for binder service, node tokens, private input, and redaction hooks."""

    @abstractmethod
    def security_level(self) -> str:
        raise NotImplementedError("requires a manually provisioned AOSP/device implementation")


class AgentRunnerAdapter(ABC):
    @abstractmethod
    def run_task(self, task: Mapping[str, object]) -> Mapping[str, object]:
        raise NotImplementedError("requires an external agent repository and model configuration")


class BenchmarkAdapter(ABC):
    @abstractmethod
    def load_trials(self, root: str) -> Iterable[Mapping[str, object]]:
        raise NotImplementedError("requires manually provisioned benchmark files")


class PlatformFlowAdapter(ABC):
    """B2 contract for Autofill, OTP Autofill, or Credential Manager."""

    @abstractmethod
    def enter(self, task: Mapping[str, object]) -> Mapping[str, object]:
        raise NotImplementedError("requires Android platform APIs and a cooperating application")
