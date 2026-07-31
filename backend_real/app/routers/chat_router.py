from fastapi import APIRouter, Depends

from app.core.auth_dependency import get_current_user
from app.schemes.chat_scheme import ChatRequest, ChatResponse
from app.services.chat_service import call_gemini


chat_router = APIRouter(tags=["Chat"])


@chat_router.post("/chat/gemini")
def chat_gemini(
    chat_request: ChatRequest,
    current_user: str = Depends(get_current_user),
) -> ChatResponse:
    # current_user는 사용자가 입력한 값이 아니라 JWT의 sub에서 가져온 ID입니다.
    return call_gemini(chat_request, current_user)
