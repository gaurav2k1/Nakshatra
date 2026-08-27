"""Validated domain input models."""

from datetime import date, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Coordinates(BaseModel):
    """A geographic position in decimal degrees using the WGS 84 convention."""

    model_config = ConfigDict(frozen=True)

    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)


class BirthInput(BaseModel):
    """Civil birth time, IANA timezone, and geographic coordinates."""

    model_config = ConfigDict(frozen=True)

    date: date
    time: time
    timezone: str
    coordinates: Coordinates

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        """Require a timezone name available through the IANA database."""
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as error:
            raise ValueError(f"Unknown IANA timezone: {value}") from error
        return value
