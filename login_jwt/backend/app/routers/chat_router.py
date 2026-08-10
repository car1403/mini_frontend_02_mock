"""로그인한 사용자가 Gemini 채팅을 요청하는 API입니다."""

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
    """JWT를 확인한 뒤 사용자의 질문을 Gemini에 전달합니다."""

    # current_user는 사용자가 입력한 값이 아니라 JWT의 sub에서 가져온 ID입니다.
    # Depends 때문에 토큰이 없거나 잘못되면 call_gemini()까지 실행되지 않습니다.
    return call_gemini(chat_request, current_user)
