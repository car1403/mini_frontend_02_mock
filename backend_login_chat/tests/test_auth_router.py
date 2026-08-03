from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_creates_session():
    response = client.post(
        "/auth/login",
        json={"id": "id01", "pwd": "pwd01"},
    )

    assert response.status_code == 200
    assert response.json()["session_token"]
    assert response.json()["user"] == {"id": "id01", "name": "이말숙"}


def test_wrong_password_is_rejected():
    response = client.post(
        "/auth/login",
        json={"id": "id01", "pwd": "wrong"},
    )

    assert response.status_code == 401
