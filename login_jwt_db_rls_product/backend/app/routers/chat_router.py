from fastapi import APIRouter, Depends

from app.core.auth_dependency import get_current_user
from app.schemes.auth_scheme import CurrentUser
from app.schemes.chat_scheme import ChatRequest, ChatResponse
from app.services.chat_service import call_gemini


chat_router = APIRouter(tags=["Chat"])


@chat_router.post("/chat/gemini")
def chat_gemini(
    chat_request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> ChatResponse:
    # current_user.user_id는 Supabase가 검증한 Access Token의 사용자 UUID입니다.
    return call_gemini(chat_request, current_user.user_id)
