from datetime import UTC, datetime

import pytest

from nakshatra.astronomy.julian_day import julian_day


@pytest.mark.parametrize(
    ("instant", "expected"),
    [
        (datetime(2000, 1, 1, 12, tzinfo=UTC), 2451545.0),
        (datetime(1987, 1, 27, 0, tzinfo=UTC), 2446822.5),
        (datetime(1987, 6, 19, 12, tzinfo=UTC), 2446966.0),
    ],
)
def test_julian_day_matches_meeus_examples(instant: datetime, expected: float) -> None:
    assert julian_day(instant) == pytest.approx(expected, abs=1e-9)


def test_julian_day_requires_aware_datetime() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        julian_day(datetime(2000, 1, 1, 12))
