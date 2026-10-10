from secrethandle.redaction import ObservationRedactor
from secrethandle.schemas import Observation, ObservationItem, SecretType


def test_redaction_masks_targeted_channels():
    redactor = ObservationRedactor()
    redactor.register("v", "h", SecretType.OTP, 1.0)
    observation = Observation(
        (
            ObservationItem("screenshot", "123456", "v", True, "w"),
            ObservationItem("accessibility", "public", "other", True, "w"),
        )
    )
    result = redactor.redact(observation)
    assert result.items[0].text == "[OTP PROTECTED]"
    assert result.items[1].text == "public"


def test_unstable_identity_suppresses_frame():
    redactor = ObservationRedactor()
    redactor.register("v", "h", SecretType.OTP, 1.0)
    result = redactor.redact(Observation((ObservationItem("pixel", "123456", "v", False, "w"),)))
    assert result.frame_suppressed
    assert result.items[0].text == "[WINDOW SUPPRESSED]"
