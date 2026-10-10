from secrethandle.schemas import LifecycleState


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
