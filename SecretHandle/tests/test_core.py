from secrethandle.adapters import DeterministicConfirmationProvider, InMemoryInjector
from secrethandle.schemas import LifecycleState, OpaqueHandle, SecretType


def test_legitimate_resolve_consumes_and_never_returns_secret(service_bundle):
    service, resolver, task, handle, good, _ = service_bundle
    injector = InMemoryInjector()
    result = service.resolve(
        handle, task, good.token_id, resolver, DeterministicConfirmationProvider(), injector, 1001.0
    )
    assert result.success and result.status == "entered"
    assert not hasattr(result, "secret")
    assert injector.deliveries[0][1] == b"123456"
    assert service.store.load(handle.identifier).state is LifecycleState.CONSUMED


def test_wrong_destination_and_forgery_reject(service_bundle):
    service, resolver, task, handle, good, attacker = service_bundle
    injector = InMemoryInjector()
    denied = service.resolve(
        handle, task, attacker.token_id, resolver, DeterministicConfirmationProvider(), injector, 1001.0
    )
    assert not denied.success
    assert not injector.deliveries
    forged = OpaqueHandle(handle.identifier, SecretType.OTP, "00" * 32)
    assert not service.resolve(
        forged, task, good.token_id, resolver, DeterministicConfirmationProvider(), injector, 1001.0
    ).success


def test_replay_rejected(service_bundle):
    service, resolver, task, handle, good, _ = service_bundle
    injector = InMemoryInjector()
    provider = DeterministicConfirmationProvider()
    assert service.resolve(handle, task, good.token_id, resolver, provider, injector, 1001.0).success
    assert not service.resolve(handle, task, good.token_id, resolver, provider, injector, 1002.0).success
    assert len(injector.deliveries) == 1


def test_expired_handle_has_value_oblivious_unavailable_status(service_bundle):
    service, resolver, task, handle, good, _ = service_bundle
    result = service.resolve(
        handle, task, good.token_id, resolver, DeterministicConfirmationProvider(),
        InMemoryInjector(), 1060.0,
    )
    assert not result.success and result.status == "unavailable handle"
