from secrethandle.adapters import DeterministicConfirmationProvider, InMemoryInjector
from secrethandle.schemas import (
    ConfirmationMode,
    DestinationPolicy,
    LifecycleState,
    PolicyHints,
    Provenance,
    SecretType,
)


def test_expiry_is_monotonic(service_bundle):
    service, _, _, handle, _, _ = service_bundle
    assert service.store.expire(1060.0) == 1
    assert service.store.load(handle.identifier).state is LifecycleState.EXPIRED
    assert service.store.expire(900.0) == 0
    assert service.store.load(handle.identifier).state is LifecycleState.EXPIRED


def test_reserved_recovery_consumes(service_bundle):
    service, _, _, handle, _, _ = service_bundle
    assert service.store.reserve(handle.identifier, "r", 1001.0) is not None
    assert service.store.recover_reserved() == 1
    assert service.store.load(handle.identifier).state is LifecycleState.CONSUMED


def test_budget_is_decremented_at_reservation_and_refunded_on_rollback(service_bundle):
    service, _, _, handle, _, _ = service_bundle
    assert service.store.load(handle.identifier).remaining_uses == 1
    reserved = service.store.reserve(handle.identifier, "r", 1001.0)
    assert reserved is not None and reserved.remaining_uses == 0
    assert service.store.load(handle.identifier).metadata.use_budget == 1  # H is immutable
    refunded = service.store.rollback(handle.identifier, "r", delivery_impossible=True)
    assert refunded.state is LifecycleState.LIVE and refunded.remaining_uses == 1


def test_multi_use_handle_resolves_twice_with_valid_metadata(service_bundle):
    service, resolver, task, handle, good, _ = service_bundle
    assert service.store.load(handle.identifier).metadata.use_budget == 1
    multi = service.mint(
        b"id-42",
        SecretType.IDENTIFIER,
        Provenance("sms", "test-source"),
        task,
        DestinationPolicy(
            packages=frozenset({"com.example.bank"}),
            origins=frozenset({"https://bank.example"}),
            fields=frozenset({"otp"}),
            require_origin=True,
            require_field=True,
        ),
        PolicyHints(60.0, 2, ConfirmationMode.NONE),
        now=1000.0,
    )
    injector = InMemoryInjector()
    provider = DeterministicConfirmationProvider()
    first = service.resolve(multi, task, good.token_id, resolver, provider, injector, 1001.0)
    second = service.resolve(multi, task, good.token_id, resolver, provider, injector, 1002.0)
    assert first.success and second.success
    assert len(injector.deliveries) == 2
    assert service.store.load(multi.identifier).state is LifecycleState.CONSUMED
    assert service.store.load(multi.identifier).metadata.use_budget == 2  # H unchanged


