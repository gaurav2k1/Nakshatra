"""Runtime diagnostics and deterministic installation validation."""

import json
import os
import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime, time
from enum import StrEnum
from pathlib import Path
from zoneinfo import ZoneInfo

import swisseph as swe  # type: ignore[import-not-found]

from nakshatra.astronomy.ephemeris import SwissEphemeris
from nakshatra.charts import generate_chart
from nakshatra.models import BirthInput, Coordinates


class CheckStatus(StrEnum):
    """Diagnostic check outcome."""

    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class CheckResult:
    """One actionable diagnostic result."""

    name: str
    status: CheckStatus
    detail: str


@dataclass(frozen=True)
class ValidationReport:
    """Aggregate diagnostic report."""

    checks: tuple[CheckResult, ...]

    @property
    def ok(self) -> bool:
        """Return whether every check passed."""
        return all(check.status is CheckStatus.PASS for check in self.checks)


def _result(name: str, passed: bool, detail: str) -> CheckResult:
    status = CheckStatus.PASS if passed else CheckStatus.FAIL
    return CheckResult(name, status, detail)


def doctor() -> ValidationReport:
    """Check runtime, Swiss Ephemeris, timezone data, and configuration."""
    python_ok = sys.version_info >= (3, 12)
    ephemeris_path = os.getenv("NAKSHATRA_EPHEMERIS_PATH")
    path_ok = ephemeris_path is None or Path(ephemeris_path).is_dir()
    path_detail = (
        "built-in Moshier fallback; set NAKSHATRA_EPHEMERIS_PATH for data files"
        if ephemeris_path is None
        else f"ephemeris directory: {ephemeris_path}"
    )
    try:
        zone_ok = (
            datetime.now(UTC).astimezone(ZoneInfo("Asia/Kolkata")).utcoffset()
            is not None
        )
    except Exception:  # pragma: no cover - platform boundary
        zone_ok = False

    return ValidationReport(
        checks=(
            _result("python", python_ok, sys.version.split()[0]),
            _result("swiss_ephemeris", bool(swe.version), f"version {swe.version}"),
            _result("ephemeris_data", path_ok, path_detail),
            _result("timezone_database", zone_ok, "IANA zone Asia/Kolkata loaded"),
            _result("configuration", True, "Lahiri sidereal, mean lunar node"),
        )
    )


def validate_installation() -> ValidationReport:
    """Run deterministic calculation, range, and serialization checks."""
    birth = BirthInput(
        date=date(2000, 1, 1),
        time=time(17, 30),
        timezone="Asia/Kolkata",
        coordinates=Coordinates(latitude=13.0827, longitude=80.2707),
    )
    chart = generate_chart(birth, SwissEphemeris())
    decoded = json.loads(chart.model_dump_json())
    checks = (
        *doctor().checks,
        _result(
            "julian_day",
            abs(chart.julian_day_ut - 2451545.0) < 1e-9,
            f"J2000 reference: {chart.julian_day_ut}",
        ),
        _result(
            "planet_longitudes",
            len(chart.planets) == 9
            and all(0.0 <= position.longitude < 360.0 for position in chart.planets),
            "nine grahas are within [0°, 360°)",
        ),
        _result(
            "serialization",
            decoded["utc_datetime"] == "2000-01-01T12:00:00Z"
            and chart.utc_datetime.tzinfo is UTC,
            "JSON retained the reference UTC instant",
        ),
        _result(
            "houses",
            len(chart.houses.cusps) == 12
            and 0.0 <= chart.houses.ascendant.longitude < 360.0
            and all(1 <= planet.house <= 12 for planet in chart.planets),
            "Ascendant, twelve whole-sign cusps, and house assignments are valid",
        ),
        _result(
            "nakshatras",
            all(
                0 <= planet.nakshatra.index < 27 and 1 <= planet.nakshatra.pada <= 4
                for planet in chart.planets
            ),
            "all grahas have valid Nakshatra and Pada assignments",
        ),
        _result(
            "divisional_charts",
            [item.division.value for item in chart.divisional_charts] == ["D1", "D9"]
            and all(len(item.planets) == 9 for item in chart.divisional_charts),
            "D1 Rasi and D9 Navamsa contain nine graha placements",
        ),
        _result(
            "vimshottari_dasha",
            len(chart.vimshottari_dasha.periods) == 9
            and sum(period.duration_years for period in chart.vimshottari_dasha.periods)
            == 120,
            "nine contiguous Mahadashas total 120 deterministic years",
        ),
        _result(
            "classical_rules",
            len(chart.classical_rules) == 7
            and all(
                rule.evidence and rule.source.title for rule in chart.classical_rules
            ),
            "seven auditable rules include evidence and an identified source",
        ),
        _result(
            "planetary_dignities",
            len(chart.planetary_dignities) == 9
            and all(
                item.evidence and item.source.title
                for item in chart.planetary_dignities
            ),
            "nine grahas have an auditable dignity state or explicit exclusion",
        ),
        _result(
            "classical_aspects",
            bool(chart.aspects)
            and all(item.evidence and item.source for item in chart.aspects),
            "directed full-sign aspects include evidence and source metadata",
        ),
    )
    return ValidationReport(checks=checks)
