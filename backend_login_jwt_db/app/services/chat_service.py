import os

from google import genai

from app.schemes.chat_scheme import ChatRequest, ChatResponse


def call_gemini(
    chat_request: ChatRequest,
    user_id: str,
) -> ChatResponse:
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=chat_request.prompt,
    )

    # 나중에 DB에 저장할 때 user_id, prompt, answer를 함께 저장하면 됩니다.
    return ChatResponse(
        user_id=user_id,
        answer=response.text,
    )
