"""Whole-sign Vedic house models and assignments."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from nakshatra.astrology.signs import SignPosition, sign_position


class HouseChart(BaseModel):
    """Ascendant and twelve whole-sign house cusps."""

    model_config = ConfigDict(frozen=True)

    system: Literal["whole_sign"] = "whole_sign"
    ascendant: SignPosition
    cusps: tuple[
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ]


def house_for_longitude(longitude: float, ascendant_longitude: float) -> int:
    """Return the 1-based whole-sign house containing a longitude."""
    planet_sign = sign_position(longitude).sign.value
    ascendant_sign = sign_position(ascendant_longitude).sign.value
    return (planet_sign - ascendant_sign) % 12 + 1
