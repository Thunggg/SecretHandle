import pytest

from secrethandle.schemas import DestinationPolicy, PolicyHints, SecretType, TrialOutcome


def test_trial_output_never_has_secret_field():
    assert "secret" not in TrialOutcome.__dataclass_fields__


def test_policy_hints_are_typed_objects():
    hints = PolicyHints(30.0, 1)
    assert hints.ttl_seconds == 30.0 and hints.use_budget == 1


def test_secret_type_rejects_unknown_values():
    with pytest.raises(ValueError):
        SecretType("unknown")
