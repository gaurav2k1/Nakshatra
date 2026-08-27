from datetime import date, time

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
