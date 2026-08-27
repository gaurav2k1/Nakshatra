"""The 27 equal Nakshatra divisions and four Padas."""

from enum import StrEnum
from math import isfinite

from pydantic import BaseModel, ConfigDict, Field

NAKSHATRA_SPAN = 360.0 / 27.0
PADA_SPAN = NAKSHATRA_SPAN / 4.0


class Nakshatra(StrEnum):
    """The 27 Nakshatras in sidereal-longitude order."""

    ASHWINI = "ashwini"
    BHARANI = "bharani"
    KRITTIKA = "krittika"
    ROHINI = "rohini"
    MRIGASHIRA = "mrigashira"
    ARDRA = "ardra"
    PUNARVASU = "punarvasu"
    PUSHYA = "pushya"
    ASHLESHA = "ashlesha"
    MAGHA = "magha"
    PURVA_PHALGUNI = "purva_phalguni"
    UTTARA_PHALGUNI = "uttara_phalguni"
    HASTA = "hasta"
    CHITRA = "chitra"
    SWATI = "swati"
    VISHAKHA = "vishakha"
    ANURADHA = "anuradha"
    JYESHTHA = "jyeshtha"
    MULA = "mula"
    PURVA_ASHADHA = "purva_ashadha"
    UTTARA_ASHADHA = "uttara_ashadha"
    SHRAVANA = "shravana"
    DHANISHTHA = "dhanishtha"
    SHATABHISHA = "shatabhisha"
    PURVA_BHADRAPADA = "purva_bhadrapada"
    UTTARA_BHADRAPADA = "uttara_bhadrapada"
    REVATI = "revati"


class NakshatraPosition(BaseModel):
    """A longitude's Nakshatra, Pada, and offset within the Nakshatra."""

    model_config = ConfigDict(frozen=True)

    nakshatra: Nakshatra
    index: int = Field(ge=0, lt=27)
    pada: int = Field(ge=1, le=4)
    longitude: float = Field(ge=0.0, lt=360.0)
    degrees_in_nakshatra: float = Field(ge=0.0, lt=NAKSHATRA_SPAN)


def nakshatra_position(longitude: float) -> NakshatraPosition:
    """Map any finite sidereal longitude to one of 27 Nakshatras and Padas.

    The zodiac is divided into 27 equal spans of 13 degrees 20 arcminutes,
    beginning with Ashwini at 0 degrees sidereal Aries. Each span contains four
    equal Padas of 3 degrees 20 arcminutes.
    """
    if not isfinite(longitude):
        raise ValueError("Longitude must be finite")
    normalized = longitude % 360.0
    if normalized >= 360.0:
        normalized = 0.0
    index = min(int(normalized / NAKSHATRA_SPAN), 26)
    offset = normalized - index * NAKSHATRA_SPAN
    pada = min(int(offset / PADA_SPAN) + 1, 4)
    return NakshatraPosition(
        nakshatra=tuple(Nakshatra)[index],
        index=index,
        pada=pada,
        longitude=normalized,
        degrees_in_nakshatra=offset,
    )
