"""Chart generation orchestration."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from nakshatra.astrology.divisional import (
    Division,
    DivisionalChart,
    build_divisional_chart,
)
from nakshatra.astrology.houses import HouseChart, house_for_longitude
from nakshatra.astronomy.ephemeris import SwissEphemeris
from nakshatra.astronomy.julian_day import julian_day
from nakshatra.models import BirthInput
from nakshatra.planets import ChartPlanetPosition
from nakshatra.time import to_utc


class BirthChart(BaseModel):
    """Serializable deterministic birth-chart calculation result."""

    model_config = ConfigDict(frozen=True)

    birth: BirthInput
    utc_datetime: datetime
    julian_day_ut: float
    ayanamsa: str
    ayanamsa_degrees: float
    houses: HouseChart
    planets: tuple[ChartPlanetPosition, ...]
    divisional_charts: tuple[DivisionalChart, DivisionalChart]


def generate_chart(
    birth: BirthInput, ephemeris: SwissEphemeris | None = None
) -> BirthChart:
    """Generate deterministic chart facts from validated birth input."""
    utc_datetime = to_utc(birth)
    jd_ut = julian_day(utc_datetime)
    calculator = ephemeris or SwissEphemeris()
    result = calculator.positions(jd_ut)
    houses = calculator.houses(jd_ut, birth.coordinates)
    planets = tuple(
        ChartPlanetPosition(
            **position.model_dump(),
            house=house_for_longitude(position.longitude, houses.ascendant.longitude),
        )
        for position in result.planets
    )
    divisional_charts = (
        build_divisional_chart(Division.D1, houses.ascendant.longitude, result.planets),
        build_divisional_chart(Division.D9, houses.ascendant.longitude, result.planets),
    )
    return BirthChart(
        birth=birth,
        utc_datetime=utc_datetime,
        julian_day_ut=jd_ut,
        ayanamsa=result.ayanamsa,
        ayanamsa_degrees=result.ayanamsa_degrees,
        houses=houses,
        planets=planets,
        divisional_charts=divisional_charts,
    )
