"""Deterministic Rasi (D1) and Navamsa (D9) transformations."""

from enum import StrEnum
from math import isfinite

from pydantic import BaseModel, ConfigDict, Field

from nakshatra.astrology.signs import ZodiacSign
from nakshatra.planets import Planet, PlanetPosition


class Division(StrEnum):
    """Supported Varga divisions."""

    D1 = "D1"
    D9 = "D9"


class DivisionalPosition(BaseModel):
    """A longitude transformed into a divisional sign and degree."""

    model_config = ConfigDict(frozen=True)

    division: Division
    sign: ZodiacSign
    degrees_in_sign: float = Field(ge=0.0, lt=30.0)


class DivisionalPlanet(BaseModel):
    """A graha's position and house in one divisional chart."""

    model_config = ConfigDict(frozen=True)

    planet: Planet
    sign: ZodiacSign
    degrees_in_sign: float = Field(ge=0.0, lt=30.0)
    house: int = Field(ge=1, le=12)
    retrograde: bool


class DivisionalChart(BaseModel):
    """Ascendant and graha placements for one supported Varga."""

    model_config = ConfigDict(frozen=True)

    division: Division
    name: str
    ascendant: DivisionalPosition
    planets: tuple[DivisionalPlanet, ...]


_DIVISION_NAMES = {Division.D1: "Rasi", Division.D9: "Navamsa"}


def divisional_position(longitude: float, division: Division) -> DivisionalPosition:
    """Transform a finite sidereal longitude into D1 or D9.

    Navamsa divides the zodiac into 108 equal portions of 3 degrees 20
    arcminutes. Their signs repeat from Aries through Pisces, which is
    equivalent to multiplying the normalized longitude by nine and taking its
    position within the 360-degree zodiac.
    """
    if not isfinite(longitude):
        raise ValueError("Longitude must be finite")
    normalized = longitude % 360.0
    if normalized >= 360.0:
        normalized = 0.0
    transformed = normalized if division is Division.D1 else (normalized * 9.0) % 360.0
    sign = ZodiacSign(int(transformed // 30.0))
    return DivisionalPosition(
        division=division,
        sign=sign,
        degrees_in_sign=transformed - sign.value * 30.0,
    )


def build_divisional_chart(
    division: Division,
    ascendant_longitude: float,
    planets: tuple[PlanetPosition, ...],
) -> DivisionalChart:
    """Build a divisional Ascendant and whole-sign graha houses."""
    ascendant = divisional_position(ascendant_longitude, division)
    placements = []
    for planet in planets:
        position = divisional_position(planet.longitude, division)
        placements.append(
            DivisionalPlanet(
                planet=planet.planet,
                sign=position.sign,
                degrees_in_sign=position.degrees_in_sign,
                house=(position.sign.value - ascendant.sign.value) % 12 + 1,
                retrograde=planet.retrograde,
            )
        )
    return DivisionalChart(
        division=division,
        name=_DIVISION_NAMES[division],
        ascendant=ascendant,
        planets=tuple(placements),
    )
