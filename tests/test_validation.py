from nakshatra.validation import CheckStatus, doctor, validate_installation


def test_doctor_reports_required_runtime_checks() -> None:
    report = doctor()

    assert report.ok
    assert {check.name for check in report.checks} >= {
        "python",
        "swiss_ephemeris",
        "timezone_database",
        "configuration",
    }
    assert all(check.status is CheckStatus.PASS for check in report.checks)


def test_validate_installation_runs_calculation_and_serialization_checks() -> None:
    report = validate_installation()

    assert report.ok
    assert {check.name for check in report.checks} >= {
        "julian_day",
        "planet_longitudes",
        "serialization",
        "houses",
        "nakshatras",
        "divisional_charts",
        "vimshottari_dasha",
        "classical_rules",
        "planetary_dignities",
        "classical_aspects",
    }
