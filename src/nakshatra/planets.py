"""Planet identifiers and calculated position models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nakshatra.astrology.nakshatras import NakshatraPosition
from nakshatra.astrology.signs import SignPosition


class Planet(StrEnum):
    """Vedic grahas supported by the deterministic position engine."""

    SUN = "sun"
    MOON = "moon"
    MERCURY = "mercury"
    VENUS = "venus"
    MARS = "mars"
    JUPITER = "jupiter"
    SATURN = "saturn"
    RAHU = "rahu"
    KETU = "ketu"


class PlanetPosition(BaseModel):
    """A calculated apparent geocentric sidereal planet position."""

    model_config = ConfigDict(frozen=True)

    planet: Planet
    longitude: float = Field(ge=0.0, lt=360.0)
    latitude: float
    distance_au: float = Field(ge=0.0)
    speed_longitude: float
    retrograde: bool
    sign: SignPosition
    nakshatra: NakshatraPosition


class ChartPlanetPosition(PlanetPosition):
    """A planet position assigned to a whole-sign house."""

    house: int = Field(ge=1, le=12)
