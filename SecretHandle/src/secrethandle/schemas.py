"""Typed objects corresponding to Sections 4-9 and Appendix A of the paper."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SecretType(str, Enum):
    OTP = "otp"
    CREDENTIAL = "credential"
    IDENTIFIER = "identifier"
    CLIPBOARD = "clipboard"
    PAYMENT = "payment"


class LifecycleState(str, Enum):
    LIVE = "live"
    RESERVED = "reserved"
    CONSUMED = "consumed"
    EXPIRED = "expired"
    REVOKED = "revoked"


class ConfirmationMode(str, Enum):
    NONE = "none"
    USER = "user"
    PROTECTED = "protected"


class DeliveryState(str, Enum):
    DELIVERED = "delivered"
    NOT_DELIVERED = "not_delivered"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class Provenance:
    source_class: str
    source_id: str


@dataclass(frozen=True)
class TaskToken:
    task_id: str
    allowed_packages: frozenset[str]
    valid: bool = True


@dataclass(frozen=True)
class DestinationPolicy:
    """Finite typed policy for Equation (7).

    ``None`` means an explicit wildcard. An empty set means no destination is allowed.
    Required flags make missing target attributes fail closed even when a policy set exists.
    """

    packages: frozenset[str] | None = None
    origins: frozenset[str] | None = None
    fields: frozenset[str] | None = None
    nodes: frozenset[str] | None = None
    require_origin: bool = False
    require_field: bool = False
    require_node: bool = False


@dataclass(frozen=True)
class PolicyHints:
    ttl_seconds: float
    use_budget: int
    confirmation: ConfirmationMode = ConfirmationMode.NONE


@dataclass(frozen=True)
class TargetContext:
    package: str
    origin: str | None
    field_class: str | None
    node_id: str | None
    generation: int
    window_id: str


@dataclass(frozen=True)
class TargetToken:
    token_id: str
    context: TargetContext
    expires_at: float


@dataclass(frozen=True)
class HandleMetadata:
    identifier: str
    secret_type: SecretType
    provenance: Provenance
    destination: DestinationPolicy
    task_id: str
    issued_at: float
    expires_at: float
    use_budget: int
    confirmation: ConfirmationMode
    schema_version: int = 1


@dataclass(frozen=True)
class OpaqueHandle:
    identifier: str
    secret_type: SecretType
    authenticator_hex: str


@dataclass
class SecretRecord:
    """Equation (1). The secret field must never enter public serialization.

    ``metadata`` (the authenticated ``H``) stays immutable so the authenticator
    ``a=F_K(enc(H))`` remains valid for the whole lifetime; the mutable use
    budget is tracked separately in ``remaining_uses`` and decremented at the
    reservation step (decision D4), never inside ``H``.
    """

    secret: bytes = field(repr=False)
    metadata: HandleMetadata
    authenticator: bytes = field(repr=False)
    remaining_uses: int
    state: LifecycleState = LifecycleState.LIVE
    reservation_nonce: str | None = None
    version: int = 0


@dataclass(frozen=True)
class ConfirmationEvidence:
    approved: bool
    reservation_nonce: str
    assurance: str = "synthetic"


@dataclass(frozen=True)
class InjectionResult:
    state: DeliveryState
    detail: str = ""


@dataclass(frozen=True)
class ResolveResult:
    success: bool
    status: str
    handle_id: str
    target_package: str | None = None


@dataclass(frozen=True)
class RedactionObligation:
    target_token_id: str
    handle_id: str
    secret_type: SecretType
    created_at: float
    mask: str
    active: bool = True


@dataclass(frozen=True)
class ObservationItem:
    channel: str
    text: str
    target_token_id: str | None = None
    stable_identity: bool = True
    window_id: str | None = None


@dataclass(frozen=True)
class Observation:
    items: tuple[ObservationItem, ...]
    frame_suppressed: bool = False


@dataclass(frozen=True)
class AuditEvent:
    event: str
    pseudonymous_handle_id: str
    secret_type: str
    source_class: str
    destination_class: str
    decision: str
    latency_bucket_ms: int | None
    policy_version: int = 1


@dataclass(frozen=True)
class Artifact:
    channel: str
    content: str


@dataclass(frozen=True)
class TrialOutcome:
    trial_id: str
    condition: str
    attack: str
    applicable: bool
    exposure: bool | None
    redirection_success: bool | None
    utility_success: bool | None
    post_entry_leakage: bool | None
    forgery_acceptance: bool | None
    replay_acceptance: bool | None
    latency_ms: float | None
    policy_rejected: bool | None = None
    false_rejection: bool | None = None
    identity_available: bool | None = None
    confirmations: int = 0
    synthetic: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = dict(self.__dict__)
        data["metadata"] = dict(self.metadata)
        return data


@dataclass(frozen=True)
class MetricEstimate:
    name: str
    numerator: int
    denominator: int
    value: float | None
    ci_low: float | None
    ci_high: float | None


@dataclass(frozen=True)
class ExperimentSummary:
    label: str
    metrics: tuple[MetricEstimate, ...]
    latency: Mapping[str, float | None]
    exclusions: Mapping[str, int]
    provenance: Mapping[str, Any]
