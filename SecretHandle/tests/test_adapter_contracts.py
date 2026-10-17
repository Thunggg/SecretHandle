"""Adapter contract v1 freeze.

These tests lock the public surface of every adapter ABC and verify that the
in-repo reference implementations satisfy the contract. Renaming a method,
reordering parameters, or changing a default makes the corresponding test fail,
forcing a deliberate, documented contract revision.
"""

from __future__ import annotations

import inspect

import pytest

from secrethandle import adapters

# class -> {method: [ordered parameter names]}
FROZEN_CONTRACT: dict[str, dict[str, list[str]]] = {
    "TaskTokenVerifier": {"verify": ["self", "token"]},
    "TargetContextResolver": {"resolve": ["self", "token_id", "now"]},
    "ConfirmationProvider": {
        "obtain": ["self", "mode", "handle_id", "task_id", "reservation_nonce"]
    },
    "PrivateInjector": {"inject": ["self", "target", "secret", "reservation_nonce"]},
    "AospAdapter": {"security_level": ["self"]},
    "AgentRunnerAdapter": {"run_task": ["self", "task"]},
    "BenchmarkAdapter": {"load_trials": ["self", "root"]},
    "PlatformFlowAdapter": {"enter": ["self", "task"]},
}

# ABC -> in-repo reference implementations that must satisfy it.
REFERENCE_IMPLEMENTATIONS: dict[str, list[str]] = {
    "TaskTokenVerifier": ["StrictTaskTokenVerifier"],
    "TargetContextResolver": ["InMemoryTargetResolver"],
    "ConfirmationProvider": ["DeterministicConfirmationProvider"],
    "PrivateInjector": ["InMemoryInjector"],
}


@pytest.mark.parametrize("class_name", sorted(FROZEN_CONTRACT))
def test_abstract_surface_is_frozen(class_name):
    cls = getattr(adapters, class_name)
    expected = FROZEN_CONTRACT[class_name]
    assert set(cls.__abstractmethods__) == set(expected)
    for method_name, params in expected.items():
        signature = inspect.signature(getattr(cls, method_name))
        assert list(signature.parameters) == params


@pytest.mark.parametrize("class_name", sorted(REFERENCE_IMPLEMENTATIONS))
def test_reference_implementations_satisfy_contract(class_name):
    cls = getattr(adapters, class_name)
    for impl_name in REFERENCE_IMPLEMENTATIONS[class_name]:
        impl = getattr(adapters, impl_name)
        assert issubclass(impl, cls)
        assert impl.__abstractmethods__ == frozenset()
        for method_name in FROZEN_CONTRACT[class_name]:
            assert callable(getattr(impl, method_name))


def test_external_adapters_remain_abstract():
    for class_name in ("AospAdapter", "AgentRunnerAdapter", "BenchmarkAdapter", "PlatformFlowAdapter"):
        cls = getattr(adapters, class_name)
        assert cls.__abstractmethods__, class_name
