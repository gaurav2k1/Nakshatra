"""Classical full-sign graha Drishti calculations."""

from pydantic import BaseModel, ConfigDict, Field

from nakshatra.astrology.signs import ZodiacSign
from nakshatra.planets import Planet


class PlanetAspect(BaseModel):
    """One directed, full classical aspect between grahas."""

    model_config = ConfigDict(frozen=True)

    aspecting_planet: Planet
    aspected_planet: Planet
    relative_sign: int = Field(ge=1, le=12)
    special: bool
    evidence: str
    source: str = "Brihat Parashara Hora Shastra, chapter 27, verse 3"


_SPECIAL = {
    Planet.MARS: {4, 8},
    Planet.JUPITER: {5, 9},
    Planet.SATURN: {3, 10},
}
_ASPECTORS = frozenset(
    {
        Planet.SUN,
        Planet.MOON,
        Planet.MERCURY,
        Planet.VENUS,
        Planet.MARS,
        Planet.JUPITER,
        Planet.SATURN,
    }
)


def full_aspects(placements: dict[Planet, ZodiacSign]) -> tuple[PlanetAspect, ...]:
    """Return directed whole-sign full aspects, excluding disputed node Drishti."""
    results: list[PlanetAspect] = []
    for aspector, source_sign in placements.items():
        if aspector not in _ASPECTORS:
            continue
        valid = {7, *_SPECIAL.get(aspector, set())}
        for target, target_sign in placements.items():
            if target is aspector:
                continue
            relative = (target_sign.value - source_sign.value) % 12 + 1
            if relative in valid:
                results.append(
                    PlanetAspect(
                        aspecting_planet=aspector,
                        aspected_planet=target,
                        relative_sign=relative,
                        special=relative != 7,
                        evidence=(
                            f"{aspector.value.title()} casts its {relative}th full "
                            f"aspect on {target.value.title()}."
                        ),
                    )
                )
    return tuple(results)
