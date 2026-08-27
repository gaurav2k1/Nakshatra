"""Deterministic Vimshottari Mahadasha calculations."""

from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field

from nakshatra.astrology.nakshatras import NAKSHATRA_SPAN, NakshatraPosition
from nakshatra.planets import Planet

VIMSHOTTARI_YEAR_DAYS = 365.25
VIMSHOTTARI_CYCLE_YEARS = 120

_LORDS = (
    Planet.KETU,
    Planet.VENUS,
    Planet.SUN,
    Planet.MOON,
    Planet.MARS,
    Planet.RAHU,
    Planet.JUPITER,
    Planet.SATURN,
    Planet.MERCURY,
)
_YEARS = {
    Planet.KETU: 7,
    Planet.VENUS: 20,
    Planet.SUN: 6,
    Planet.MOON: 10,
    Planet.MARS: 7,
    Planet.RAHU: 18,
    Planet.JUPITER: 16,
    Planet.SATURN: 19,
    Planet.MERCURY: 17,
}


class MahadashaPeriod(BaseModel):
    """One complete planetary period in the Vimshottari cycle."""

    model_config = ConfigDict(frozen=True)

    lord: Planet
    start: datetime
    end: datetime
    duration_years: int = Field(gt=0)


class VimshottariDasha(BaseModel):
    """Birth balance and complete nine-lord Mahadasha cycle."""

    model_config = ConfigDict(frozen=True)

    birth_lord: Planet
    elapsed_fraction: float = Field(ge=0.0, lt=1.0)
    balance_years: float = Field(gt=0.0)
    year_days: float = VIMSHOTTARI_YEAR_DAYS
    periods: tuple[MahadashaPeriod, ...]


def _duration(years: float) -> timedelta:
    return timedelta(days=years * VIMSHOTTARI_YEAR_DAYS)


def vimshottari_dasha(
    birth_instant: datetime, moon_nakshatra: NakshatraPosition
) -> VimshottariDasha:
    """Calculate the nine-period Vimshottari cycle containing a birth instant.

    The lord sequence repeats every nine Nakshatras. The elapsed and remaining
    portions of the birth Mahadasha follow the Moon's traversed and untraversed
    fractions of its Nakshatra. A deterministic 365.25-day Dasha year converts
    traditional year lengths into civil instants.
    """
    if birth_instant.tzinfo is None or birth_instant.utcoffset() is None:
        raise ValueError("Vimshottari Dasha requires a timezone-aware birth instant")

    lord_index = moon_nakshatra.index % len(_LORDS)
    birth_lord = _LORDS[lord_index]
    elapsed_fraction = moon_nakshatra.degrees_in_nakshatra / NAKSHATRA_SPAN
    balance_years = _YEARS[birth_lord] * (1.0 - elapsed_fraction)
    period_start = birth_instant - _duration(_YEARS[birth_lord] * elapsed_fraction)

    periods = []
    for offset in range(len(_LORDS)):
        lord = _LORDS[(lord_index + offset) % len(_LORDS)]
        period_end = period_start + _duration(_YEARS[lord])
        periods.append(
            MahadashaPeriod(
                lord=lord,
                start=period_start,
                end=period_end,
                duration_years=_YEARS[lord],
            )
        )
        period_start = period_end

    return VimshottariDasha(
        birth_lord=birth_lord,
        elapsed_fraction=elapsed_fraction,
        balance_years=balance_years,
        periods=tuple(periods),
    )
