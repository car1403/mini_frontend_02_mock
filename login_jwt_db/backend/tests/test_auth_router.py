from fastapi.testclient import TestClient

from app.main import app
from app.routers import auth_router
from app.schemes.auth_scheme import AuthPublic, TokenResponse


client = TestClient(app)


def test_signup_returns_created_customer(monkeypatch):
    monkeypatch.setattr(
        auth_router,
        "signup_process",
        lambda auth: AuthPublic(id=auth.id, name=auth.name),
    )

    response = client.post(
        "/auth/signup",
        json={"id": "new-user", "pwd": "password", "name": "홍길동"},
    )

    assert response.status_code == 201
    assert response.json() == {"id": "new-user", "name": "홍길동"}


def test_login_returns_token_and_db_user(monkeypatch):
    monkeypatch.setattr(
        auth_router,
        "login_process",
        lambda auth: TokenResponse(
            access_token="test-token",
            token_type="bearer",
            user=AuthPublic(id=auth.id, name="홍길동"),
        ),
    )

    response = client.post(
        "/auth/login",
        json={"id": "new-user", "pwd": "password"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "test-token",
        "token_type": "bearer",
        "user": {"id": "new-user", "name": "홍길동"},
    }
