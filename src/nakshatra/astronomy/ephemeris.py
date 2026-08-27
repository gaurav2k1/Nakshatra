"""Thread-safe Swiss Ephemeris integration."""

import os
from threading import RLock

import swisseph as swe  # type: ignore[import-not-found]
from pydantic import BaseModel, ConfigDict, Field

from nakshatra.astrology.signs import sign_position
from nakshatra.planets import Planet, PlanetPosition


class EphemerisError(RuntimeError):
    """Raised when Swiss Ephemeris cannot produce a requested position."""


class EphemerisResult(BaseModel):
    """All v0.1 graha positions for one UT Julian Day."""

    model_config = ConfigDict(frozen=True)

    julian_day_ut: float
    ayanamsa: str = "Lahiri"
    ayanamsa_degrees: float = Field(ge=0.0, lt=360.0)
    planets: tuple[PlanetPosition, ...]


_PLANET_IDS = {
    Planet.SUN: swe.SUN,
    Planet.MOON: swe.MOON,
    Planet.MERCURY: swe.MERCURY,
    Planet.VENUS: swe.VENUS,
    Planet.MARS: swe.MARS,
    Planet.JUPITER: swe.JUPITER,
    Planet.SATURN: swe.SATURN,
    Planet.RAHU: swe.MEAN_NODE,
}
_PLANET_ORDER = tuple(Planet)
_FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL
_EPHEMERIS_LOCK = RLock()


class SwissEphemeris:
    """Calculate Lahiri sidereal positions through pyswisseph.

    Swiss Ephemeris stores the sidereal mode and data path process-globally. All
    access is serialized and the Lahiri mode is set for every calculation,
    preventing another in-process caller from changing Nakshatra's result.
    """

    def __init__(self, ephemeris_path: str | None = None) -> None:
        self._ephemeris_path = ephemeris_path or os.getenv("NAKSHATRA_EPHEMERIS_PATH")

    def _configure(self) -> None:
        if self._ephemeris_path is not None:
            swe.set_ephe_path(self._ephemeris_path)
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    def position(self, julian_day_ut: float, planet: Planet) -> PlanetPosition:
        """Calculate one planet position at a UT Julian Day."""
        if planet is Planet.KETU:
            rahu = self.position(julian_day_ut, Planet.RAHU)
            return self._ketu_from_rahu(rahu)

        with _EPHEMERIS_LOCK:
            self._configure()
            try:
                values, _return_flags = swe.calc_ut(
                    julian_day_ut, _PLANET_IDS[planet], _FLAGS
                )
            except swe.Error as error:
                raise EphemerisError(
                    f"Swiss Ephemeris failed for {planet.value}: {error}"
                ) from error

        longitude = values[0] % 360.0
        speed = values[3]
        return PlanetPosition(
            planet=planet,
            longitude=longitude,
            latitude=values[1],
            distance_au=values[2],
            speed_longitude=speed,
            retrograde=speed < 0.0,
            sign=sign_position(longitude),
        )

    def positions(self, julian_day_ut: float) -> EphemerisResult:
        """Calculate the complete ordered set of v0.1 graha positions."""
        with _EPHEMERIS_LOCK:
            self._configure()
            ayanamsa = swe.get_ayanamsa_ut(julian_day_ut) % 360.0
            positions = tuple(
                self.position(julian_day_ut, planet) for planet in _PLANET_ORDER
            )
        return EphemerisResult(
            julian_day_ut=julian_day_ut,
            ayanamsa_degrees=ayanamsa,
            planets=positions,
        )

    @staticmethod
    def _ketu_from_rahu(rahu: PlanetPosition) -> PlanetPosition:
        longitude = (rahu.longitude + 180.0) % 360.0
        return PlanetPosition(
            planet=Planet.KETU,
            longitude=longitude,
            latitude=-rahu.latitude,
            distance_au=rahu.distance_au,
            speed_longitude=rahu.speed_longitude,
            retrograde=rahu.retrograde,
            sign=sign_position(longitude),
        )
