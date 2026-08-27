import pytest
from hypothesis import given
from hypothesis import strategies as st

from nakshatra.astrology.signs import ZodiacSign, sign_position


def test_sign_boundaries() -> None:
    assert sign_position(0).sign is ZodiacSign.ARIES
    assert sign_position(29.999).sign is ZodiacSign.ARIES
    assert sign_position(30).sign is ZodiacSign.TAURUS
    assert sign_position(359.999).sign is ZodiacSign.PISCES


@given(st.floats(min_value=-100_000, max_value=100_000, allow_nan=False))
def test_sign_position_normalizes_all_finite_longitudes(longitude: float) -> None:
    position = sign_position(longitude)

    assert 0 <= position.longitude < 360
    assert 0 <= position.degrees_in_sign < 30
    assert position.sign.value == int(position.longitude // 30)


@pytest.mark.parametrize("longitude", [float("nan"), float("inf"), float("-inf")])
def test_sign_position_rejects_non_finite_longitude(longitude: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        sign_position(longitude)
