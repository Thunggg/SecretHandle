from dataclasses import replace

from secrethandle.policy import intersect, is_empty, is_safe_attenuation, matches
from secrethandle.schemas import (
    ConfirmationMode,
    DestinationPolicy,
    HandleMetadata,
    Provenance,
    SecretType,
    TargetContext,
)


def target(package="pkg", origin="https://a", field="otp", node="n"):
    return TargetContext(package, origin, field, node, 1, "w")


def test_match_is_conjunctive_and_missing_required_identity_fails():
    policy = DestinationPolicy(
        packages=frozenset({"pkg"}), origins=frozenset({"https://a"}),
        fields=frozenset({"otp"}), require_origin=True, require_field=True,
    )
    assert matches(policy, target())
    assert not matches(policy, target(package="other"))
    assert not matches(policy, target(origin=None))


def test_intersection_only_narrows():
    broad = DestinationPolicy(packages=frozenset({"a", "b"}), fields=None)
    narrow = DestinationPolicy(packages=frozenset({"b"}), fields=frozenset({"otp"}))
    result = intersect(broad, narrow)
    assert result.packages == frozenset({"b"})
    assert result.fields == frozenset({"otp"})
    assert not is_empty(result)


def test_safe_attenuation():
    original = HandleMetadata(
        "n", SecretType.OTP, Provenance("sms", "s"),
        DestinationPolicy(packages=frozenset({"a", "b"})), "t", 0, 100, 2,
        ConfirmationMode.NONE,
    )
    candidate = replace(
        original,
        destination=DestinationPolicy(packages=frozenset({"a"})),
        expires_at=90,
        use_budget=1,
        confirmation=ConfirmationMode.USER,
    )
    assert is_safe_attenuation(original, candidate)
    assert not is_safe_attenuation(candidate, original)
