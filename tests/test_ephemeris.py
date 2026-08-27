import json
from pathlib import Path

import pytest

from nakshatra.astronomy.ephemeris import SwissEphemeris
from nakshatra.planets import Planet

GOLDEN_PATH = Path(__file__).parent / "golden" / "j2000_lahiri.json"


def test_lahiri_positions_match_swiss_ephemeris_golden_chart() -> None:
    expected = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    result = SwissEphemeris().positions(expected["julian_day_ut"])

    assert result.ayanamsa_degrees == pytest.approx(
        expected["ayanamsa_degrees"], abs=1 / 3_600
    )
    for position in result.planets:
        assert position.longitude == pytest.approx(
            expected["positions"][position.planet.value], abs=1 / 3_600
        )


def test_ketu_is_exactly_opposite_rahu() -> None:
    positions = {
        position.planet: position
        for position in SwissEphemeris().positions(2451545).planets
    }

    assert positions[Planet.KETU].longitude == pytest.approx(
        (positions[Planet.RAHU].longitude + 180) % 360
    )


def test_position_contains_sign_and_retrograde_state() -> None:
    result = SwissEphemeris().position(2451545, Planet.SATURN)

    assert result.sign.sign.name == "ARIES"
    assert result.retrograde is True
    assert result.speed_longitude < 0


def test_direct_ketu_calculation_is_supported() -> None:
    result = SwissEphemeris().position(2451545, Planet.KETU)

    assert result.planet is Planet.KETU


def test_custom_ephemeris_path_is_accepted(tmp_path: Path) -> None:
    result = SwissEphemeris(str(tmp_path)).position(2451545, Planet.SUN)

    assert 0 <= result.longitude < 360


def test_ephemeris_path_can_come_from_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NAKSHATRA_EPHEMERIS_PATH", str(tmp_path))

    result = SwissEphemeris().position(2451545, Planet.SUN)

    assert 0 <= result.longitude < 360
