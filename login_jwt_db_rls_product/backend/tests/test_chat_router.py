from fastapi.testclient import TestClient

from app.core.auth_dependency import get_current_user
from app.main import app
from app.routers import chat_router
from app.schemes.auth_scheme import CurrentUser
from app.schemes.chat_scheme import ChatResponse


client = TestClient(app)


def test_chat_requires_login():
    response = client.post("/chat/gemini", json={"prompt": "Hello"})
    assert response.status_code == 401


def test_chat_uses_verified_supabase_user(monkeypatch):
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(
        user_id="user-uuid",
        email="user@example.com",
        role="user",
        access_token="user-token",
    )

    def fake_call_gemini(request, user_id):
        return ChatResponse(user_id=user_id, answer="Mocked Gemini answer")

    monkeypatch.setattr(chat_router, "call_gemini", fake_call_gemini)

    try:
        response = client.post("/chat/gemini", json={"prompt": "Hello"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["user_id"] == "user-uuid"
