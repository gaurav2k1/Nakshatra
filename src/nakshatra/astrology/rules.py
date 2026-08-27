"""Transparent, source-cited classical Yoga and Dosha rule evaluation."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nakshatra.astrology.signs import ZodiacSign
from nakshatra.planets import Planet


class RuleCategory(StrEnum):
    """Supported classical rule categories."""

    YOGA = "yoga"
    DOSHA = "dosha"


class RuleSource(BaseModel):
    """Human-readable provenance and exact implemented rule scope."""

    model_config = ConfigDict(frozen=True)

    title: str
    section: str
    implemented_scope: str


class RulePlanet(BaseModel):
    """Minimum verified placement facts consumed by classical rules."""

    model_config = ConfigDict(frozen=True)

    planet: Planet
    sign: ZodiacSign
    house: int = Field(ge=1, le=12)


class ClassicalRuleResult(BaseModel):
    """A deterministic rule outcome with evidence and provenance."""

    model_config = ConfigDict(frozen=True)

    rule_id: str
    name: str
    category: RuleCategory
    present: bool
    evidence: tuple[str, ...]
    source: RuleSource


def _planet_map(placements: tuple[RulePlanet, ...]) -> dict[Planet, RulePlanet]:
    return {placement.planet: placement for placement in placements}


def evaluate_classical_rules(
    placements: tuple[RulePlanet, ...],
) -> tuple[ClassicalRuleResult, ...]:
    """Evaluate the explicitly scoped D1 placement rules."""
    planets = _planet_map(placements)
    sun = planets[Planet.SUN]
    mercury = planets[Planet.MERCURY]
    moon = planets[Planet.MOON]
    jupiter = planets[Planet.JUPITER]
    mars = planets[Planet.MARS]

    budha_present = sun.sign is mercury.sign
    budha_evidence = (
        f"Sun and Mercury are both in {sun.sign.name}."
        if budha_present
        else (
            f"Sun is in {sun.sign.name}; Mercury is in {mercury.sign.name}, "
            "not the same sign."
        )
    )

    jupiter_from_moon = (jupiter.sign.value - moon.sign.value) % 12 + 1
    gajakesari_present = jupiter_from_moon in {1, 4, 7, 10}
    gajakesari_evidence = (
        f"Jupiter is {jupiter_from_moon} from the Moon, a kendra position."
        if gajakesari_present
        else f"Jupiter is {jupiter_from_moon} from the Moon, not a kendra position."
    )

    mangala_houses = {1, 4, 7, 8, 12}
    mangala_present = mars.house in mangala_houses
    mangala_evidence = (
        f"Mars is in whole-sign house {mars.house}, included in this "
        "five-house variant."
        if mangala_present
        else (
            f"Mars is in whole-sign house {mars.house}, not included in this "
            "five-house variant."
        )
    )

    solar_candidates = {
        Planet.MERCURY,
        Planet.VENUS,
        Planet.MARS,
        Planet.JUPITER,
        Planet.SATURN,
    }
    second_from_sun = tuple(
        item.planet
        for item in placements
        if item.planet in solar_candidates
        and (item.sign.value - sun.sign.value) % 12 + 1 == 2
    )
    twelfth_from_sun = tuple(
        item.planet
        for item in placements
        if item.planet in solar_candidates
        and (item.sign.value - sun.sign.value) % 12 + 1 == 12
    )
    solar_evidence = (
        f"2nd from Sun: {', '.join(item.value for item in second_from_sun) or 'none'}; "
        "12th from Sun: "
        f"{', '.join(item.value for item in twelfth_from_sun) or 'none'}."
    )

    benefic_relatives = {
        planet: (planets[planet].sign.value - moon.sign.value) % 12 + 1
        for planet in (Planet.MERCURY, Planet.JUPITER, Planet.VENUS)
    }
    adhi_present = {6, 7, 8}.issubset(benefic_relatives.values())
    adhi_positions = "; ".join(
        f"{planet.value.title()} is {relative} from Moon"
        for planet, relative in benefic_relatives.items()
    )
    adhi_evidence = adhi_positions + (
        "; all 6th, 7th, and 8th positions are occupied."
        if adhi_present
        else "; the strict 6th, 7th, and 8th set is incomplete."
    )

    solar_source = RuleSource(
        title="Brihat Parashara Hora Shastra",
        section="Chapter 37, solar Yogas",
        implemented_scope=(
            "Planets other than Moon and the nodes in the 2nd and/or 12th from Sun; "
            "the three returned formations are treated as mutually exclusive."
        ),
    )

    return (
        ClassicalRuleResult(
            rule_id="budha_aditya",
            name="Budha-Aditya Yoga",
            category=RuleCategory.YOGA,
            present=budha_present,
            evidence=(budha_evidence,),
            source=RuleSource(
                title="Brihat Parashara Hora Shastra",
                section="Classical Yoga catalogue",
                implemented_scope="Sun and Mercury occupying the same sidereal sign.",
            ),
        ),
        ClassicalRuleResult(
            rule_id="gajakesari_basic",
            name="Gajakesari structural condition",
            category=RuleCategory.YOGA,
            present=gajakesari_present,
            evidence=(gajakesari_evidence,),
            source=RuleSource(
                title="Brihat Parashara Hora Shastra",
                section="Gajakesari Yoga",
                implemented_scope=(
                    "Jupiter in a kendra (1, 4, 7, or 10) from the Moon. "
                    "Additional strength and affliction qualifications are not "
                    "evaluated."
                ),
            ),
        ),
        ClassicalRuleResult(
            rule_id="mangala_lagna_phaladeepika",
            name="Mangala Dosha — five-house Lagna variant",
            category=RuleCategory.DOSHA,
            present=mangala_present,
            evidence=(mangala_evidence,),
            source=RuleSource(
                title="Phaladeepika",
                section="Chapter 7, traditionally cited Mangala placement rule",
                implemented_scope=(
                    "Mars in whole-sign houses 1, 4, 7, 8, or 12 from Lagna. "
                    "Cancellations and alternate six-house variants are not evaluated."
                ),
            ),
        ),
        ClassicalRuleResult(
            rule_id="vesi",
            name="Vesi Yoga",
            category=RuleCategory.YOGA,
            present=bool(second_from_sun) and not twelfth_from_sun,
            evidence=(solar_evidence,),
            source=solar_source,
        ),
        ClassicalRuleResult(
            rule_id="vosi",
            name="Vosi Yoga",
            category=RuleCategory.YOGA,
            present=bool(twelfth_from_sun) and not second_from_sun,
            evidence=(solar_evidence,),
            source=solar_source,
        ),
        ClassicalRuleResult(
            rule_id="ubhayachari",
            name="Ubhayachari Yoga",
            category=RuleCategory.YOGA,
            present=bool(second_from_sun and twelfth_from_sun),
            evidence=(solar_evidence,),
            source=solar_source,
        ),
        ClassicalRuleResult(
            rule_id="adhi_strict",
            name="Adhi Yoga — strict structural condition",
            category=RuleCategory.YOGA,
            present=adhi_present,
            evidence=(adhi_evidence,),
            source=RuleSource(
                title="Brihat Parashara Hora Shastra",
                section="Chapter 37, verse 5",
                implemented_scope=(
                    "Mercury, Jupiter, and Venus collectively occupy all of the "
                    "6th, 7th, and 8th signs from Moon; strength is not evaluated."
                ),
            ),
        ),
    )
