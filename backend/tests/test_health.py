from fastapi.testclient import TestClient

from app.main import app


def test_health_check_returns_ok():
    """An API test: send a request and assert its observable response."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
