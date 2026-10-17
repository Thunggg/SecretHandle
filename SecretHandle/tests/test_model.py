"""Model-based tests: crash/concurrency schedules at the reserve/commit boundaries.

These explore schedules the paper argues about (crash between reserve and
commit, rollback of an undelivered reservation, terminal single-use) and assert
the core invariants: a single-use record is never committed twice, and a
reservation whose delivery is uncertain is consumed conservatively.
"""

from __future__ import annotations

import random

import pytest

from secrethandle.schemas import (
    ConfirmationMode,
    DestinationPolicy,
    HandleMetadata,
    LifecycleState,
    Provenance,
    SecretRecord,
    SecretType,
)
from secrethandle.store import SecretStore, StoreError

_SEED = 20261017
_IDENTIFIER = "h1"
_NONCE = "n1"


def _record(use_budget: int = 1, expires_at: float = 1060.0) -> SecretRecord:
    metadata = HandleMetadata(
        identifier=_IDENTIFIER,
        secret_type=SecretType.OTP,
        provenance=Provenance("sms", "test-source"),
        destination=DestinationPolicy(packages=frozenset({"com.example.bank"})),
        task_id="task",
        issued_at=1000.0,
        expires_at=expires_at,
        use_budget=use_budget,
        confirmation=ConfirmationMode.NONE,
    )
    return SecretRecord(b"123456", metadata, b"tag", use_budget)


def test_crash_between_reserve_and_commit_consumes_single_use():
    store = SecretStore()
    store.insert(_record())
    assert store.reserve(_IDENTIFIER, _NONCE, 1001.0) is not None
    assert store.recover_reserved() == 1  # crash / restart
    assert store.load(_IDENTIFIER).state is LifecycleState.CONSUMED
    assert store.reserve(_IDENTIFIER, _NONCE + "-again", 1001.0) is None


def test_uncertain_commit_is_terminal():
    store = SecretStore()
    store.insert(_record())
    store.reserve(_IDENTIFIER, _NONCE, 1001.0)
    record = store.commit(_IDENTIFIER, _NONCE, uncertain=True)
    assert record.state is LifecycleState.CONSUMED
    assert store.reserve(_IDENTIFIER, _NONCE + "-again", 1001.0) is None


def test_rollback_requires_proof_delivery_was_impossible():
    store = SecretStore()
    store.insert(_record())
    store.reserve(_IDENTIFIER, _NONCE, 1001.0)
    with pytest.raises(StoreError):
        store.rollback(_IDENTIFIER, _NONCE, delivery_impossible=False)
    store.rollback(_IDENTIFIER, _NONCE, delivery_impossible=True)
    assert store.load(_IDENTIFIER).state is LifecycleState.LIVE
    assert store.reserve(_IDENTIFIER, _NONCE + "-retry", 1001.0) is not None


def test_commit_after_rollback_is_rejected():
    store = SecretStore()
    store.insert(_record())
    store.reserve(_IDENTIFIER, _NONCE, 1001.0)
    store.rollback(_IDENTIFIER, _NONCE, delivery_impossible=True)
    with pytest.raises(StoreError):
        store.commit(_IDENTIFIER, _NONCE)


def test_random_schedules_never_exceed_use_budget():
    rng = random.Random(_SEED)
    for _ in range(300):
        store = SecretStore()
        store.insert(_record())
        delivered = 0
        reserved = False
        nonce = None
        ops = rng.choices(
            ["reserve", "commit", "rollback", "recover", "expire", "revoke"],
            k=rng.randint(2, 10),
        )
        for op in ops:
            try:
                if op == "reserve" and not reserved:
                    reserved = store.reserve(_IDENTIFIER, _NONCE, 1001.0) is not None
                    nonce = _NONCE if reserved else None
                elif op == "commit" and reserved and nonce is not None:
                    store.commit(_IDENTIFIER, nonce, uncertain=rng.random() < 0.5)
                    delivered += 1
                    reserved = False
                elif op == "rollback" and reserved and nonce is not None:
                    store.rollback(_IDENTIFIER, nonce, delivery_impossible=True)
                    reserved = False
                elif op == "recover":
                    store.recover_reserved()
                    reserved = False
                elif op == "expire":
                    store.expire(2000.0)
                    reserved = False
                elif op == "revoke":
                    store.revoke(_IDENTIFIER)
                    reserved = False
            except StoreError:
                pass
        assert delivered <= 1, (delivered, ops)
