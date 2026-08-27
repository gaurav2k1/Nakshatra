"""Julian Day calculations."""

from datetime import UTC, datetime


def julian_day(instant: datetime) -> float:
    """Return the Julian Day for a timezone-aware Gregorian datetime.

    Implements Jean Meeus, *Astronomical Algorithms*, 2nd ed., chapter 7. The
    proleptic Gregorian calendar is used because Python's ``datetime`` uses it.
    """
    if instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError("Julian Day calculation requires a timezone-aware datetime")

    utc = instant.astimezone(UTC)
    year = utc.year
    month = utc.month
    day_fraction = (
        utc.day
        + utc.hour / 24.0
        + utc.minute / 1_440.0
        + utc.second / 86_400.0
        + utc.microsecond / 86_400_000_000.0
    )

    if month <= 2:
        year -= 1
        month += 12

    century = year // 100
    correction = 2 - century + century // 4
    return (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day_fraction
        + correction
        - 1524.5
    )
