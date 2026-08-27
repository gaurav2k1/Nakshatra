from nakshatra.astrology.rules import RuleCategory, RulePlanet, evaluate_classical_rules
from nakshatra.astrology.signs import ZodiacSign
from nakshatra.planets import Planet


def placement(planet: Planet, sign: ZodiacSign, house: int) -> RulePlanet:
    return RulePlanet(planet=planet, sign=sign, house=house)


def test_rules_report_matches_and_non_matches_with_evidence() -> None:
    results = evaluate_classical_rules(
        (
            placement(Planet.SUN, ZodiacSign.ARIES, 1),
            placement(Planet.MERCURY, ZodiacSign.ARIES, 1),
            placement(Planet.MOON, ZodiacSign.CANCER, 4),
            placement(Planet.JUPITER, ZodiacSign.LIBRA, 7),
            placement(Planet.MARS, ZodiacSign.SCORPIO, 8),
            placement(Planet.VENUS, ZodiacSign.GEMINI, 3),
            placement(Planet.SATURN, ZodiacSign.AQUARIUS, 11),
        )
    )
    by_id = {result.rule_id: result for result in results}

    assert by_id["budha_aditya"].present
    assert by_id["gajakesari_basic"].present
    assert by_id["mangala_lagna_phaladeepika"].present
    assert by_id["mangala_lagna_phaladeepika"].category is RuleCategory.DOSHA
    assert all(result.evidence for result in results)
    assert all(result.source.title for result in results)


def test_rules_explain_absence_without_interpretation() -> None:
    results = evaluate_classical_rules(
        (
            placement(Planet.SUN, ZodiacSign.ARIES, 1),
            placement(Planet.MERCURY, ZodiacSign.TAURUS, 2),
            placement(Planet.MOON, ZodiacSign.CANCER, 4),
            placement(Planet.JUPITER, ZodiacSign.LEO, 5),
            placement(Planet.MARS, ZodiacSign.GEMINI, 3),
            placement(Planet.VENUS, ZodiacSign.LEO, 5),
            placement(Planet.SATURN, ZodiacSign.LEO, 5),
        )
    )

    by_id = {result.rule_id: result for result in results}
    assert not by_id["budha_aditya"].present
    assert not by_id["gajakesari_basic"].present
    assert not by_id["mangala_lagna_phaladeepika"].present


def test_solar_yogas_are_mutually_exclusive_and_exclude_moon() -> None:
    results = evaluate_classical_rules(
        (
            placement(Planet.SUN, ZodiacSign.ARIES, 1),
            placement(Planet.MOON, ZodiacSign.PISCES, 12),
            placement(Planet.MERCURY, ZodiacSign.TAURUS, 2),
            placement(Planet.VENUS, ZodiacSign.PISCES, 12),
            placement(Planet.MARS, ZodiacSign.GEMINI, 3),
            placement(Planet.JUPITER, ZodiacSign.CANCER, 4),
            placement(Planet.SATURN, ZodiacSign.LEO, 5),
        )
    )
    by_id = {result.rule_id: result for result in results}

    assert by_id["ubhayachari"].present
    assert not by_id["vesi"].present
    assert not by_id["vosi"].present


def test_strict_adhi_requires_all_three_lunar_positions() -> None:
    results = evaluate_classical_rules(
        (
            placement(Planet.SUN, ZodiacSign.LEO, 1),
            placement(Planet.MOON, ZodiacSign.ARIES, 1),
            placement(Planet.MERCURY, ZodiacSign.VIRGO, 6),
            placement(Planet.JUPITER, ZodiacSign.LIBRA, 7),
            placement(Planet.VENUS, ZodiacSign.SCORPIO, 8),
            placement(Planet.MARS, ZodiacSign.CAPRICORN, 10),
            placement(Planet.SATURN, ZodiacSign.AQUARIUS, 11),
        )
    )

    assert next(item for item in results if item.rule_id == "adhi_strict").present
