from __future__ import annotations

import pytest

from secrethandle.adapters import InMemoryTargetResolver
from secrethandle.core import SecretHandleService
from secrethandle.schemas import (
    ConfirmationMode,
    DestinationPolicy,
    PolicyHints,
    Provenance,
    SecretType,
    TaskToken,
)
from secrethandle.synthetic import SeededIdentifierSource, synthetic_key, target_tokens


@pytest.fixture
def service_bundle():
    service = SecretHandleService(
        synthetic_key(1), identifier_source=SeededIdentifierSource(1), clock=lambda: 1000.0
    )
    good, attacker, stale = target_tokens()
    resolver = InMemoryTargetResolver({t.token_id: t for t in (good, attacker, stale)})
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
        now=1000.0,
    )
    return service, resolver, task, handle, good, attacker
