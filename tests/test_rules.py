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
        )
    )

    assert not any(result.present for result in results)
    assert all("not" in result.evidence[0].lower() for result in results)
