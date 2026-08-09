from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, examples=["안녕하세요!"])


class ChatResponse(BaseModel):
    user_id: str
    answer: str
