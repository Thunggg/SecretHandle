from secrethandle.crypto import authenticate, canonical_encode, forgery_bound, verify
from secrethandle.schemas import (
    ConfirmationMode,
    DestinationPolicy,
    HandleMetadata,
    Provenance,
    SecretType,
)


def metadata():
    return HandleMetadata(
        "01", SecretType.OTP, Provenance("sms", "source"),
        DestinationPolicy(packages=frozenset({"b", "a"})), "task", 1.0, 2.0, 1,
        ConfirmationMode.NONE,
    )


def test_canonical_encoding_and_authentication():
    key = b"k" * 32
    first = canonical_encode(metadata())
    second = canonical_encode(metadata())
    assert first == second
    tag = authenticate(key, metadata())
    assert verify(key, metadata(), tag)
    assert not verify(b"x" * 32, metadata(), tag)


def test_forgery_bound_equation_6():
    value = forgery_bound(0.0, 4, 128)
    assert value == 4 / 2**128
