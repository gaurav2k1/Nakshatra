"""Sidereal zodiac sign calculations."""

from enum import IntEnum
from math import isfinite

from pydantic import BaseModel, ConfigDict, Field


class ZodiacSign(IntEnum):
    """The twelve zodiac signs in longitude order."""

    ARIES = 0
    TAURUS = 1
    GEMINI = 2
    CANCER = 3
    LEO = 4
    VIRGO = 5
    LIBRA = 6
    SCORPIO = 7
    SAGITTARIUS = 8
    CAPRICORN = 9
    AQUARIUS = 10
    PISCES = 11


class SignPosition(BaseModel):
    """A normalized longitude and its position within a zodiac sign."""

    model_config = ConfigDict(frozen=True)

    sign: ZodiacSign
    longitude: float = Field(ge=0.0, lt=360.0)
    degrees_in_sign: float = Field(ge=0.0, lt=30.0)


def sign_position(longitude: float) -> SignPosition:
    """Map any finite ecliptic longitude onto the twelve equal 30° signs."""
    if not isfinite(longitude):
        raise ValueError("Longitude must be finite")
    normalized = longitude % 360.0
    if normalized >= 360.0:
        normalized = 0.0
    sign = ZodiacSign(int(normalized // 30.0))
    return SignPosition(
        sign=sign,
        longitude=normalized,
        degrees_in_sign=normalized - sign.value * 30.0,
    )
