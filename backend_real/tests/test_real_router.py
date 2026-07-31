from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def login_headers() -> dict[str, str]:
    response = client.post("/auth/login", json={"id": "id01", "pwd": "pwd01"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_real_data_requires_login():
    response = client.get("/real/one")

    assert response.status_code == 401


def test_real_data_after_login():
    response = client.get("/real/one", headers=login_headers())

    assert response.status_code == 200
    assert response.json()["number"] == 1
    assert "temperature" in response.json()
    assert "status" in response.json()
