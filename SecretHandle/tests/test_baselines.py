from secrethandle.baselines import DetectedPlaceholderBaseline, PlatformFlowBaseline, UnprotectedBaseline


def test_unprotected_and_placeholder_are_distinct():
    raw = UnprotectedBaseline().run("123456", "attacker", "bank")
    placeholder = DetectedPlaceholderBaseline().run("123456", "attacker", "bank")
    assert raw.public_value == "123456"
    assert "123456" not in placeholder.public_value
    assert not raw.bound_to_destination and not placeholder.bound_to_destination


def test_platform_flow_is_explicit_adapter_gap():
    result = PlatformFlowBaseline().run("123456", "bank", "bank")
    assert not result.applicable
    assert "requires Android" in result.note
