"""Canonical metadata authentication and Equation (6) utilities."""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Dict, Optional

from .schemas import DestinationPolicy, HandleMetadata


def _sorted(values: Optional[frozenset]) -> Optional[list]:
    return None if values is None else sorted(values)


def metadata_dict(metadata: HandleMetadata) -> Dict[str, Any]:
    destination: DestinationPolicy = metadata.destination
    return {
        "confirmation": metadata.confirmation.value,
        "destination": {
            "fields": _sorted(destination.fields),
            "nodes": _sorted(destination.nodes),
            "origins": _sorted(destination.origins),
            "packages": _sorted(destination.packages),
            "require_field": destination.require_field,
            "require_node": destination.require_node,
            "require_origin": destination.require_origin,
        },
        "expires_at": metadata.expires_at,
        "identifier": metadata.identifier,
        "issued_at": metadata.issued_at,
        "provenance": {
            "source_class": metadata.provenance.source_class,
            "source_id": metadata.provenance.source_id,
        },
        "schema_version": metadata.schema_version,
        "secret_type": metadata.secret_type.value,
        "task_id": metadata.task_id,
        "use_budget": metadata.use_budget,
    }


def canonical_encode(metadata: HandleMetadata) -> bytes:
    """Canonical injective encoding assumed by Assumption 3 and Algorithm 1 line 7."""

    return json.dumps(
        metadata_dict(metadata), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def authenticate(key: bytes, metadata: HandleMetadata) -> bytes:
    if len(key) < 16:
        raise ValueError("authentication key must contain at least 128 bits")
    return hmac.new(key, canonical_encode(metadata), hashlib.sha256).digest()


def verify(key: bytes, metadata: HandleMetadata, tag: bytes) -> bool:
    return hmac.compare_digest(authenticate(key, metadata), tag)


def forgery_bound(euf_advantage: float, attempts: int, lambda_bits: int) -> float:
    """Numerically evaluate the upper bound in Equation (6)."""

    if not 0.0 <= euf_advantage <= 1.0:
        raise ValueError("EUF advantage must be in [0, 1]")
    if attempts < 0 or lambda_bits <= 0:
        raise ValueError("attempts must be nonnegative and lambda_bits positive")
    return min(1.0, euf_advantage + attempts / float(2**lambda_bits))
