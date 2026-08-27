from datetime import date, time

import pytest

from nakshatra.charts import generate_chart
from nakshatra.models import BirthInput, Coordinates


def test_generate_chart_connects_time_and_ephemeris() -> None:
    birth = BirthInput(
        date=date(2000, 1, 1),
        time=time(17, 30),
        timezone="Asia/Kolkata",
        coordinates=Coordinates(latitude=13.0827, longitude=80.2707),
    )

    chart = generate_chart(birth)

    assert chart.julian_day_ut == 2451545.0
    assert chart.utc_datetime.isoformat() == "2000-01-01T12:00:00+00:00"
    assert len(chart.planets) == 9
    assert chart.model_dump(mode="json")["birth"]["timezone"] == "Asia/Kolkata"
    assert chart.houses.ascendant.sign.name == "GEMINI"
    assert chart.planets[0].house == 7
    assert chart.planets[0].nakshatra.nakshatra.value == "purva_ashadha"
    assert chart.planets[1].nakshatra.pada == 4
    assert [item.division for item in chart.divisional_charts] == ["D1", "D9"]
    rasi, navamsa = chart.divisional_charts
    assert rasi.ascendant.sign.name == "GEMINI"
    assert navamsa.ascendant.sign.name == "CAPRICORN"
    assert navamsa.planets[0].sign.name == "LEO"
    assert navamsa.planets[0].house == 8
    assert chart.vimshottari_dasha.birth_lord.value == "rahu"
    assert len(chart.vimshottari_dasha.periods) == 9
    assert chart.vimshottari_dasha.balance_years == pytest.approx(0.7147, abs=0.001)
    rules = {rule.rule_id: rule for rule in chart.classical_rules}
    assert rules["budha_aditya"].present
    assert rules["gajakesari_basic"].present
    assert not rules["mangala_lagna_phaladeepika"].present
    dignities = {item.planet: item for item in chart.planetary_dignities}
    assert len(dignities) == 9
    assert dignities["jupiter"].dignity == "neutral"
    assert dignities["rahu"].dignity == "not_evaluated"
