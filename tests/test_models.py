from datetime import date, time

import pytest
from pydantic import ValidationError

from nakshatra.models import BirthInput, Coordinates


def test_coordinates_accept_valid_values() -> None:
    coordinates = Coordinates(latitude=13.0827, longitude=80.2707)

    assert coordinates.latitude == 13.0827
    assert coordinates.longitude == 80.2707


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("latitude", -90.0001),
        ("latitude", 90.0001),
        ("longitude", -180.0001),
        ("longitude", 180.0001),
    ],
)
def test_coordinates_reject_out_of_range_values(field: str, value: float) -> None:
    values = {"latitude": 0.0, "longitude": 0.0, field: value}

    with pytest.raises(ValidationError):
        Coordinates(**values)


def test_birth_input_serializes_without_losing_timezone() -> None:
    birth = BirthInput(
        date=date(2000, 1, 1),
        time=time(12, 0),
        timezone="Asia/Kolkata",
        coordinates=Coordinates(latitude=13.0827, longitude=80.2707),
    )

    assert birth.model_dump(mode="json") == {
        "date": "2000-01-01",
        "time": "12:00:00",
        "timezone": "Asia/Kolkata",
        "coordinates": {"latitude": 13.0827, "longitude": 80.2707},
    }


def test_birth_input_rejects_unknown_timezone() -> None:
    with pytest.raises(ValidationError, match="Unknown IANA timezone"):
        BirthInput(
            date=date(2000, 1, 1),
            time=time(12, 0),
            timezone="Mars/Olympus_Mons",
            coordinates=Coordinates(latitude=0, longitude=0),
        )
