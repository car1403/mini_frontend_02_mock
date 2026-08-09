import os

from google import genai

from app.schemes.chat_scheme import ChatRequest, ChatResponse


def call_gemini(
    chat_request: ChatRequest,
    user_id: str,
) -> ChatResponse:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    response = client.models.generate_content(
        model=model,
        contents=chat_request.prompt,
    )
    return ChatResponse(user_id=user_id, answer=response.text)
