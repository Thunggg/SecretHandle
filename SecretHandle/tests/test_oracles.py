from secrethandle.oracles import DisclosureOracle
from secrethandle.schemas import Artifact


def test_disclosure_oracle_detects_exact_and_encoded():
    oracle = DisclosureOracle()
    exact = oracle.scan("123456", [Artifact("prompt", "OTP 123456")])
    assert exact.exposed and "prompt" in exact.channels
    encoded = oracle.scan("secret", [Artifact("log", "c2VjcmV0")])
    assert encoded.exposed and "base64" in encoded.detectors
    grouped = oracle.scan("123456", [Artifact("screen", "code 123 456")])
    assert grouped.exposed and "digits_normalized" in grouped.detectors


def test_disclosure_oracle_ignores_mask():
    assert not DisclosureOracle().scan("123456", [Artifact("tree", "[OTP PROTECTED]")]).exposed
