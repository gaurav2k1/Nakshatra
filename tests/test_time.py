from datetime import UTC, date, datetime, time

import pytest

from nakshatra.models import BirthInput, Coordinates
from nakshatra.time import AmbiguousLocalTimeError, NonexistentLocalTimeError, to_utc


def make_birth(day: date, local_time: time, zone: str) -> BirthInput:
    return BirthInput(
        date=day,
        time=local_time,
        timezone=zone,
        coordinates=Coordinates(latitude=0, longitude=0),
    )


def test_to_utc_converts_iana_timezone() -> None:
    birth = make_birth(date(2000, 1, 1), time(12, 0), "Asia/Kolkata")

    assert to_utc(birth) == datetime(2000, 1, 1, 6, 30, tzinfo=UTC)


def test_to_utc_rejects_nonexistent_dst_time() -> None:
    birth = make_birth(date(2024, 3, 10), time(2, 30), "America/New_York")

    with pytest.raises(NonexistentLocalTimeError):
        to_utc(birth)


def test_to_utc_rejects_ambiguous_dst_time_without_fold() -> None:
    birth = make_birth(date(2024, 11, 3), time(1, 30), "America/New_York")

    with pytest.raises(AmbiguousLocalTimeError):
        to_utc(birth)
