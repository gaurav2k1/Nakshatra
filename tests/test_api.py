from fastapi.testclient import TestClient

from nakshatra.api.app import app

client = TestClient(app)


def test_home_renders_birth_chart_workspace() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Nakshatra AI" in response.text
    assert "Generate verified chart" in response.text
    assert response.headers["x-content-type-options"] == "nosniff"


def test_live_and_ready_health_checks() -> None:
    live = client.get("/health/live")
    ready = client.get("/health/ready")

    assert live.status_code == 200
    assert live.json() == {"status": "ok", "version": "0.2.0"}
    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"


def test_generate_chart_api_returns_verified_facts() -> None:
    response = client.post(
        "/api/v1/charts",
        json={
            "date": "2000-01-01",
            "time": "17:30:00",
            "timezone": "Asia/Kolkata",
            "coordinates": {"latitude": 13.0827, "longitude": 80.2707},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["julian_day_ut"] == 2451545.0
    assert payload["ayanamsa"] == "Lahiri"
    assert len(payload["planets"]) == 9


def test_generate_chart_api_rejects_invalid_input() -> None:
    response = client.post(
        "/api/v1/charts",
        json={
            "date": "2000-01-01",
            "time": "17:30:00",
            "timezone": "Not/AZone",
            "coordinates": {"latitude": 91, "longitude": 80},
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]
