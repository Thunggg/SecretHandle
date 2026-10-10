import pytest

from secrethandle.adapters import AospAdapter, BenchmarkAdapter, PlatformFlowAdapter


def test_external_adapters_are_abstract_not_fake_implementations():
    with pytest.raises(TypeError):
        AospAdapter()
    with pytest.raises(TypeError):
        BenchmarkAdapter()
    with pytest.raises(TypeError):
        PlatformFlowAdapter()
