from fastapi.testclient import TestClient

from app.main import app
from app.routers import auth_router
from app.schemes.auth_scheme import AuthPublic, TokenResponse


client = TestClient(app)


def test_signup_returns_supabase_user(monkeypatch):
    monkeypatch.setattr(
        auth_router,
        "signup_process",
        lambda auth: AuthPublic(
            id="user-uuid",
            email=auth.email,
            name=auth.name,
            role="user",
        ),
    )

    response = client.post(
        "/auth/signup",
        json={"email": "user@example.com", "pwd": "password", "name": "홍길동"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": "user-uuid",
        "email": "user@example.com",
        "name": "홍길동",
        "role": "user",
    }


def test_login_returns_token_and_role(monkeypatch):
    monkeypatch.setattr(
        auth_router,
        "login_process",
        lambda auth: TokenResponse(
            access_token="test-token",
            token_type="bearer",
            user=AuthPublic(
                id="admin-uuid",
                email=auth.email,
                name="관리자",
                role="admin",
            ),
        ),
    )

    response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "pwd": "password"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "test-token"
    assert response.json()["user"]["role"] == "admin"
