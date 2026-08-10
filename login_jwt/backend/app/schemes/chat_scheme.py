"""채팅 API의 요청과 응답 데이터 모양을 정의합니다."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    # user_id는 요청 Body로 받지 않고 JWT에서 안전하게 가져옵니다.
    prompt: str = Field(min_length=1, examples=["안녕!"])


class ChatResponse(BaseModel):
    """Gemini 답변과 질문한 사용자 ID를 함께 반환합니다."""

    user_id: str = Field(examples=["id01"])
    answer: str = Field(min_length=1, examples=["안녕하세요!"])
