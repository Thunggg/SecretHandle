from concurrent.futures import ThreadPoolExecutor

from secrethandle.adapters import DeterministicConfirmationProvider, InMemoryInjector


def test_single_use_linearizable_under_concurrency(service_bundle):
    service, resolver, task, handle, good, _ = service_bundle
    injector = InMemoryInjector()
    provider = DeterministicConfirmationProvider()

    def attempt(_):
        return service.resolve(handle, task, good.token_id, resolver, provider, injector, 1001.0).success

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(attempt, range(20)))
    assert sum(results) == 1
    assert len(injector.deliveries) == 1
