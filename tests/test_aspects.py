from nakshatra.astrology.aspects import full_aspects
from nakshatra.astrology.signs import ZodiacSign
from nakshatra.planets import Planet


def test_universal_and_special_aspects_are_directed() -> None:
    placements = {
        Planet.MARS: ZodiacSign.ARIES,
        Planet.MOON: ZodiacSign.CANCER,
        Planet.SUN: ZodiacSign.LIBRA,
        Planet.JUPITER: ZodiacSign.SAGITTARIUS,
    }
    aspects = full_aspects(placements)
    pairs = {(item.aspecting_planet, item.aspected_planet): item for item in aspects}

    assert pairs[(Planet.MARS, Planet.MOON)].relative_sign == 4
    assert pairs[(Planet.MARS, Planet.MOON)].special
    assert pairs[(Planet.MARS, Planet.SUN)].relative_sign == 7
    assert not pairs[(Planet.MARS, Planet.SUN)].special
    assert (Planet.MOON, Planet.MARS) not in pairs


def test_nodes_do_not_cast_aspects_but_can_receive_them() -> None:
    aspects = full_aspects(
        {Planet.SUN: ZodiacSign.ARIES, Planet.RAHU: ZodiacSign.LIBRA}
    )

    assert len(aspects) == 1
    assert aspects[0].aspected_planet is Planet.RAHU
