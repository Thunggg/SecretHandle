from secrethandle.schemas import SecretType
from secrethandle.synthetic import SeededIdentifierSource, canary, synthetic_key


def test_synthetic_generation_is_deterministic():
    assert canary(7) == canary(7)
    assert synthetic_key(7) == synthetic_key(7)
    first = SeededIdentifierSource(7)
    second = SeededIdentifierSource(7)
    assert [first() for _ in range(3)] == [second() for _ in range(3)]
    assert canary(7, SecretType.CREDENTIAL).startswith("SH-CREDENTIAL-")
