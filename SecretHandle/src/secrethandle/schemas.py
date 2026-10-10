"""Typed objects corresponding to Sections 4-9 and Appendix A of the paper."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Mapping, Optional, Tuple


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
    allowed_packages: FrozenSet[str]
    valid: bool = True


@dataclass(frozen=True)
class DestinationPolicy:
    """Finite typed policy for Equation (7).

    ``None`` means an explicit wildcard. An empty set means no destination is allowed.
    Required flags make missing target attributes fail closed even when a policy set exists.
    """

    packages: Optional[FrozenSet[str]] = None
    origins: Optional[FrozenSet[str]] = None
    fields: Optional[FrozenSet[str]] = None
    nodes: Optional[FrozenSet[str]] = None
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
    origin: Optional[str]
    field_class: Optional[str]
    node_id: Optional[str]
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
    """Equation (1). The secret field must never enter public serialization."""

    secret: bytes = field(repr=False)
    metadata: HandleMetadata
    authenticator: bytes = field(repr=False)
    state: LifecycleState = LifecycleState.LIVE
    reservation_nonce: Optional[str] = None
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
    target_package: Optional[str] = None


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
    target_token_id: Optional[str] = None
    stable_identity: bool = True
    window_id: Optional[str] = None


@dataclass(frozen=True)
class Observation:
    items: Tuple[ObservationItem, ...]
    frame_suppressed: bool = False


@dataclass(frozen=True)
class AuditEvent:
    event: str
    pseudonymous_handle_id: str
    secret_type: str
    source_class: str
    destination_class: str
    decision: str
    latency_bucket_ms: Optional[int]
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
    exposure: Optional[bool]
    redirection_success: Optional[bool]
    utility_success: Optional[bool]
    post_entry_leakage: Optional[bool]
    forgery_acceptance: Optional[bool]
    replay_acceptance: Optional[bool]
    latency_ms: Optional[float]
    policy_rejected: Optional[bool] = None
    false_rejection: Optional[bool] = None
    identity_available: Optional[bool] = None
    confirmations: int = 0
    synthetic: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = dict(self.__dict__)
        data["metadata"] = dict(self.metadata)
        return data


@dataclass(frozen=True)
class MetricEstimate:
    name: str
    numerator: int
    denominator: int
    value: Optional[float]
    ci_low: Optional[float]
    ci_high: Optional[float]


@dataclass(frozen=True)
class ExperimentSummary:
    label: str
    metrics: Tuple[MetricEstimate, ...]
    latency: Mapping[str, Optional[float]]
    exclusions: Mapping[str, int]
    provenance: Mapping[str, Any]
