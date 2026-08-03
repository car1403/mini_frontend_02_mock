from fastapi.testclient import TestClient

from app.main import app
from app.routers import real_router


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_data(monkeypatch):
    saved_item = {
        "id": "11111111-1111-1111-1111-111111111111",
        "device_name": "sensor-01",
        "temperature": 25.5,
        "humidity": 60,
        "created_at": "2026-07-31T10:00:00+00:00",
    }

    async def publish_success(item):
        return None

    monkeypatch.setattr(real_router, "save_real_data", lambda data: saved_item.copy())
    monkeypatch.setattr(real_router, "publish_real_data", publish_success)

    response = client.post(
        "/real-data",
        json={"device_name": "sensor-01", "temperature": 25.5, "humidity": 60},
    )

    assert response.status_code == 200
    assert response.json()["event_published"] is True


def test_create_data_when_redis_publish_fails(monkeypatch):
    saved_item = {
        "id": "11111111-1111-1111-1111-111111111111",
        "device_name": "sensor-01",
        "temperature": 25.5,
        "humidity": 60,
        "created_at": "2026-07-31T10:00:00+00:00",
    }

    async def publish_failure(item):
        raise RuntimeError("Redis 연결 실패")

    monkeypatch.setattr(real_router, "save_real_data", lambda data: saved_item.copy())
    monkeypatch.setattr(real_router, "publish_real_data", publish_failure)

    response = client.post(
        "/real-data",
        json={"device_name": "sensor-01", "temperature": 25.5, "humidity": 60},
    )

    assert response.status_code == 200
    assert response.json()["event_published"] is False


def test_recent_data_without_login(monkeypatch):
    rows = [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "device_name": "sensor-01",
            "temperature": 25.5,
            "humidity": 60,
            "created_at": "2026-07-31T10:00:00+00:00",
        }
    ]
    monkeypatch.setattr(real_router, "get_recent_data", lambda limit: rows)

    response = client.get("/real-data/recent")

    assert response.status_code == 200
    assert response.json() == rows
