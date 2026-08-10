"""채팅 API의 로그인 보호와 요청 검증을 확인하는 테스트입니다."""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat_router
from app.schemes.chat_scheme import ChatResponse


client = TestClient(app)


def login_headers() -> dict[str, str]:
    """테스트 계정으로 로그인하고 JWT가 포함된 요청 헤더를 만듭니다."""

    response = client.post("/auth/login", json={"id": "id01", "pwd": "pwd01"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_chat_requires_login():
    # 토큰 없이 보호된 채팅 API를 호출하면 401이어야 합니다.
    response = client.post("/chat/gemini", json={"prompt": "Hello"})

    assert response.status_code == 401


def test_chat_uses_user_id_from_jwt(monkeypatch):
    # 실제 Gemini API를 호출하지 않도록 가짜 함수로 교체합니다.
    def fake_call_gemini(request, user_id):
        assert request.prompt == "Hello"
        assert user_id == "id01"
        return ChatResponse(user_id=user_id, answer="Mocked Gemini answer")

    # monkeypatch로 이 테스트가 실행되는 동안에만 함수를 바꿉니다.
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
    # prompt의 min_length=1 검증 때문에 빈 문자열은 422가 되어야 합니다.
    response = client.post(
        "/chat/gemini",
        json={"prompt": ""},
        headers=login_headers(),
    )

    assert response.status_code == 422
