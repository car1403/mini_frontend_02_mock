from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat_router
from app.schemes.chat_scheme import ChatResponse


client = TestClient(app)


def login_headers() -> dict[str, str]:
    response = client.post("/auth/login", json={"id": "id01", "pwd": "pwd01"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_chat_requires_login():
    response = client.post("/chat/gemini", json={"prompt": "Hello"})

    assert response.status_code == 401


def test_chat_uses_user_id_from_jwt(monkeypatch):
    def fake_call_gemini(request, user_id):
        assert request.prompt == "Hello"
        assert user_id == "id01"
        return ChatResponse(user_id=user_id, answer="Mocked Gemini answer")

    monkeypatch.setattr(chat_router, "call_gemini", fake_call_gemini)

    response = client.post(
        "/chat/gemini",
        json={"prompt": "Hello"},
        headers=login_headers(),
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "id01",
        "answer": "Mocked Gemini answer",
    }


def test_chat_rejects_empty_prompt():
    response = client.post(
        "/chat/gemini",
        json={"prompt": ""},
        headers=login_headers(),
    )

    assert response.status_code == 422
