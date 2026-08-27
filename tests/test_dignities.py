import pytest

from nakshatra.astrology.dignities import Dignity, evaluate_dignity
from nakshatra.astrology.signs import ZodiacSign
from nakshatra.planets import Planet


@pytest.mark.parametrize(
    ("planet", "sign", "expected", "deep_degree"),
    [
        (Planet.SUN, ZodiacSign.ARIES, Dignity.EXALTED, 10.0),
        (Planet.MOON, ZodiacSign.SCORPIO, Dignity.DEBILITATED, 3.0),
        (Planet.MARS, ZodiacSign.ARIES, Dignity.OWN_SIGN, None),
        (Planet.MERCURY, ZodiacSign.VIRGO, Dignity.EXALTED, 15.0),
        (Planet.JUPITER, ZodiacSign.GEMINI, Dignity.NEUTRAL, None),
        (Planet.VENUS, ZodiacSign.PISCES, Dignity.EXALTED, 27.0),
        (Planet.SATURN, ZodiacSign.ARIES, Dignity.DEBILITATED, 20.0),
    ],
)
def test_visible_planet_dignity(
    planet: Planet,
    sign: ZodiacSign,
    expected: Dignity,
    deep_degree: float | None,
) -> None:
    result = evaluate_dignity(planet, sign)

    assert result.dignity is expected
    assert result.deep_degree == deep_degree
    assert result.source.title == "Brihat Parashara Hora Shastra"
    assert result.evidence


@pytest.mark.parametrize("planet", [Planet.RAHU, Planet.KETU])
def test_lunar_nodes_are_explicitly_not_evaluated(planet: Planet) -> None:
    result = evaluate_dignity(planet, ZodiacSign.TAURUS)

    assert result.dignity is Dignity.NOT_EVALUATED
    assert result.deep_degree is None
    assert "not evaluated" in result.evidence.lower()


def test_debilitation_is_opposite_exaltation() -> None:
    result = evaluate_dignity(Planet.JUPITER, ZodiacSign.CAPRICORN)

    assert result.dignity is Dignity.DEBILITATED
    assert result.deep_degree == 5.0
