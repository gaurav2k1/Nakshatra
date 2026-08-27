"""Deterministic sign-level planetary dignity classification."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from nakshatra.astrology.signs import ZodiacSign
from nakshatra.planets import Planet


class Dignity(StrEnum):
    """Supported sign-level dignity states."""

    EXALTED = "exalted"
    DEBILITATED = "debilitated"
    OWN_SIGN = "own_sign"
    NEUTRAL = "neutral"
    NOT_EVALUATED = "not_evaluated"


class DignitySource(BaseModel):
    """Classical source and exact implementation scope."""

    model_config = ConfigDict(frozen=True)

    title: str
    section: str
    implemented_scope: str


class PlanetaryDignity(BaseModel):
    """Auditable sign-level dignity for one graha."""

    model_config = ConfigDict(frozen=True)

    planet: Planet
    sign: ZodiacSign
    dignity: Dignity
    deep_degree: float | None
    evidence: str
    source: DignitySource


_EXALTATION = {
    Planet.SUN: (ZodiacSign.ARIES, 10.0),
    Planet.MOON: (ZodiacSign.TAURUS, 3.0),
    Planet.MARS: (ZodiacSign.CAPRICORN, 28.0),
    Planet.MERCURY: (ZodiacSign.VIRGO, 15.0),
    Planet.JUPITER: (ZodiacSign.CANCER, 5.0),
    Planet.VENUS: (ZodiacSign.PISCES, 27.0),
    Planet.SATURN: (ZodiacSign.LIBRA, 20.0),
}

_OWN_SIGNS = {
    Planet.SUN: {ZodiacSign.LEO},
    Planet.MOON: {ZodiacSign.CANCER},
    Planet.MARS: {ZodiacSign.ARIES, ZodiacSign.SCORPIO},
    Planet.MERCURY: {ZodiacSign.GEMINI, ZodiacSign.VIRGO},
    Planet.JUPITER: {ZodiacSign.SAGITTARIUS, ZodiacSign.PISCES},
    Planet.VENUS: {ZodiacSign.TAURUS, ZodiacSign.LIBRA},
    Planet.SATURN: {ZodiacSign.CAPRICORN, ZodiacSign.AQUARIUS},
}

_SOURCE = DignitySource(
    title="Brihat Parashara Hora Shastra",
    section="Chapter 3, verses 49-50",
    implemented_scope=(
        "Sign rulership plus exaltation signs, deepest exaltation degrees, and "
        "the opposite signs of debilitation for the seven visible grahas."
    ),
)

_NODE_SOURCE = DignitySource(
    title="Phaladeepika",
    section="Chapter 1, dignity table commentary",
    implemented_scope=(
        "Rahu and Ketu are excluded because classical authorities differ on "
        "their exaltation and debilitation signs."
    ),
)


def evaluate_dignity(planet: Planet, sign: ZodiacSign) -> PlanetaryDignity:
    """Classify one graha by its sidereal sign without interpreting effects."""
    if planet not in _EXALTATION:
        return PlanetaryDignity(
            planet=planet,
            sign=sign,
            dignity=Dignity.NOT_EVALUATED,
            deep_degree=None,
            evidence=f"{planet.value.title()} dignity is not evaluated.",
            source=_NODE_SOURCE,
        )

    exaltation_sign, deep_degree = _EXALTATION[planet]
    debilitation_sign = ZodiacSign((exaltation_sign.value + 6) % 12)
    if sign is exaltation_sign:
        dignity = Dignity.EXALTED
        evidence = (
            f"{planet.value.title()} is in {sign.name.title()}, its exaltation sign; "
            f"deepest exaltation is {deep_degree:g}°."
        )
        result_degree: float | None = deep_degree
    elif sign is debilitation_sign:
        dignity = Dignity.DEBILITATED
        evidence = (
            f"{planet.value.title()} is in {sign.name.title()}, opposite its "
            f"exaltation sign; deepest debilitation is {deep_degree:g}°."
        )
        result_degree = deep_degree
    elif sign in _OWN_SIGNS[planet]:
        dignity = Dignity.OWN_SIGN
        evidence = f"{planet.value.title()} is in its own sign, {sign.name.title()}."
        result_degree = None
    else:
        dignity = Dignity.NEUTRAL
        evidence = (
            f"{planet.value.title()} in {sign.name.title()} is neither exalted, "
            "debilitated, nor in its own sign in this scope."
        )
        result_degree = None

    return PlanetaryDignity(
        planet=planet,
        sign=sign,
        dignity=dignity,
        deep_degree=result_degree,
        evidence=evidence,
        source=_SOURCE,
    )
