"""Chart generation orchestration."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from nakshatra.astronomy.ephemeris import SwissEphemeris
from nakshatra.astronomy.julian_day import julian_day
from nakshatra.models import BirthInput
from nakshatra.planets import PlanetPosition
from nakshatra.time import to_utc


class BirthChart(BaseModel):
    """Serializable v0.1 birth-chart calculation result."""

    model_config = ConfigDict(frozen=True)

    birth: BirthInput
    utc_datetime: datetime
    julian_day_ut: float
    ayanamsa: str
    ayanamsa_degrees: float
    planets: tuple[PlanetPosition, ...]


def generate_chart(
    birth: BirthInput, ephemeris: SwissEphemeris | None = None
) -> BirthChart:
    """Generate deterministic v0.1 chart facts from validated birth input."""
    utc_datetime = to_utc(birth)
    jd_ut = julian_day(utc_datetime)
    result = (ephemeris or SwissEphemeris()).positions(jd_ut)
    return BirthChart(
        birth=birth,
        utc_datetime=utc_datetime,
        julian_day_ut=jd_ut,
        ayanamsa=result.ayanamsa,
        ayanamsa_degrees=result.ayanamsa_degrees,
        planets=result.planets,
    )
