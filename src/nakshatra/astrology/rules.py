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
) -> tuple[ClassicalRuleResult, ClassicalRuleResult, ClassicalRuleResult]:
    """Evaluate the explicitly scoped v0.6 D1 placement rules."""
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
    )
