from fastapi import APIRouter, Depends

from app.core.session_dependency import get_current_user
from app.schemes.auth_scheme import AuthPublic
from app.schemes.chat_scheme import ChatRequest, ChatResponse
from app.services.chat_service import call_gemini


chat_router = APIRouter(prefix="/chat", tags=["Chat"])


@chat_router.post("/gemini", response_model=ChatResponse)
def chat_gemini(
    chat_request: ChatRequest,
    current_user: AuthPublic = Depends(get_current_user),
):
    return call_gemini(chat_request, current_user.id)
