import pytest
from hypothesis import given
from hypothesis import strategies as st

from nakshatra.astrology.nakshatras import Nakshatra, nakshatra_position


def test_nakshatra_and_pada_boundaries() -> None:
    assert nakshatra_position(0).nakshatra is Nakshatra.ASHWINI
    assert nakshatra_position(3 + 20 / 60).pada == 2
    assert nakshatra_position(13 + 20 / 60).nakshatra is Nakshatra.BHARANI
    assert nakshatra_position(359.999).nakshatra is Nakshatra.REVATI
    assert nakshatra_position(359.999).pada == 4


@given(st.floats(min_value=-100_000, max_value=100_000, allow_nan=False))
def test_nakshatra_position_normalizes_finite_longitudes(longitude: float) -> None:
    position = nakshatra_position(longitude)

    assert 0 <= position.longitude < 360
    assert 0 <= position.index < 27
    assert 1 <= position.pada <= 4
    assert 0 <= position.degrees_in_nakshatra < 360 / 27


@pytest.mark.parametrize("longitude", [float("nan"), float("inf")])
def test_nakshatra_position_rejects_non_finite_values(longitude: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        nakshatra_position(longitude)
