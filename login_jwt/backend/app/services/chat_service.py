"""Gemini API를 호출하고 채팅 응답을 만드는 서비스입니다."""

import os

from google import genai

from app.schemes.chat_scheme import ChatRequest, ChatResponse


def call_gemini(
    chat_request: ChatRequest,
    user_id: str,
) -> ChatResponse:
    """환경변수의 설정으로 Gemini를 호출하고 답변을 반환합니다."""

    # 비밀값인 API 키는 코드에 직접 작성하지 않고 .env에서 읽습니다.
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    # API 키를 사용해 Gemini 클라이언트를 생성합니다.
    client = genai.Client(api_key=api_key)
    # 사용자가 입력한 prompt를 선택한 Gemini 모델에 전달합니다.
    response = client.models.generate_content(
        model=model,
        contents=chat_request.prompt,
    )

    # 나중에 DB에 저장할 때 user_id, prompt, answer를 함께 저장하면 됩니다.
    # response.text에는 Gemini가 만든 답변 문자열이 들어 있습니다.
    return ChatResponse(
        user_id=user_id,
        answer=response.text,
    )
