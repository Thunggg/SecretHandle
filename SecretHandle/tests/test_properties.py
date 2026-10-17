"""Deterministic property-style tests for the reference model.

These exercise the algebraic and lifecycle properties the paper claims
(monotone policy intersection, no-resurrection after expiry, linearizable
single-use, and secret non-leakage through public representations) by
sampling many cases from a fixed seed instead of a property-based library,
keeping the harness dependency-free and reproducible.
"""

from __future__ import annotations

import random
from concurrent.futures import ThreadPoolExecutor

import pytest

from secrethandle.adapters import (
    DeterministicConfirmationProvider,
    InMemoryInjector,
    InMemoryTargetResolver,
)
from secrethandle.core import SecretHandleService
from secrethandle.policy import intersect, matches
from secrethandle.schemas import (
    ConfirmationMode,
    DestinationPolicy,
    PolicyHints,
    Provenance,
    SecretType,
    TargetContext,
    TaskToken,
)
from secrethandle.synthetic import SeededIdentifierSource, synthetic_key, target_tokens

_SEED = 20261017
_ITERATIONS = 2000

_SOURCES = ["a", "b", "c"]
_ORIGINS = ["https://a", "https://b"]
_FIELDS = ["otp", "user", "pass"]
_NODES = ["n1", "n2"]


def _maybe_values(rng, domain):
    choice = rng.choice(("wild", "empty", "some"))
    if choice == "wild":
        return None
    if choice == "empty":
        return frozenset()
    return frozenset(rng.sample(domain, rng.randint(1, len(domain))))


def _random_policy(rng):
    return DestinationPolicy(
        packages=_maybe_values(rng, _SOURCES),
        origins=_maybe_values(rng, _ORIGINS),
        fields=_maybe_values(rng, _FIELDS),
        nodes=_maybe_values(rng, _NODES),
        require_origin=rng.random() < 0.5,
        require_field=rng.random() < 0.5,
        require_node=rng.random() < 0.5,
    )


def _random_target(rng):
    def maybe(domain):
        return None if rng.random() < 0.25 else rng.choice(domain)

    return TargetContext(
        package=rng.choice(_SOURCES),
        origin=maybe(_ORIGINS),
        field_class=maybe(_FIELDS),
        node_id=maybe(_NODES),
        generation=rng.randint(0, 3),
        window_id="w",
    )


def test_intersection_never_broadens_authority():
    rng = random.Random(_SEED)
    for _ in range(_ITERATIONS):
        left, right, target = _random_policy(rng), _random_policy(rng), _random_target(rng)
        if matches(intersect(left, right), target):
            assert matches(left, target)
            assert matches(right, target)


def test_intersection_is_commutative_and_idempotent_on_targets():
    rng = random.Random(_SEED + 1)
    for _ in range(_ITERATIONS):
        left, right, target = _random_policy(rng), _random_policy(rng), _random_target(rng)
        assert matches(intersect(left, right), target) == matches(intersect(right, left), target)
        assert matches(intersect(left, left), target) == matches(left, target)


def _bundle(seed, now):
    service = SecretHandleService(
        synthetic_key(seed),
        identifier_source=SeededIdentifierSource(seed),
        clock=lambda: now,
    )
    good, _attacker, _stale = target_tokens()
    resolver = InMemoryTargetResolver({good.token_id: good})
    task = TaskToken("task-login", frozenset({"com.example.bank"}))
    handle = service.mint(
        b"123456",
        SecretType.OTP,
        Provenance("sms", "test-source"),
        task,
        DestinationPolicy(
            packages=frozenset({"com.example.bank"}),
            origins=frozenset({"https://bank.example"}),
            fields=frozenset({"otp"}),
            require_origin=True,
            require_field=True,
        ),
        PolicyHints(60.0, 1, ConfirmationMode.NONE),
        now=now,
    )
    return service, resolver, task, handle, good


def test_resolution_outcomes_are_monotone_and_expire_terminally():
    marks = [1000.0, 1030.0, 1059.0, 1060.0, 1061.0, 1100.0]
    outcomes = []
    for now in marks:
        service, resolver, task, handle, good = _bundle(7, now)
        outcomes.append(
            service.resolve(
                handle,
                task,
                good.token_id,
                resolver,
                DeterministicConfirmationProvider(),
                InMemoryInjector(),
                now,
            ).success
        )
    assert outcomes[0] is True
    assert outcomes == sorted(outcomes, reverse=True), outcomes


@pytest.mark.parametrize("seed", [1, 2, 3, 4, 5])
def test_single_use_is_linearizable_across_seeds(seed):
    service, resolver, task, handle, good = _bundle(seed, 1000.0)
    injector = InMemoryInjector()
    provider = DeterministicConfirmationProvider()

    def attempt(_):
        return service.resolve(handle, task, good.token_id, resolver, provider, injector, 1001.0).success

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(attempt, range(20)))
    assert sum(results) == 1
    assert len(injector.deliveries) == 1


def test_secret_absent_from_public_representations(service_bundle):
    service, resolver, task, handle, good, _attacker = service_bundle
    record = service.store.load(handle.identifier)
    assert record is not None
    service.resolve(
        handle,
        task,
        good.token_id,
        resolver,
        DeterministicConfirmationProvider(),
        InMemoryInjector(),
        1001.0,
    )
    secret = b"123456"
    blob = " ".join(
        [
            repr(handle),
            repr(record),
            repr(service.store),
            repr(service.audit_events),
            *(repr(event) for event in service.audit_events),
        ]
    )
    assert secret.decode() not in blob
    assert secret.hex() not in blob
