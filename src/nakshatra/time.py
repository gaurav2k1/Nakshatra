"""Conversion between civil birth time and unambiguous UTC instants."""

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from nakshatra.models import BirthInput


class LocalTimeError(ValueError):
    """Base error for a civil time that does not identify one UTC instant."""


class NonexistentLocalTimeError(LocalTimeError):
    """Raised when a civil time falls inside a forward DST transition."""


class AmbiguousLocalTimeError(LocalTimeError):
    """Raised when a civil time occurs twice during a backward DST transition."""


def _round_trips(candidate: datetime, naive: datetime, zone: ZoneInfo) -> bool:
    return candidate.astimezone(UTC).astimezone(zone).replace(tzinfo=None) == naive


def to_utc(birth: BirthInput) -> datetime:
    """Convert a birth's local civil time to UTC, rejecting DST ambiguity.

    Python's PEP 495 ``fold`` values are evaluated and round-tripped through UTC
    so nonexistent and repeated wall times cannot be silently misinterpreted.
    """
    naive = datetime.combine(birth.date, birth.time)
    zone = ZoneInfo(birth.timezone)
    first = naive.replace(tzinfo=zone, fold=0)
    second = naive.replace(tzinfo=zone, fold=1)
    first_valid = _round_trips(first, naive, zone)
    second_valid = _round_trips(second, naive, zone)

    if not first_valid and not second_valid:
        raise NonexistentLocalTimeError(
            f"{naive.isoformat()} does not exist in {birth.timezone}"
        )

    first_utc = first.astimezone(UTC)
    second_utc = second.astimezone(UTC)
    if first_valid and second_valid and first_utc != second_utc:
        raise AmbiguousLocalTimeError(
            f"{naive.isoformat()} occurs twice in {birth.timezone}; an explicit "
            "UTC offset is required"
        )

    return first_utc if first_valid else second_utc
