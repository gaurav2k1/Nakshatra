import pytest
from hypothesis import given
from hypothesis import strategies as st

from nakshatra.astrology.divisional import Division, divisional_position
from nakshatra.astrology.signs import ZodiacSign


@pytest.mark.parametrize(
    ("longitude", "expected_sign"),
    [
        (0.0, ZodiacSign.ARIES),
        (3 + 20 / 60, ZodiacSign.TAURUS),
        (29.999, ZodiacSign.SAGITTARIUS),
        (30.0, ZodiacSign.CAPRICORN),
        (60.0, ZodiacSign.LIBRA),
    ],
)
def test_navamsa_sign_boundaries(longitude: float, expected_sign: ZodiacSign) -> None:
    assert divisional_position(longitude, Division.D9).sign is expected_sign


def test_rasi_position_preserves_original_sign_and_degree() -> None:
    position = divisional_position(72.5, Division.D1)

    assert position.sign is ZodiacSign.GEMINI
    assert position.degrees_in_sign == pytest.approx(12.5)


@given(st.floats(min_value=-100_000, max_value=100_000, allow_nan=False))
def test_navamsa_position_is_always_normalized(longitude: float) -> None:
    position = divisional_position(longitude, Division.D9)

    assert 0 <= position.sign.value < 12
    assert 0 <= position.degrees_in_sign < 30


@pytest.mark.parametrize("longitude", [float("nan"), float("inf")])
def test_divisional_position_rejects_non_finite_values(longitude: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        divisional_position(longitude, Division.D9)
