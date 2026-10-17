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


def test_disclosure_oracle_detects_unicode_and_separated_digits():
    oracle = DisclosureOracle()
    full_width = oracle.scan("123456", [Artifact("screen", "code \uff11\uff12\uff13\uff14\uff15\uff16")])
    assert full_width.exposed and "unicode_normalized" in full_width.detectors
    dashed = oracle.scan("123456", [Artifact("screen", "code 12-34.56")])
    assert dashed.exposed and "separated" in dashed.detectors


def test_disclosure_oracle_does_not_flag_separated_letters():
    assert not DisclosureOracle().scan("abcdef", [Artifact("screen", "a-b-c-d-e-f")]).exposed
