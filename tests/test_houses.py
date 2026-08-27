import pytest

from nakshatra.astrology.houses import house_for_longitude
from nakshatra.astronomy.ephemeris import SwissEphemeris
from nakshatra.models import Coordinates


def test_whole_sign_houses_match_j2000_reference() -> None:
    houses = SwissEphemeris().houses(
        2451545.0, Coordinates(latitude=13.0827, longitude=80.2707)
    )

    assert houses.system == "whole_sign"
    assert houses.ascendant.longitude == pytest.approx(72.0895864677035, abs=1 / 3600)
    assert houses.ascendant.sign.name == "GEMINI"
    assert houses.cusps == pytest.approx(
        (60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 0, 30)
    )


@pytest.mark.parametrize(
    ("longitude", "ascendant", "expected"),
    [(60, 72, 1), (89.999, 72, 1), (90, 72, 2), (59.999, 72, 12), (240, 72, 7)],
)
def test_house_assignment_uses_whole_sign_boundaries(
    longitude: float, ascendant: float, expected: int
) -> None:
    assert house_for_longitude(longitude, ascendant) == expected
