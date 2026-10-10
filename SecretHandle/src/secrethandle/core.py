"""SecretHandle Mint and ENTER/Resolve reference algorithms."""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from typing import Callable, FrozenSet, Iterable, Optional, Tuple

from .adapters import (
    ConfirmationProvider,
    PrivateInjector,
    StrictTaskTokenVerifier,
    TargetContextResolver,
    TaskTokenVerifier,
)
from .crypto import authenticate, verify
from .policy import intersect, is_empty, matches
from .redaction import ObservationRedactor
from .schemas import (
    AuditEvent,
    ConfirmationMode,
    DeliveryState,
    DestinationPolicy,
    HandleMetadata,
    LifecycleState,
    OpaqueHandle,
    PolicyHints,
    Provenance,
    ResolveResult,
    SecretRecord,
    SecretType,
    TaskToken,
)
from .store import SecretStore, StoreError


class MintRejected(ValueError):
    pass


class RandomIdentifierSource:
    def __init__(self, lambda_bits: int = 128) -> None:
        if lambda_bits < 96 or lambda_bits % 8:
            raise ValueError("lambda_bits must be at least 96 and byte aligned")
        self.lambda_bits = lambda_bits

    def __call__(self) -> str:
        return secrets.token_hex(self.lambda_bits // 8)


class SecretHandleService:
    """Runnable reference model of Algorithms 1 and 2.

    The service never returns the secret through its public API. Target resolution,
    confirmation, and injection are injected trusted adapters so Android-specific hooks
    cannot be confused with this Python model.
    """

    def __init__(
        self,
        key: bytes,
        store: Optional[SecretStore] = None,
        redactor: Optional[ObservationRedactor] = None,
        task_verifier: Optional[TaskTokenVerifier] = None,
        approved_sources: Optional[Iterable[str]] = None,
        identifier_source: Optional[Callable[[], str]] = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if len(key) < 16:
            raise ValueError("key must contain at least 128 bits")
        self._key = bytes(key)
        self.store = store or SecretStore()
        self.redactor = redactor or ObservationRedactor()
        self.task_verifier = task_verifier or StrictTaskTokenVerifier()
        self.approved_sources = frozenset(approved_sources or {"sms", "credential", "clipboard", "wallet"})
        self.identifier_source = identifier_source or RandomIdentifierSource()
        self.clock = clock
        self.audit_events = []

    def mint(
        self,
        secret: bytes,
        secret_type: SecretType,
        provenance: Provenance,
        task_token: TaskToken,
        source_policy: DestinationPolicy,
        policy_hints: PolicyHints,
        now: Optional[float] = None,
    ) -> OpaqueHandle:
        """Implement Algorithm 1 and Equation (2)."""

        if not secret:
            raise MintRejected("protected value must not be empty")
        if provenance.source_class not in self.approved_sources:
            raise MintRejected("source adapter is not approved")
        task = self.task_verifier.verify(task_token)
        if policy_hints.ttl_seconds <= 0 or policy_hints.use_budget <= 0:
            raise MintRejected("lifecycle TTL and use budget must be positive")
        task_policy = DestinationPolicy(packages=task.allowed_packages)
        type_policy = self._type_policy(secret_type, policy_hints.confirmation)
        destination = intersect(intersect(task_policy, source_policy), type_policy)
        if is_empty(destination):
            raise MintRejected("destination intersection is empty")
        issued_at = self.clock() if now is None else now
        identifier = self.identifier_source()
        metadata = HandleMetadata(
            identifier=identifier,
            secret_type=secret_type,
            provenance=provenance,
            destination=destination,
            task_id=task.task_id,
            issued_at=issued_at,
            expires_at=issued_at + policy_hints.ttl_seconds,
            use_budget=policy_hints.use_budget,
            confirmation=self._required_confirmation(secret_type, policy_hints.confirmation),
        )
        tag = authenticate(self._key, metadata)
        self.store.insert(SecretRecord(bytes(secret), metadata, tag))
        self._audit(metadata, "mint", "accepted", None)
        return OpaqueHandle(identifier, secret_type, tag.hex())

    def resolve(
        self,
        handle: OpaqueHandle,
        task_token: TaskToken,
        target_token_id: str,
        target_resolver: TargetContextResolver,
        confirmation_provider: ConfirmationProvider,
        injector: PrivateInjector,
        now: Optional[float] = None,
    ) -> ResolveResult:
        """Implement Algorithm 2 and Equation (3) with conservative failure handling."""

        started = self.clock()
        current = self.clock() if now is None else now
        try:
            task = self.task_verifier.verify(task_token)
        except ValueError:
            return self._reject(handle.identifier, "invalid task", None)
        record = self.store.load(handle.identifier)
        if record is None:
            return self._reject(handle.identifier, "unavailable handle", None)
        try:
            presented_tag = bytes.fromhex(handle.authenticator_hex)
        except ValueError:
            return self._reject(handle.identifier, "unavailable handle", record)
        if (
            handle.secret_type is not record.metadata.secret_type
            or not hmac.compare_digest(presented_tag, record.authenticator)
            or not verify(self._key, record.metadata, presented_tag)
        ):
            return self._reject(handle.identifier, "unavailable handle", record)
        if (
            record.state is not LifecycleState.LIVE
            or current < record.metadata.issued_at
            or current >= record.metadata.expires_at
            or record.metadata.use_budget <= 0
        ):
            self.store.expire(current)
            return self._reject(handle.identifier, "unavailable handle", record)
        try:
            first = target_resolver.resolve(target_token_id, current)
        except ValueError:
            return self._reject(handle.identifier, "target changed", record)
        if not self._precheck(record, task, first.context, current):
            return self._reject(handle.identifier, "destination denied", record)
        reservation = self.identifier_source()
        reserved = self.store.reserve(handle.identifier, reservation, current)
        if reserved is None:
            return self._reject(handle.identifier, "unavailable handle", record)
        evidence = confirmation_provider.obtain(
            reserved.metadata.confirmation,
            handle.identifier,
            reserved.metadata.task_id,
            reservation,
        )
        if not evidence.approved or evidence.reservation_nonce != reservation:
            self._finalize_pre_delivery(handle.identifier, reservation, reserved.metadata.secret_type)
            return self._reject(handle.identifier, "confirmation not granted", reserved)
        try:
            second = target_resolver.resolve(target_token_id, current)
        except ValueError:
            self._finalize_pre_delivery(handle.identifier, reservation, reserved.metadata.secret_type)
            return self._reject(handle.identifier, "target changed", reserved)
        if second.context != first.context or not matches(reserved.metadata.destination, second.context):
            self._finalize_pre_delivery(handle.identifier, reservation, reserved.metadata.secret_type)
            return self._reject(handle.identifier, "destination denied", reserved)
        self.redactor.register(target_token_id, handle.identifier, reserved.metadata.secret_type, current)
        injection = injector.inject(second.context, reserved.secret, reservation)
        if injection.state is DeliveryState.DELIVERED:
            self.store.commit(handle.identifier, reservation, uncertain=False)
            status, success = "entered", True
        elif injection.state is DeliveryState.NOT_DELIVERED:
            self.store.rollback(handle.identifier, reservation, delivery_impossible=True)
            status, success = "entry failed", False
        else:
            self.store.commit(handle.identifier, reservation, uncertain=True)
            status, success = "entry unavailable", False
        elapsed_ms = (self.clock() - started) * 1000.0
        self._audit(reserved.metadata, "resolve", status, elapsed_ms)
        return ResolveResult(success, status, handle.identifier, second.context.package)

    def revoke(self, handle_id: str) -> bool:
        return self.store.revoke(handle_id)

    def _precheck(self, record: SecretRecord, task: TaskToken, target, now: float) -> bool:
        """Definition 2 before the post-reservation confirmation phase."""

        metadata = record.metadata
        return (
            record.state is LifecycleState.LIVE
            and metadata.issued_at <= now < metadata.expires_at
            and metadata.use_budget > 0
            and task.task_id == metadata.task_id
            and matches(metadata.destination, target)
        )

    def _finalize_pre_delivery(self, identifier: str, nonce: str, secret_type: SecretType) -> None:
        # OTP/payment reservations are consumed conservatively; identifiers may be retried.
        if secret_type in {SecretType.OTP, SecretType.PAYMENT, SecretType.CREDENTIAL}:
            self.store.commit(identifier, nonce, uncertain=True)
        else:
            self.store.rollback(identifier, nonce, delivery_impossible=True)

    @staticmethod
    def _required_confirmation(
        secret_type: SecretType, requested: ConfirmationMode
    ) -> ConfirmationMode:
        if secret_type is SecretType.PAYMENT and requested is ConfirmationMode.NONE:
            return ConfirmationMode.PROTECTED
        return requested

    @staticmethod
    def _type_policy(secret_type: SecretType, confirmation: ConfirmationMode) -> DestinationPolicy:
        if secret_type is SecretType.OTP:
            return DestinationPolicy(fields=frozenset({"otp"}), require_field=True)
        if secret_type is SecretType.PAYMENT:
            return DestinationPolicy(fields=frozenset({"payment"}), require_field=True)
        if secret_type is SecretType.CREDENTIAL:
            return DestinationPolicy(require_origin=False, require_field=True)
        return DestinationPolicy(require_field=True)

    def _reject(
        self, handle_id: str, status: str, record: Optional[SecretRecord]
    ) -> ResolveResult:
        if record is not None:
            self._audit(record.metadata, "resolve", status, None)
        return ResolveResult(False, status, handle_id)

    def _audit(
        self, metadata: HandleMetadata, event: str, decision: str, latency_ms: Optional[float]
    ) -> None:
        pseudonym = hmac.new(self._key, metadata.identifier.encode(), hashlib.sha256).hexdigest()[:16]
        bucket = None if latency_ms is None else int(round(latency_ms / 5.0) * 5)
        packages = metadata.destination.packages
        destination_class = "wildcard" if packages is None else f"{len(packages)}-package"
        self.audit_events.append(
            AuditEvent(
                event=event,
                pseudonymous_handle_id=pseudonym,
                secret_type=metadata.secret_type.value,
                source_class=metadata.provenance.source_class,
                destination_class=destination_class,
                decision=decision,
                latency_bucket_ms=bucket,
            )
        )
