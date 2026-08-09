from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    # user_id는 요청 Body로 받지 않고 JWT에서 안전하게 가져옵니다.
    prompt: str = Field(min_length=1, examples=["안녕!"])


class ChatResponse(BaseModel):
    user_id: str = Field(examples=["id01"])
    answer: str = Field(min_length=1, examples=["안녕하세요!"])
