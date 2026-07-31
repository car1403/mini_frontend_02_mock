from fastapi.testclient import TestClient

from app.main import app
from app.routers import real_router


client = TestClient(app)


def login_headers() -> dict[str, str]:
    response = client.post("/auth/login", json={"id": "id01", "pwd": "pwd01"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_recent_data_requires_login():
    response = client.get("/real-data/recent")

    assert response.status_code == 401


def test_recent_data_after_login(monkeypatch):
    rows = [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "device_name": "sensor-01",
            "temperature": 25.5,
            "humidity": 60,
            "created_by": "id01",
            "created_at": "2026-07-31T10:00:00+00:00",
        }
    ]
    monkeypatch.setattr(real_router, "get_recent_data", lambda limit: rows)

    response = client.get("/real-data/recent", headers=login_headers())

    assert response.status_code == 200
    assert response.json() == rows
