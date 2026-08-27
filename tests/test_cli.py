import json

from typer.testing import CliRunner

from nakshatra.cli.app import app

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "Nakshatra AI 0.8.0"


def test_info_command() -> None:
    result = runner.invoke(app, ["info"])

    assert result.exit_code == 0
    assert "deterministic" in result.stdout.lower()


def test_generate_command_emits_chart_json() -> None:
    result = runner.invoke(
        app,
        [
            "generate",
            "--date",
            "2000-01-01",
            "--time",
            "17:30:00",
            "--timezone",
            "Asia/Kolkata",
            "--latitude",
            "13.0827",
            "--longitude",
            "80.2707",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["julian_day_ut"] == 2451545.0
    assert len(payload["planets"]) == 9


def test_doctor_and_validate_commands_pass() -> None:
    doctor_result = runner.invoke(app, ["doctor"])
    validate_result = runner.invoke(app, ["validate"])

    assert doctor_result.exit_code == 0
    assert "PASS" in doctor_result.stdout
    assert validate_result.exit_code == 0
    assert "PASS" in validate_result.stdout
